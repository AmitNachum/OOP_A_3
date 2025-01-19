class TitleIterator:
    def __init__(self, data):
        self.data = [book for book, _ in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index].title
            self.index += 1
            return result
        else:
            raise StopIteration

class AuthorIterator:
    def __init__(self, data):
        self.data = [book for book, _ in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index].author
            self.index += 1
            return result
        else:
            raise StopIteration

class IsLoanedIterator:
    def __init__(self, data):
        self.data = [book for book, _ in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index].is_loaned
            self.index += 1
            return result
        else:
            raise StopIteration

class CopiesIterator:
    def __init__(self, data):
        self.data = [book for book, _ in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index].copies
            self.index += 1
            return result
        else:
            raise StopIteration

class GenreIterator:
    def __init__(self, data):
        self.data = [book for book, _ in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index].genre
            self.index += 1
            return result
        else:
            raise StopIteration

class YearIterator:
    def __init__(self, data):
        self.data = [book for book, _ in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index].year
            self.index += 1
            return result
        else:
            raise StopIteration

class AvailableCopiesIterator:
    def __init__(self, data):
        self.data = [additional_data for _, additional_data in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            # Access the "available_copies" field in each additional_data dictionary
            result = self.data[self.index]["available_copies"]
            self.index += 1
            return result
        else:
            raise StopIteration

class LoanedCopiesIterator:
    def __init__(self, data):
        self.data = [additional_data for _, additional_data in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            # Access the "loaned_copies" field in each additional_data dictionary
            result = self.data[self.index]["loaned_copies"]
            self.index += 1
            return result
        else:
            raise StopIteration

class LendCountIterator:
    def __init__(self, data):
        self.data = [additional_data for _, additional_data in data]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            # Access the "lend_count" field in each additional_data dictionary
            result = self.data[self.index]["lend_count"]
            self.index += 1
            return result
        else:
            raise StopIteration