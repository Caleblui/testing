from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import random
import sqlite3
from functools import wraps



def sql():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    idlist = c.execute("SELECT * FROM users").fetchall()
    conn.commit()
    conn.close()
    print(idlist)

def sqlrun():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    idlist = c.execute("SELECT * FROM users WHERE id = 31").fetchall()
    conn.commit()
    conn.close()
    print(idlist)

def check_hash():
    print(generate_password_hash("hi"))

def regsql():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT  users (username, user_password, score) VALUES(?, ?, ?)", ("calebdev", "calebdev", 0))
    print("done")
    conn.commit()
    conn.close()

def deltable():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DROP TABLE users")
    print("done")
    conn.commit()
    conn.close()

def create():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''  
              CREATE TABLE users(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              user_password TEXT NOT NULL, 
              score REAL, 
              time REAL
              )''')
    print("done")
    conn.commit()
    conn.close()

def checklogin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DROP TABLE users")
    print("done")
    conn.commit()
    conn.close()


"""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE transaction_records (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id TEXT NOT NULL, symbol TEXT NOT NULL, shares REAL NOT NULL, price REAL NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id));"""

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def trial():
    username = "calebdev"
    password = "calebdev"

    # Query database for username
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    row = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
    conn.commit()
    conn.close()

    print(row)
    print(type(row))

    # Ensure username exists and password is correct
    if row != None and check_password_hash(row[0][2], password):
        print("ok")
    else:
        print("no ok")
    

'''
    if not check_password_hash(row[0]["user_password"], password):
        print("ok")
    else:
        print("no ok")
'''

if __name__ == "__main__":
    #sqlrun()
    #deltable()
    #create()
    sql()
    print("done")

'''The issue you are facing where the login is not successful could be due to several reasons in your code. Here are a few things to check and potentially correct:

Error Handling: Ensure that error handling is in place for database queries and password verification to prevent errors from breaking the login process.

Database Query: Double-check that the database query for the username is returning the expected results and handle cases where the username does not exist.

Password Verification: Verify that the password hashing and comparison logic is working correctly to ensure the password is being checked accurately.

Session Handling: Make sure the user session is being set correctly after a successful login and that the user_id is stored in the session.

Conditional Logic: Review the conditional logic for the username existence check and password verification to accurately handle these cases.

By addressing these aspects and ensuring that the database queries, password checks, and session handling are working as expected, you should be able to troubleshoot the login issue. Additionally, consider implementing logging or print statements to track the flow of the login process and identify any specific errors that may occur.'''
