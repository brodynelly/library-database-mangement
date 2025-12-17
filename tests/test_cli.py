import unittest
from unittest.mock import patch
from library_app import cli


class TestCLI(unittest.TestCase):
    @patch("library_app.cli.get_authors")
    @patch("library_app.cli.search_books_by_author")
    @patch("builtins.input", side_effect=["1"])
    @patch("builtins.print")
    def test_search_books_with_input(
        self, mock_print, mock_input, mock_search, mock_get_authors
    ):
        mock_get_authors.return_value = [(1, "Jane Austen")]
        mock_search.return_value = [
            (1, "Pride and Prejudice", "Jane Austen", 1813, 10)
        ]

        cli.search_books_with_input()

        mock_get_authors.assert_called_once()
        mock_search.assert_called_with(1)
        # Verify output contains book info
        # This is a bit fragile as it checks print calls
        self.assertTrue(
            any("Pride and Prejudice" in str(call) for call in mock_print.call_args_list)
        )

    @patch("library_app.cli.get_available_books")
    @patch("library_app.cli.get_patrons")
    @patch("library_app.cli.check_out_book_transaction")
    @patch("builtins.input", side_effect=["1", "1"])  # Select book 1, patron 1
    @patch("builtins.print")
    def test_check_out_book_with_input(
        self,
        mock_print,
        mock_input,
        mock_checkout,
        mock_get_patrons,
        mock_get_books,
    ):
        mock_get_books.return_value = [(1, "Book 1")]
        mock_get_patrons.return_value = [(1, "Patron 1")]
        mock_checkout.return_value = {"status": "success", "message": "Success"}

        cli.check_out_book_with_input()

        mock_checkout.assert_called_with(1, 1)

    @patch("library_app.cli.get_borrowed_books")
    @patch("library_app.cli.get_patrons")
    @patch("library_app.cli.get_patrons_with_book")
    @patch("library_app.cli.return_book_transaction")
    @patch(
        "builtins.input", side_effect=["y", "1", "1"]
    )  # Yes return, select patron 1, book 1
    @patch("builtins.print")
    def test_return_book_with_input(
        self,
        mock_print,
        mock_input,
        mock_return,
        mock_get_patrons_book,
        mock_get_patrons,
        mock_get_borrowed,
    ):
        mock_get_borrowed.return_value = [(1, "Book 1")]
        mock_get_patrons.return_value = [(1, "Patron 1")]
        mock_get_patrons_book.return_value = [(1, "Patron 1")]
        mock_return.return_value = {"status": "success", "message": "Success"}

        cli.return_book_with_input()

        mock_return.assert_called_with(1, 1)
