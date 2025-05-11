from Super_Market.cart import cart

from Super_Market.models import Cart, CartItem, Product
from Super_Market import bcrypt, db
from flask import Flask, render_template , redirect, url_for, flash, session
from Super_Market.cart.forms import CartForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid



@cart.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' in session:
        user_id = session['user_id']
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
    else:
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
        if not cart:
            cart = Cart(session_id=session_id)
            db.session.add(cart)
            db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('main.Shop'))

@cart.route('/create_products')
def create_products():
    if Product.query.count() == 0:
        products = [
            Product(name="Gut Health+", description="Improve Digestion", price=44.99, image_url="/static/images/GutHealth+.png"),
            Product(name="B Complex", description="Essential B Vitamins", price=44.99, image_url="/static/images/B-Complex.png"),
            Product(name="Fiber", description="Promote Digestive Health", price=44.99, image_url="/static/images/Fiber.png"),
            Product(name="Liver", description="Support Optimal Liver Health", price=44.99, image_url="/static/images/Liver.png"),
            Product(name="Multi Mineral", description="Support Healthy Bones and Joints", price=44.99, image_url="/static/images/MultiMineral.png"),
            Product(name="Multi Vitamin", description="Provide Essential Micronutrients", price=44.99, image_url="/static/images/MultiVitamin.png"),
            Product(name="Thyroid Support", description="Keep Thyroid Operating at Optimal Rate", price=44.99, image_url="/static/images/ThyroidSupport.png"),
            Product(name="Omega 3", description="Support Cardiovascular Health", price=44.99, image_url="/static/images/Omega3.png"),
            ]
        db.session.add_all(products)
        db.session.commit()
        return "Products created!"
    else:
        return "Products already exist!"

@cart.route('/Cart')
@login_required
def CartPage():
    if 'user_id' in session:
        user_id = session['user_id']
        cart = Cart.query.filter_by(user_id=user_id).first()
    elif 'session_id' in session:
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
    else:
        cart = None

    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total = 0.0
    return render_template('Cart.Html', cart_items=cart_items, total=total)

@cart.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    cart = None
    if 'user_id' in session:
        user_id = session['user_id']
        cart = Cart.query.filter_by(user_id=user_id).first()
    elif 'session_id' in session:
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
    
    if cart:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
    return redirect(url_for('cart.CartPage'))