"""Tests for global authentication requirements"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db, User
from werkzeug.security import generate_password_hash

class TestGlobalAuthentication:
    @pytest.fixture
    def client(self):
        """Create test client with isolated database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                # Create a test user
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash=generate_password_hash('testpass123')
                )
                db.session.add(test_user)
                db.session.commit()
                yield client
                db.session.remove()
                db.drop_all()
    
    # ===== Public Routes (should be accessible without login) =====
    
    def test_home_page_public(self, client):
        """Home page should be accessible without login"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_about_page_public(self, client):
        """About page should be accessible without login"""
        response = client.get('/about')
        assert response.status_code == 200
    
    def test_login_page_public(self, client):
        """Login page should be accessible without login"""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_register_page_public(self, client):
        """Register page should be accessible without login"""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_pricing_page_public(self, client):
        """Pricing page should be accessible without login"""
        response = client.get('/pricing')
        assert response.status_code == 200
    
    def test_forgot_password_public(self, client):
        """Forgot password page should be accessible without login"""
        response = client.get('/forgot-password')
        assert response.status_code == 200
    
    def test_static_files_public(self, client):
        """Static files should be accessible without login"""
        # Test accessing a static file path (may not exist, but should not redirect)
        response = client.get('/static/test.css')
        # Should get 404 for missing file, not 302 redirect to login
        assert response.status_code == 404
    
    # ===== Protected Routes (should require login) =====
    
    def test_upload_requires_login(self, client):
        """Upload page should redirect to login"""
        response = client.get('/upload', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_dashboard_requires_login(self, client):
        """Dashboard should redirect to login"""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_form_requires_login(self, client):
        """Form page should redirect to login"""
        response = client.get('/form', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_jobs_requires_login(self, client):
        """Jobs page should redirect to login"""
        response = client.get('/jobs', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_roadmap_requires_login(self, client):
        """Roadmap page should redirect to login"""
        response = client.get('/roadmap/data-scientist', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_ats_report_requires_login(self, client):
        """ATS report page should redirect to login"""
        response = client.get('/ats-report', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_checklist_requires_login(self, client):
        """Checklist page should redirect to login"""
        response = client.get('/checklist', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_guide_requires_login(self, client):
        """Guide page should redirect to login"""
        response = client.get('/guide', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    # ===== API Endpoints =====
    
    def test_api_requires_login_json_error(self, client):
        """API endpoints should return 401 JSON error"""
        response = client.get('/api/dashboard/stats')
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert 'Authentication required' in data['error']
    
    def test_api_jobs_search_requires_login(self, client):
        """Jobs search API should return 401 JSON error"""
        response = client.get('/api/jobs/search')
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    # ===== Login with Next Parameter =====
    
    def test_login_redirects_to_next_page(self, client):
        """After login, should redirect to originally requested page"""
        # Try to access protected page
        response = client.get('/upload', follow_redirects=False)
        assert response.status_code == 302
        assert 'next=' in response.location
        
        # Now login
        response = client.post('/login?next=/upload', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=False)
        
        # Should redirect to /upload
        assert response.status_code == 302
        assert '/upload' in response.location
    
    def test_login_validates_next_parameter(self, client):
        """Login should validate that next parameter starts with /"""
        # Try to login with external URL (security check)
        response = client.post('/login?next=https://evil.com', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=False)
        
        # Should redirect to home, not to external URL
        assert response.status_code == 302
        assert 'evil.com' not in response.location
    
    # ===== Admin Routes =====
    
    def test_admin_routes_not_affected(self, client):
        """Admin routes should not be affected by global auth (they have their own)"""
        # Admin login page should be accessible
        response = client.get('/admin/login')
        assert response.status_code == 200
        
        # Admin routes should not redirect to user login
        response = client.get('/admin/dashboard', follow_redirects=False)
        # Will redirect to admin login, not user login
        assert response.status_code == 302
        # Should not redirect to /login (user login)
        if '/login' in response.location:
            assert '/admin' in response.location
