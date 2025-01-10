import tkinter as tk
from BookFactroy import BookFactory
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from FileManagement import FileManagement


class LibraryApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("500x500")
        self.factory = BookFactory()

        self.title_lable = tk.Label(root,text="Title:")
        self.title_lable.pack()
        self.title_entrty = tk.Entry(root)
        self.title_entrty.pack()


        self.author_lable = tk.Label(root,text="Author:")
        self.author_lable.pack()
        self.author_entrty = tk.Entry(root)
        self.author_entrty.pack()

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
        # Read the CSV file using pandas
        df = pd.read_csv(file_path)

        # Clear the treeview
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        # Set up the column headers
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Populate rows
        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=row.tolist())

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
        pass

    def search_book(self):
         pass


    def lend_book(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

