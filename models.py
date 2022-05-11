import sqlite3 as sql

def insertUser(username, password, admin):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password,admin) VALUES (?,?,?)", (username, password, admin))
    con.commit()
    con.close()


def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT user_id, username, password, admin FROM users")
    users = cur.fetchall()
    con.close()
    return users


def retrieveUsersByName():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT user_id, username, password, admin FROM users")
    users = cur.fetchall()
    con.close()
    return users

def insertBook(title, author):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO books (title,author) VALUES (?,?)", (title, author))
    con.commit()
    con.close()


def retrieveBooks():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT title, author FROM books")
    books = cur.fetchall()
    con.close()
    return books

