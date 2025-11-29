import unittest
from unittest.mock import MagicMock, patch
from library_app import repository


class TestRepository(unittest.TestCase):
    @patch("library_app.repository.mysql.connector.connect")
    def test_get_authors(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, "Jane Austen")]

        authors = repository.get_authors()

        self.assertEqual(authors, [(1, "Jane Austen")])
        mock_cursor.execute.assert_called_with(
            "SELECT author_id, author_name FROM Author"
        )

    @patch("library_app.repository.mysql.connector.connect")
    def test_get_available_books(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, "Pride and Prejudice")]

        books = repository.get_available_books()

        self.assertEqual(books, [(1, "Pride and Prejudice")])
        mock_cursor.execute.assert_called_with(
            "SELECT book_id, book_title FROM Book WHERE is_checked < 1"
        )

    @patch("library_app.repository.mysql.connector.connect")
    def test_search_books_by_author(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Pride and Prejudice", "Jane Austen", 1813, 10)
        ]

        books = repository.search_books_by_author(1)

        self.assertEqual(books, [(1, "Pride and Prejudice", "Jane Austen", 1813, 10)])
        # Check parameterized query usage
        self.assertTrue(mock_cursor.execute.called)
        args, _ = mock_cursor.execute.call_args
        self.assertIn("WHERE Book.author_id = %s", args[0])
        self.assertEqual(args[1], (1,))

    @patch("library_app.repository.mysql.connector.connect")
    def test_check_out_book_transaction_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock finding the book, available (is_checked=0)
        mock_cursor.fetchone.return_value = ("Book Title", 0)

        result = repository.check_out_book_transaction(1, 1)

        self.assertEqual(result["status"], "success")
        self.assertTrue(mock_conn.commit.called)

    @patch("library_app.repository.mysql.connector.connect")
    def test_check_out_book_transaction_fail_checked_out(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock finding the book, already checked out (is_checked=1)
        mock_cursor.fetchone.return_value = ("Book Title", 1)

        result = repository.check_out_book_transaction(1, 1)

        self.assertEqual(result["status"], "error")
        self.assertFalse(mock_conn.commit.called)

    @patch("library_app.repository.mysql.connector.connect")
    def test_return_book_transaction_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock finding the transaction (Book Title, patron_id, is_checked)
        mock_cursor.fetchone.return_value = ("Book Title", 1, 1)

        result = repository.return_book_transaction(1, 1)

        self.assertEqual(result["status"], "success")
        self.assertTrue(mock_conn.commit.called)
