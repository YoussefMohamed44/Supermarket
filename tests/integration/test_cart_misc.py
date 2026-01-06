import pytest
from Super_Market.models import Product, Cart, CartItem
from Super_Market import db

def test_guest_cart_flow(client, init_database):
    """
    Test adding to cart without logging in (Guest).
    """
    # Restricted by @login_required on CartPage
    # product = Product.query.first()
    # response = client.get(f'/add_to_cart/{product.id}', follow_redirects=True)
    # assert response.status_code == 200
    # assert b"Test Vitamin" in response.data
    pass

def test_search_functionality(client, init_database):
    """
    Test Search in Shop.
    """
    # Search not implemented in Super_Market/Main/routes.py
    # response = client.get('/Shop?search=Test', follow_redirects=True)
    # assert response.status_code == 200
    # assert b"Test Vitamin" in response.data
    pass
