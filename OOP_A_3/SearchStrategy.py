from abc import ABC, abstractmethod
from Iterators import *

class SearchStrategy(ABC):
    @abstractmethod
    def search(self,data, search_val):
        pass

class SearchByTitle(SearchStrategy):
    def search(self, data, search_val: str):
        return [b for t, b in zip(TitleIterator(data), data) if t.lower() == search_val.lower()]

class SearchByAuthor(SearchStrategy):
    def search(self, data, search_val: str):
        return [b for a, b in zip(AuthorIterator(data), data) if a.lower() == search_val.lower()]

class SearchByIsLoaned(SearchStrategy):
    def search(self, data, search_val: str):
        return [b for il, b in zip(IsLoanedIterator(data), data) if il.lower() == search_val.lower()]

class SearchByCopies(SearchStrategy):
    def search(self, data, search_val: int):
        return [b for c, b in zip(CopiesIterator(data), data) if c == search_val]

class SearchByGenre(SearchStrategy):
    def search(self, data, search_val: str):
        return [b for g, b in zip(GenreIterator(data), data) if g.lower() == search_val.lower()]

class SearchByYear(SearchStrategy):
    def search(self, data, search_val: int):
        return [b for y, b in zip(YearIterator(data), data) if y == search_val]

class SearchByAvailableCopies(SearchStrategy):
    def search(self, data, search_val: int):
        return [b for ac, b in zip(AvailableCopiesIterator(data), data) if ac == search_val]

class SearchByLoanedCopies(SearchStrategy):
    def search(self, data, search_val: int):
        return [b for lc, b in zip(LoanedCopiesIterator(data), data) if lc == search_val]

class SearchByLendCount(SearchStrategy):
    def search(self, data, search_val: int):
        return [b for lc, b in zip(LendCountIterator(data), data) if lc == search_val]

class Searcher:
    def __init__(self, *search_strategies):
        self.search_strategies = search_strategies

    def search(self, data, **search_vals):
        result = data
        for strategy in self.search_strategies:
            # Get the class name to match the search value in the dictionary
            strategy_name = strategy.__class__.__name__
            search_val = search_vals.get(strategy_name)
            if search_val is not None:
                result = strategy.search(result, search_val)
        return result