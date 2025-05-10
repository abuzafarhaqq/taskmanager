from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user, login_required
from app import taskmanager, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@taskmanager.route("/")
def index():
    return render_template("index.html", title="Home Page")


@taskmanager.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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
            next_page = url_for("home")
        return redirect(next_page)
        # flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
    return render_template("login.html", title="Sign In", form=form)


@taskmanager.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register Account", form=form)


@taskmanager.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@taskmanager.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """This the home page of the application only accessible to logged in users"""
    return render_template("home.html", title="Home Page")


@taskmanager.route("/user/<username>")
@login_required
def user(username):
    """This is the user profile page"""
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", title="User Profile", user=user)
