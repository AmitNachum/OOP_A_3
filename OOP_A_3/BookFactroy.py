from Book import Book
from FileManagement import FileManagement


class BookFactory:
    books_list = FileManagement.read_file_to_books("Files/books.csv")

    @staticmethod
    def create_book(title, author, genre, year, copies: int = 1, is_loaned = "No"):
        for book in BookFactory.books_list:
            # Compare books without the `copies` field
            if [book.title, book.author, book.genre, book.year] == [title, author, genre, year]:
                book.copies += copies  # Increment `copies` by the new value
                return book

            # If no match is found, create a new book
        new_book = Book(title, author, genre, year, copies, is_loaned)
        BookFactory.books_list.append(new_book)
        return new_book


if __name__ == "__main__":
    print(FileManagement.read_file("Files/books.csv"))
    factory = BookFactory()
    book2 = factory.create_book("mkalsdnfk", "askjdfn", "akfna", 2013)
    #FileManagement.add_book(book2, "Files/books.csv")
    print(FileManagement.read_file("Files/books.csv"))
    FileManagement.remove_book(book2, "Files/books.csv")
