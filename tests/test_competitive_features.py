"""
Tests for the new competitive features:
- Explainable Scoring System
- Forgot Password System
- Freemium System
- Score Trends API
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db


class TestExplainableScorer:
    """Tests for the explainable scoring system"""
    
    def test_scorer_import(self):
        """Test that explainable scorer can be imported"""
        from services.explainable_scorer import get_explainable_scorer
        scorer = get_explainable_scorer()
        assert scorer is not None
    
    def test_analyze_basic_resume(self):
        """Test basic resume analysis"""
        from services.explainable_scorer import get_explainable_scorer
        scorer = get_explainable_scorer()
        
        sample_text = """
        John Doe
        Email: john@example.com
        Phone: 1234567890
        
        Summary
        Experienced Python developer with expertise in machine learning and data analysis.
        
        Skills
        Python, SQL, Machine Learning, TensorFlow, Pandas, NumPy
        
        Experience
        Senior Data Scientist at TechCorp
        - Led development of ML pipeline that improved accuracy by 25%
        - Developed automated reporting system
        - Managed team of 5 data analysts
        
        Education
        Master of Science in Computer Science
        """
        
        result = scorer.analyze(sample_text, 'data scientist', ['python', 'sql', 'tensorflow'])
        
        assert 'overall_score' in result
        assert 'category_scores' in result
        assert 'priority_fixes' in result
        assert 'radar_chart_data' in result
        assert isinstance(result['overall_score'], (int, float))
        assert 0 <= result['overall_score'] <= 100
    
    def test_category_breakdown(self):
        """Test that all 6 categories are present"""
        from services.explainable_scorer import get_explainable_scorer
        scorer = get_explainable_scorer()
        
        result = scorer.analyze("Sample resume text with skills and experience", 'default')
        
        categories = result['category_scores']
        assert 'keywords_skills' in categories
        assert 'ats_formatting' in categories
        assert 'content_impact' in categories
        assert 'parseability' in categories
        assert 'readability' in categories
        assert 'section_completeness' in categories
    
    def test_category_weights_sum_to_100(self):
        """Test that category weights sum to 100"""
        from services.explainable_scorer import ExplainableScorer
        
        total_weight = sum(ExplainableScorer.WEIGHTS.values())
        assert total_weight == 100
    
    def test_priority_fixes_ordered(self):
        """Test that priority fixes are ordered by priority"""
        from services.explainable_scorer import get_explainable_scorer
        scorer = get_explainable_scorer()
        
        result = scorer.analyze("Minimal resume", 'data scientist')
        
        if result['priority_fixes']:
            priorities = [fix['priority'] for fix in result['priority_fixes']]
            assert priorities == sorted(priorities)
    
    def test_radar_chart_data_structure(self):
        """Test radar chart data structure"""
        from services.explainable_scorer import get_explainable_scorer
        scorer = get_explainable_scorer()
        
        result = scorer.analyze("Sample resume", 'default')
        
        radar_data = result['radar_chart_data']
        assert 'labels' in radar_data
        assert 'scores' in radar_data
        assert 'weights' in radar_data
        assert 'target' in radar_data
        assert len(radar_data['labels']) == 6
        assert len(radar_data['scores']) == 6


class TestForgotPasswordRoutes:
    """Tests for forgot password functionality"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.session.remove()
                db.drop_all()
    
    def test_forgot_password_page_loads(self, client):
        """Test forgot password page loads"""
        response = client.get('/forgot-password')
        assert response.status_code == 200
        assert b'Forgot Password' in response.data or b'forgot' in response.data.lower()
    
    def test_forgot_password_post_empty_email(self, client):
        """Test forgot password with empty email"""
        response = client.post('/forgot-password', data={'email': ''})
        assert response.status_code == 200
    
    def test_forgot_password_post_with_email(self, client):
        """Test forgot password with email (should not reveal if email exists)"""
        response = client.post('/forgot-password', 
                               data={'email': 'test@example.com'},
                               follow_redirects=True)
        assert response.status_code == 200
    
    def test_reset_password_invalid_token(self, client):
        """Test reset password with invalid token"""
        response = client.get('/reset-password/invalidtoken123')
        assert response.status_code == 200
        # Should show expired message or similar


