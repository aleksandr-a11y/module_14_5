import sqlite3
from tkinter import INSERT

connection = sqlite3.connect('prod_baza.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')


def get_all_products():
    product_list = cursor.execute("SELECT * FROM Products").fetchall()
    connection.commit()
    return product_list

def add_user(username, email, age):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?,?,?,?)",
                  (username, email, age, 1000))
    connection.commit()

def is_included(username):
    if cursor.execute("SELECT * From Users WHERE username=?", (username,)).fetchone() is None:
        connection.commit()
        return False
    else:
        connection.commit()
        return True
