from flask import render_template
from app import taskmanager


@taskmanager.route("/")
@taskmanager.route("/index")
def index():
    return render_template("index.html", title="Home Page")
