from typing import List

from OOP_A_3.Book import Book


def open_file(file_path:str)->List[Book]:
    books = []

    with open(file_path, 'r') as f:
        for line in f.readlines()[1:]:
            split_line = line.split(',')
            new_book = Book(split_line[0],split_line[1],split_line[2],split_line[3],split_line[4],split_line[5])
            books.append(new_book)

    return books


books = open_file("Files/books.csv")

