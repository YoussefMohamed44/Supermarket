# Supermarket – Full Stack Flask Web App
A fully functional, blueprint-based Flask web application for an online supermarket store. Users can browse products, register, log in, write reviews, and manage a shopping cart. The site is styled with Bootstrap and supports authentication, product management, and more.

---

## 🔧 Tech Stack

### Backend
- **Python 3**
- **Flask** – Web framework
- **Flask-WTF** – Secure form handling with CSRF protection
- **WTForms** – Form rendering and validation
- **Flask-SQLAlchemy** – ORM for database access
- **Flask-Bcrypt** – Password hashing
- **Flask-Login** – User authentication and session management
- **email-validator** – Validates emails during registration

### Frontend
- **HTML5**
- **CSS3**
- **Bootstrap 5** – UI styling and responsiveness

---

## 📦 Features

- 🔐 **User Authentication** (Register, Login, Logout)
- 🛍️ **Product Catalog** with images and descriptions
- 🛒 **Cart System** (session and user-based)
- ✍️ **User Reviews** (Add/Edit/Delete)
- 🧾 **Admin Product Initialization**
- 🧹 **Clear Cart Functionality**
- ✅ **Form Validation and Flash Messaging**

---

## 📂 Project Structure (Blueprint-Based)
## 🖥️ Pages and Functionalities

- `/` or `/Home`: Home page
- `/About`: About the store
- `/Shop`: Product listing with “Add to Cart” functionality
- `/Cart`: User cart summary and total price
- `/Reviews`: Authenticated user reviews
- `/register`: User registration
- `/login`: User login
- `/logout`: User logout
- `/clear_cart`: Clear current user's cart (POST)

## 📥 Installation Guide

### 1. Clone the Repository
git clone https://github.com/YoussefMohamed44/Supermarket

### 2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

## 📥 Dependencies (requirements.txt)
flask
flask-sqlalchemy
flask-wtf
flask-login
flask-bcrypt 
email_validator 

## 🚀 Live Deployment

Docker Hub Image: [youssefmohamed4/supermarket-app](https://hub.docker.com/r/youssefmohamed4/supermarket-app)  
To run with Docker:
```bash
docker pull youssefmohamed4/supermarket-app
docker run -p 5555:9999 youssefmohamed4/supermarket-app