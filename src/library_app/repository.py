import mysql.connector
from .config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    """Establishes and returns a database connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME,
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def get_authors():
    """Returns a list of all authors."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT author_id, author_name FROM Author")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return []
    finally:
        conn.close()


def get_available_books():
    """Returns a list of books that are available (not checked out)."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT book_id, book_title FROM Book WHERE is_checked < 1")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return []
    finally:
        conn.close()


def get_patrons_with_book(book_id):
    """Returns a list of patrons who have borrowed a specific book."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = """
            SELECT Patron.patron_id, patron_name
            FROM Patron
            JOIN Transaction ON Patron.patron_id = Transaction.patron_id
            WHERE Transaction.book_id = %s
        """
        cursor.execute(query, (book_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return []
    finally:
        conn.close()


def get_patrons():
    """Returns a list of all patrons."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT patron_id, patron_name FROM Patron")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return []
    finally:
        conn.close()


def get_borrowed_books():
    """Returns a list of borrowed books."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = """
            SELECT Book.book_id, book_title, author_name
            FROM Book
            JOIN Author ON Book.author_id = Author.author_id
            WHERE is_checked > 0
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return []
    finally:
        conn.close()


def search_books_by_author(author_id):
    """Searches for books by a specific author."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = """
            SELECT Book.book_id, book_title, author_name, publish_year, times_checked_out
            FROM Book
            JOIN Author ON Book.author_id = Author.author_id
            WHERE Book.author_id = %s
        """
        cursor.execute(query, (author_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        return []
    finally:
        conn.close()


def check_out_book_transaction(patron_id, book_id):
    """
    Checks out a book for a patron.
    Returns a dictionary with status ('success' or 'error') and message.
    """
    conn = get_connection()
    if not conn:
        return {"status": "error", "message": "Database connection failed"}

    try:
        cursor = conn.cursor()
        # Check if the book is available
        cursor.execute(
            "SELECT book_title, is_checked FROM Book WHERE book_id = %s", (book_id,)
        )
        book_data = cursor.fetchone()

        if not book_data:
            return {"status": "error", "message": "Book not found."}

        book_title, is_checked = book_data

        if is_checked != 0:
            return {
                "status": "error",
                "message": f"{book_title} is not available for checkout.",
            }

        # Reserve the book
        cursor.execute(
            "UPDATE Book SET times_checked_out = times_checked_out + 1, is_checked = 1 WHERE book_id = %s",  # noqa: E501
            (book_id,),
        )

        # Create a transaction record (assuming librarian_id 1 for now)
        cursor.execute(
            "INSERT INTO Transaction (librarian_id, book_id, patron_id) VALUES (1, %s, %s)",  # noqa: E501
            (book_id, patron_id),
        )

        conn.commit()
        return {"status": "success", "message": "Book checked out successfully."}

    except mysql.connector.Error as err:
        return {"status": "error", "message": f"Error executing SQL query: {err}"}
    finally:
        conn.close()


def return_book_transaction(patron_id, book_id):
    """
    Returns a book from a patron.
    Returns a dictionary with status ('success' or 'error') and message.
    """
    conn = get_connection()
    if not conn:
        return {"status": "error", "message": "Database connection failed"}

    try:
        cursor = conn.cursor()
        # Check if the book is borrowed by the specified patron
        query = """
            SELECT Book.book_title, Transaction.patron_id, Book.is_checked
            FROM Transaction
            JOIN Book ON Transaction.book_id = Book.book_id
            WHERE Transaction.book_id = %s AND Transaction.patron_id = %s
        """
        cursor.execute(query, (book_id, patron_id))
        transaction_data = cursor.fetchone()

        if not transaction_data:
            return {
                "status": "error",
                "message": "Book is not borrowed by the specified patron or transaction record not found.",  # noqa: E501
            }

        book_title, retrieved_patron_id, is_checked = transaction_data

        if is_checked <= 0:
            return {"status": "error", "message": "Book is already available."}

        # Update book status to "available"
        cursor.execute("UPDATE Book SET is_checked = 0 WHERE book_id = %s", (book_id,))
        conn.commit()

        return {
            "status": "success",
            "message": f"{book_title} has been successfully returned.",
        }

    except mysql.connector.Error as err:
        return {"status": "error", "message": f"Error executing SQL query: {err}"}
    finally:
        conn.close()
