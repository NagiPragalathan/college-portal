from flask_login import login_required, current_user
from . import parent


@parent.route("/")
@login_required
def home():
    return f"<h1>Parent's Homepage</h1><p>Welcome,{current_user.u_name}</p>"
