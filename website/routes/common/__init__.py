from flask import Blueprint

common = Blueprint("common", __name__)

from . import api
from . import views
