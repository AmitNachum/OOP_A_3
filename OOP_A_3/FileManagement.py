import csv
from typing import List
from Book import Book
from User import User
from SearchStrategy import *
import pandas as pd

class FileManagement:
    books_path = "Files/books.csv"

    @staticmethod
    def read_users():
        try:
            # Try reading the CSV file
            users = pd.read_csv("Files/users.csv")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file is missing or empty, return an empty DataFrame
            users = pd.DataFrame(columns=['user_name', 'password'])
        return users

    @staticmethod
    def sign_up_user(user: User):
        users = FileManagement.read_users()

        # Check if the user_name already exists in the DataFrame
        if user.user_name in users['user_name'].values:
            return False
        else:
            # Convert the user object to a DataFrame row
            new_user = pd.DataFrame([{
                'user_name': user.user_name,
                'password': user.password,  # Assuming the user has these attributes
            }])

            # Use concat to add the new row to the DataFrame
            users = pd.concat([users, new_user], ignore_index=True)

            # Save the updated DataFrame back to the CSV file
            users.to_csv("Files/users.csv", index=False)

            return True

    @staticmethod
    def add_book(book: Book):
        # Step 1: Read the existing CSV file
        try:
            df = pd.read_csv(FileManagement.books_path)
        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame with necessary columns
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])

        # Step 2: Calculate `available_copies` and `loaned_copies` for the new book
        available_copies = book.copies if book.is_loaned == "No" else 0
        loaned_copies = book.copies if book.is_loaned == "Yes" else 0

        # Step 3: Convert the Book object to a dictionary including the calculated values
        new_book = {
            "title": book.title,
            "author": book.author,
            "is_loaned": book.is_loaned,
            "copies": book.copies,
            "genre": book.genre,
            "year": book.year,
            "available_copies": available_copies,
            "loaned_copies": loaned_copies,
        }

        # Step 4: Append the new book to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)

        # Step 5: Save the updated DataFrame back to the file
        df.to_csv(FileManagement.books_path, index=False)
        print(f"Book '{book.title}' added successfully!")

    @staticmethod
    def remove_book(book: Book):
        try:
            # Step 1: Load the CSV file
            df = pd.read_csv(FileManagement.books_path)
        except FileNotFoundError:
            print("The books file does not exist.")
            return

            # Step 2: Find and remove the matching book
        initial_length = len(df)
        df = df[~(
                (df["title"] == book.title) &
                (df["author"] == book.author) &
                (df["copies"] == book.copies) &
                (df["is_loaned"] == book.is_loaned) &
                (df["genre"] == book.genre) &
                (df["year"] == book.year)
        )]

        # Step 3: Check if a book was removed
        if len(df) < initial_length:
            # Step 4: Save the updated DataFrame
            df.to_csv(FileManagement.books_path, index=False)
            print(f"Book '{book.title}' by {book.author} has been removed successfully.")
        else:
            print(f"Book '{book.title}' by {book.author} was not found in the library.")

    @staticmethod
    def lend_book(book: Book):
        try:
            # Step 1: Load the CSV file
            df = pd.read_csv(FileManagement.books_path)
        except FileNotFoundError:
            print("The books file does not exist.")
            return

            # Step 2: Find the matching book
        book_mask = (
                (df["title"] == book.title) &
                (df["author"] == book.author)
        )
        if not book_mask.any():
            print(f"Book '{book.title}' by {book.author} was not found in the library.")
            return

        # Step 3: Check availability
        index = df[book_mask].index[0]  # Get the index of the matching book
        if df.at[index, "available_copies"] <= 0:
            print(f"No available copies of '{book.title}' by {book.author} to lend.")
            return

        # Step 4: Update the book details
        df.at[index, "available_copies"] -= 1
        df.at[index, "loaned_copies"] += 1

        # Step 5: Save the updated DataFrame
        df.to_csv(FileManagement.books_path, index=False)
        print(f"Book '{book.title}' by {book.author} has been successfully loaned.")

    @staticmethod
    def load_books_to_list():
        books = []
        try:
            df = pd.read_csv(FileManagement.books_path)
            for _, row in df.iterrows():
                # Create a Book object for each row
                book = Book(
                    title=row["title"],
                    author=row["author"],
                    is_loaned=row["is_loaned"],
                    copies=row["copies"],
                    genre=row["genre"],
                    year=row["year"]
                )
                books.append(book)
        except FileNotFoundError:
            print("The file does not exist.")
        except KeyError as e:
            print(f"Missing expected column in the file: {e}")
        return books

    # @staticmethod
    # def read_file(file_path: str) -> List:
    #     try:
    #         with open(file_path, 'r') as f:
    #             reader = list(csv.reader(f))
    #             return reader
    #
    #     except FileNotFoundError:
    #         print(f"File {file_path} was not found.")
    #         return []
    #
    # @staticmethod
    # def read_file_to_books(file_path: str, copies_type: str = "copies") -> List[Book]:
    #     books = []
    #
    #     try:
    #         with open(file_path, 'r') as f:
    #             reader = list(csv.reader(f))
    #             for line in reader[1:]:  # Skip the header row
    #                 dynamic_args = {copies_type: int(line[3])}
    #                 new_book = Book(title= line[0], author= line[1], genre= line[4], year= int(line[5]), is_loaned=line[2], **dynamic_args)
    #                 books.append(new_book)
    #     except FileNotFoundError:
    #         print(f"File {file_path} was not found.")
    #     except Exception as e:
    #         print(f"Error while reading file: {e}")
    #
    #     return books
    #
    # @staticmethod
    # def write_books(file_path: str, header: List[str], books: List[Book], field_method: str = "get_fields"):
    #     with open(file_path, 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(header)  # Write the header
    #         for book in books:  # Write each book
    #             # Dynamically call the method specified by `field_method`
    #             fields = getattr(book, field_method)()
    #             writer.writerow(fields)
    #
    # @staticmethod
    # def add_book(book: Book, books_path: str):
    #     header = FileManagement.read_file(books_path)[0]
    #     books = []
    #
    #     if books_path.endswith("books_available.csv"):
    #         books = FileManagement.read_file_to_books(books_path, "available_copies")
    #     elif books_path.endswith("books_loaned.csv"):
    #         books = FileManagement.read_file_to_books(books_path, "loaned_copies")
    #     elif books_path.endswith("books.csv"):
    #         books = FileManagement.read_file_to_books(books_path)
    #
    #     found = False
    #
    #     # Update the specific file
    #     for b in books:
    #         if b == book:
    #             if books_path.endswith("books_available.csv"):
    #                 b.available_copies += 1
    #             elif books_path.endswith("books_loaned.csv"):
    #                 b.loaned_copies += 1
    #             elif books_path.endswith("books.csv"):
    #                 b.copies += 1
    #                 b.available_copies = b.copies - b.loaned_copies
    #                 b.loaned_copies = b.copies - b.available_copies
    #             found = True
    #             break
    #
    #     if not found:  # If the book doesn't exist in the file
    #         if books_path.endswith("books_available.csv"):
    #             book.available_copies = book.copies - book.loaned_copies
    #         elif books_path.endswith("books_loaned.csv"):
    #             book.loaned_copies = book.copies - book.available_copies
    #         elif books_path.endswith("books.csv"):
    #             book.copies = 1
    #         books.append(book)
    #
    #     # Write updated books back to the file
    #     FileManagement.write_books(
    #         books_path,
    #         header,
    #         books,
    #         field_method="get_available_fields" if "available" in books_path else
    #         "get_loaned_fields" if "loaned" in books_path else
    #         "get_fields"
    #     )
    #
    #     if not found and books_path.endswith("books.csv"):
    #         FileManagement.load_available_books()
    #         FileManagement.load_loaned_books()
    #
    #     print("Book added successfully.")
    #
    # @staticmethod
    # def remove_book(book: Book, books_path: str):
    #     header = FileManagement.read_file(books_path)[0]
    #     books = []
    #
    #     if books_path.endswith("books_available.csv"):
    #         books = FileManagement.read_file_to_books(books_path, "available_copies")
    #     elif books_path.endswith("books_loaned.csv"):
    #         books = FileManagement.read_file_to_books(books_path, "loaned_copies")
    #     elif books_path.endswith("books.csv"):
    #         books = FileManagement.read_file_to_books(books_path)
    #
    #     updated_books = []  # To store updated data
    #     found = False
    #
    #     for b in books:
    #         if b == book:
    #             if books_path.endswith("books_available.csv"):  # Update books_available.csv
    #                 if b.available_copies > 1:
    #                     b.available_copies -= 1
    #                     found = True
    #                 else:
    #                     b.is_loaned = "yes"
    #                     found = True
    #                     continue  # Skip this book (remove it)
    #             elif books_path.endswith("books_loaned.csv"):  # Update books_loaned.csv
    #                 if b.loaned_copies > 1:
    #                     b.loaned_copies -= 1
    #                     found = True
    #                 else:
    #                     b.is_loaned = "no"
    #                     found = True
    #                     continue  # Skip this book (remove it)
    #             elif books_path.endswith("books.csv"):  # Update books.csv
    #                 if b.copies > 1:
    #                     b.copies -= 1
    #                     b.available_copies = b.copies - b.loaned_copies
    #                     b.loaned_copies = b.copies - b.available_copies
    #                     found = True
    #                 else:
    #                     found = True
    #                     continue  # Skip this book (remove it)
    #         updated_books.append(b)
    #
    #     if not found:
    #         print(f"Book '{book.title}' not found in {books_path}.")
    #     else:
    #         print(updated_books)
    #         # Write updated books back to the file
    #         FileManagement.write_books(
    #             books_path,
    #             header,
    #             updated_books,
    #             field_method="get_available_fields" if "available" in books_path else
    #             "get_loaned_fields" if "loaned" in books_path else
    #             "get_fields"
    #         )
    #
    #         if books_path.endswith("books.csv"):
    #             FileManagement.load_available_books()
    #             FileManagement.load_loaned_books()
    #
    #         print("Book removed successfully.")


    @staticmethod
    def search_book(*search_strategies, **search_vals):
        try:
            df = pd.read_csv(FileManagement.books_path, nrows=0)  # Read only the headers
            header = df.columns.tolist()  # Return headers as a list
        except FileNotFoundError:
            print("The file does not exist.")
            return None

        data = FileManagement.load_books_to_list()
        searcher = Searcher(*search_strategies)
        result = searcher.search(data, **search_vals)

        with open("Files/search.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write header
            for row in result:  # Write data rows
                writer.writerow(row.get_fields())  # Convert Book to iterable
        print("Data updated successfully.")

    # @staticmethod
    # def load_available_books():
    #     data = FileManagement.read_file_to_books("Files/books.csv")
    #     available = [b for il, b in zip(IsLoanedIterator(data), data) if il.lower() == "no"]
    #
    #     with open("Files/books_available.csv", 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['title', 'author', 'is_loaned', 'copies_available', 'genre', 'year'])  # Write header
    #         for row in available:  # Write data rows
    #             writer.writerow(row.get_available_fields())  # Convert Book to iterable
    #     print("Data updated successfully.")
    #
    # @staticmethod
    # def load_loaned_books():
    #     data = FileManagement.read_file_to_books("Files/books.csv")
    #     loaned = [b for il, b in zip(IsLoanedIterator(data), data) if il.lower() == "yes"]
    #
    #     with open("Files/books_loaned.csv", 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['title', 'author', 'is_loaned', 'copies_loaned', 'genre', 'year'])  # Write header
    #         for row in loaned:  # Write data rows
    #             writer.writerow(row.get_loaned_fields())  # Convert Book to iterable
    #     print("Data updated successfully.")
    #
    # @staticmethod
    # def lend_book(book: Book):
    #     available = FileManagement.read_file_to_books("Files/books_available.csv")
    #     found = False
    #     for b in available:
    #         if b == book:  # Use __eq__ to compare books
    #             found = True
    #             break
    #
    #     if found:
    #         FileManagement.remove_book(book, "Files/books_available.csv")
    #         FileManagement.add_book(book, "Files/books_loaned.csv")
    #         print("Lending process completed successfully.")
    #     else:
    #         print(f"Book '{book.title}' doesn't have any available copies and cannot be loaned!")


if __name__ == '__main__':
    pass

