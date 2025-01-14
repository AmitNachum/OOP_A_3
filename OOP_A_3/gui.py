import tkinter as tk
from BookFactroy import BookFactory
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from FileManagement import FileManagement
from SearchStrategy import *

class LoginWindow(tk.Toplevel):
    pass

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x800")
        self.factory = BookFactory()

        self.title_lable = tk.Label(root,text="Title:")
        self.title_lable.pack()
        self.title_entrty = tk.Entry(root)
        self.title_entrty.pack()

        self.author_lable = tk.Label(root,text="Author:")
        self.author_lable.pack()
        self.author_entrty = tk.Entry(root)
        self.author_entrty.pack()

        self.is_loaned_lable = tk.Label(root, text="Is Loaned?:")
        self.is_loaned_lable.pack()
        self.is_loaned_entrty = tk.Entry(root)
        self.is_loaned_entrty.pack()

        self.copies_lable = tk.Label(root, text="Copies:")
        self.copies_lable.pack()
        self.copies_entrty = tk.Entry(root)
        self.copies_entrty.pack()

        self.genre_lable = tk.Label(root, text="Genre:")
        self.genre_lable.pack()
        self.genre_entrty = tk.Entry(root)
        self.genre_entrty.pack()

        self.year_lable = tk.Label(root,text="Year:")
        self.year_lable.pack()
        self.year_entrty = tk.Entry(root)
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

        FileManagement.load_available_books()
        FileManagement.load_loaned_books()

        #Buttons
        tk.Button(root , text="Add Book",command=self.add_book).pack(pady=5)
        tk.Button(root , text="Remove Book",command=self.remove_book).pack(pady=5)
        tk.Button(root , text="Search Book",command=self.search_book).pack(pady=5)
        tk.Button(root , text="Lend Book",command=self.lend_book).pack(pady=5)
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

