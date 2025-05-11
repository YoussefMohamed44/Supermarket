from Super_Market.Review import Reviews

from Super_Market.models import Review
from Super_Market import db
from flask import Flask, render_template , redirect, url_for, flash, session
from Super_Market.Review.forms import ReviewForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid


@Reviews.route('/Reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            title=form.title.data.strip(),
            content=form.content.data.strip(),
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added!', 'success')
        return redirect(url_for('Reviews.reviews'))
    
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.id.desc()).all()
    return render_template('Review.html', form=form, reviews=user_reviews)


@Reviews.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews.', 'danger')
        return redirect(url_for('Reviews.reviews'))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review.title = form.title.data.strip()
        review.content = form.content.data.strip()
        db.session.commit()
        flash('Review updated!', 'success')
        return redirect(url_for('Reviews.reviews'))
    
    form.title.data = review.title
    form.content.data = review.content
    return render_template('Edit_Review.html', form=form, review=review)


@Reviews.route('/reviews/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.user_id != current_user.id:
        flash('You are not allowed to delete this review.', 'danger')
        return redirect(url_for('Reviews.reviews'))
    
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'info')
    return redirect(url_for('Reviews.reviews'))