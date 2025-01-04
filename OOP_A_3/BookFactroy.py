from Book import Book
class BookFactory:

    def __init__(self):
        self.book_table = {}

    def create_book(self,title,author,year):

        key = Book(title,author,year)
        current_count = self.book_table.get(key , 0) + 1
        self.book_table[key] = current_count
        return key



    def get_table(self):
        return self.book_table


    def get_book_count(self,book):

        if not isinstance(book, Book):
            return "Error: This is not a valid Book object."

            # 2) Now safely try to get the count from the dictionary
        try:
            return f"Copies of {book.title} by {book.author}: {self.book_table[book]}"
        except KeyError:
            return "Error: This book doesn't exist in the table!"

    def remove_book(self,book):
        if book in self.book_table:
            del self.book_table[book]

    def search_book(self,book):
        if book in self.book_table:
            return self.book_table[book]
        else:
            return "Error: This book doesn't exist in the table"


if __name__ == "__main__":
    factory = BookFactory()
    book1 = factory.create_book("The Great Gatsby", "F. Scott Fitzgerald" ,1990)
    book2 = factory.create_book("The Great Gatsby", "F. Scott Fitzgerald",1990)
    book3 = factory.create_book("The Big Whale" ,"Sir Alexander" , 1980)

    print(book1)
    print("\n")

    print(book3)


    print(factory.get_table())
    print("\n")