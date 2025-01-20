from Book import Book


class BookFactory:

    @staticmethod
    def create_book(title, author, genre, year, copies: int = 1, is_loaned = "No"):
        new_book = Book(title, author, genre, year, copies, is_loaned= is_loaned)
        return new_book