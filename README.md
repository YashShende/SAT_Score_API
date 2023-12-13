
# SAT Score API

This repository contains a simple Flask API for managing SAT scores.

## Files

- **appLocalDB.py**: Flask application using a local SQLite database.
- **appSQL.py**: Flask application using SQLAlchemy for database management.
- **requirements.txt**: File containing the Python dependencies for the project.
- **sat_results.db**: SQLite database file storing SAT results data.
- **scores.json**: JSON file containing a backup of SAT results data.
- **start_api_server.bat**: Batch file to start the Flask API server.
- **test_app.py**: Unit tests for the Flask API.
- **thunder-collection SAT Score API Test Collection**: A Thunder collection file for testing API endpoints.
- **unit test runner.bat**: Batch file to run unit tests.

## How to Run

1. Install Python (if not already installed).

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the API:
    - For `appSQL.py`:
        ```bash
        python appSQL.py
        ```
    - Alternatively, you can use `start_api_server.bat` for convenience.

4. Access the API at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Unit Tests

Run the unit tests using the provided `unit test runner.bat`:

```bash
unit_test_runner.bat
