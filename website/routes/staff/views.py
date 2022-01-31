from flask import redirect, session, url_for
from flask_login import login_required, current_user
import pickle

from . import staff


@staff.route("/")
@login_required
def home():
    if pickle.loads(session.get("user_data")).get("is_cc"):
        return redirect(url_for("cc.home"))
    return f"<h1>Staff's Homepage</h1><p>Welcome,{current_user.u_name}</p>"
