from os import environ as env
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
app.config["TEMPLATE_JSON"] = env.get("TEMPLATE_JSON")


@app.route("/admin-login")
def admin_login():
    return render_template("login/admin.html.j2")


@app.route("/common-login")
def common_login():
    return render_template("login/common.html.j2", role="staff")


@app.route("/create-staff-login")
def create_staff_login():
    with open(
        os.path.join(
            app.config.get("TEMPLATE_JSON"), "admin", "create_staff_login.json"
        )
    ) as f:
        page_template = json.load(f)

    return render_template(
        "admin/create_staff_login.html.j2",
        page_template=page_template,
    )


@app.route("/create-student-login")
def create_student_login():
    with open(
        os.path.join(
            app.config.get("TEMPLATE_JSON"), "staff", "create_student_login.json"
        )
    ) as f:
        page_template = json.load(f)

    return render_template(
        "staff/create_student_login.html.j2",
        page_template=page_template,
    )
