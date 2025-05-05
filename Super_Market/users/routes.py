from Super_Market.users import users

from Super_Market.models import User
from Super_Market import bcrypt, db
from flask import Flask, render_template , redirect, url_for, flash, session
from Super_Market.users.forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user
import uuid



@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['user_id'] = user.id
            flash(f"Logged in successfully! Welcome {user.username}", "success")
            return redirect(url_for("main.Home"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template('login.html', form=form)

@users.route('/register', methods=['GET','POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.strip()).first():
            flash("Email already registered. Please log in.", "danger")
            return render_template('signup.HTML', form=form)
        if User.query.filter_by(phone=form.phone.data.strip()).first():
            flash("Phone number already registered. Please log in.", "danger")
            return render_template('signup.HTML', form=form)
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            phone=form.phone.data.strip(),
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("users.login"))
   return render_template('signup.HTML', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for('main.Home'))