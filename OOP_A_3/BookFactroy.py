from Book import Book
from FileManagement import FileManagement


class BookFactory:
    books_list = FileManagement.read_file2("Files/books.csv")

    def create_book(self, title, author, genre, year):
        new_fields = [title, author, genre, year]
        for book in BookFactory.books_list:
            for field in book.get_fields():
                if field in new_fields:
                    book.copies = int(book.copies) + 1
                    return book

        return Book(title, author, genre, year)

    def get_books_list(self):
        return self.books_list

    def get_book_count(self, book):

        if not isinstance(book, Book):
            return "Error: This is not a valid Book object."

            # 2) Now safely try to get the count from the dictionary
        try:
            return f"Copies of {book.title} by {book.author}: {self.books_list[book]}"
        except KeyError:
            return "Error: This book doesn't exist in the table!"

    def remove_book(self, book):
        if book in self.books_list:
            del self.books_list[book]

    def search_book(self, book):
        if book in self.books_list:
            return self.books_list[book]
        else:
            return "Error: This book doesn't exist in the table"


if __name__ == "__main__":
    print(FileManagement.read_file("Files/books.csv"))
    factory = BookFactory()
    book2 = factory.create_book("mkalsdnfkj", "askjdfn", "akfna", 2012)
    FileManagement.add_book(book2, "Files/books.csv")