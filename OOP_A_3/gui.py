import tkinter as tk
from math import expm1
from tkinter import messagebox
import Book
import BookFactroy


class LibraryApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("500x500")
        self.factory = BookFactroy


        self.title_lable = tk.Label(root,text="Title:")
        self.title_lable.pack()
        self.title_entrty = tk.Entry(root)
        self.title_entrty.pack()


        self.author_lable = tk.Label(root,text="Author:")
        self.author_lable.pack()
        self.author_entrty = tk.Entry(root)
        self.author_entrty.pack()


        self.year_lable = tk.Label(root,text="Year:")
        self.year_lable.pack()
        self.year_entrty = tk.Entry(root)
        self.year_entrty.pack()




        #Buttons
        tk.Button(root , text="Add Book",command=self.add_book).pack(pady=5)
        tk.Button(root , text="Remove Book",command=self.remove_book).pack(pady=5)
        tk.Button(root , text="Search Book",command=self.search_book).pack(pady=5)
        tk.Button(root , text="View Book",command=self.view_books).pack(pady=5)
        tk.Button(root , text="Lend Book",command=self.lend_book).pack(pady=5)
#        tk.Button(root , text="Return Book",command=self.return_book).pack(pady=5)
 #       tk.Button(root,text="Logout",command=self.logout).pack(pady=5)
  #      tk.Button(root,text="Login",command=self.login).pack(pady=5)
   #     tk.Button(root,text="Register",command=self.register).pack(pady=5)

        #Place Holder for Methods

    def add_book(self):
       title = self.title_entrty.get()
       author = self.author_entrty.get()
       year = self.year_entrty.get()

       if not title or not author or not year:
           messagebox.showerror("Error","Please enter all fields")
           return

       try:
           year = int(year)
       except ValueError:
           messagebox.showerror("Error","Please enter a valid year")
           return

       book = self.factory.create_book(title, author, year)
       messagebox.showinfo("Success",f"Added the Book {book}")


    def remove_book(self):
        title = self.title_entrty.get()
        author = self.author_entrty.get()
        year = self.year_entrty.get()

        if not title or not author or not year:
            messagebox.showerror("Error","Please enter all fields")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error","Please enter a valid year")
            return

        book = self.factory.delete_book(title, author, year)
        if book in self.factory.get_table():
            self.factory.delete_book(title, author, year)
            messagebox.showinfo("Success",f"Removed the Book {book}")

        else:
            messagebox.showerror("Error","Book not found")
            return


    def search_book(self):
         title = self.title_entrty.get()
         author = self.author_entrty.get()
         year = self.year_entrty.get()

         if not title or not author or not year:
             messagebox.showerror("Error","Please enter all fields")

         books = self.factory.get_table()
         matching_books = []
         for book in books:
             if (title and title.lower() in book.title.lower()) or (author and author.lower() in book.author.lower()) or (year and year.lower() in book.year.lower()):
                 matching_books.append(str(book))

         if matching_books:
            result_message = "\n".join(matching_books)
            messagebox.showinfo("Search Results",result_message)
         else:
             messagebox.showerror("Search Results","Book not found")


    def view_books(self):
        books = self.factory.get_books()
        if not books:
            messagebox.showerror("Library","No books found")
        else:
            book_list = "\n".join([str(books) for books in books])
            messagebox.showinfo("Library Books",book_list)

    def lend_book(self):

        title = self.title_entrty.get()
        author = self.author_entrty.get()
        year = self.year_entrty.get()

        if not title or not author or not year:
            messagebox.showerror("Error","Please enter all fields")

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error","Please enter a valid year")
            return

        if book not in self.factory.get_table():
            messagebox.showerror("Error","Book not found")
            return

        count = self.factory.get_count(book)
        if count == 0:
            messagebox.showerror("Library",f"No available copies of {book}")
            return

        self.factory.get_table()[book] -= 1
        messagebox.showinfo("Success",f"Successfully borrowed the Book {book}")









if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

