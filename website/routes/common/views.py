from flask import redirect, render_template, url_for
from flask_login import login_required, current_user, logout_user

from . import common


@common.route("/login")
def login():
    return render_template("login/common.html.j2", role="staff")


@common.route("/logout")
def logout():
    if current_user.role.role_name == "Admin":
        redirect_url = url_for("admin.login")
    else:
        redirect_url = url_for("common.login")
    logout_user()
    return redirect(redirect_url)
