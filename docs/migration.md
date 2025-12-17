# Migration Guide

This document details the changes made during the refactoring process to improve code quality, security, and maintainability.

## Summary of Changes

### Directory Structure

The project has been restructured to follow standard Python project conventions:

-   `Database/` -> `scripts/` (Database initialization scripts)
-   `LibraryApp/` -> `src/library_app/` (Application source code)
-   Added `tests/` directory for unit tests.

### Renaming

-   `database.py` -> `scripts/init_db.py`
-   `main.py` -> `src/library_app/main.py`
-   `library_app.py` -> `src/library_app/cli.py`
-   Merged `helpers.py` and `sql_queries.py` into `src/library_app/repository.py`.

### Code Refactoring

1.  **Dependency Injection & Configuration**:
    -   Removed hardcoded credentials.
    -   Introduced `src/library_app/config.py` to load credentials from `.env` file.

2.  **Security**:
    -   Replaced f-string SQL queries with parameterized queries (`%s`) to prevent SQL injection vulnerabilities.

3.  **Database Management**:
    -   Implemented `get_connection()` function with error handling.
    -   Used `try...finally` blocks to ensure database connections are closed properly.
    -   Refactored `repository.py` to separate data access logic from UI logic.

4.  **User Interface**:
    -   `cli.py` now handles all user interaction (print/input).
    -   `repository.py` returns data structures (lists/dicts) instead of printing directly to stdout.

### Testing

-   Added unit tests using `pytest` and `unittest.mock`.
-   Tests mock the database connection, allowing testing without a running MySQL instance.

### Quality Assurance

-   Added `.editorconfig` for consistent editor settings.
-   Added `.flake8` configuration.
-   Added GitHub Actions workflow (`.github/workflows/ci.yml`) for automated testing and linting.
-   Formatted code with `black`.

## Usage Changes

-   **Initialization**: Run `python scripts/init_db.py` instead of running `database.py`.
-   **Execution**: Run `python src/library_app/main.py` to start the application.
