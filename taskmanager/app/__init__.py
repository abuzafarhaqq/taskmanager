from flask import Flask
from config import Config

taskmanager = Flask(__name__)
taskmanager.config.from_object(Config)

from app import routes
