from flask import render_template, session
from flask_login import login_required, current_user
import pickle
from ... import models

from . import admin


@admin.route("/login")
def login():
    return render_template("login/admin.html.j2")


@admin.route("/")
@login_required
def home():
    admin: dict = pickle.loads(session.get("user_data"))
    return f"<h1>Admin's Homepage</h1><p>Welcome,{current_user.u_name}{admin}</p>"
