class Book:
    """
       Represents a book in the library system.

       Attributes:
           title (str): The title of the book.
           author (str): The author of the book.
           genre (str): The genre of the book.
           year (int): The publication year of the book.
           copies (int): The number of copies available. Default is 1.
           is_loaned (str): Indicates whether the book is loaned. Default is 'No'.
       """
    def __init__(self, title, author, genre, year : int, copies: int = 1, is_loaned = "No"):
        """Initializes a new Book object with the given attributes."""
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.copies = copies
        self.is_loaned = is_loaned


    def get_fields(self):
        """Returns a list of the book's main attributes."""
        return [self.title,
        self.author,
        self.is_loaned,
        self.copies,
        self.genre,
        self.year,
        ]

    def __str__(self):
        """Returns a user-friendly string representation of the book."""
        if self.copies == 0:
            return f"{self.title} by {self.author}, published at:{self.year}"

        else:
            return f"{self.title} by {self.author}, published at:{self.year}. has {self.copies} copies"

    def __repr__(self):
        """Returns a string representation for debugging."""
        return f"Book({self.title!r}, {self.author!r},{self.genre!r},{self.year!r})"

    def __eq__(self, other):
        """Checks equality based on title, author, genre, year, and loan status."""

        return (isinstance(other, Book) and
        self.title.lower() == other.title.lower() and
        self.author.lower() == other.author.lower() and
        self.genre.lower() == other.genre.lower() and
        self.year == other.year and
        self.is_loaned.lower() == other.is_loaned.lower())

    def __hash__(self):
        """Returns a hash based on title, author, and year."""

        return hash((self.title, self.author, self.year))