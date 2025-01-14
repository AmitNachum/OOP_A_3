class Book:

    def __init__(self, title, author, genre, year : int, copies: int = 1, is_loaned = "No"):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.copies = copies
        self.available_copies = self.copies if is_loaned.lower() == "no" else 0
        self.loaned_copies = self.copies if is_loaned.lower() == "yes" else 0
        self.is_loaned = is_loaned

    def get_title(self):
        return self.title

    def get_year(self):
        return self.year

    def get_author(self):
        return self.author

    def get_genre(self):
        return self.genre

    def get_copies(self):
        return self.copies

    def get_is_loaned(self):
        return self.is_loaned

    def get_fields(self):
        return [self.title, self.author, self.is_loaned, self.copies, self.genre, self.year]

    def get_available_fields(self):
        return [self.title, self.author, self.is_loaned, self.available_copies, self.genre, self.year]

    def get_loaned_fields(self):
        return [self.title, self.author, self.is_loaned, self.loaned_copies, self.genre, self.year]

    def __str__(self):
        if self.copies == 0:
            return f"{self.title} by {self.author}, published at:{self.year}.\n"

        else:
            return f"{self.title} by {self.author}, published at:{self.year}. has {self.copies} copies\n"

    def __repr__(self):
        return f"Book({self.title!r}, {self.author!r},{self.genre!r},{self.year!r})"

    def __eq__(self, other):
        return (isinstance(other, Book) and
        self.title.lower() == other.title.lower() and
        self.author.lower() == other.author.lower() and
        self.genre.lower() == other.genre.lower() and
        self.year == other.year and
        self.is_loaned.lower() == other.is_loaned.lower())

    def __hash__(self):
        return hash((self.title, self.author, self.year))





