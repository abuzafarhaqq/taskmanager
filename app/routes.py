from flask_migrate import current, log
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user, login_required
from flask_restx import Resource, Api, fields
from flask_restx.inputs import email
from app import taskmanager, db, api, limiter
from app.forms import LoginForm, RegistrationForm, TaskForm, EditTaskForm
from app.models import User, Task, TaskStatus
import bcrypt
from datetime import datetime
from email_validator import EmailNotValidError


@taskmanager.route("/")
@taskmanager.route("/index/")
@login_required
def index():
    if current_user.is_authenticated:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return render_template("index.html", title="Home Page", tasks=tasks)
    return redirect(url_for("login"))


@taskmanager.route("/add/", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            task = Task(
                title=form.title.data,
                deadline=form.deadline.data,
                status=TaskStatus.TODO,
                description=form.description.data,
                user_id=current_user.id,
            )
            db.session.add(task)
            db.session.commit()
            flash("Task added successfully", "success")
            return redirect(url_for("index"))
        flash("Task add failed", "error")
    return render_template("add_task.html", form=form)


@taskmanager.route("/complete/<int:task_id>")
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized actions!", "error")
        return redirect(url_for("index"))
    task.status = TaskStatus.DONE
    db.session.commit()
    flash("Task marked as completed!", "success")
    return redirect(url_for("index"))


@taskmanager.route("/edit/<int:task_id>/", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized action", "error")
        return redirect("index")
    form = EditTaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        task.status = TaskStatus(form.status.data) if form.status.data else task.status
        db.session.commit()
        flash("Task Updated successfully!", "success")
        return redirect(url_for("index"))
    return render_template("edit_task.html", form=form, task=task)


@taskmanager.route("/delete/<int:task_id>/")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized action!", "error")
        return redirect(url_for("index"))
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for("index"))


@taskmanager.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        # flash("Login requested for user {}, remember_me={}, password {}".format(form.username.data, form.remember_me.data, form.password.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            # flash(f"Next page: {next_page}")
            next_page = url_for("index")
        return redirect(next_page)
        # flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
    return render_template("login.html", title="Sign In", form=form)


@taskmanager.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if User.query.filter_by(email=form.email.data).first():
                flash("Email already registered!", "error")
                return redirect(url_for("register"))
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you are now a registered user!")
            return redirect(url_for("login"))
        except EmailNotValidError:
            flash("Invalid email address", "error")
    return render_template("register.html", title="Register Account", form=form)


@taskmanager.route("/logout/")
def logout():
    logout_user()
    flash("Logged Out successfully", "success")
    return redirect(url_for("login"))


@taskmanager.route("/user/")
@login_required
def user():
    """This is the user profile page"""
    return render_template("user.html", title="User Profile", user=current_user)


# ---------------- API Routes --------------
task_model = api.model(
    "Task",
    {
        "id": fields.Integer,
        "title": fields.String,
        "deadline": fields.DateTime,
        "status": fields.String,
        "description": fields.String,
        "user_id": fields.Integer,
    },
)


@api.route("/tasks")
class TaskList(Resource):
    @login_required
    @limiter.limit("100/minute")
    @api.marshal_list_with(task_model)
    def get(self):
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return [Task.serialize() for task in tasks]

    @login_required
    @api.expect(task_model)
    @api.marshal_with(task_model, code=201)
    def post(self):
        data = api.payload
        task = Task(
            title=data["title"],
            deadline=datetime.fromisoformat(data["deadline"])
            if data.get("deadline")
            else None,
            status=TaskStatus.TODO,
            description=data.get("description") if data.get("description") else None,
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        return task_serialize(), 201


@api.route("/tasks/<int:task_id>")
class TaskResource(Resource):
    @login_required
    @api.marshal_with(task_model)
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            api.abort(403, "Unauthorized")
        return task.serialize()

    @login_required
    @api.expect(task_model)
    @api.marshal_with(task_model)
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            api.abort(403, "Unauthorized")
        data = api.payload
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        if data.get("deadline"):
            task.deadline = datetime.fromisoformat(data["deadline"])
        task.status = TaskStatus(data.get("status", task.status.value))
        db.session.commit()
        return task.serialize()

    @login_required
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            api.abort(403, "Unauthorized")
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted"}, 200
