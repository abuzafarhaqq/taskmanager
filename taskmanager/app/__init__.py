from flask import Flask

taskmanager = Flask(__name__)

from app import routes
