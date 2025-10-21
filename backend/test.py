import pytest
from backend.main import create_app, db
from config import Config
from models import Project, Contact

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    MAIL_SUPPRESS_SEND = True

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_projects(client):
    # Test empty projects list
    response = client.get('/api/portfolio/')
    assert response.status_code == 200
    assert response.json == []

    # Add test project
    with app().app_context():
        project = Project(
            title='Test Project',
            description='Test Description',
            image_url='http://test.com/image.jpg',
            project_url='http://test.com',
            github_url='http://github.com/test'
        )
        db.session.add(project)
        db.session.commit()

        # Test projects list with one project
        response = client.get('/api/portfolio/')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['title'] == 'Test Project'

def test_submit_contact(client):
    # Test valid contact submission
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'subject': 'Test Subject',
        'message': 'Test Message'
    }
    response = client.post('/api/contact/', json=data)
    assert response.status_code == 201
    
    # Test invalid email
    data['email'] = 'invalid-email'
    response = client.post('/api/contact/', json=data)
    assert response.status_code == 400
    
    # Test missing required field
    del data['name']
    response = client.post('/api/contact/', json=data)
    assert response.status_code == 400