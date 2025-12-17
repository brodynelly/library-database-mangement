from .repository import (
    get_authors,
    get_available_books,
    get_patrons,
    get_borrowed_books,
    get_patrons_with_book,
    search_books_by_author,
    check_out_book_transaction,
    return_book_transaction,
)


def search_books_with_input():
    authors = get_authors()
    if authors:
        print("Select an author to search for books:")
        for author in authors:
            print(f"{author[0]}. {author[1]}")
        author_choice = input("Enter the number corresponding to the author: ")

        try:
            author_id = int(author_choice)
            if author_id not in [author[0] for author in authors]:
                print("Invalid author selection.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        books = search_books_by_author(author_id)
        if books:
            print("\nMatching Books:")
            print("(book_id, book_title, author_name, publish_year, times_checked_out)")
            for book in books:
                print(book)
        else:
            print("No books found for the selected author.")
    else:
        print("No authors found in the database.")


def check_out_book_with_input():
    available_books = get_available_books()
    if not available_books:
        print("No available books.")
        return

    print("\nPlease Select an Available Book to Check Out:")
    for book in available_books:
        print(f"{book[0]}. {book[1]}")

    book_choice = input("Enter the number corresponding to the book to check out: ")

    try:
        book_id = int(book_choice)
        if book_id not in [book[0] for book in available_books]:
            print("Invalid book selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    patrons = get_patrons()
    if not patrons:
        print("No patrons found.")
        return

    print("\n Which Patron are You?:")
    for patron in patrons:
        print(f"{patron[0]}. {patron[1]}")

    patron_choice = input(
        "Enter the number corresponding to the patron to check out the book: "
    )

    try:
        patron_id = int(patron_choice)
        if patron_id not in [patron[0] for patron in patrons]:
            print("Invalid patron selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    result = check_out_book_transaction(patron_id, book_id)
    print(result["message"])


def return_book_with_input():
    borrowed_books = get_borrowed_books()
    if not borrowed_books:
        print("No borrowed books.")
        return

    return_book_question = input("\nwould you like to return a book?(y/n): ")
    if return_book_question.lower() == "y":
        print("Continuing...")
    elif return_book_question.lower() == "n":
        print("Exiting...")
        return
    else:
        print("Invalid input. Please enter 'y' for Yes or 'n' for No.")
        return  # Added return to stop if invalid input

    print("\nPlease select which patron you are:")
    patrons = get_patrons()
    if not patrons:
        print("No patrons found.")
        return

    for patron in patrons:
        print(f"{patron[0]}. {patron[1]}")

    patron_choice = input("enter the number coorasponding to your name: ")

    print("\nList of Borrowed Books:")
    for book in borrowed_books:
        print(f"{book[0]}. {book[1]}")

    book_choice = input("Enter the number corresponding to the book to return: ")

    try:
        book_id = int(book_choice)
        if book_id not in [book[0] for book in borrowed_books]:
            print("Invalid book selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    patrons_with_book = get_patrons_with_book(book_id)
    if not patrons_with_book:
        print("\nNo patrons found who borrowed this book.")
        return

    try:
        patron_id = int(patron_choice)
        if patron_id not in [patron[0] for patron in patrons_with_book]:
            print("\nYou have not checked out the selected book!")
            print("You are currently only able to return books you have checked out :(")
            return
    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    result = return_book_transaction(patron_id, book_id)
    print(result["message"])
