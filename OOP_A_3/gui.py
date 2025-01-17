import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from FileManagement import FileManagement
from BookFactroy import BookFactory
from User import User
from SearchStrategy import *

class AskInfoWindow(tk.Toplevel):
    def __init__(self, parent, book, callback):
        super().__init__(parent)
        self.title("Enter User Information")
        self.geometry("300x200")
        self.configure(bg="#f7f7f7")  # Match the light gray background of the system
        self.book = book
        self.callback = callback  # A callback function to handle the info data

        # Title Label
        tk.Label(
            self,
            text="Enter User Information",
            font=("Arial", 16, "bold"),
            bg="#f7f7f7",
            fg="#333333"
        ).pack(pady=10)

        # Labels and Entry Fields
        form_frame = tk.Frame(self, bg="#f7f7f7")
        form_frame.pack(pady=5)

        tk.Label(
            form_frame,
            text="Name:",
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333333"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.name_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(
            form_frame,
            text="Email:",
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333333"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.email_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        # Submit Button
        tk.Button(
            self,
            text="Submit",
            command=self.submit_info,
            bg="#5d7f71",
            fg="black",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(pady=20)

    def submit_info(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name or not email:
            messagebox.showerror("Error", "Please fill in all fields", parent=self)
            return

        # Call the callback function with the entered info
        self.callback({"name": name, "email": email}, self.book)

        # Close the window
        self.destroy()

class LoginWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Login Window")
        self.geometry("400x400")
        self.configure(bg="#ececec")  # Light gray background

        tk.Label(self, text="Library Management Login", font=("Arial", 18, "bold"), bg="#ececec", fg="#333333").pack(pady=20)

        self.username_label = tk.Label(self, text="Enter Username:", bg="#ececec", fg="#333333")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Enter Password:", bg="#ececec", fg="#333333")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Register", command=self.sign_up, bg="#6d9e69", fg="black", font=("Arial", 10, "bold"), width=15).pack(pady=10)
        tk.Button(self, text="Login", command=self.log_in, bg="#5a7dab", fg="black", font=("Arial", 10, "bold"), width=15).pack(pady=5)

    def sign_up(self):
        user_name = self.username_entry.get()
        password = self.password_entry.get()
        user = User(user_name, password)

        if not FileManagement.sign_up_user(user):
            messagebox.showerror("Error", f"User {user.user_name} already signed up")
        else:
            messagebox.showinfo("Success", f"Signed up as {user.user_name}")

    def log_in(self):
        user_name = self.username_entry.get()
        password = self.password_entry.get()
        users = FileManagement.read_users()

        user_row = users[users['user_name'] == user_name]

        if not user_row.empty:
            stored_hashed_password = user_row.iloc[0]['password']

            user = User(user_name, password)
            if user.password == stored_hashed_password:
                messagebox.showinfo("Success", f"Welcome {user_name}!")
                self.app.logged_in = True
                self.app.setup_ui()
                self.destroy()
                return True
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "User not found")

class LibraryApp:
    def __init__(self, root):
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

        tk.Label(self.root, text="Library Management System", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333333").pack(pady=20)

        form_frame = tk.Frame(self.root, bg="#f7f7f7")
        form_frame.pack(pady=10)

        self.create_form(form_frame)

        button_frame = tk.Frame(self.root, bg="#f7f7f7")
        button_frame.pack(pady=20)

        self.create_buttons(button_frame)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.create_table(table_frame)
        self.load_csv("Files/books.csv")

    def create_form(self, frame):
        labels = ["Title", "Author", "Is Loaned?", "Copies", "Genre", "Year"]
        self.entries = {}

        # Create a frame for the form layout
        form_frame = tk.Frame(frame, bg="#f7f7f7")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Adjust layout for better fitting
        for i, label_text in enumerate(labels):
            # Add the label with the input field
            label = tk.Label(
                form_frame,
                text=label_text + ":",
                font=("Arial", 12),
                bg="#f7f7f7",
                fg="#333333",
                anchor="w"
            )
            label.grid(row=0, column=2 * i + 1, padx=(5, 2), pady=5, sticky="w")

            # Make the entry fields smaller and fit better
            entry = tk.Entry(form_frame, width=12, font=("Arial", 12))
            entry.grid(row=1, column=2 * i + 1, padx=(10, 15), pady=5, sticky="w")
            self.entries[label_text.lower().replace(" ", "_")] = entry

        # Adjust column weights to make sure everything scales well
        form_frame.grid_columnconfigure(0, weight=1, minsize=80)
        form_frame.grid_columnconfigure(1, weight=3, minsize=100)

    def create_buttons(self, frame):
        buttons = [
            ("Add Book", self.add_book, "#5d7f71"),
            ("Remove Book", self.remove_book, "#9b4a4a"),
            ("Search Book", self.search_book, "#b78b54"),
            ("View Books", self.view_books, "#5f88a8"),
            ("Lend Book", self.lend_book, "#5f88a8"),
            ("Return Book", self.return_book, "#5d8884"),
            ("Popular Books", self.view_populars, "#85725c")
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
                font=("Arial", 10, "bold"),
                width=15
            ).grid(row=row, column=col, padx=10, pady=5)

    def create_table(self, frame):
        self.tree = ttk.Treeview(frame)
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
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
            return

        book = self.factory.create_book(title, author, genre, year)
        FileManagement.add_book(book)

        self.load_csv("Files/books.csv")
        messagebox.showinfo("Success", f"Added the Book {book}")

    def remove_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()

        if not title or not author or not genre or not year:
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
            return

        book = self.factory.create_book(title, author, genre, year)
        FileManagement.remove_book(book)

        self.load_csv("Files/books.csv")
        messagebox.showinfo("Success", f"Removed the Book {book}")

    def search_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()
        is_loaned = self.entries["is_loaned?"].get()
        copies = self.entries["copies"].get()

        try:
            year = int(year) if year else None
            copies = int(copies) if copies else None
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year or copies number")
            return

        # Map inputs to corresponding search strategies and values
        strategies_and_values = [
            (SearchByTitle(), title) if title else None,
            (SearchByAuthor(), author) if author else None,
            (SearchByIsLoaned(), is_loaned) if is_loaned else None,
            (SearchByCopies(), copies) if copies is not None else None,
            (SearchByGenre(), genre) if genre else None,
            (SearchByYear(), year) if year is not None else None,
        ]

        # Filter out None values (i.e., unused strategies)
        active_strategies = list(filter(None, strategies_and_values))

        if not active_strategies:
            messagebox.showinfo("Info", "Please enter at least one search criteria")
            return

        strategies = (pair[0] for pair in active_strategies)
        search_vals = {strategy.__class__.__name__: value for strategy, value in active_strategies}

        FileManagement.search_book("Files/books.csv", *strategies, **search_vals)
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
            messagebox.showerror("Error", "Please enter all fields")
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
            # Success message
            messagebox.showinfo("Success", f"Loaned the Book {book}")

    @staticmethod
    def handle_info_submission(info, book):
        FileManagement.ask_info(book, info)
        messagebox.showinfo("Info", "Your details have been added to the waiting list.")

    def return_book(self):
        title = self.entries["title"].get()
        author = self.entries["author"].get()
        genre = self.entries["genre"].get()
        year = self.entries["year"].get()

        if not title or not author or not genre or not year:
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year")
            return

        # Create a book object and add it to the CSV
        book = self.factory.create_book(title, author, genre, year)
        FileManagement.return_book(book)

        # Reload the CSV into the Treeview
        self.load_csv("Files/books.csv")

        # Success message
        messagebox.showinfo("Success", f"Returned the Book {book}")

    def view_populars(self):
        FileManagement.load_populars_to_csv()
        # Reload the CSV into the Treeview
        self.load_csv("Files/popular_books.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

