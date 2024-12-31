
class Book:

    def __init__(self, title, author,year,copies = None):
        self.title = title
        self.author = author
        self.copies = copies
        self.year = year


    def __str__(self):
        if self.copies is None:
         return f"{self.title} by {self.author}.\n year:{self.year}.\n"

        else:
            return f"{self.title} by {self.author} {self.year}"

    def __repr__(self):
        return f"Book({self.title!r}, {self.author!r}, {self.year!r})"

    def __eq__(self, other):
        return (isinstance(other, Book) and
        self.title == other.title and
        self.author == other.author and
        self.year == other.year)

    def __hash__(self):
        return hash((self.title, self.author, self.year))





