from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '123 456 789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Orders.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def init_db():
    # from Super_Market.models import Product
    with app.app_context():
        db.create_all()
        
        # if Product.query.count() == 0:
        #     products = [
        #         Product(name="Avocado", description="A healthy and nutritious fruit", price=3.99, image_url="/static/images/avocado.jpeg"),
        #         Product(name="Banana", description="A healthy and nutritious fruit", price=0.99, image_url="/static/images/banana.png"),
        #         Product(name="Apple", description="A healthy and nutritious fruit", price=1.49, image_url="/static/images/apple.png"),
        #         Product(name="Orange", description="A healthy and nutritious fruit", price=1.99, image_url="/static/images/orange.jpeg"),
        #         Product(name="Carrot", description="A healthy and nutritious vegetable", price=1.99, image_url="/static/images/Carrot.png"),
        #         Product(name="Potato", description="A healthy and nutritious vegetable", price=1.49, image_url="/static/images/Potato.png"),
        #         Product(name="Onion", description="A healthy and nutritious vegetable", price=1.99, image_url="/static/images/Onion.png"),
        #         Product(name="Tomato", description="A healthy and nutritious vegetable", price=2.99, image_url="/static/images/Tomato.png"),
        #         Product(name="Cucumber", description="A healthy and nutritious vegetable", price=1.99, image_url="/static/images/Cucumber.png"),
        #         Product(name="Egg", description="A healthy and nutritious protein", price=2.99, image_url="/static/images/egg.jpg"),
        #         Product(name="Milk", description="A healthy and nutritious protein", price=2.99, image_url="/static/images/milk.jpeg"),
        #         Product(name="Cheese", description="A healthy and nutritious protein", price=2.99, image_url="/static/images/cheese.png"),
        #         Product(name="Butter", description="A healthy and nutritious protein", price=2.99, image_url="/static/images/Butter.png"),
        #         Product(name="Bread", description="A healthy and nutritious protein", price=2.99, image_url="/static/images/bread.jpg"),
        #         Product(name="Jam", description="A healthy and nutritious protein", price=2.99, image_url="/static/images/Jam.png"),
        #     ]
        #     db.session.add_all(products)
        #     db.session.commit()
        
init_db()

# Import routes after initializing app to avoid circular imports
import os
import sys

# Add the parent directory to Python path
basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(basedir)
sys.path.insert(0, project_root)
sys.path.insert(0, basedir)

from Super_Market.Main.routes import main
from Super_Market.users.routes import users
# from Super_Market.Review.routes import Reviews 
# from Super_Market.cart.routes import cart

app.register_blueprint(main)
app.register_blueprint(users)
# app.register_blueprint(Reviews)
# app.register_blueprint(cart)

# Delay user loader to break circular dependency
def set_user_loader():
    from Super_Market.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

set_user_loader()