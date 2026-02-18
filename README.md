# Library Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![CI](https://github.com/brodynelly/library-database-mangement/actions/workflows/ci.yml/badge.svg)](https://github.com/brodynelly/library-database-mangement/actions/workflows/ci.yml) ![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python)

A secure Library Management System built with Python and MySQL. This application allows librarians and patrons to manage books, authors, and transactions effectively.

## Features

-   **Book Management**: Search books by author, view available books.
-   **Transaction Management**: Check out and return books.
-   **Patron Management**: Track patron activity.
-   **Secure Database Interactions**: Uses parameterized queries to prevent SQL injection.
-   **Configuration**: Environment-based configuration for database credentials.

## Stack

-   **Language**: Python 3.12+
-   **Database**: MySQL
-   **Libraries**: `mysql-connector-python`, `python-dotenv`
-   **Testing**: `pytest`
-   **Linting**: `flake8`, `black`

## Setup

### Prerequisites

-   Python 3.12 or higher
-   MySQL Server installed and running

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure environment variables:
    Create a `.env` file in the root directory with the following content:
    ```env
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=library_db
    ```

4.  Initialize the database:
    ```bash
    python scripts/init_db.py
    ```

### Running the Application

To run the interactive command-line interface:

```bash
python src/library_app/main.py
```

## Architecture

The project follows a modular structure:

-   `src/library_app/`: Contains the application source code.
    -   `cli.py`: Handles user input and output.
    -   `repository.py`: Manages database interactions (Data Access Object pattern).
    -   `config.py`: Manages configuration settings.
    -   `main.py`: Entry point of the application.
-   `scripts/`: Contains utility scripts (e.g., database initialization).
-   `tests/`: Contains unit tests.

## Development

### Running Tests

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest
```

### Linting and Formatting

```bash
flake8 .
black .
```
