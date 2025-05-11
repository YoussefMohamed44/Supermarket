from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class CartForm(FlaskForm):
    title = StringField('Item Name', validators=[DataRequired()])
    submit = SubmitField('Add Order')