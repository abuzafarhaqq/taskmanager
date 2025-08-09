from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restx import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# initialize flask application
taskmanager = Flask(__name__)
taskmanager.config.from_object(Config)

# flask login Manager
login = LoginManager(taskmanager)
login.login_view = "login"

# flask api
api = Api(
    title="Task Manager API",
    description="A simple Task Manager API",
    version="1.0",
    prefix="/api",
    doc=False,
)

# flask api limiter
limiter = Limiter(key_func=get_remote_address)
api.init_app(taskmanager)
limiter.init_app(taskmanager)

# csrf protection for flask application
csrf = CSRFProtect(taskmanager)
csrf.init_app(taskmanager)


@login.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))


# database setup for my flask application
db = SQLAlchemy(taskmanager)
migrate = Migrate(taskmanager, db)

# importing routes and models for my flask application
from app import routes, models
