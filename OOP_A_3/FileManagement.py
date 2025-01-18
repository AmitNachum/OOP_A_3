import csv
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
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ]
)

class FileManagement:
    books_path = "Files/books.csv"
    waiting_list = {}
    lend_counter = {}

    @staticmethod
    def read_users():
        try:
            # Try reading the CSV file
            users = pd.read_csv("Files/users.csv")
            logging.info("Users file read successfully.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            users = pd.DataFrame(columns=['user_name', 'password'])
            logging.error("Failed to read users file.")
        return users

    @staticmethod
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
    def get_popular_books():
        if not FileManagement.lend_counter:
            print("No popular books are currently available")
            return

        popular_books = sorted(FileManagement.lend_counter.items(), key=lambda item: item[1], reverse= True)

        temp_list = popular_books[:10]
        keys = list(map(lambda item: item[0], temp_list))
        book = FileManagement.load_books_to_list()

        return [key for key in keys if key in book]

    @staticmethod
    def load_populars_to_csv():
        # Define the file path for saving the CSV
        file_path = "Files/popular_books.csv"
        populars = FileManagement.get_popular_books()

        try:
            df = pd.read_csv(FileManagement.books_path)
            logging.info("Popular Books file read successfully.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist, create a new DataFrame with necessary columns
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
            logging.error("Failed to read Popular books file.")

        # Step 4: Extract headers for search.csv
        header = pd.DataFrame(columns=list(df.columns))  # Original headers from the CSV file

        if not populars:
            header.to_csv(file_path, index=False)
            logging.info("No popular books found. File not updated.")
            return

        # Step 5: Map found books to their `available_copies` and `loaned_copies`
        found_books = []
        for book in populars:
            # Find the corresponding row in the DataFrame for each book
            matching_row = df[
                (df["title"] == book.title) &
                (df["author"] == book.author) &
                (df["copies"] == book.copies) &
                (df["is_loaned"] == book.is_loaned) &
                (df["genre"] == book.genre) &
                (df["year"] == book.year)
                ]
            if not matching_row.empty:
                # Get `available_copies` and `loaned_copies`
                available_copies = matching_row["available_copies"].iloc[0]
                loaned_copies = matching_row["loaned_copies"].iloc[0]

                # Add these to the book's fields
                book_data = book.get_fields() + [available_copies, loaned_copies]
                found_books.append(book_data)

        df = pd.DataFrame(found_books)
        df.to_csv(file_path, index=False)
        logging.info("Popular books saved to CSV.")

    @staticmethod
    def add_book(book: Book):
        # Step 1: Read the existing CSV file
        try:
            df = pd.read_csv(FileManagement.books_path)
            logging.info("Books file read successfully.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist, create a new DataFrame with necessary columns
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
            logging.error("Failed to read books file.")

        # Step 2: Check if the book already exists (match by title and author)
        book_mask = (df["title"] == book.title) & (df["author"] == book.author)

        if book_mask.any():
            # Book exists: Update the `copies` and `available_copies`
            index = df[book_mask].index[0]
            df.at[index, "copies"] += book.copies
            if df.at[index, "is_loaned"] == "No":
                df.at[index, "available_copies"] += book.copies
            logging.info(f"Updated copies for '{book.title}' by {book.author}.")
        else:
            # Book does not exist: Add it as a new row
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

        # Step 3: Save the updated DataFrame back to the file
        df.to_csv(FileManagement.books_path, index=False)

    @staticmethod
    def remove_book(book: Book):
        try:
            df = pd.read_csv(FileManagement.books_path)
            logging.info("Books file read successfully.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies",
                                       "loaned_copies"])
            logging.error("Failed to read books file.")

        match = (df["title"] == book.title) & (df["author"] == book.author)

        if match.any():
            book_index = df[match].index[0]
            if df.at[book_index, "copies"] > 1:
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

        df.to_csv(FileManagement.books_path, index=False)

    @staticmethod
    def lend_book(book: Book):
        try:
            df = pd.read_csv(FileManagement.books_path)
            logging.info("Books file read successfully.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies",
                                       "loaned_copies"])
            logging.error("Failed to read books file.")

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

        df.to_csv(FileManagement.books_path, index=False)
        logging.info(f"Book '{book.title}' by {book.author} has been successfully loaned.")
        return True

    @staticmethod
    def ask_info(book: Book, info):
        if book not in FileManagement.waiting_list:
            FileManagement.waiting_list[book] = []
        FileManagement.waiting_list[book].append(info)

    @staticmethod
    def load_waiting_list():
        file_path = "Files/waiting_list.csv"
        try:
            # Try to load the CSV file
            df = pd.read_csv(file_path)
            logging.info(f"Waiting list file loaded successfully from {file_path}.")
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            # If the file does not exist or is empty, create an empty DataFrame
            df = pd.DataFrame(columns=["title", "name", "email"])
            logging.error(f"Failed to load waiting list from {file_path}. Error: {e}")

        # Process each book's waiting list (list of dictionaries)
        for title, entries in FileManagement.waiting_list.items():
            for entry in entries:
                new_row = {"title": title.title, "name": entry.get("name", ""), "email": entry.get("email", "")}

                # Check if the row already exists in the DataFrame
                if not ((df['title'] == new_row['title']) &
                        (df['name'] == new_row['name']) &
                        (df['email'] == new_row['email'])).any():
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    logging.info(f"Added new entry for '{new_row['title']}' in the waiting list.")

        # Save the updated DataFrame back to the CSV file
        try:
            df.to_csv(file_path, index=False)
            logging.info(f"Waiting list saved successfully to {file_path}.")
        except Exception as e:
            logging.error(f"Failed to save the waiting list to {file_path}. Error: {e}")

    @staticmethod
    def load_books_to_list():
        books = []
        try:
            # Attempt to load the books CSV file
            df = pd.read_csv(FileManagement.books_path)
            logging.info(f"Books file loaded successfully from {FileManagement.books_path}.")
        except FileNotFoundError:
            logging.error(f"Books file not found at {FileManagement.books_path}.")
            return books
        except pd.errors.EmptyDataError:
            logging.error(f"Books file at {FileManagement.books_path} is empty.")
            return books
        except KeyError as e:
            logging.error(f"Missing expected column in the books file: {e}")
            return books

        # Process each row in the DataFrame and create a list of Book objects
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

        # Log a summary of the loaded books
        logging.info(f"Successfully loaded {len(books)} books from the file.")
        return books

    @staticmethod
    def search_book(*search_strategies, **search_vals):
        try:
            # Step 1: Read the entire CSV file into a DataFrame
            df = pd.read_csv(FileManagement.books_path)
            logging.info(f"Books file loaded successfully from {FileManagement.books_path}.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist, create a new DataFrame with necessary columns
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies", "loaned_copies"])
            logging.error(f"Books file does not exist or is empty at {FileManagement.books_path}.")

        # Step 2: Load the books data into a list of Book objects
        data = FileManagement.load_books_to_list()
        logging.info(f"Loaded {len(data)} books into the search process.")

        # Step 3: Use Searcher to apply search strategies
        searcher = Searcher(*search_strategies)
        result = searcher.search(data, **search_vals)
        logging.info(f"Search completed with {len(result)} results.")

        # Step 4: Extract headers for search.csv
        header = list(df.columns)  # Original headers from the CSV file

        # Step 5: Map found books to their `available_copies` and `loaned_copies`
        found_books = []
        for book in result:
            # Find the corresponding row in the DataFrame for each book
            matching_row = df[
                (df["title"] == book.title) &
                (df["author"] == book.author) &
                (df["copies"] == book.copies) &
                (df["is_loaned"] == book.is_loaned) &
                (df["genre"] == book.genre) &
                (df["year"] == book.year)
                ]
            if not matching_row.empty:
                # Get `available_copies` and `loaned_copies`
                available_copies = matching_row["available_copies"].iloc[0]
                loaned_copies = matching_row["loaned_copies"].iloc[0]

                # Add these to the book's fields
                book_data = book.get_fields() + [available_copies, loaned_copies]
                found_books.append(book_data)

        # Step 6: Write the search results to search.csv
        with open("Files/search.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the headers
            writer.writerows(found_books)  # Write the found books' data
        logging.info(f"Search results written to 'Files/search.csv'. {len(found_books)} books found and saved.")

    @staticmethod
    def return_book(book: Book):
        try:
            df = pd.read_csv(FileManagement.books_path)
            logging.info("Books file read successfully.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies",
                                       "loaned_copies"])
            logging.error("Failed to read books file.")

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
        df.to_csv(FileManagement.books_path, index=False)
        logging.info(f"Book '{book.title}' by {book.author} has been successfully returned.")


if __name__ == '__main__':
    pass

