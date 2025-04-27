from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

taskmanager = Flask(__name__)
taskmanager.config.from_object(Config)
csrf = CSRFProtect(taskmanager)
csrf.init_app(taskmanager)

db = SQLAlchemy(taskmanager)
migrate = Migrate(taskmanager, db)

from app import routes, models
