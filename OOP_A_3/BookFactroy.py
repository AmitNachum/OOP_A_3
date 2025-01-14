from Book import Book
from FileManagement import FileManagement


class BookFactory:

    @staticmethod
    def create_book(title, author, genre, year, copies: int = 1, is_loaned = "No"):
        new_book = Book(title, author, genre, year, copies, is_loaned)
        return new_book