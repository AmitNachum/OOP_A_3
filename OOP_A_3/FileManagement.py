import csv
from typing import List
from Book import Book

class FileManagement:

    @staticmethod
    def read_file(file_path: str) -> List:
        try:
            with open(file_path, 'r') as f:
                reader = list(csv.reader(f))
                return reader

        except FileNotFoundError:
            print(f"File {file_path} was not found.")
            return []

    @staticmethod
    def read_file2(file_path:str) -> List[Book]:
        books =[]
        try:
            with open(file_path , 'r') as f:
                reader = list(csv.reader(f))
                for line in reader:
                    new_book = Book(line[0],line[1],line[4],line[5],int(line[3]),line[2])
                    books.append(new_book)

        except FileNotFoundError:
            print(f"File {file_path} was not found")

        return books




    @staticmethod
    def add_book(book : Book, books_path: str):
        with open(books_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(book.get_fields())

        print("Data written to books.csv successfully")


    @staticmethod
    def remove_book(book : Book, books_path: str):

    # Step 1: Read all rows and filter out the book to be removed
        try:
             with open(books_path, 'r') as file:
                reader = csv.reader(file)
                rows = [row for row in reader if row != book.get_fields()]  # Keep rows not matching the book

            # Step 2: Write the filtered rows back to the file
             with open(books_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
             print("Book removed successfully from books.csv.")

        except FileNotFoundError:
            print(f"File {books_path} was not found.")

    @staticmethod
    def search_book(self):
        pass








