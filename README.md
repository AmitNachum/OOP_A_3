# Library Management System

The Library Management System is a Python-based project designed to facilitate the management of books, users, and library operations. It provides a comprehensive GUI for easy interaction and supports backend operations like lending, returning, and searching for books.

## Features

1. **Book Management**

    - Add, remove, lend, and return books.
    - Maintain data for books such as title, author, genre, year, copies, and availability.
    - Track lending statistics for popular books.

2. **User Management**

    - Register and authenticate users with encrypted passwords.
    - Notify users with system updates and book availability.

3. **Search Functionality**

    - Search for books using multiple strategies (title, author, genre, etc.).
    - Write search results to a CSV file for future reference.

4. **Waiting List**

    - Allow users to join a waiting list for unavailable books.
    - Store user details for notifications when books are available.

5. **GUI Integration**

    - Built with `Tkinter` for an interactive user experience.
    - View and manage books, notifications, and user accounts.

6. **File Management**

    - Use CSV files for persistent storage of book and user data.
    - Handle file creation and updates dynamically.

7. **Unit Testing**

    - Comprehensive test coverage for core functionalities using `unittest`.

## File Structure

- `Book.py`:
  Defines the `Book` class to represent book data, including attributes and equality checks.

- `BookFactory.py`:
  Contains the `BookFactory` class to create `Book` objects with predefined parameters.

- `FileManagement.py`:
  Handles backend operations such as file reading, writing, user registration, notifications, and book management.

- `gui.py`:
  Implements the graphical user interface for the library system, integrating all core functionalities into a user-friendly design.

- `Iterators.py`:
  Defines iterator classes to traverse specific fields in book datasets (e.g., title, author, year).

- `SearchStrategy.py`:
  Provides an abstract `SearchStrategy` class and its implementations for flexible and dynamic searching of books.

- `User.py`:
  Defines the `User` class for user registration, authentication, and notifications.

- `unit_tests.py`:
  Includes unit tests for validating the correctness of file management, user notifications, and other critical functionalities.

## Prerequisites

- Python 3.x
- `Tkinter` (comes pre-installed with Python)
- `pandas` for handling CSV files

Install dependencies with:

```bash
pip install pandas
```

## How to Run

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Ensure the `Files` folder exists and contains:
    - `books.csv`: To store book data.
    - `users.csv`: To store user data.
    - `log.txt`: To store logs.
4. Run the application:

```bash
python gui.py
```

## Unit Testing

Run tests using:

```bash
python -m unittest unit_tests.py
```

## Contributors

Developed by Adi Wayn and Amit Nachum. Contributions and suggestions are welcome!

 
