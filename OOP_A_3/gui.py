import logging
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from FileManagement import FileManagement
from BookFactroy import BookFactory
from User import User
from SearchStrategy import *

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("Files/log.txt"),
        logging.StreamHandler()
    ]
)

class AskInfoWindow(tk.Toplevel):
    def __init__(self, parent, book, callback):
        super().__init__(parent)
        self.title("Enter User Information")
        self.geometry("300x250")
        self.configure(bg="#f7f7f7")

        self.book = book
        self.callback = callback

        # Title Label with improved font size
        tk.Label(
            self,
            text="Enter User Information",
            font=("Arial", 16, "bold"),
            bg="#f7f7f7",
            fg="#333333"
        ).pack(pady=10)

        # Form Frame
        form_frame = tk.Frame(self, bg="#f7f7f7")
        form_frame.pack(pady=5)

        # User Info Labels and Entries
        tk.Label(
            form_frame,
            text="Name:",
            font=("Arial", 14),
            bg="#f7f7f7",
            fg="#333333"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(form_frame, font=("Arial", 14), width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(
            form_frame,
            text="Email:",
            font=("Arial", 14),
            bg="#f7f7f7",
            fg="#333333"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(form_frame, font=("Arial", 14), width=25)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        # Set focus to the first entry
        self.name_entry.focus()

        # Submit Button
        tk.Button(
            self,
            text="Submit",
            command=self.submit_info,
            bg="#5d7f71",
            fg="black",
            font=("Arial", 14, "bold"),
            width=15
        ).pack(pady=20)

    def submit_info(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name or not email:
            messagebox.showerror("Error", "Please fill in all fields", parent=self)
            return

        self.callback({"name": name, "email": email}, self.book)
        self.destroy()

class LoginWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Login Window")
        self.geometry("400x400")
        self.configure(bg="#ececec")

        # Title Label
        tk.Label(self, text="Library Management Login", font=("Arial", 18, "bold"), bg="#ececec", fg="#333333").pack(pady=20)

        # Username and Password Entry Fields
        self.username_label = tk.Label(self, text="Enter Username:", bg="#ececec", fg="#333333", font=("Ariel", 14))
        self.username_label.pack()
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Enter Password:", bg="#ececec", fg="#333333", font=("Ariel", 14))
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        # Buttons
        tk.Button(self, text="Register", command=self.sign_up, bg="#6d9e69", fg="black", font=("Arial", 14, "bold"), width=15).pack(pady=10)
        tk.Button(self, text="Login", command=self.log_in, bg="#5a7dab", fg="black", font=("Arial", 14, "bold"), width=15).pack(pady=5)


    def sign_up(self):
        user_name = self.username_entry.get()
        password = self.password_entry.get()

        if not user_name or not password:
            messagebox.showerror("Error", "Both username and password are required!")
            return

        user = User(user_name, password)
        if not FileManagement.sign_up_user(user):
            messagebox.showerror("Error", f"User {user.user_name} already signed up")
        else:
            messagebox.showinfo("Success", f"Signed up as {user.user_name}")

    def log_in(self):
        user_name = self.username_entry.get()
        password = self.password_entry.get()

        if not user_name or not password:
            messagebox.showerror("Error", "Both username and password are required!")
            return

        users = FileManagement.read_users()
        user_row = users[users['user_name'] == user_name]

        if not user_row.empty:
            stored_hashed_password = user_row.iloc[0]['password']
            user = User(user_name, password)
            if user.password == stored_hashed_password:
                messagebox.showinfo("Success", f"Welcome {user_name}!")
                logging.info("logged in successfully")
                self.app.logged_in = True
                self.app.logged_in_user = user_name
                self.app.setup_ui()
                self.destroy()
                return True
            else:
                messagebox.showerror("Error", "Incorrect password")
                logging.error("login failed, Incorrect password")
        else:
            messagebox.showerror("Error", "User not found")
            logging.warning("login failed, User not found")

class LibraryApp:
    def __init__(self, root):
        self.logged_in_user = None
        self.logged_in = False
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f7f7f7")  # Light gray background

        self.login_window = LoginWindow(self)
        self.root.wait_window(self.login_window)

        if self.logged_in:
            self.setup_ui()

    def setup_ui(self):
        if hasattr(self, 'tree'):
            return

        self.factory = BookFactory()

        # Top Frame for the Title and Logout Button
        top_frame = tk.Frame(self.root, bg="#f7f7f7")
        top_frame.pack(fill=tk.X, pady=(0, 20))

        # Title Label
        tk.Label(
            top_frame,
            text="Library Management System",
            font=("Arial", 24, "bold"),
            bg="#f7f7f7",
            fg="#333333"
        ).pack(padx=20)

        # Logged-in User Label
        if hasattr(self, 'logged_in_user') and self.logged_in_user:
            tk.Label(
                top_frame,
                text=f"Logged in as: {self.logged_in_user}",
                font=("Arial", 16, "bold"),
                bg="#f7f7f7",
                fg="#333333"
            ).pack(padx=20, side=tk.LEFT)

        # Notifications Button
        tk.Button(
            top_frame,
            text="View Notifications",
            command=self.view_notifications,
            bg="#ffc107",
            fg="black",
            font=("Arial", 14, "bold"),
            width=15
        ).pack(side=tk.RIGHT, padx=10)

        # Logout Button
        tk.Button(
            top_frame,
            text="Logout",
            command=self.logout,
            bg="#ff0000",
            fg="black",
            font=("Arial", 14, "bold"),
            width=10
        ).pack(side=tk.RIGHT, padx=20)

        # Main UI Elements
        form_frame = tk.Frame(self.root, bg="#f7f7f7")
        form_frame.pack(pady=10)

        self.create_form(form_frame)

        button_frame = tk.Frame(self.root, bg="#f7f7f7")
        button_frame.pack(pady=20)

        self.create_buttons(button_frame)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.create_table(table_frame)

        self.users = FileManagement.load_users_to_list()
        self.load_notifications()

        FileManagement.load_populars_to_csv()
        FileManagement.load_waiting_list()
        self.load_csv("Files/books.csv")

    def create_form(self, frame):
        labels = ["Title", "Author", "Is Loaned?", "Copies", "Genre", "Year", "Available Copies", "Loaned Copies", "Lend Count"]
        self.entries = {}

        # Create a frame for the form layout
        form_frame = tk.Frame(frame, bg="#f7f7f7")
        form_frame.grid(row=0, column=0, padx=15, pady=10, sticky="w")  # Increase outer padding further

        # Adjust layout for better fitting with two rows per label-entry pair
        for i, label_text in enumerate(labels):
            row = i // 5  # Split into two rows: one for labels, one for entries
            col = i % 5  # 5 columns per row

            # Add the label
            label = tk.Label(
                form_frame,
                text=label_text + ":",
                font=("Arial", 14),
                bg="#f7f7f7",
                fg="#333333",
                anchor="w"
            )
            label.grid(row=row * 2, column=col, padx=(15, 5), pady=5, sticky="w")  # More space before entry

            # Make the entry fields even wider
            entry = tk.Entry(form_frame, width=16, font=("Arial", 14))  # Increase width more for better fitting
            entry.grid(row=row * 2 + 1, column=col, padx=(5, 15), pady=5, sticky="w")  # Increase space after entry
            self.entries[label_text.lower().replace(" ", "_")] = entry

        # Adjust column weights to make sure everything scales well
        for i in range(5):  # Max of 5 columns in each row
            form_frame.grid_columnconfigure(i, weight=1, minsize=120)  # Increase column width for more space

        # Adjust row configuration for two rows of fields with more vertical spacing
        for i in range(2 * len(labels) // 5):  # Number of label-entry rows
            form_frame.grid_rowconfigure(i, weight=1, minsize=50)  # Increase vertical spacing between rows

    def create_buttons(self, frame):
        buttons = [
            ("Add Book", self.add_book, "#5d7f71"),
            ("Remove Book", self.remove_book, "#9b4a4a"),
            ("Search Book", self.search_book, "#b78b54"),
            ("View Books", self.view_books, "#5f88a8"),
            ("Lend Book", self.lend_book, "#5f88a8"),
            ("Return Book", self.return_book, "#5d8884"),
            ("Popular Books", self.view_populars, "#85725c"),
            ("Waiting List", self.view_waiting_list, "#85725c")
        ]

        # Set the maximum number of buttons per row
        max_columns = 4
        for i, (text, command, color) in enumerate(buttons):
            row = i // max_columns
            col = i % max_columns
            tk.Button(
                frame,
                text=text,
                command=command,
                bg=color,
                fg="black",
                font=("Arial", 14, "bold"),
                width=15
            ).grid(row=row, column=col, padx=10, pady=5)

    def create_table(self, frame):
        self.tree = ttk.Treeview(frame, show="headings", selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

    def load_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            self.tree.delete(*self.tree.get_children())

            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"

            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="center")

            for _, row in df.iterrows():
                self.tree.insert("", "end", values=row.tolist())

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
        except pd.errors.EmptyDataError:
            messagebox.showinfo("Info", "The CSV file is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def add_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()

        if not title or not author or not genre or not year:
            messagebox.showerror("Error", "Please enter all fields:\n title\n author \n genre\n year")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
            return

        book = self.factory.create_book(title, author, genre, year)
        FileManagement.add_book(book)

        self.notify(f"Added the Book {book.title}")

        self.load_csv("Files/books.csv")
        messagebox.showinfo("Success", f"Added the Book {book.title}")

    def remove_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()

        if not title or not author or not genre or not year:
            messagebox.showerror("Error", "Please enter all fields:\n title\n author \n genre\n year")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
            return

        book = self.factory.create_book(title, author, genre, year)
        success = FileManagement.remove_book(book)
        if not success:
            messagebox.showinfo("Error", f"Cannot remove the Book {book.title}")

        self.load_csv("Files/books.csv")
        if success:
            self.notify(f"Removed the Book {book.title}")
            messagebox.showinfo("Success", f"Removed the Book {book.title}")

    def search_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()
        is_loaned = self.entries["is_loaned?"].get()
        copies = self.entries["copies"].get()
        available_copies = self.entries["available_copies"].get()
        loaned_copies = self.entries["loaned_copies"].get()
        lend_count = self.entries["lend_count"].get()


        try:
            year = int(year) if year else None
            copies = int(copies) if copies else None
            available_copies = int(available_copies) if available_copies else None
            loaned_copies = int(loaned_copies) if loaned_copies else None
            lend_count = int(lend_count) if lend_count else None
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        # Map inputs to corresponding search strategies and values
        strategies_and_values = [
            (SearchByTitle(), title) if title else None,
            (SearchByAuthor(), author) if author else None,
            (SearchByIsLoaned(), is_loaned) if is_loaned else None,
            (SearchByCopies(), copies) if copies is not None else None,
            (SearchByGenre(), genre) if genre else None,
            (SearchByYear(), year) if year is not None else None,
            (SearchByAvailableCopies(), available_copies) if available_copies is not None else None,
            (SearchByLoanedCopies(), loaned_copies) if loaned_copies is not None else None,
            (SearchByLendCount(), lend_count) if lend_count is not None else None
        ]

        # Filter out None values (i.e., unused strategies)
        active_strategies = list(filter(None, strategies_and_values))

        if not active_strategies:
            messagebox.showinfo("Info", "Please enter at least one search criteria:\n title \n author \n genre\n year\n is loaned?\n copies\n"
                                        "available copies\n loaned_copies\n lend count")
            return

        strategies = (pair[0] for pair in active_strategies)
        search_vals = {strategy.__class__.__name__: value for strategy, value in active_strategies}

        FileManagement.search_book(*strategies, **search_vals)
        self.load_csv("Files/search.csv")

    def view_books(self):
        # Reload the CSV into the Treeview
        self.load_csv("Files/books.csv")

    def lend_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()

        if not title or not author or not genre or not year:
            messagebox.showerror("Error", "Please enter all fields:\n title\n author \n genre\n year")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
            return

        # Create a book object and try to lend it
        book = self.factory.create_book(title, author, genre, year)
        success = FileManagement.lend_book(book)

        if not success:
            # Show the AskInfoWindow to collect user info
            AskInfoWindow(self.root, book, self.handle_info_submission)

        # Reload the CSV into the Treeview
        self.load_csv("Files/books.csv")

        if success:
            self.notify(f"Loaned the Book {book.title}")
            # Success message
            messagebox.showinfo("Success", f"Loaned the Book {book.title}")

    def handle_info_submission(self, info, book):
        FileManagement.ask_info(book, info)
        name = info.get("name")
        self.notify(f"Added {name} to the Book {book.title} waiting list")

        messagebox.showinfo("Info", "Your details have been added to the waiting list.")

    def return_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()

        if not title or not author or not genre or not year:
            messagebox.showerror("Error", "Please enter all fields:\n title\n author \n genre\n year")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
            return

        # Create a book object and add it to the CSV
        book = self.factory.create_book(title, author, genre, year)
        success = FileManagement.return_book(book)
        if not success:
            messagebox.showinfo("Error", f"Cannot return the Book {book.title}")

        # Reload the CSV into the Treeview
        self.load_csv("Files/books.csv")
        if success:
            self.notify(f"Returned the Book {book.title}")
            # Success message
            messagebox.showinfo("Success", f"Returned the Book {book.title}")

    def view_populars(self):
        FileManagement.load_populars_to_csv()
        # Reload the CSV into the Treeview
        self.load_csv("Files/popular_books.csv")

    def logout(self):
        self.logged_in = False

        # Clear the main window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reset any attributes that might interfere with reinitialization
        if hasattr(self, 'tree'):
            del self.tree

        logging.info("log out successful")

        # Show the login window again
        self.login_window = LoginWindow(self)
        self.root.wait_window(self.login_window)

        if self.logged_in:
            self.setup_ui()

    def notify(self, message):
        user_names = [user.user_name for user in self.users]
        for user in self.users:
            if user.user_name in user_names and user.user_name != self.logged_in_user:
                user.update(self.logged_in_user,message)
                FileManagement.write_message(user)

    def view_waiting_list(self):
        FileManagement.load_waiting_list()
        # Reload the CSV into the Treeview
        self.load_csv("Files/waiting_list.csv")

    def load_notifications(self):
        for user in self.users:
            user.notifications = FileManagement.get_user_notifications(user.user_name)

    def view_notifications(self):
        """Open a window to display notifications."""
        if not hasattr(self, 'logged_in_user') or not self.logged_in_user:
            messagebox.showerror("Error", "No user is logged in!")
            return

        # Example: Retrieve notifications for the user
        user_notifications = FileManagement.get_user_notifications(self.logged_in_user)

        if not user_notifications:
            messagebox.showinfo("Notifications", "You have no notifications.")
            return

        # Create a new window for notifications
        notif_window = tk.Toplevel(self.root)
        notif_window.title("Notifications")
        notif_window.geometry("400x300")
        notif_window.configure(bg="#f7f7f7")

        tk.Label(
            notif_window,
            text="Your Notifications",
            font=("Arial", 18, "bold"),
            bg="#f7f7f7",
            fg="#333333"
        ).pack(pady=10)

        # Listbox for notifications
        notif_list = tk.Listbox(notif_window, font=("Arial", 14), width=50, height=10)
        notif_list.pack(pady=10, padx=10)

        # Populate the listbox with sender and messages
        for sender, messages in user_notifications.items():
            notif_list.insert(tk.END, f"{sender}:")  # Display the sender
            for message in messages:
                notif_list.insert(tk.END, f"  - {message}")  # Display each message with indentation

        # Close button
        tk.Button(
            notif_window,
            text="Close",
            command=notif_window.destroy,
            bg="#ff0000",
            fg="black",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

