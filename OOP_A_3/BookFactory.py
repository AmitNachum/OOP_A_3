from Book import Book


class BookFactory:
    """
      A factory class to create Book objects.
      """
    @staticmethod
    def create_book(title, author, genre, year, copies: int = 1, is_loaned = "No"):
        """
       Creates and returns a new Book object.

       Args:
           title (str): Title of the book.
           author (str): Author of the book.
           genre (str): Genre of the book.
           year (int): Publication year of the book.
           copies (int): Number of copies. Default is 1.
           is_loaned (str): Loan status. Default is 'No'.

       Returns:
           Book: A new Book object.
       """
        new_book = Book(title, author, genre, year, copies, is_loaned= is_loaned)
        return new_book