from flask_login import login_required, current_user
from . import cc


@cc.route("/")
@login_required
def home():
    return f"<h1>CC's Homepage</h1><p>Welcome,{current_user.u_name}</p>"
