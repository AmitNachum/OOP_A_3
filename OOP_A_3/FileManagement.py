import ast
import csv
import functools
import inspect
import os
from Book import Book
from User import User
from SearchStrategy import *
import pandas as pd
import logging
"""
Handles file-related operations such as reading, writing, and modifying library data stored in CSV files.
"""
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
                df.to_csv(file_path, index=False)
                logging.warning(f"Created new DataFrame with columns: {required_columns}")
            kwargs["df"] = df
            return func(*args, **kwargs)
        return wrapper
    return decorator

class FileManagement:
    """
   Provides static methods to manage books, users, notifications, and waiting lists in the library system.
   """
    waiting_list = {}

    @staticmethod
    @log_action("Got User Notification")
    @handle_exceptions
    def get_user_notifications(user_name):
        """Fetch the notifications for a given user from the database."""
        users = FileManagement.read_users()
        user_row = users[users['user_name'] == user_name]

        if not user_row.empty:
            # Access the serialized 'notifications' field
            notifications_str = user_row.iloc[0]['notifications']

            try:
                # Convert the serialized string back into a dictionary
                notifications = ast.literal_eval(notifications_str)

                # Return the messages for the specific user
                if isinstance(notifications, dict):
                    return notifications
            except (ValueError, SyntaxError):
                logging.error(f"Failed to parse notifications for user: {user_name}")
                return {}
        return {}

    @staticmethod
    @log_action("Load users to list")
    @handle_exceptions
    @ensure_csv_columns(["user_name", "password", "notifications"])
    def load_users_to_list(file_path="Files/users.csv",df=None):
        """
       Loads user data from a CSV file and creates User objects.

       Args:
           file_path (str): Path to the users CSV file. Default is 'Files/users.csv'.
           df (pandas.DataFrame): DataFrame containing user data.

       Returns:
           list: List of User objects.
       """
        users = []
        for _, row in df.iterrows():
            try:
                user = User(
                    user_name= row["user_name"],
                    password= row["password"]
                )
                users.append(user)
            except KeyError as e:
                logging.error(f"Missing expected column in user data: {e}")

        logging.info(f"Successfully loaded {len(users)} users from the file.")
        return users

    @staticmethod
    @log_action("Notification Added")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["user_name", "password", "notifications"])
    def write_message(user, file_path="Files/users.csv",df=None):
        """
        Updates user notifications in the CSV file.

        Args:
            user (User): The user to update notifications for.
            file_path (str): Path to the users CSV file.
            df (pandas.DataFrame): DataFrame containing user data.
        """
        user_mask = (df["user_name"] == user.user_name)
        # Ensure the "notifications" column can store objects
        df["notifications"] = df["notifications"].astype(object)

        if user_mask.any():
            index = df[user_mask].index[0]
            df.at[index, "notifications"] = user.notifications
            df.to_csv(file_path, index=False)

    @staticmethod
    @handle_exceptions
    @check_file_exists
    @log_action("User file read")
    @ensure_csv_columns(["user_name", "password", "notifications"])
    def read_users(file_path="Files/users.csv",  df=None):
        """
        Reads user data from a CSV file.

        Args:
            file_path (str): Path to the users CSV file.

        Returns:
            pandas.DataFrame: DataFrame containing user data.
        """
        users = pd.read_csv(file_path)
        return users

    @staticmethod
    @handle_exceptions
    @log_action(f"User sign-up")
    def sign_up_user(user: User):
        """
        Signs up a new user and adds them to the CSV file.

        Args:
            user (User): The user to sign up.

        Returns:
            bool: True if sign-up is successful, False otherwise.
        """
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
        """
        Fetches the top 10 most popular books by lend count.

        Returns:
            list: List of popular Book objects.
        """
        books_df = pd.read_csv("Files/books.csv")
        books_df = books_df.sort_values(by="lend_count", ascending=False)
        top_books = books_df.head(10)

        all_books = FileManagement.load_books_to_list()
        popular_books = [
            book for book, additional_data in all_books if (book.title, book.author) in zip(top_books["title"], top_books["author"])
        ]
        return popular_books

    @staticmethod
    @log_action("Load popular books to CSV")
    @handle_exceptions
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies", "lend_count"])
    def load_populars_to_csv(file_path="Files/popular_books.csv", df=None):
        """
        Saves the top 10 most popular books to a CSV file.

        Args:
            file_path (str): Path to the popular books CSV file.
            df (pandas.DataFrame): DataFrame containing popular books data.
        """
        popular_books = FileManagement.get_popular_books()
        books_df = pd.read_csv("Files/books.csv")

        if not popular_books:
            logging.info("No popular books found.")
            return

        # Prepare the data to save
        popular_data = []
        for book in popular_books:
            matching_row = books_df[
                (books_df["title"] == book.title) &
                (books_df["author"] == book.author)
                ]
            if not matching_row.empty:
                book_data = {
                    "title": book.title,
                    "author": book.author,
                    "is_loaned": book.is_loaned,
                    "copies": book.copies,
                    "genre": book.genre,
                    "year": book.year,
                    "available_copies": matching_row["available_copies"].iloc[0],
                    "loaned_copies": matching_row["loaned_copies"].iloc[0],
                    "lend_count": matching_row["lend_count"].iloc[0],
                }
                popular_data.append(book_data)

        # Update the DataFrame and save it
        df = pd.DataFrame(popular_data)
        df = df.sort_values(by="lend_count", ascending=False)
        df.to_csv(file_path, index=False)
        logging.info(f"Popular books saved to {file_path}.")

    @staticmethod
    @log_action("Book added")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies", "lend_count"])
    def add_book(book: Book, file_path="Files/books.csv", df=None):
        """
        Adds a book to the library.

        Args:
        book (Book): The Book object to add.
        file_path (str): Path to the books CSV file. Default is 'Files/books.csv'.
        df (pandas.DataFrame): DataFrame containing book data.

        Returns:
             None
        """
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
            lend_count = 0  # Initializing lend_count to 0 for new book
            new_book = {
                "title": book.title,
                "author": book.author,
                "is_loaned": book.is_loaned,
                "copies": book.copies,
                "genre": book.genre,
                "year": book.year,
                "available_copies": available_copies,
                "loaned_copies": loaned_copies,
                "lend_count": lend_count,  # Add lend_count column
            }
            df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
            logging.info(f"Book '{book.title}' by {book.author} added successfully.")

        df.to_csv(file_path, index=False)

    @staticmethod
    @log_action("Book removed")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies", "lend_count"])
    def remove_book(book: Book, file_path = "Files/books.csv",  df=None):
        """
        Removes a copy of a book from the library or deletes it entirely if no copies remain.

        Args:
            book (Book): The Book object to remove.
            file_path (str): Path to the books CSV file.
            df (pandas.DataFrame): DataFrame containing book data.

        Returns:
            bool: True if the book was removed, False otherwise.
        """
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
                return False
        else:
            logging.warning(f"Book '{book.title}' by {book.author} was not found in the library.")
            return False

        df.to_csv(file_path, index=False)
        return True

    @staticmethod
    @log_action("Book lent")
    @handle_exceptions
    @check_file_exists
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies", "lend_count"])
    def lend_book(book: Book, file_path="Files/books.csv", df=None):
        """
        Lends a book to a user by decrementing available copies and incrementing loaned copies.

        Args:
            book (Book): The Book object to lend.
            file_path (str): Path to the books CSV file.
            df (pandas.DataFrame): DataFrame containing book data.

        Returns:
            bool: True if the book was successfully lent, False otherwise.
        """
        book_mask = (df["title"] == book.title) & (df["author"] == book.author)
        if not book_mask.any():
            logging.warning(f"Book '{book.title}' by {book.author} was not found.")
            return False

        index = df[book_mask].index[0]
        if df.at[index, "available_copies"] <= 0:
            logging.warning(f"No available copies of '{book.title}' by {book.author} to lend.")
            return False

        # Update the available and loaned copies
        df.at[index, "available_copies"] -= 1
        df.at[index, "loaned_copies"] += 1

        # Update the lend_count for tracking popularity
        df.at[index, "lend_count"] += 1

        # Save the changes to books.csv
        df.to_csv(file_path, index=False)

        # Update popular_books.csv to reflect lend count changes
        FileManagement.load_populars_to_csv()
        logging.info(f"Book '{book.title}' by {book.author} has been successfully loaned.")
        return True

    @staticmethod
    @log_action("Add to waiting list")
    @handle_exceptions
    def ask_info(book: Book, info):
        """
        Adds user information to a waiting list for a specific book.

        Args:
            book (Book): The book to add to the waiting list.
            info (dict): User information such as name and email.
        """
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

        Args:
            file_path (str): Path to the waiting list CSV file.
            df (pandas.DataFrame): DataFrame containing waiting list data.
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
        """
        Loads all books from the specified CSV file into a list of Book objects with additional data.

        Args:
            file_path (str): Path to the books CSV file.
            df (pandas.DataFrame): Optional DataFrame containing book data.

        Returns:
            list: A list of tuples containing Book objects and additional data.
        """
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
                additional_data = {
                    "available_copies": row["available_copies"],
                    "loaned_copies": row["loaned_copies"],
                    "lend_count": row["lend_count"]
                }
                books.append((book, additional_data))
            except KeyError as e:
                logging.error(f"Missing expected column in book data: {e}")

        logging.info(f"Successfully loaded {len(books)} books from the file.")
        return books

    @staticmethod
    @log_action("Search books")
    @handle_exceptions
    def search_book(*search_strategies, **search_vals):
        """
        Searches for books using specified strategies and writes the results to a CSV file.

        Args:
            *search_strategies: Strategies to filter the books.
            **search_vals: Parameters for the search strategies.

        Writes:
            CSV file containing the search results.
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
        results = [book for book, _ in results]
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
                lend_count = matching_row["lend_count"].iloc[0]
                book_data = book.get_fields() + [available_copies, loaned_copies, lend_count]
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
    @ensure_csv_columns(["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies", "lend_count"])
    def return_book(book: Book, file_path = "Files/books.csv",  df=None):
        """
        Handles the return of a loaned book by updating the book's data in the library.

        Args:
            book (Book): The Book object to be returned.
            file_path (str): Path to the books CSV file.
            df (pandas.DataFrame): Optional DataFrame containing book data.

        Returns:
            bool: True if the book was successfully returned, False otherwise.
        """
        book_mask = (df["title"] == book.title) & (df["author"] == book.author)

        if not book_mask.any():
            logging.warning(f"Book '{book.title}' by {book.author} was not found.")
            return False

        index = df[book_mask].index[0]
        if df.at[index, "loaned_copies"] <= 0:
            logging.warning(f"Cannot return a book that is not loaned.")
            return False

        df.at[index, "available_copies"] += 1
        df.at[index, "loaned_copies"] -= 1
        df.to_csv(file_path, index=False)
        logging.info(f"Book '{book.title}' by {book.author} has been successfully returned.")
        return True



if __name__ == '__main__':
    pass

