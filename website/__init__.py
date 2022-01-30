from os import environ as env
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/admin-login')
def admin_login():
    return render_template("login/admin.html.j2")

@app.route('/common-login')
def common_login():
    return render_template("login/common.html.j2", role="staff")
