import csv
from typing import List
from Book import Book
from SearchStrategy import *

class FileManagement:

    @staticmethod
    def read_file(file_path: str) -> List:
        try:
            with open(file_path, 'r') as f:
                reader = list(csv.reader(f))
                return reader

        except FileNotFoundError:
            print(f"File {file_path} was not found.")
            return []

    @staticmethod
    def read_file_to_books(file_path: str) -> List[Book]:
        books = []
        try:
            with open(file_path, 'r') as f:
                reader = list(csv.reader(f))
                for line in reader[1:]:  # Skip the first row (header)
                    new_book = Book(line[0], line[1], line[4], int(line[5]), int(line[3]), line[2])
                    books.append(new_book)


        except FileNotFoundError:
            print(f"File {file_path} was not found")

        return books



    @staticmethod
    def add_book(book : Book, books_path: str):
        # Read the file
        data = [['title', 'author', 'is_loaned', 'copies', 'genre', 'year']] + FileManagement.read_file_to_books(books_path)

        # Check if the book exists
        for b in data:
            if b == book:
                index = data.index(b)
                data[index] = book
                # Overwrite the file with updated data
                with open(books_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data[0])
                    for row in data[1:]:
                        writer.writerow(row.get_fields())  # Convert Book to iterable
                print("Data updated successfully.")
                return

        with open(books_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(book.get_fields())

        print("Data written to books.csv successfully")

    @staticmethod
    def remove_book(book: Book, books_path: str):
        # Read the file
        data = [['title', 'author', 'is_loaned', 'copies', 'genre', 'year']] + FileManagement.read_file_to_books(books_path)
        found = False

        # Check if the book exists
        for i in range(1, len(data)):  # Skip the header row
            b = data[i]
            if b == book:  # Use __eq__ to compare books
                found = True
                if b.copies > 1:
                    b.copies -= 1
                    data[i] = b
                else:
                    del data[i]  # Remove the book completely
                    break  # Stop after finding and handling the book

        if found:
        # Overwrite the file with updated data
            with open(books_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data[0])  # Write header
                for row in data[1:]:  # Write data rows
                    writer.writerow(row.get_fields())  # Convert Book to iterable
            print("Data updated successfully.")
        else:
            print(f"Book '{book.title}' doesn't exist and cannot be removed!")


    @staticmethod
    def search_book(books_path: str, *search_strategies, **search_vals):
        data = FileManagement.read_file_to_books(books_path)
        searcher = Searcher(*search_strategies)
        result = searcher.search(data, **search_vals)

        print(result)

        with open("Files/exe.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year'])  # Write header
            for row in result:  # Write data rows
                writer.writerow(row.get_fields())  # Convert Book to iterable
        print("Data updated successfully.")

if __name__ == '__main__':
    s = (SearchByIsLoaned(), SearchByGenre(), SearchByAuthor())
    FileManagement.search_book("Files/books.csv", *s, SearchByIsLoaned="No", SearchByGenre="Fiction", SearchByAuthor="Leo Tolstoy")

