import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
import os
from FileManagement import FileManagement
from User import User
from Book import Book


class TestFileManagement(unittest.TestCase):
    @patch("pandas.read_csv")
    def test_get_user_notifications(self, mock_read_csv):
        # This test verifies if user notifications are correctly fetched from the mock data.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'user_name': ['test_user'],
            'password': ['test_password'],
            'notifications': ["{'admin': ['Welcome to the system']}"]
        })
        mock_read_csv.return_value = mock_data

        notifications = FileManagement.get_user_notifications("test_user")
        self.assertEqual(notifications, {'admin': ['Welcome to the system']})

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_sign_up_user(self, mock_to_csv, mock_read_csv):
        # This test ensures that new users are added to the mock data and that the DataFrame reflects this addition.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'user_name': ['existing_user'],
            'password': ['password123']
        })
        mock_read_csv.return_value = mock_data

        def to_csv_side_effect(path, index):
            nonlocal mock_data
            new_user = pd.DataFrame([{
                'user_name': 'new_user',
                'password': 'password123'
            }])
            mock_data = pd.concat([mock_data, new_user], ignore_index=True)

        mock_to_csv.side_effect = to_csv_side_effect

        new_user = User("new_user", "password123")
        result = FileManagement.sign_up_user(new_user)
        self.assertTrue(result)

        # Check that the user was added to the DataFrame
        self.assertIn("new_user", mock_data["user_name"].values)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_add_book(self, mock_to_csv, mock_read_csv):
        # This test checks if a new book is added to the mock dataset and ensures data integrity.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'title': ['Book1'],
            'author': ['Author1'],
            'copies': [5],
            'available_copies': [5],
            'is_loaned': ['No']
        })
        mock_read_csv.return_value = mock_data

        def to_csv_side_effect(path, index):
            nonlocal mock_data
            new_book = pd.DataFrame([{
                'title': 'Book2',
                'author': 'Author2',
                'copies': 3,
                'available_copies': 3,
                'is_loaned': 'No'
            }])
            mock_data = pd.concat([mock_data, new_book], ignore_index=True)

        mock_to_csv.side_effect = to_csv_side_effect

        book = Book(title="Book2", author="Author2", genre="Fiction", year=2023, copies=3, is_loaned="No")
        FileManagement.add_book(book)

        # Check if the book was added to the DataFrame
        self.assertIn("Book2", mock_data["title"].values)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_remove_book(self, mock_to_csv, mock_read_csv):
        # This test verifies the behavior of the function when removing a book and adjusting copies.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'title': ['Book1'],
            'author': ['Author1'],
            'copies': [2],
            'available_copies': [2],
            'is_loaned': ['No']
        })
        mock_read_csv.return_value = mock_data

        book = Book(title="Book1", author="Author1", genre="Fiction", year=2023, copies=1, is_loaned="No")
        result = FileManagement.remove_book(book)

        self.assertTrue(result)
        self.assertEqual(mock_data.loc[0, 'copies'], 1)
        self.assertEqual(mock_data.loc[0, 'available_copies'], 1)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_return_book(self, mock_to_csv, mock_read_csv):
        # This test checks if returning a book updates the available and loaned copies correctly.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'title': ['Book1'],
            'author': ['Author1'],
            'copies': [5],
            'available_copies': [2],
            'loaned_copies': [3],
            'is_loaned': ['No']
        })
        mock_read_csv.return_value = mock_data

        book = Book(title="Book1", author="Author1", genre="Fiction", year=2023, copies=1, is_loaned="No")
        result = FileManagement.return_book(book)

        self.assertTrue(result)
        self.assertEqual(mock_data.loc[0, 'available_copies'], 3)
        self.assertEqual(mock_data.loc[0, 'loaned_copies'], 2)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_lend_book(self, mock_to_csv, mock_read_csv):
        # This test validates that lending a book updates the relevant fields in the dataset correctly.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'title': ['Book1'],
            'author': ['Author1'],
            'copies': [5],
            'available_copies': [2],
            'loaned_copies': [3],
            'is_loaned': ['No'],
            'lend_count': [5]
        })
        mock_read_csv.return_value = mock_data

        book = Book(title="Book1", author="Author1", genre="Fiction", year=2023, copies=1, is_loaned="No")
        result = FileManagement.lend_book(book)

        self.assertTrue(result)
        self.assertEqual(mock_data.loc[0, 'available_copies'], 1)
        self.assertEqual(mock_data.loc[0, 'loaned_copies'], 4)
        self.assertEqual(mock_data.loc[0, 'lend_count'], 6)

    @patch("pandas.read_csv")
    def test_get_popular_books(self, mock_read_csv):
        # This test ensures that the function retrieves popular books based on lend counts from the mock data.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'title': ['Book1', 'Book2'],
            'author': ['Author1', 'Author2'],
            'lend_count': [10, 5],
            'genre': ['Fiction', 'Science'],
            'copies': [10, 8],
            'is_loaned': ['No', 'No'],
            'available_copies': [7, 6],
            'loaned_copies': [3, 2],
            'year': [2020, 2018]
        })
        mock_read_csv.return_value = mock_data

        popular_books = FileManagement.get_popular_books()
        self.assertEqual(len(popular_books), 2)  # Assert two books are retrieved

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_write_message(self, mock_to_csv, mock_read_csv):
        # This test checks whether notifications for a user are correctly written to the dataset.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'user_name': ['test_user'],
            'password': ['password'],
            'notifications': [{}]
        })
        mock_read_csv.return_value = mock_data

        def to_csv_side_effect(path, index):
            nonlocal mock_data
            mock_data.loc[0, 'notifications'] = "{'admin': ['Test message']}"

        mock_to_csv.side_effect = to_csv_side_effect

        user = User("test_user", "password")
        user.notifications = {'admin': ['Test message']}
        FileManagement.write_message(user)

        self.assertEqual(mock_data.loc[0, 'notifications'], "{'admin': ['Test message']}")

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_search_book(self, mock_to_csv, mock_read_csv):
        # This test ensures the search functionality works and that results are written to the correct file.
        # Mocking the data returned by pandas.read_csv
        mock_data = pd.DataFrame({
            'title': ['Book1', 'Book2'],
            'author': ['Author1', 'Author2'],
            'genre': ['Fiction', 'Science'],
            'year': [2020, 2018],
            'is_loaned': ['No', 'No'],
            'copies': [10, 8],
            'available_copies': [7, 6],
            'loaned_copies': [3, 2],
            'lend_count': [5, 2]
        })
        mock_read_csv.return_value = mock_data

        class MockSearchStrategy:
            def search(self, books, **kwargs):
                return [(Book("Book1", "Author1", "Fiction", 2020, 10, "No"), {})]

        search_file_path = "Files/search.csv"

        with patch("builtins.open", mock_open()) as mocked_file:
            FileManagement.search_book(MockSearchStrategy())
            # Check if the search results were written to the correct file
            mocked_file.assert_called_with(search_file_path, 'w', newline='')

    @patch("pandas.read_csv")
    def test_ask_info(self, mock_read_csv):
        # This test validates if the function properly updates the waiting list with user details.
        FileManagement.waiting_list = {}
        book = Book(title="Book1", author="Author1", genre="Fiction", year=2023, copies=1, is_loaned="No")
        FileManagement.ask_info(book, {"name": "Test User", "email": "test@example.com"})

        self.assertIn(book, FileManagement.waiting_list)
        self.assertEqual(FileManagement.waiting_list[book], [{"name": "Test User", "email": "test@example.com"}])


if __name__ == "__main__":
    unittest.main()
