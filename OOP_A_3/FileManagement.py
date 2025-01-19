import csv
import functools
import inspect
import os
from Book import Book
from User import User
from SearchStrategy import *
import pandas as pd
import logging

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("Files/log.txt"),
        logging.StreamHandler()
    ]
)

# Define decorators
def log_action(action, level=logging.INFO):
    """Decorator to log the action performed with a specific logging level."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Log the action at the specified log level
            logging.log(level, f"{action} performed successfully.")
            return result
        return wrapper
    return decorator

def handle_exceptions(func):
    """
    A decorator to handle exceptions and provide structured error responses.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {str(e)}")
            return {"status": "error", "error": "File not found", "details": str(e)}
        except ValueError as e:
            logging.error(f"ValueError: {str(e)}")
            return {"status": "error", "error": "Value error", "details": str(e)}
    return wrapper

def check_file_exists(func):
    """Decorator to check if a file exists before performing operations."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get function signature to handle default values
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()  # Apply default values

        # Get the file_path from bound arguments (which includes default if not provided)
        file_path = bound_args.arguments.get('file_path')

        # Check if the file path exists
        if file_path is None:
            logging.error("file_path is required but not provided.")
            return

        if not os.path.exists(file_path):
            logging.error(f"File does not exist: {file_path}")
            return

        return func(*args, **kwargs)

    return wrapper

def ensure_csv_columns(required_columns):
    """Decorator to ensure a DataFrame has the required columns."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature to handle default values
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()  # Apply default values

            # Get the file_path from bound arguments (which includes default if not provided)
            file_path = bound_args.arguments.get('file_path')
            try:
                df = pd.read_csv(file_path)
            except (FileNotFoundError, pd.errors.EmptyDataError):
                # Create a new DataFrame if the file is missing or empty
                df = pd.DataFrame(columns=required_columns)
                logging.warning(f"Created new DataFrame with columns: {required_columns}")
            kwargs["df"] = df
            return func(*args, **kwargs)
        return wrapper
    return decorator

