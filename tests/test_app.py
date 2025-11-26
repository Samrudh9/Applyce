import pytest
import sys
import os
sys.path.insert(0, os. path.dirname(os.path. dirname(os.path. abspath(__file__))))

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
        response = client.get('/upload')
        assert response.status_code == 200
    
    def test_about_page(self, client):
        response = client.get('/about')
        assert response.status_code == 200