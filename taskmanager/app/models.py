from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    # __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = so.relationship("Task", backref="author", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default="todo")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Task {self.title}>"
