from flask import Blueprint

cart = Blueprint("cart", __name__)

from Super_Market.cart import routes