import tkinter as tk
from BookFactroy import BookFactory
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from FileManagement import FileManagement
from User import User
from SearchStrategy import *

class LoginWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app  # Reference to the parent LibraryApp instance
        self.title("Login Window")
        self.geometry("400x400")

        self.username_label = tk.Label(self, text="Enter Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Enter Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self)
        self.password_entry.pack()

        tk.Button(self, text="Sign Up", command=self.sign_up).pack(pady=5)
        tk.Button(self, text="Log In", command=self.log_in).pack(pady=5)


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
            # User found, retrieve the stored hashed password from the CSV
            stored_hashed_password = user_row.iloc[0]['password']

            # Verify the entered password by hashing it and comparing with the stored hash
            user = User(user_name, password)  # The entered password gets hashed here
            if user.password == stored_hashed_password:  # Compare the hashed password
                messagebox.showinfo("Success", f"Welcome {user_name}!")
                self.app.logged_in = True  # Mark the app as logged in
                self.app.setup_ui()  # Call setup_ui to initialize the main app
                self.destroy()  # Close the login window
                return True
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "User not found")


class LibraryApp:
    def __init__(self, root):
        self.logged_in = False  # Flag to track login status
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x800")

        # Show login window initially
        self.login_window = LoginWindow(self)
        self.root.wait_window(self.login_window)  # Wait for login window to close

        # Proceed with the rest of the app if logged in
        if self.logged_in:
            self.setup_ui()

    def setup_ui(self):
        # Check if UI has already been set up to avoid multiple setups
        if hasattr(self, 'tree'):
            return

        self.factory = BookFactory()

        self.title_lable = tk.Label(self.root, text="Title:")
        self.title_lable.pack()
        self.title_entrty = tk.Entry(self.root)
        self.title_entrty.pack()

        self.author_lable = tk.Label(self.root, text="Author:")
        self.author_lable.pack()
        self.author_entrty = tk.Entry(self.root)
        self.author_entrty.pack()

        self.is_loaned_lable = tk.Label(self.root, text="Is Loaned?:")
        self.is_loaned_lable.pack()
        self.is_loaned_entrty = tk.Entry(self.root)
        self.is_loaned_entrty.pack()

        self.copies_lable = tk.Label(self.root, text="Copies:")
        self.copies_lable.pack()
        self.copies_entrty = tk.Entry(self.root)
        self.copies_entrty.pack()

        self.genre_lable = tk.Label(self.root, text="Genre:")
        self.genre_lable.pack()
        self.genre_entrty = tk.Entry(self.root)
        self.genre_entrty.pack()

        self.year_lable = tk.Label(self.root, text="Year:")
        self.year_lable.pack()
        self.year_entrty = tk.Entry(self.root)
        self.year_entrty.pack()

        # Create a frame for the Treeview
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Add a Treeview widget
        self.tree = ttk.Treeview(frame)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        self.load_csv("Files/books.csv")

        try:
            pd.read_csv("Files/books_available.csv")
        except pd.errors.EmptyDataError:
            FileManagement.load_available_books()
            FileManagement.load_loaned_books()

        # Buttons for library operations
        tk.Button(self.root, text="Add Book", command=self.add_book).pack(pady=5)
        tk.Button(self.root, text="Remove Book", command=self.remove_book).pack(pady=5)
        tk.Button(self.root, text="Search Book", command=self.search_book).pack(pady=5)
        tk.Button(self.root, text="Lend Book", command=self.lend_book).pack(pady=5)
#        tk.Button(root , text="Return Book",command=self.return_book).pack(pady=5)
 #       tk.Button(root,text="Logout",command=self.logout).pack(pady=5)
  #      tk.Button(root,text="Login",command=self.login).pack(pady=5)
   #     tk.Button(root,text="Register",command=self.register).pack(pady=5)

        #Place Holder for Methods

    def load_csv(self, file_path):
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file_path)

            # Clear the Treeview
            self.tree.delete(*self.tree.get_children())

            # Set up Treeview columns and headings
            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"

            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="center")

            # Populate the Treeview with rows from the CSV
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=row.tolist())

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
        except pd.errors.EmptyDataError:
            messagebox.showinfo("Info", "The CSV file is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def add_book(self):
       title = self.title_entrty.get()
       author = self.author_entrty.get()
       genre = self.genre_entrty.get()
       year = self.year_entrty.get()

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
       FileManagement.add_book(book, "Files/books.csv")

       # Clear the current Treeview rows
       for item in self.tree.get_children():
           self.tree.delete(item)

       # Reload the CSV into the Treeview
       self.load_csv("Files/books.csv")

       # Success message
       messagebox.showinfo("Success", f"Added the Book {book}")

    def remove_book(self):
        title = self.title_entrty.get()
        author = self.author_entrty.get()
        genre = self.genre_entrty.get()
        year = self.year_entrty.get()

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
        FileManagement.remove_book(book, "Files/books.csv")

        # Clear the current Treeview rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reload the CSV into the Treeview
        self.load_csv("Files/books.csv")

        # Success message
        messagebox.showinfo("Success", f"Removed the Book {book}")

    def search_book(self):
        title = self.title_entrty.get()
        author = self.author_entrty.get()
        is_loaned = self.is_loaned_entrty.get()
        copies = self.copies_entrty.get()
        genre = self.genre_entrty.get()
        year = self.year_entrty.get()

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

    def lend_book(self):
        title = self.title_entrty.get()
        author = self.author_entrty.get()
        genre = self.genre_entrty.get()
        year = self.year_entrty.get()

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
        FileManagement.lend_book(book)

        # Success message
        messagebox.showinfo("Success", f"loaned the Book {book}")

if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