class TestFreemiumSystem:
    """Tests for the freemium system"""
    
    def test_user_model_has_freemium_fields(self):
        """Test that User model has freemium fields"""
        from models.user import User
        
        # Check model has the required attributes
        assert hasattr(User, 'account_type')
        assert hasattr(User, 'resume_scans_today')
        assert hasattr(User, 'resume_scans_total')
        assert hasattr(User, 'last_scan_date')
        assert hasattr(User, 'premium_expires_at')
    
    def test_user_model_has_freemium_methods(self):
        """Test that User model has freemium methods"""
        from models.user import User
        
        # Check model has the required methods
        assert hasattr(User, 'can_scan_resume')
        assert hasattr(User, 'record_scan')
        assert hasattr(User, 'upgrade_to_premium')
        assert hasattr(User, 'get_feature_access')
    
    def test_tier_limits_defined(self):
        """Test that tier limits are properly defined"""
        from models.user import TIER_LIMITS
        
        assert 'free' in TIER_LIMITS
        assert 'premium' in TIER_LIMITS
        assert 'enterprise' in TIER_LIMITS
        
        assert TIER_LIMITS['free']['daily_scans'] == 3
        assert TIER_LIMITS['premium']['daily_scans'] == 50
        assert TIER_LIMITS['enterprise']['daily_scans'] == -1  # Unlimited


class TestPasswordResetMethods:
    """Tests for password reset methods in User model"""
    
    def test_user_has_reset_methods(self):
        """Test that User model has password reset methods"""
        from models.user import User
        
        assert hasattr(User, 'generate_reset_token')
        assert hasattr(User, 'verify_reset_token')
        assert hasattr(User, 'clear_reset_token')
        assert hasattr(User, 'reset_password')
    
    def test_user_has_reset_fields(self):
        """Test that User model has reset token fields"""
        from models.user import User
        
        assert hasattr(User, 'reset_token')
        assert hasattr(User, 'reset_token_expiry')


class TestPricingRoute:
    """Tests for pricing page"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_pricing_page_loads(self, client):
        """Test pricing page loads"""
        response = client.get('/pricing')
        assert response.status_code == 200
        assert b'Pricing' in response.data or b'pricing' in response.data.lower()
    
    def test_pricing_page_shows_plans(self, client):
        """Test pricing page shows plan information"""
        response = client.get('/pricing')
        assert response.status_code == 200
        assert b'Free' in response.data
        assert b'Premium' in response.data


class TestAuthServiceExtensions:
    """Tests for auth service password reset extensions"""
    
    def test_auth_service_has_reset_methods(self):
        """Test that AuthService has password reset methods"""
        from services.auth_service import AuthService
        
        assert hasattr(AuthService, 'initiate_password_reset')
        assert hasattr(AuthService, 'reset_password')
        assert hasattr(AuthService, 'get_user_by_reset_token')


class TestExplainableScoreAPI:
    """Tests for the explainable score API endpoint"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                from models.user import User
                from werkzeug.security import generate_password_hash
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash=generate_password_hash('testpass123')
                )
                db.session.add(test_user)
                db.session.commit()
                # Log in the test user
                client.post('/login', data={
                    'email_or_username': 'testuser',
                    'password': 'testpass123'
                })
                yield client
                db.session.remove()
                db.drop_all()
    
    def test_explainable_score_api_requires_data(self, client):
        """Test API requires data"""
        response = client.post('/api/explainable-score',
                               json={},
                               content_type='application/json')
        assert response.status_code == 400
    
    def test_explainable_score_api_with_data(self, client):
        """Test API with valid data"""
        response = client.post('/api/explainable-score',
                               json={
                                   'resume_text': 'Sample resume with python and sql skills',
                                   'target_role': 'backend developer'
                               },
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'overall_score' in data
        assert 'category_scores' in data
