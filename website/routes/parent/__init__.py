from flask import Blueprint
from flask_login import current_user

parent = Blueprint("parent", __name__)


@parent.before_request
def before_request():
    if "Parent" != current_user.role.role_name:
        return "<h1>Unauthorized Access</h1>"


from . import api
from . import views
