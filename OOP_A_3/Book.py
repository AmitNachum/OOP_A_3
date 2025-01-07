class Book:

    def __init__(self, title, author, genre, year, copies = 0, is_loaned = False):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.copies = copies
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

    def __str__(self):
        if self.copies == 0:
            return f"{self.title} by {self.author}, published at:{self.year}.\n"

        else:
            return f"{self.title} by {self.author}, published at:{self.year}. has {self.copies} copies\n"

    def __repr__(self):
        return f"Book({self.title!r}, {self.author!r},{self.genre!r},{self.year!r})"

    def __eq__(self, other):
        return (isinstance(other, Book) and
        self.title == other.title and
        self.author == other.author and
        self.year == other.year)

    def __hash__(self):
        return hash((self.title, self.author, self.year))





