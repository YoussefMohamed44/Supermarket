import pytest
from Super_Market.models import User, Product, Cart, CartItem
from Super_Market import db, bcrypt

def test_home_page(client):
    """
    Test that the home page loads correctly.
    """
    response = client.get('/Home')
    response = client.get('/Home')
    assert response.status_code == 200
    # Updated to match actual template content
    assert b"Whole Foods" in response.data

def test_register_and_login_flow(client):
    """
    Test the full registration and login flow.
    Integration: Tests User Model + DB + Routes + Auth Logic.
    """
    # 1. Register
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@test.com',
        'phone': '01012345678',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created" in response.data

    # Verify DB
    user = User.query.filter_by(email='new@test.com').first()
    assert user is not None
    assert user.username == 'newuser'

    # 2. Login
    response = client.post('/login', data={
        'email': 'new@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

def test_add_to_cart_and_checkout_flow(client, init_database):
    """
    Test adding items to cart and clearing it (Checkout simulation).
    Integration: Tests Product -> Cart -> CartItem -> DB Relationship.
    """
    # Login first
    client.post('/login', data={'email': 'test@example.com', 'password': 'hashedpassword'}) # Password hash mismatch in fixture?
    # Actually, let's create a user properly with bcrypt for this test to be sure
    hashed_pw = bcrypt.generate_password_hash('realpassword').decode('utf-8')
    user = User(username="shopper", email="shop@test.com", phone="01111111111", password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    # Login
    client.post('/login', data={'email': 'shop@test.com', 'password': 'realpassword'})

    # Get a product ID (created in init_database fixture)
    product = Product.query.first()
    assert product is not None

    # Add to Cart
    response = client.get(f'/add_to_cart/{product.id}', follow_redirects=True)
    assert response.status_code == 200

    # Verify Cart Page
    response = client.get('/Cart')
    assert b"Test Vitamin" in response.data
    assert b"20.0" in response.data

    # Verify DB State
    cart = Cart.query.filter_by(user_id=user.id).first()
    assert cart is not None
    assert len(cart.items) == 1
    assert cart.items[0].product_id == product.id

    # Simulated Checkout (Clear Cart)
    response = client.post('/clear_cart', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify Empty
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    assert len(cart_items) == 0
    assert b"Your cart is empty" in response.data

def test_database_crud_product(client):
    """
    Test direct Database CRUD operations for Products.
    """
    # Create
    new_prod = Product(name="New Protein", price=50.0, category="Fitness")
    db.session.add(new_prod)
    db.session.commit()

    # Read
    retrieved = Product.query.filter_by(name="New Protein").first()
    assert retrieved is not None
    assert retrieved.price == 50.0

    # Update
    retrieved.price = 55.0
    db.session.commit()
    updated = Product.query.filter_by(name="New Protein").first()
    assert updated.price == 55.0

    # Delete
    db.session.delete(updated)
    db.session.commit()
    deleted = Product.query.filter_by(name="New Protein").first()
    assert deleted is None
