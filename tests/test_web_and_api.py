import pytest

from plataforma_qa import create_app
from plataforma_qa.config import Config
from plataforma_qa.extensions import db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_list_users(client):
    response = client.post(
        "/users/",
        data={"name": "Nico Migliorini", "email": "nico@example.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Nico Migliorini" in html
    assert "nico@example.com" in html
