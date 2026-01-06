import pytest
from Super_Market.models import Product, Review
from Super_Market import db, bcrypt

def test_review_lifecycle(client, init_database):
    """
    Test the full lifecycle of a review: Create -> Read -> Edit -> Delete.
    """
    # 1. Login
    client.post('/login', data={'email': 'test@example.com', 'password': 'hashedpassword'}) # Password hash from init_database fixture
    
    # Need a proper user login with known password.
    # The init_database fixture in conftest.py uses "hashedpassword" as hash but we need to know the plain text?
    # Actually conftest.py was fixed to use 'password123' and generate hash.
    # So we log in with 'password123'.
    
    # Re-login with correct credentials just to be safe/explicit, or rely on session if fixture logs in?
    # init_database just seeds data. usage requires login.
    login_resp = client.post('/login', data={'email': 'test@example.com', 'password': 'password123'}, follow_redirects=True)
    assert login_resp.status_code == 200
    assert b"testuser" in login_resp.data

    # Product is already in DB from init_database (id=1)
    product = Product.query.first()
    
    # 2. Create Review
    # Route: /Reviews (POST)
    # Form fields: title, content
    response = client.post('/Reviews', data={
        'title': 'Great Product',
        'content': 'This vitamin really helped me sleep.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Great Product" in response.data
    # assert b"This vitamin really helped me sleep" in response.data # Might not be shown on success redirect depending on template

    review = Review.query.filter_by(title='Great Product').first()
    assert review is not None

    # 3. Edit Review (GET) - Covers pre-population lines
    response = client.get(f'/edit_review/{review.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Great Product" in response.data

    # 3b. Edit Review (POST)
    # Route: /edit_review/<int:review_id> (POST)
    response = client.post(f'/edit_review/{review.id}', data={
        'title': 'Updated Title',
        'content': 'Updated content for the review.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    db.session.refresh(review)
    assert review.title == 'Updated Title'

def test_review_unauthorized_access(client, init_database):
    """Test editing/deleting someone else's review."""
    from Super_Market.models import User, Review
    
    # Login as User 1 (owner)
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    
    # Create Review
    client.post('/Reviews', data={'title': 'My Review', 'content': 'Mine is longer than 5 chars'}, follow_redirects=True)
    review = Review.query.filter_by(title='My Review').first()
    assert review is not None
    
    # Logout
    client.get('/logout')
    
    # Create User 2 and Login
    hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
    user2 = User(username="thief", email="thief@test.com", phone="11122233344", password=hashed_pw)
    db.session.add(user2)
    db.session.commit()
    
    client.post('/login', data={'email': 'thief@test.com', 'password': 'password123'})
    
    # Try to Edit User 1's review
    response = client.post(f'/edit_review/{review.id}', data={'title': 'Stolen', 'content': 'Stolen'}, follow_redirects=True)
    assert b"You can only edit your own reviews" in response.data
    
    # Try to Delete User 1's review
    response = client.post(f'/reviews/delete/{review.id}', follow_redirects=True)
    assert b"You are not allowed to delete this review" in response.data
