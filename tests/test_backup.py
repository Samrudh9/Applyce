import pytest
import sys
import os
import json
import tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class TestBackupService:
    """Tests for the backup service"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_backup_service_import(self):
        """Test that backup service can be imported"""
        from services.backup_service import BackupService
        assert BackupService is not None
    
    def test_get_statistics(self):
        """Test getting database statistics"""
        from services.backup_service import BackupService
        with app.app_context():
            stats = BackupService._get_statistics()
            assert 'total_users' in stats
            assert 'total_feedback' in stats
            assert 'total_patterns' in stats
            assert 'total_resumes' in stats
    
    def test_export_all_data(self):
        """Test exporting all data"""
        from services.backup_service import BackupService
        with app.app_context():
            data = BackupService.export_all_data()
            assert 'export_date' in data
            assert 'version' in data
            assert 'statistics' in data
            assert 'skill_patterns' in data
            assert 'feedback' in data
            assert 'users' in data
            assert 'resume_history' in data
    
    def test_export_skill_patterns_csv(self):
        """Test exporting skill patterns as CSV"""
        from services.backup_service import BackupService
        with app.app_context():
            csv_content = BackupService.export_skill_patterns_csv()
            assert isinstance(csv_content, str)
            # Should have header row
            assert 'id,skill,career,confidence' in csv_content
    
    def test_get_backup_status(self):
        """Test getting backup status"""
        from services.backup_service import BackupService
        with app.app_context():
            backups = BackupService.get_backup_status()
            assert isinstance(backups, list)


class TestAdminBackupRoutes:
    """Tests for admin backup routes"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_admin_login_page(self, client):
        """Test admin login page loads"""
        response = client.get('/admin/login')
        assert response.status_code == 200
        assert b'Admin Access' in response.data or b'admin' in response.data.lower()
    
    def test_admin_login_invalid_credentials(self, client):
        """Test admin login with invalid credentials"""
        response = client.post('/admin/login', data={
            'admin_id': 'wrong',
            'admin_password': 'wrong'
        })
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'invalid' in response.data.lower()
    
    def test_admin_login_valid_credentials(self, client):
        """Test admin login with valid credentials"""
        from config import config
        response = client.post('/admin/login', data={
            'admin_id': config.ADMIN_ID,
            'admin_password': config.ADMIN_PASSWORD
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to backup page
        assert b'Backup' in response.data or b'backup' in response.data.lower()
    
    def test_admin_backup_page_requires_auth(self, client):
        """Test that backup page requires authentication"""
        response = client.get('/admin/backup')
        # Should redirect to login
        assert response.status_code == 302
        assert '/admin/login' in response.location
    
    def test_admin_backup_page_with_auth(self, client):
        """Test backup page with authentication"""
        from config import config
        # Login first
        client.post('/admin/login', data={
            'admin_id': config.ADMIN_ID,
            'admin_password': config.ADMIN_PASSWORD
        })
        # Now access backup page
        response = client.get('/admin/backup')
        assert response.status_code == 200
        assert b'Data Backup' in response.data or b'backup' in response.data.lower()
    
    def test_create_backup_json(self, client):
        """Test creating a JSON backup"""
        from config import config
        # Login first
        client.post('/admin/login', data={
            'admin_id': config.ADMIN_ID,
            'admin_password': config.ADMIN_PASSWORD
        })
        # Create backup
        response = client.post('/admin/backup/create', data={'format': 'json'})
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        # Verify it's valid JSON
        data = json.loads(response.data)
        assert 'version' in data
        assert 'statistics' in data
    
    def test_create_backup_csv(self, client):
        """Test creating a CSV backup"""
        from config import config
        # Login first
        client.post('/admin/login', data={
            'admin_id': config.ADMIN_ID,
            'admin_password': config.ADMIN_PASSWORD
        })
        # Create backup
        response = client.post('/admin/backup/create', data={'format': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response.content_type
    
    def test_admin_logout(self, client):
        """Test admin logout"""
        from config import config
        # Login first
        client.post('/admin/login', data={
            'admin_id': config.ADMIN_ID,
            'admin_password': config.ADMIN_PASSWORD
        })
        # Logout
        response = client.get('/admin/logout', follow_redirects=True)
        assert response.status_code == 200
        # Should no longer have access to backup page
        response = client.get('/admin/backup')
        assert response.status_code == 302
    
    def test_api_admin_stats_requires_auth(self, client):
        """Test that API stats endpoint requires authentication"""
        response = client.get('/api/admin/stats')
        # Should redirect to login
        assert response.status_code == 302
    
    def test_api_admin_stats_with_auth(self, client):
        """Test API stats endpoint with authentication"""
        from config import config
        # Login first
        client.post('/admin/login', data={
            'admin_id': config.ADMIN_ID,
            'admin_password': config.ADMIN_PASSWORD
        })
        # Get stats
        response = client.get('/api/admin/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'stats' in data
