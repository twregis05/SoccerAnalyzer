from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User
from random import randint

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("stats.index"))
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )
            user.save()
            return redirect(url_for("users.login"))
    return render_template("signup.html", form=form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("stats.index"))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("stats.index"))
            else:
                flash("Login failed. Check your username and/or password")
    return render_template("login.html", form=form)



# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html")


@users.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            User.objects(username=current_user.username).update(
                set__username=update_username_form.username.data
            )
            logout_user()
            return redirect(url_for("users.settings"))
        update_username_form.username.data = ""

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            image = update_profile_pic_form.picture.data
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic is None:
                current_user.profile_pic.put(
                    image.stream, 
                    content_type=content_type
                )
            else:
                current_user.profile_pic.replace(
                    image.stream,
                    content_type=content_type
                )
            current_user.save()
            return redirect(url_for("users.settings"))

    # TODO: handle get requests
    user = User.objects(username=current_user.username).first()
   
    greeting = random_greeting() + current_user.username + '!'
    image = None
    if user.profile_pic:
        bytes_im = BytesIO(user.profile_pic.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
    
    return render_template(
        "settings.html", 
        greeting=greeting, 
        update_username_form=update_username_form,
        update_profile_pic_form=update_profile_pic_form,
        image=image
    )
    
def random_greeting():
    arr = [
        "Welcome back, ", 
        "Howdy, ",
        "Good to see you, ",
        "Hello, "
    ]
    return arr[randint(0, len(arr) - 1)]