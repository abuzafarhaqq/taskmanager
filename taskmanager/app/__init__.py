from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

taskmanager = Flask(__name__)
taskmanager.config.from_object(Config)
csrf = CSRFProtect(taskmanager)
csrf.init_app(taskmanager)
login = LoginManager(taskmanager)
login.login_view = "login"


@login.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))


db = SQLAlchemy(taskmanager)
migrate = Migrate(taskmanager, db)

from app import routes, models
