import pytest
from app import app, db
from app.models import User, Task, TaskStatus
import bcrypt


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://taskadmin:taskAdminPass123!@localhost:5432/taskmanager_test"
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_and_login(client):
    # Register a user
    response = client.post(
        "/register", data={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 302
    assert User.query.filter_by(email="test@example.com").first() is not None

    # Login
    response = client.post(
        "/login", data={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 302


def test_add_task(client):
    # Register and login
    client.post(
        "/register", data={"email": "test@example.com", "password": "password123"}
    )
    client.post("/login", data={"email": "test@example.com", "password": "password123"})

    # Add a task
    response = client.post(
        "/add", data={"title": "Test Task", "deadline": "2025-07-10"}
    )
    assert response.status_code == 302
    assert Task.query.filter_by(title="Test Task").first() is not None


def test_complete_and_delete_task(client):
    # Register, login, and add a task
    client.post(
        "/register", data={"email": "test@example.com", "password": "password123"}
    )
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    client.post("/add", data={"title": "Test Task", "deadline": "2025-07-10"})

    task = Task.query.filter_by(title="Test Task").first()

    # Complete task
    response = client.get(f"/complete/{task.id}")
    assert response.status_code == 302
    assert Task.query.get(task.id).status == TaskStatus.DONE

    # Delete task
    response = client.get(f"/delete/{task.id}")
    assert response.status_code == 302
    assert Task.query.get(task.id) is None
