# 📦 Supermarket – Full Stack Flask Web App

A fully functional, blueprint‑based **Flask e‑commerce web application** that simulates an online supermarket store. Users can browse products, register/login, add reviews, and manage a shopping cart. Styled with **Bootstrap 5**, it includes authentication, session/cart persistence, and basic admin functionalities.

---

## 🚀 Table of Contents

1. 🔹 [Features](#-features)  
2. 🧱 [Tech Stack](#-tech-stack)  
3. 🗂️ [Project Structure](#️-project-structure)  
4. 🛠️ [Installation](#️-installation)  
5. 📦 [Running Locally](#-running-locally)  
6. 🧪 [Testing](#-testing)  
7. 🐳 [Docker Deployment](#-docker‑deployment)  
8. 🤝 [Contributing](#-contributing)  
9. 📄 [License](#-license)

---

## ⭐ Features

✔️ User authentication (register/login/logout)  
✔ Product catalog with images & descriptions  
✔ Cart system (session‑based & persistent)  
✔ User reviews (add/edit/delete)  
✔ Admin product initialization  
✔ Flash messaging and form validation  
✔ Responsive frontend with Bootstrap

---

## 🧱 Tech Stack

**Backend:**  
- Python 3  
- Flask – lightweight web framework  
- Flask‑WTF – secure forms + CSRF  
- Flask‑Login – user session management  
- Flask‑SQLAlchemy – ORM for DB  
- Flask‑Bcrypt – password hashing

**Frontend:**  
- HTML5, CSS3  
- Bootstrap 5

**Dev / Testing:**  
- pytest – test framework  
- pytest‑cov (optional) – coverage reporting

---

## 📁 Project Structure

```
Supermarket/
├─ Super_Market/         # main application package
├─ instance/             # config & local DB storage
├─ tests/                # unit & functional tests
├─ test_dashboard/       # dashboard tests/UI tests
├─ .coverage             # coverage results
├─ Dockerfile
├─ README.md
├─ Running.md
├─ requirements.txt
├─ pytest.ini            # pytest config file
└─ …
```

---

## 🛠️ Installation

### 1) Clone the repository

```bash
git clone https://github.com/YoussefMohamed44/Supermarket.git
cd Supermarket
```

### 2) Create & activate a virtual environment

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Locally

Start the development server:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

or (Windows PowerShell):

```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
```

Now open your browser at:  
👉 `http://127.0.0.1:5000`

---

## 🧪 Testing

This project includes automated tests (unit/functional) using **pytest**.

### 🧾 Available Tests

- `tests/` – core app tests
- `test_dashboard/` – UI/dashboard tests  

### 📌 Running Tests

To run all tests:

```bash
pytest
```

To run tests with a coverage report:

```bash
pytest --cov=Super_Market
```

✅ **Notes for tests**
- Ensure your virtual environment is active.
- The `pytest.ini` file configures defaults for your test runs.

---

## 🐳 Docker Deployment

You can build and run your app in Docker:

```bash
docker build -t supermarket-app .
docker run -p 5000:5000 supermarket-app
```

Or pull the prebuilt image:

```bash
docker pull youssefmohamed4/supermarket-app
docker run -p 5555:9999 youssefmohamed4/supermarket-app
```

---

## 🤝 Contributing

Thank you for considering contributing!  
To contribute:

1. ⭐ Star the repo  
2. 🐣 Fork it  
3. 📦 Create a feature branch  
4. 🧪 Add tests for new features  
5. 🔀 Open a pull request
