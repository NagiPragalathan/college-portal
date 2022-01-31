from typing import Dict, List, Union
from flask import make_response, session, request, jsonify, url_for
from flask_login import login_user
from datetime import datetime, timedelta
import json
import pickle

from . import common
from ... import models
from ... import constants


@common.route("/login-val", methods=["POST"])
def login_val():
    redirect_url = None

    req: Dict[Union[str, list]] = json.loads(request.data)
    print(req)

    # Getting data from js
    u_name: str = req.get("form-username-input-field")
    pass_: str = req.get("form-password-input-field")
    remember_me: List = req.get("form-remember-me")
    role: models.Role = req.get("role")

    if role == "Student":
        role = constants.ROLE.STUDENT
        redirect_url = url_for("student.home")
    elif role == "Staff":
        role = constants.ROLE.STAFF
    else:
        role = constants.ROLE.PARENT
        redirect_url = url_for("parent.home")

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
        user_data = user.get_data()
        session["user_data"] = pickle.dumps(user_data.as_dict())
        if user.role.role_name == constants.ROLE.STAFF.role_name:
            if user_data.is_cc:
                redirect_url = url_for("cc.home")
                class_data: models.ClassCc = [
                    class_ for class_ in user_data.classes_as_cc if class_.is_active
                ][0]
                session["class_data"] = pickle.dumps(class_data.class_.as_dict())
            else:
                redirect_url = url_for("staff.home")
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

    res = make_response(jsonify(res))
    res.set_cookie(
        "role",
        value=role.role_name.lower(),
        expires=datetime.now() + timedelta(weeks=30),
    )

    return res
