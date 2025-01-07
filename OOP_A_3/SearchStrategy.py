from FileManagement import FileManagement

class SearchStrategy:
    def search(self):
        pass

class SearchByTitle(SearchStrategy):
    def search(self):
        books = FileManagement.read_file("book.csv")
        for book in books:
            book[0]


class SearchByAuthor(SearchStrategy):
    def search(self):
        books = FileManagement.read_file("book.csv")
        for book in books:
            book[1]

class SearchByIsLoaned(SearchStrategy):
    def search(self):
        books = FileManagement.read_file("book.csv")
        for book in books:
            book[2]

class SearchByCopies(SearchStrategy):
    def search(self):
        books = FileManagement.read_file("book.csv")
        for book in books:
            book[3]

class SearchByGenre(SearchStrategy):
    def search(self):
        books = FileManagement.read_file("book.csv")
        for book in books:
            book[4]
        return books

class SearchByYear(SearchStrategy):
    def search(self):
        books = FileManagement.read_file("book.csv")
        for book in books:
            book[5]


if __name__ == '__main__':
    searcher = SearchByGenre()
    print(searcher.search())