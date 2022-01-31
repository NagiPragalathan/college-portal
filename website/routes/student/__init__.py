from flask import Blueprint
from flask_login import current_user

student = Blueprint("student", __name__)


@student.before_request
def before_request():
    if "Student" != current_user.role.role_name:
        return "<h1>Unauthorized Access</h1>"


from . import api
from . import views
