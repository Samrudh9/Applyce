"""
Tests for Job Match API endpoint.
"""

import json
import pytest
from app import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestJobMatchAPI:
    """Test suite for /api/job-match endpoint."""
    
    def test_job_match_with_resume_text(self, client):
        """Test job match with resume text provided."""
        payload = {
            'resume_text': 'I have experience with Python, SQL, Machine Learning, and AWS. '
                          'Built data pipelines and ML models.',
            'job_description': 'Looking for a Data Scientist with Python, SQL, Machine Learning, '
                             'TensorFlow, and AWS experience.',
            'required_skills': ['Python', 'SQL', 'Machine Learning'],
            'preferred_skills': ['TensorFlow', 'AWS']
        }
        
        response = client.post(
            '/api/job-match',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'match_percentage' in data
        assert data['match_percentage'] > 0
        assert 'required_matched' in data
        assert 'preferred_matched' in data
        assert 'missing_required' in data
        assert 'missing_preferred' in data
        assert 'recommendation' in data
    
    def test_job_match_only_job_description(self, client):
        """Test job match with only job description (auto-extract skills)."""
        payload = {
            'resume_text': 'Full stack developer with React, Node.js, Python, and SQL experience.',
            'job_description': 'We need a full stack developer proficient in React, Node.js, '
                             'Python, SQL, Docker, and Kubernetes.'
        }
        
        response = client.post(
            '/api/job-match',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert data['match_percentage'] > 0
        assert len(data['required_matched']) > 0
    
    def test_job_match_missing_resume(self, client):
        """Test error when neither resume_text nor resume_id provided."""
        payload = {
            'job_description': 'Looking for Python developer'
        }
        
        response = client.post(
            '/api/job-match',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_job_match_missing_job_info(self, client):
        """Test error when neither job_description nor required_skills provided."""
        payload = {
            'resume_text': 'Python developer with 5 years experience'
        }
        
        response = client.post(
            '/api/job-match',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_job_match_invalid_json(self, client):
        """Test error when request body is not JSON."""
        response = client.post(
            '/api/job-match',
            data='not json',
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_job_match_high_score(self, client):
        """Test job match with high matching skills."""
        payload = {
            'resume_text': 'Python, SQL, Machine Learning, TensorFlow, AWS, Docker, React, JavaScript',
            'required_skills': ['Python', 'SQL', 'Machine Learning'],
            'preferred_skills': ['TensorFlow', 'AWS']
        }
        
        response = client.post(
            '/api/job-match',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        # Should have high match since all required skills are present
        assert data['match_percentage'] >= 70
        assert len(data['required_matched']) == 3
        assert len(data['missing_required']) == 0
    
    def test_job_match_low_score(self, client):
        """Test job match with low matching skills."""
        payload = {
            'resume_text': 'Marketing, Sales, Communication, Excel',
            'required_skills': ['Python', 'SQL', 'Machine Learning'],
            'preferred_skills': ['TensorFlow', 'AWS']
        }
        
        response = client.post(
            '/api/job-match',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        # Should have low match since no technical skills match
        assert data['match_percentage'] < 50
        assert len(data['missing_required']) > 0


class TestJobMatchService:
    """Test suite for JobMatchService."""
    
    def test_extract_skills_from_text(self):
        """Test skill extraction from text."""
        from services.job_match_service import job_match_service
        
        text = "Looking for Python developer with React, SQL, and AWS experience."
        skills = job_match_service.extract_skills_from_text(text)
        
        assert 'python' in skills
        assert 'react' in skills
        assert 'sql' in skills
        assert 'aws' in skills
    
    def test_semantic_similarity(self):
        """Test semantic similarity calculation."""
        from services.job_match_service import job_match_service
        
        text1 = "Python machine learning data science"
        text2 = "Python ML data scientist"
        
        similarity = job_match_service.calculate_semantic_similarity(text1, text2)
        
        assert similarity > 0
        assert similarity <= 1.0
    
    def test_calculate_job_match_full(self):
        """Test full job match calculation."""
        from services.job_match_service import job_match_service
        
        resume_skills = ['python', 'sql', 'machine learning', 'aws']
        required_skills = ['python', 'sql', 'machine learning']
        preferred_skills = ['tensorflow', 'docker']
        job_description = "We need a Python developer with SQL and machine learning skills."
        
        result = job_match_service.calculate_job_match(
            resume_skills=resume_skills,
            job_description=job_description,
            required_skills=required_skills,
            preferred_skills=preferred_skills
        )
        
        assert 'match_percentage' in result
        assert 'required_matched' in result
        assert 'preferred_matched' in result
        assert 'missing_required' in result
        assert 'recommendation' in result
        
        # All required skills are present
        assert len(result['required_matched']) == 3
        assert len(result['missing_required']) == 0
        assert result['match_percentage'] >= 70


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
