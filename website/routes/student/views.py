from flask_login import login_required, current_user
from . import student


@student.route("/")
@login_required
def home():
    return f"<h1>Student's Homepage</h1><p>Welcome,{current_user.u_name}</p>"
