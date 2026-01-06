# System & UI Tests (Page Object Model)

## Overview
These tests use **Selenium WebDriver** and the **Page Object Model (POM)** design pattern to verify critical system flows from the user's perspective.

## Directory Structure
- `pages/`: Contains Page Objects (`login_page.py`, `shop_page.py`, etc.) representing screens.
- `base_page.py`: Common wrapper for Selenium actions with **Explicit Waits**.
- `test_pom_system.py`: The actual test script utilizing page objects.
- `conftest.py`: Configuration for Chrome Driver, Live Server, and **Screenshot on Failure**.

## Why UI Tests are Fewer but Critical
1.  **High Maintenance & Slower**: UI tests are slower to run and more brittle (sensitive to UI changes) than unit tests, so we write fewer of them.
2.  **Integration Validator**: They are the **only** tests that verify the entire stack (Database -> Backend -> Frontend -> Browser) works together.
3.  **User Confidence**: They simulate actual user behavior (clicking, typing), providing the highest confidence that the "Happy Path" works for customers.
4.  **Catch "Glue" Bugs**: They catch issues that Unit/Integration tests miss, like broken JavaScript, CSS issues blocking clicks, or missing template assets.

## Running Tests
Ensure Google Chrome is installed, then run:
```bash
python -m pytest tests/ui/test_pom_system.py -v
```
If a test fails, a screenshot will be saved in the `tests/ui/` directory.
