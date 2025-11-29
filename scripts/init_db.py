import mysql.connector
import os
import sys

# Add src to path so we can import config
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
# E402 module level import not at top of file - ignoring because of sys.path hack
from library_app.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME  # noqa: E402


def init_db():
    print(f"Connecting to MySQL at {DB_HOST} as {DB_USER}...")
    # Connect without database first to create it
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return

    mycursor = db.cursor()

    print(f"Creating database {DB_NAME} if not exists...")
    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    db.close()

    # Reconnect with database
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME,
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME}: {err}")
        return

    mycursor = db.cursor()

    print("Creating tables...")
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Author (
        author_id int PRIMARY KEY AUTO_INCREMENT,
        author_name VARCHAR(50) NOT NULL)
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Book (
            book_id INT PRIMARY KEY AUTO_INCREMENT,
            book_title VARCHAR(50) NOT NULL,
            publish_year INT NOT NULL,
            times_checked_out INT NOT NULL,
            is_checked INT NOT NULL,
            author_id INT,
            FOREIGN KEY (author_id) REFERENCES Author(author_id)
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Librarian (
            librarian_id INT PRIMARY KEY AUTO_INCREMENT,
            librarian_name VARCHAR(50) NOT NULL,
            book_id INT,
            FOREIGN KEY (book_id) REFERENCES Book(book_id)
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Vendor (
            vendor_name VARCHAR(50) NOT NULL,
            book_id INT,
            FOREIGN KEY (book_id) REFERENCES Book(book_id)
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Patron (
            patron_id INT PRIMARY KEY AUTO_INCREMENT,
            patron_name VARCHAR(50) NOT NULL
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS PatronAddress (
            patron_address_id INT PRIMARY KEY AUTO_INCREMENT,
            patron_id INT,
            street VARCHAR(50) NOT NULL,
            city VARCHAR(50) NOT NULL,
            state VARCHAR(50) NOT NULL,
            FOREIGN KEY (patron_id) REFERENCES Patron(patron_id)
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Transaction (
            transaction_id INT PRIMARY KEY AUTO_INCREMENT,
            librarian_id INT,
            book_id INT,
            patron_id INT,
            FOREIGN KEY (librarian_id) REFERENCES Librarian(librarian_id),
            FOREIGN KEY (book_id) REFERENCES Book(book_id),
            FOREIGN KEY (patron_id) REFERENCES Patron(patron_id)
        )
    """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS TransactionRecord (
            record_id INT PRIMARY KEY AUTO_INCREMENT,
            date_issue DATETIME,
            date_return DATETIME,
            transaction_id INT,
            FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id)
        )
    """)
    db.commit()

    print("Checking if data needs to be populated...")
    # Check if Author table is empty
    mycursor.execute("SELECT COUNT(*) FROM Author")
    if mycursor.fetchone()[0] == 0:
        print("Populating Author table...")
        author_data = [
            ("Jane Austen",),
            ("Charles Dickens",),
            ("J.K. Rowling",),
            ("Mark Twain",),
            ("William Shakespeare",),
        ]
        mycursor.executemany(
            "INSERT INTO Author (author_name) VALUES (%s)", author_data
        )
        db.commit()

    # Check if Book table is empty
    mycursor.execute("SELECT COUNT(*) FROM Book")
    if mycursor.fetchone()[0] == 0:
        print("Populating Book table...")
        book_data = [
            ("Pride and Prejudice", 1813, 10, 0, 1),
            ("Great Expectations", 1861, 8, 0, 2),
            ("Harry Potter and the Philosopher's Stone", 1997, 15, 0, 3),
            ("The Adventures of Tom Sawyer", 1876, 5, 0, 4),
            ("Romeo and Juliet", 1597, 12, 0, 5),
        ]
        mycursor.executemany(
            "INSERT INTO Book (book_title, publish_year, times_checked_out, is_checked, author_id) VALUES (%s, %s, %s, %s, %s)",  # noqa: E501
            book_data,
        )
        db.commit()

    # Check if Librarian table is empty
    mycursor.execute("SELECT COUNT(*) FROM Librarian")
    if mycursor.fetchone()[0] == 0:
        print("Populating Librarian table...")
        librarian_data = [("John Smith", 1), ("Emma Johnson", 2), ("Michael Williams", 3)]
        mycursor.executemany(
            "INSERT INTO Librarian (librarian_name, book_id) VALUES (%s, %s)",
            librarian_data,
        )
        db.commit()

    # Check if Vendor table is empty
    mycursor.execute("SELECT COUNT(*) FROM Vendor")
    if mycursor.fetchone()[0] == 0:
        print("Populating Vendor table...")
        vendor_data = [("Book Supplier A", 2), ("Book Supplier B", 4), ("Book Supplier C", 5)]
        mycursor.executemany(
            "INSERT INTO Vendor (vendor_name, book_id) VALUES (%s, %s)",
            vendor_data,
        )
        db.commit()

    # Check if Patron table is empty
    mycursor.execute("SELECT COUNT(*) FROM Patron")
    if mycursor.fetchone()[0] == 0:
        print("Populating Patron table...")
        patron_data = [
            ("Alice Smith",),
            ("Bob Johnson",),
            ("Charlie Williams",),
        ]
        mycursor.executemany(
            "INSERT INTO Patron (patron_name) VALUES (%s)", patron_data
        )
        db.commit()

    # Check if PatronAddress table is empty
    mycursor.execute("SELECT COUNT(*) FROM PatronAddress")
    if mycursor.fetchone()[0] == 0:
        print("Populating PatronAddress table...")
        patron_address_data = [
            (1, "123 Main St", "Cityville", "State A"),
            (2, "456 Elm St", "Townsville", "State B"),
            (3, "789 Oak St", "Villagetown", "State C"),
        ]
        mycursor.executemany(
            "INSERT INTO PatronAddress (patron_id, street, city, state) VALUES (%s, %s, %s, %s)",  # noqa: E501
            patron_address_data,
        )
        db.commit()

    print("Database initialization complete.")
    db.close()


if __name__ == "__main__":
    init_db()
