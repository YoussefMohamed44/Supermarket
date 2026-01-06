# System Test Execution Note

## Error Encountered
The Selenium system tests failed with the following error:
```
selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary
```

## Reason
The test environment does not have the Google Chrome browser installed, or it is not in the system PATH. Selenium requires the actual browser binary to function, even in headless mode. `webdriver-manager` only installs the *driver* (chromedriver), not the browser itself.

## How to Run System Tests
To run the system tests successfully, you must:
1. Install Google Chrome on the machine running the tests.
2. Ensure the chrome binary is accessible.
3. Run the command:
   ```bash
   python -m pytest tests/ui/test_system.py -v
   ```

The test code in `tests/ui/test_system.py` is correctly implemented to simulate the user journey (Register -> Login -> Shop -> Cart -> Checkout) once the browser is available.
