from Super_Market.Main import main

# from Super_Market.models import Product
from Super_Market import bcrypt, db
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid


@main.route('/')
@main.route("/Home", methods=['GET','POST'])
def Home():
    return render_template('Home.HTML', title = "Home", cssFile = "Static/css/Home.css")

@main.route("/About")
def about():
    return render_template('About.HTML', title = "About", cssFile = "Static/css/About.css")

# @main.route("/Shop")
# def Shop():
#     products = Product.query.all()
#     return render_template('Shop.html', products=products)