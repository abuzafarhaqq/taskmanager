# create_test_data.py
from app import taskmanager, db
from app.models import User, Task
from datetime import datetime, timedelta


def seed_data():
    with taskmanager.app_context():
        db.create_all()

        # Delete existing data (nuclear option)
        db.session.query(Task).delete()
        db.session.query(User).delete()

        # User 1 (Project Manager)
        user1 = User(
            username="abuzafar",
            email="abuzafar@gmail.com",
            password_hash="abuzafarpass",  # Use bcrypt in production
        )

        # User 2 (Developer)
        user2 = User(
            username="dev",
            email="dev@gmail.com",
            password_hash="devpass",
        )

        # Tasks
        task1 = Task(
            title="Design Auth System",
            description="OAuth2 and JWT integration",
            status="todo",
            user_id=user1,
        )

        task2 = Task(
            title="Implement Docker",
            description="Write docker-compose.yml",
            status="in_progress",
            user_id=user2,
        )

        db.session.add_all([user1, user2, task1, task2])
        db.session.commit()


seed_data()
