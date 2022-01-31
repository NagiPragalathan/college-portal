from flask import Blueprint
from flask_login import current_user

admin = Blueprint("admin", __name__)


@admin.before_request
def before_request():
    if current_user.is_authenticated and "Admin" != current_user.role.role_name:
        return "<h1>Unauthorized Access</h1>"


from . import api
from . import views
