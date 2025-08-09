from hashlib import md5
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.types import Text
import sqlalchemy.orm as so
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import enum
from app import db, login


class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.Text, nullable=False)
    tasks = so.relationship("Task", backref="users", lazy="dynamic")

    def get_id(self):
        return str(self.id)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    deadline = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "description": self.description,
            "status": self.status.value,
            "user_id": self.user_id,
        }

    def __repr__(self):
        return f"<Task {self.title}>"


@login.user_loader
def load_user(id: int):
    return db.session.get(User, int(id))