class FileManagement:
    waiting_list = {}
    lend_counter = {}

    @staticmethod
    @handle_exceptions
    @check_file_exists
    @log_action("User file read")
    @ensure_csv_columns(["user_name", "password"])
    def read_users(file_path="Files/users.csv",  df=None):
        users = pd.read_csv(file_path)
        return users

    @staticmethod
    @handle_exceptions
    @log_action(f"User sign-up")
    def sign_up_user(user: User):
        users = FileManagement.read_users()

        # Check if the user_name already exists in the DataFrame
        if user.user_name in users['user_name'].values:
            logging.warning(f"Sign-up failed: User '{user.user_name}' already exists.")
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
            logging.info(f"User '{user.user_name}' signed up successfully.")
            return True

    @staticmethod
    @log_action("Get Popular Books")
    @handle_exceptions
    def get_popular_books():
        if not FileManagement.lend_counter:
            return

        popular_books = sorted(FileManagement.lend_counter.items(), key=lambda item: item[1], reverse= True)

        temp_list = popular_books[:10]
        keys = list(map(lambda item: item[0], temp_list))
        book = FileManagement.load_books_to_list()

        return [key for key in keys if key in book]

    @staticmethod
    @log_action("Load popular books to CSV")
    @handle_exceptions
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
    def load_populars_to_csv(file_path = "Files/popular_books.csv",  df=None):
        populars = FileManagement.get_popular_books()

        if not populars:
            logging.info("No popular books found.")
            return

        found_books = []

        for book in populars:
            matching_row = df[
                (df["title"] == book.title) &
                (df["author"] == book.author) &
                (df["copies"] == book.copies) &
                (df["is_loaned"] == book.is_loaned) &
                (df["genre"] == book.genre) &
                (df["year"] == book.year)
                ]
            if not matching_row.empty:
                available_copies = matching_row["available_copies"].iloc[0]
                loaned_copies = matching_row["loaned_copies"].iloc[0]
                book_data = book.get_fields() + [available_copies, loaned_copies]
                found_books.append(book_data)

        df = pd.DataFrame(found_books)
        df.to_csv(file_path, index=False)
        logging.info(f"Popular books saved to CSV.")

    @staticmethod
    @log_action("Book added")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
    def add_book(book: Book, file_path = "Files/books.csv",  df=None):
        book_mask = (df["title"] == book.title) & (df["author"] == book.author)
        if book_mask.any():
            index = df[book_mask].index[0]
            df.at[index, "copies"] += book.copies
            if df.at[index, "is_loaned"] == "No":
                df.at[index, "available_copies"] += book.copies
            logging.info(f"Updated copies for '{book.title}' by {book.author}.")
        else:
            available_copies = book.copies if book.is_loaned == "No" else 0
            loaned_copies = book.copies if book.is_loaned == "Yes" else 0
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
            df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
            logging.info(f"Book '{book.title}' by {book.author} added successfully.")

        df.to_csv(file_path, index=False)

    @staticmethod
    @log_action("Book removed")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
    def remove_book(book: Book, file_path = "Files/books.csv",  df=None):
        match = (df["title"] == book.title) & (df["author"] == book.author)
        if match.any():
            book_index = df[match].index[0]
            if df.at[book_index, "copies"] > 1 and df.at[book_index, "available_copies"] > 1:
                df.at[book_index, "copies"] -= 1
                df.at[book_index, "available_copies"] -= 1
                logging.info(f"One copy of '{book.title}' by {book.author} has been removed.")
            elif df.at[book_index, "loaned_copies"] == 0:
                df = df[~match]
                logging.info(f"Book '{book.title}' by {book.author} has been removed completely.")
            else:
                logging.warning(f"Cannot remove '{book.title}' by {book.author} because there are loaned copies.")
        else:
            logging.warning(f"Book '{book.title}' by {book.author} was not found in the library.")

        df.to_csv(file_path, index=False)

    @staticmethod
    @log_action("Book lent")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
    def lend_book(book: Book, file_path = "Files/books.csv",  df=None):
        book_mask = (df["title"] == book.title) & (df["author"] == book.author)
        if not book_mask.any():
            logging.warning(f"Book '{book.title}' by {book.author} was not found.")
            return False

        index = df[book_mask].index[0]
        if df.at[index, "available_copies"] <= 0:
            logging.warning(f"No available copies of '{book.title}' by {book.author} to lend.")
            return False

        df.at[index, "available_copies"] -= 1
        df.at[index, "loaned_copies"] += 1
        if book not in FileManagement.lend_counter:
            FileManagement.lend_counter[book] = 0
        FileManagement.lend_counter[book] += 1

        df.to_csv(file_path, index=False)
        logging.info(f"Book '{book.title}' by {book.author} has been successfully loaned.")
        return True

    @staticmethod
    @log_action("Add to waiting list")
    @handle_exceptions
    def ask_info(book: Book, info):
        if book not in FileManagement.waiting_list:
            FileManagement.waiting_list[book] = []
        FileManagement.waiting_list[book].append(info)

    @staticmethod
    @log_action("Load waiting list")
    @handle_exceptions
    @ensure_csv_columns(["title", "name", "email"])
    def load_waiting_list(file_path="Files/waiting_list.csv", df=None):
        """
        Loads and updates the waiting list from a CSV file, avoiding duplicates.
        """
        # Process each book's waiting list
        for title, entries in FileManagement.waiting_list.items():
            for entry in entries:
                new_row = {"title": title.title, "name": entry.get("name", ""), "email": entry.get("email", "")}
                if not ((df['title'] == new_row['title']) &
                        (df['name'] == new_row['name']) &
                        (df['email'] == new_row['email'])).any():
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    logging.info(f"Added new entry for '{new_row['title']}' in the waiting list.")

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
        logging.info(f"Waiting list saved successfully to {file_path}.")

    @staticmethod
    @log_action("Load books to list")
    @handle_exceptions
    @check_file_exists
    def load_books_to_list(file_path = "Files/books.csv",  df=None):
        books = []
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            try:
                book = Book(
                    title=row["title"],
                    author=row["author"],
                    is_loaned=row["is_loaned"],
                    copies=row["copies"],
                    genre=row["genre"],
                    year=row["year"]
                )
                books.append(book)
            except KeyError as e:
                logging.error(f"Missing expected column in book data: {e}")

        logging.info(f"Successfully loaded {len(books)} books from the file.")
        return books

    @staticmethod
    @log_action("Search books")
    @handle_exceptions
    def search_book(*search_strategies, **search_vals):
        """
        Searches for books using search strategies and writes the results to a CSV file.
        """
        file_path = "Files/books.csv"
        try:
            # Step 1: Read the entire CSV file into a DataFrame
            df = pd.read_csv(file_path)
            logging.info(f"Books file loaded successfully from {file_path}.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist, create a new DataFrame with necessary columns
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
            logging.error(f"Books file does not exist or is empty at {file_path}.")

        # Load the books data into a list of Book objects
        books = FileManagement.load_books_to_list()
        logging.info(f"Loaded {len(books)} books for searching.")

        # Use Searcher to apply search strategies
        searcher = Searcher(*search_strategies)
        results = searcher.search(books, **search_vals)
        logging.info(f"Search completed with {len(results)} results.")

        # Map found books to their `available_copies` and `loaned_copies`
        found_books = []
        for book in results:
            matching_row = df[
                (df["title"] == book.title) &
                (df["author"] == book.author) &
                (df["copies"] == book.copies) &
                (df["is_loaned"] == book.is_loaned) &
                (df["genre"] == book.genre) &
                (df["year"] == book.year)
                ]
            if not matching_row.empty:
                available_copies = matching_row["available_copies"].iloc[0]
                loaned_copies = matching_row["loaned_copies"].iloc[0]
                book_data = book.get_fields() + [available_copies, loaned_copies]
                found_books.append(book_data)

        # Write the results to the CSV file
        with open("Files/search.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(df.columns)  # Write headers
            writer.writerows(found_books)  # Write the found books' data
        logging.info(f"Search results saved to {file_path}.")

    @staticmethod
    @log_action("Return book")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
    def return_book(book: Book, file_path = "Files/books.csv",  df=None):
        book_mask = (df["title"] == book.title) & (df["author"] == book.author)

        if not book_mask.any():
            logging.warning(f"Book '{book.title}' by {book.author} was not found.")
            return

        index = df[book_mask].index[0]
        if df.at[index, "loaned_copies"] <= 0:
            logging.warning(f"Cannot return a book that is not loaned.")
            return

        df.at[index, "available_copies"] += 1
        df.at[index, "loaned_copies"] -= 1
        df.to_csv(file_path, index=False)
        logging.info(f"Book '{book.title}' by {book.author} has been successfully returned.")


if __name__ == '__main__':
    pass

