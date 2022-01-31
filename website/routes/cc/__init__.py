from flask import Blueprint, session
from flask_login import current_user
import pickle

cc = Blueprint("cc", __name__)


@cc.before_request
def before_request():
    if "Staff" != current_user.role.role_name and not pickle.loads(
        session.get("user_data")
    ).get("is_cc"):
        return "<h1>Unauthorized Access</h1>"


from . import api
from . import views
