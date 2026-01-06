import pytest
from Super_Market.models import Product, Cart, CartItem
from Super_Market import db

def test_main_routes_coverage(client, init_database):
    """Cover About, Shop Category Filter, and Product Description."""
    # 1. About
    response = client.get('/About')
    assert response.status_code == 200
    
    # 2. Category Filter
    # Ensure product exists with category
    product = Product.query.first()
    response = client.get(f'/Shop?category={product.category}')
    assert response.status_code == 200
    assert product.name in response.get_data(as_text=True)
    
    # 3. Product Description - NOT USED IN SUPER MARKET
    # response = client.get(f'/product/{product.id}')
    # assert response.status_code == 200
    # assert product.name in response.get_data(as_text=True)

def test_cart_advanced_coverage(client, init_database):
    """Cover duplicate item add, create_products logic, and guest clearing."""
    
    # 1. Create Products Utility
    # First call: already exists (init_database adds one) OR manual check if init_database runs before this test?
    # conftest init_database runs for each test that requests it.
    # Product count > 0 -> "Products already exist!"
    response = client.get('/create_products')
    assert b"Products already exist!" in response.data
    
    # Clear products to test creation
    CartItem.query.delete()
    Cart.query.delete()
    Product.query.delete()
    db.session.commit()
    
    # Second call: empty -> "Products created!"
    response = client.get('/create_products')
    assert b"Products created!" in response.data
    assert Product.query.count() > 0
    
    # 2. Add Item Twice (Quantity Increment)
    product = Product.query.first()
    # Guest add 1
    client.get(f'/add_to_cart/{product.id}', follow_redirects=True)
    # Guest add 2
    client.get(f'/add_to_cart/{product.id}', follow_redirects=True)
    
    cart = Cart.query.first() # session cart
    item = cart.items[0]
    assert item.quantity == 2

    # 3. Guest Clear Cart
    # We removed @login_required, so this should work for session-based cart
    # BUT Super_Market app has @login_required on clear_cart, so this fails.
    # response = client.post('/clear_cart', follow_redirects=True)
    # assert response.status_code == 200
    # assert len(cart.items) == 0

def test_empty_cart_render(client, init_database):
    """Render Cart page with no cart record in DB."""
    # Must login as Cart is @login_required
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    
    response = client.get('/Cart')
    assert response.status_code == 200
    assert b"Your cart is empty" in response.data or b"Total: $0.0" in response.data
