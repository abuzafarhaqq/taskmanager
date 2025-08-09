import os


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "bongoDev-task-manager-project-is-secret"
    )
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql+psycopg2://taskadmin:taskAdminPass123!@localhost:5432/taskmanager"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
