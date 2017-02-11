from flask import Blueprint

api = Blueprint('api', __name__)

from . import sign, signup, tasks, users, views, comments
