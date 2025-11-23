# Estrato E2E Tests

Automated End-to-End testing suite for the Estrato application using Selenium WebDriver.

## Tech Stack

* **Language:** Python 3.12
* **Library:** Selenium
* **Driver Manager:** Webdriver Manager
* **Pattern:** Action-based / Scripted Flow

## Configuration

1.  Clone the repository.
2.  Ensure **Google Chrome** is installed on your machine.
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  (Optional) Verify `src/config.py` to ensure `BASE_URL` points to your target environment (e.g., `http://localhost:3000` for local testing).

## Running the Tests

To execute the full test suite (Register -> Login -> Flows -> Delete Account):

```bash
python main.py
```

- The script will launch a Chrome window and perform the test actions automatically.
- **Requirement:** Ensure the Frontend and Backend services are running before starting the tests.

## Structure
- `main.py:` Entry point that orchestrates the entire test flow.
- `data/roteiro.json:` Contains test data (mock users, note content, etc.).
- `src/actions/:` Modules containing specific interactions for each feature (Dashboard, Notes, Profile, etc.).