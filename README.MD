
# PostgreSQL Database Connection

  

This code connects to a PostgreSQL database, gets data from four different tables, and displays them in dropdown menus using the customtkinter library.

  

## Requirements

- Python 3.10

- customtkinter library

- psycopg2 library

  

## Usage

1. Update the `host`, `user`, `password`, and `db_name` variables in the `config.py` file with your database credentials.

2. Run the code using `python main.py`.

  

## Features

- Connects to a PostgreSQL database using the `psycopg2` library.

- Gets data from four different tables: `fam`, `names`, `otch`, and `street`.

- Displays the data in dropdown menus using the `customtkinter` library.

- Can add information about a person to the database.

- Can search for a person in the database.

- Can show a list of all people in the database.

- Can delete a people from the database.

  

## Notes

- The `customtkinter` library is a custom, dark-themed tkinter library.

- The code uses a `try-except` block to handle any errors that may occur while connecting to the database.

- The `get_surnames`, `get_names`, `get_otchestva`, and `get_streets` functions are used to fetch data from the respective tables and return the data as lists.

- The dropdown menus are created using the `CTkComboBox` class from the `customtkinter` library.