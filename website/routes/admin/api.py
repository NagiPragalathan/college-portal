from typing import Dict, List, Union
from flask import request, jsonify, url_for, session
from flask_login import login_user
from datetime import datetime, timedelta
import json
import pickle

from . import admin
from ... import models
from ... import constants


@admin.route("/login-val", methods=["POST"])
def login_val():
    redirect_url = url_for("admin.home")

    req: Dict[Union[str, list]] = json.loads(request.data)
    print(req)

    # Getting data from js
    u_name: str = req.get("form-username-input-field")
    pass_: str = req.get("form-password-input-field")
    remember_me: List = req.get("form-remember-me")
    role: models.Role = constants.ROLE.ADMIN

    user: models.User = (
        models.User.query.filter(
            (models.User.u_name == u_name) | (models.User.email == u_name)
        )
        .filter(models.User.role == role)
        .first()
    )

    remember_me: bool = True if remember_me else False
    status = True if user and user.password == pass_ else False
    errors = {k: "" for k in req.keys()}

    if status:
        session["user_data"] = pickle.dumps(user.get_data().as_dict())
        login_user(user, remember=remember_me)

    else:
        if not user:
            errors["form-username-input-field"] = "Invalid Username or Email."
        elif not status and user:
            errors["form-password-input-field"] = "Invalid Password."

    res = {
        "status": status,
        "redirect_url": redirect_url if status else "",
        "errors": errors,
    }

    return res
