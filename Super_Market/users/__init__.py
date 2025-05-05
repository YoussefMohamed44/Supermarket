from flask import Blueprint

users = Blueprint("users", __name__)

from Super_Market.users import routes