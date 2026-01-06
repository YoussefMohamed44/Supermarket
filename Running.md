###Running the Project
flask run

###Running the Dashboard
python test_dashboard/app.py

###Testing Whole Project
pytest tests/

###Testing a folder
pytest tests/e2e/
pytest tests/unit/
pytest tests/integration/
pytest tests/ui/

###Testing Single Function
pytest tests/unit/test_services.py::TestServiceLayer::test_user_authentication_logic