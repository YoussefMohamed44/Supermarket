# End-to-End Tests with Selenium

This directory contains the End-to-End (E2E) test suite for the Supermarket application.

## Prerequisites

1.  **Google Chrome**: Ensure Google Chrome is installed on the machine.
2.  **Drivers**: The `webdriver-manager` package will automatically handle the ChromeDriver installation.

## Running the Tests

To run the entire E2E suite:

```bash
pytest tests/e2e -v
```

To run a specific test file:

```bash
pytest tests/e2e/test_auth.py -v
```

## Structure

*   **`conftest.py`**: Handles test configuration, including:
    *   Setting up the Flask application in a separate thread.
    *   Configuring the Selenium WebDriver (Chrome Headless).
    *   Managing a temporary `test_e2e_suite.db` database.
    *   Providing `driver` and `authorized_driver` fixtures.
*   **`test_auth.py`**: Authentication scenarios (Registration, Login, Invalid Login).
*   **`test_shop.py`**: Product browsing and visibility validation.
*   **`test_cart.py`**: Cart operations (Add, Increase Quantity, Clear Cart).
*   **`test_checkout.py`**: Checkout flow placeholders (Skipped pending feature implementation).

## Test Data

The `conftest.py` automatically seeds the test database with:
*   A user: `e2e@example.com` / `password123`
*   Sample products: "E2E Milk", "E2E Bread", "E2E Eggs"

## Troubleshooting

If tests fail with `WebDriverException`:
*   Check if Chrome is installed.
*   Check if `webdriver-manager` can access the internet to download the driver.
*   Ensure the `headless` mode is enabled if running on a server without a display.
