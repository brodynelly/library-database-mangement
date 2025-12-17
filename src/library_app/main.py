from library_app.cli import (
    search_books_with_input,
    check_out_book_with_input,
    return_book_with_input,
)


def run():
    search_books_with_input()
    check_out_book_with_input()
    return_book_with_input()


if __name__ == "__main__":
    run()

    repeat = True
    while repeat:
        conApp = input("Would you like to leave the library? (y/n)")
        if conApp.lower() == "y":
            repeat = False
            break
        elif conApp.lower() == "n":
            run()
        else:
            print("Please enter y to leave, or n to stay. Please try again!")
