from flask import Blueprint
from flask_login import current_user

staff = Blueprint("staff", __name__)


@staff.before_request
def before_request():
    if "Staff" != current_user.role.role_name:
        return "<h1>Unauthorized Access</h1>"


from . import api
from . import views
