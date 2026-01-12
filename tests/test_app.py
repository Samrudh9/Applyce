import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestFlaskApp:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
    
    def test_upload_page(self, client):
        """Upload page should redirect to login when not authenticated"""
        response = client.get('/upload', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_about_page(self, client):
        response = client.get('/about')
        assert response.status_code == 200

    def test_guide_page(self, client):
        """Test the resume guide page requires authentication"""
        response = client.get('/guide', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location

    def test_checklist_redirect_without_data(self, client):
        """Test checklist requires authentication"""
        response = client.get('/checklist', follow_redirects=False)
        # Should redirect to login (not to upload page anymore)
        assert response.status_code == 302
        assert '/login' in response.location

    def test_feedback_endpoint(self, client):
        """Test the feedback endpoint requires authentication"""
        response = client.post('/feedback', 
                               json={'feedback_type': 'positive'},
                               content_type='application/json',
                               follow_redirects=False)
        # Should redirect to login since user is not authenticated
        assert response.status_code == 302
        assert '/login' in response.location

    def test_feedback_endpoint_missing_data(self, client):
        """Test the feedback endpoint requires authentication"""
        response = client.post('/feedback',
                               data='',
                               content_type='application/json',
                               follow_redirects=False)
        # Should redirect to login since user is not authenticated
        assert response.status_code == 302
        assert '/login' in response.location


class TestResumeEvaluator:
    """Tests for the resume evaluator service"""
    
    def test_evaluator_import(self):
        """Test that resume evaluator can be imported"""
        from services.resume_evaluator import get_evaluator
        evaluator = get_evaluator()
        assert evaluator is not None

    def test_evaluator_evaluate(self):
        """Test resume evaluation"""
        from services.resume_evaluator import get_evaluator
        evaluator = get_evaluator()
        
        sample_text = """
        John Doe
        Email: john@example.com
        Phone: 1234567890
        
        Summary
        Experienced developer with Python and JavaScript skills.
        
        Skills
        Python, JavaScript, React, SQL
        
        Experience
        Software Developer
        - Led development of customer portal
        - Developed automated testing
        
        Education
        Bachelor in Computer Science
        """
        
        result = evaluator.evaluate(sample_text, 'backend developer')
        
        assert 'overall_score' in result
        assert 'checklist' in result
        assert 'suggestions' in result
        assert 'red_flags' in result
        assert isinstance(result['overall_score'], int)

    def test_action_verbs_list(self):
        """Test that action verbs list is populated"""
        from services.resume_evaluator import get_action_verbs_list
        verbs = get_action_verbs_list()
        assert len(verbs) >= 50
        assert 'led' in verbs
        assert 'developed' in verbs

    def test_career_tips(self):
        """Test career tips retrieval"""
        from services.resume_evaluator import get_career_tips
        tips = get_career_tips('data scientist')
        assert len(tips) > 0
        
        default_tips = get_career_tips('unknown_career')
        assert len(default_tips) > 0

    def test_sample_bullet_points(self):
        """Test sample bullet points retrieval"""
        from services.resume_evaluator import get_sample_bullet_points
        samples = get_sample_bullet_points()
        assert 'good' in samples
        assert 'bad' in samples
        assert len(samples['good']) > 0
        assert len(samples['bad']) > 0