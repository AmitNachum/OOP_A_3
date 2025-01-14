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
                for line in reader[1:]:  # Skip the header row
                    print(f"Reading line: {line}")
                    new_book = Book(line[0], line[1], line[4], int(line[5]), int(line[3]), line[2])
                    books.append(new_book)
        except FileNotFoundError:
            print(f"File {file_path} was not found.")
        except Exception as e:
            print(f"Error while reading file: {e}")

        return books

    # @staticmethod
    # def add_book(book : Book, books_path: str):
    #     header = FileManagement.read_file(books_path)[0]
    #     # Read the file
    #     data = [header] + FileManagement.read_file_to_books(books_path)
    #     copies_type = header[3]
    #
    #     # Check if the book exists
    #     for i in range(1, len(data)):
    #         b = data[i]
    #         if b == book:
    #             match copies_type:
    #
    #                 case "copies":
    #                     b.copies += 1
    #                     data[i] = b
    #
    #                     # Overwrite the file with updated data
    #                     with open(books_path, 'w', newline='') as file:
    #                         writer = csv.writer(file)
    #                         writer.writerow(data[0])
    #                         for row in data[1:]:
    #                             writer.writerow(row.get_fields())  # Convert Book to iterable
    #
    #                     FileManagement.load_available_books()
    #                     FileManagement.load_loaned_books()
    #                     print("Data updated successfully.")
    #                     return
    #
    #                 case "copies_available":
    #                     b.available_copies += 1
    #                     data[i] = b
    #
    #                     # Overwrite the file with updated data
    #                     with open(books_path, 'w', newline='') as file:
    #                         writer = csv.writer(file)
    #                         writer.writerow(data[0])
    #                         for row in data[1:]:
    #                             writer.writerow(row.get_available_fields())  # Convert Book to iterable
    #
    #                     FileManagement.load_available_books()
    #                     FileManagement.load_loaned_books()
    #                     print("Data updated successfully.")
    #                     return
    #
    #
    #                 case "copies_loaned":
    #                     b.loaned_copies += 1
    #                     data[i] = b
    #
    #                     # Overwrite the file with updated data
    #                     with open(books_path, 'w', newline='') as file:
    #                         writer = csv.writer(file)
    #                         writer.writerow(data[0])
    #                         for row in data[1:]:
    #                             writer.writerow(row.get_loaned_fields())  # Convert Book to iterable
    #
    #                     FileManagement.load_available_books()
    #                     FileManagement.load_loaned_books()
    #                     print("Data updated successfully.")
    #                     return
    #
    #
    #     match copies_type:
    #
    #         case "copies":
    #             with open(books_path, 'a') as file:
    #                 writer = csv.writer(file)
    #                 writer.writerow(book.get_fields())
    #
    #             FileManagement.load_available_books()
    #             FileManagement.load_loaned_books()
    #             print("Data written successfully")
    #
    #         case "copies_available":
    #             with open(books_path, 'a') as file:
    #                 writer = csv.writer(file)
    #                 writer.writerow(book.get_available_fields())
    #
    #             FileManagement.load_available_books()
    #             FileManagement.load_loaned_books()
    #             print("Data written successfully")
    #
    #         case "copies_loaned":
    #             with open(books_path, 'a') as file:
    #                 writer = csv.writer(file)
    #                 writer.writerow(book.get_loaned_fields())
    #
    #             FileManagement.load_available_books()
    #             FileManagement.load_loaned_books()
    #             print("Data written successfully")
    #
    # @staticmethod
    # def remove_book(book: Book, books_path: str):
    #     header = FileManagement.read_file(books_path)[0]
    #     # Read the file
    #     data = [header] + FileManagement.read_file_to_books(books_path)
    #     copies_type = header[3]
    #
    #     # Check if the book exists
    #     for i in range(1, len(data)):  # Skip the header row
    #         b = data[i]
    #         if b == book:  # Use __eq__ to compare books
    #             match copies_type:
    #
    #                 case "copies":
    #                     if b.copies > 1:
    #                         b.copies -= 1
    #                         data[i] = b
    #                     else:
    #                         del data[i]
    #                     # Remove the book completely
    #
    #                      # Overwrite the file with updated data
    #                     with open(books_path, 'w', newline='') as file:
    #                         writer = csv.writer(file)
    #                         writer.writerow(data[0])  # Write header
    #                         for row in data[1:]:  # Write data rows
    #                             writer.writerow(row.get_fields())  # Convert Book to iterable
    #
    #                     FileManagement.load_available_books()
    #                     FileManagement.load_loaned_books()
    #                     print("Data updated successfully.")
    #                     return
    #
    #                 case "copies_available":
    #                     print("entered the start of the if")
    #                     if b.available_copies > 1:
    #                         print("execute the if statement!!!!!")
    #                         b.available_copies -= 1
    #                         data[i] = b
    #                         print(f"entered if {data[i].available_copies}")
    #
    #                     else:
    #                         print(f"entered else {data[i].available_copies}!!!")
    #                         data[i].is_loaned = "Yes"
    #                         del data[i]
    #                        # Remove the book completely
    #
    #                     # Overwrite the file with updated data
    #                     with open(books_path, 'w', newline='') as file:
    #                         writer = csv.writer(file)
    #                         writer.writerow(data[0])  # Write header
    #                         for row in data[1:]:  # Write data rows
    #                             writer.writerow(row.get_available_fields())  # Convert Book to iterable
    #
    #                     FileManagement.load_available_books()
    #                     FileManagement.load_loaned_books()
    #                     print("Data updated successfully.")
    #                     return
    #
    #                 case "copies_loaned":
    #                     if b.loaned_copies > 1:
    #                         b.loaned_copies -= 1
    #                         data[i] = b
    #                     else:
    #                         data[i].is_loaned = "No"
    #                         del data[i]  # Remove the book completely
    #
    #                     # Overwrite the file with updated data
    #                     with open(books_path, 'w', newline='') as file:
    #                         writer = csv.writer(file)
    #                         writer.writerow(data[0])  # Write header
    #                         for row in data[1:]:  # Write data rows
    #                             writer.writerow(row.get_loaned_fields())  # Convert Book to iterable
    #
    #                     FileManagement.load_available_books()
    #                     FileManagement.load_loaned_books()
    #                     print("Data updated successfully.")
    #                     return
    #
    #
    #     print(f"Book '{book.title}' doesn't exist and cannot be removed!")

    @staticmethod
    def write_books(file_path: str, header: List[str], books: List[Book], field_method: str = "get_fields"):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the header
            for book in books:  # Write each book
                # Dynamically call the method specified by `field_method`
                fields = getattr(book, field_method)()
                writer.writerow(fields)

    @staticmethod
    def add_book(book: Book, books_path: str):
        header = FileManagement.read_file(books_path)[0]
        books = FileManagement.read_file_to_books(books_path)
        found = False

        # Update the specific file
        for b in books:
            if b == book:
                if books_path.endswith("available_books.csv"):
                    b.available_copies += 1
                elif books_path.endswith("loaned_books.csv"):
                    b.loaned_copies += 1
                elif books_path.endswith("books.csv"):
                    b.copies += 1
                found = True
                break

        if not found:  # If the book doesn't exist in the file
            if books_path.endswith("available_books.csv"):
                book.available_copies = 1
            elif books_path.endswith("loaned_books.csv"):
                book.loaned_copies = 1
            elif books_path.endswith("books.csv"):
                book.copies = 1
            books.append(book)

        # Write updated books back to the file
        FileManagement.write_books(
            books_path,
            header,
            books,
            field_method="get_available_fields" if "available" in books_path else
            "get_loaned_fields" if "loaned" in books_path else
            "get_fields"
        )

        FileManagement.load_available_books()
        FileManagement.load_loaned_books()
        print("Book added successfully.")

    @staticmethod
    def remove_book(book: Book, books_path: str):
        header = FileManagement.read_file(books_path)[0]
        books = FileManagement.read_file_to_books(books_path)
        updated_books = []  # To store updated data
        found = False

        for b in books:
            if b == book:
                if books_path.endswith("available_books.csv"):  # Update available_books.csv
                    if b.available_copies > 1:
                        b.available_copies -= 1
                    else:
                        continue  # Skip this book (remove it)
                elif books_path.endswith("loaned_books.csv"):  # Update loaned_books.csv
                    if b.loaned_copies > 1:
                        b.loaned_copies -= 1
                    else:
                        continue  # Skip this book (remove it)
                elif books_path.endswith("books.csv"):  # Update books.csv
                    if b.copies > 1:
                        b.copies -= 1
                    else:
                        continue  # Skip this book (remove it)
                found = True
            updated_books.append(b)

        if not found:
            print(f"Book '{book.title}' not found in {books_path}.")
        else:
            # Write updated books back to the file
            FileManagement.write_books(
                books_path,
                header,
                updated_books,
                field_method="get_available_fields" if "available" in books_path else
                "get_loaned_fields" if "loaned" in books_path else
                "get_fields"
            )

            FileManagement.load_available_books()
            FileManagement.load_loaned_books()
            print("Book removed successfully.")

    @staticmethod
    def search_book(books_path: str, *search_strategies, **search_vals):
        header = FileManagement.read_file(books_path)[0]
        data = FileManagement.read_file_to_books(books_path)
        searcher = Searcher(*search_strategies)
        result = searcher.search(data, **search_vals)

        with open("Files/search.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write header
            for row in result:  # Write data rows
                writer.writerow(row.get_fields())  # Convert Book to iterable
        print("Data updated successfully.")

    @staticmethod
    def load_available_books():
        data = FileManagement.read_file_to_books("Files/books.csv")
        available = [b for il, b in zip(IsLoanedIterator(data), data) if il.lower() == "no"]

        with open("Files/available_books.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'author', 'is_loaned', 'copies_available', 'genre', 'year'])  # Write header
            for row in available:  # Write data rows
                writer.writerow(row.get_available_fields())  # Convert Book to iterable
        print("Data updated successfully.")

    @staticmethod
    def load_loaned_books():
        data = FileManagement.read_file_to_books("Files/books.csv")
        loaned = [b for il, b in zip(IsLoanedIterator(data), data) if il.lower() == "yes"]

        with open("Files/loaned_books.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'author', 'is_loaned', 'copies_loaned', 'genre', 'year'])  # Write header
            for row in loaned:  # Write data rows
                writer.writerow(row.get_loaned_fields())  # Convert Book to iterable
        print("Data updated successfully.")

    @staticmethod
    def lend_book(book: Book):
        print(f"Lending book: {book}")
        available = FileManagement.read_file_to_books("Files/available_books.csv")
        print(f"Available books: {available}")

        found = False
        for b in available:
            if b == book:  # Use __eq__ to compare books
                found = True
                print(f"Book found: {b}")
                break

        if found:
            FileManagement.remove_book(book, "Files/available_books.csv")
            FileManagement.add_book(book, "Files/loaned_books.csv")
            print("Lending process completed successfully.")
        else:
            print(f"Book '{book.title}' doesn't have any available copies and cannot be loaned!")


if __name__ == '__main__':
    # Test adding books
    book1 = Book("Book Title", "Author Name", "Fiction", 2021)
    #FileManagement.add_book(book1, "Files/books.csv")

    # Test lending a book
    FileManagement.lend_book(book1)
