import sqlite3 as lite

con = lite.connect(r'D:\capstone.db')

tblGame = \
    "CREATE TABLE IF NOT EXISTS " \
        "tblGame (" \
            "name TEXT, " \
            "link TEXT, " \
            "image TEXT, " \
            "developer TEXT, " \
            "genre TEXT, " \
            "rating TEXT, " \
            "rlsDate TEXT, " \
            "summary TEXT" \
        ")"
tblMovie = \
    "CREATE TABLE IF NOT EXISTS " \
        "tblMovie (" \
            "name TEXT, " \
            "date TEXT, " \
            "link TEXT, " \
            "image TEXT, " \
            "genre TEXT, " \
            "rlsDate TEXT, " \
            "runtime INT, " \
            "director TEXT, " \
            "summary TEXT, " \
            "rating TEXT" \
        ")"
tblTVShow = \
    "CREATE TABLE IF NOT EXISTS " \
        "tblTVShow (" \
            "name TEXT, " \
            "date TEXT, " \
            "link TEXT, " \
            "image TEXT, " \
            "genre TEXT, " \
            "rlsDate TEXT, " \
            "runtime INT, " \
            "creator TEXT, " \
            "summary TEXT" \
        ")"
tblReview = \
    "CREATE TABLE IF NOT EXISTS " \
        "tblReview (" \
            "gameID INT, " \
            "movieID INT, " \
            "tvShowID INT, " \
            "author TEXT, " \
            "publication TEXT, " \
            "text TEXT, " \
            "score INT, " \
            "date TEXT, " \
            "thumbsUp INT, " \
            "thumbsDown INT, " \
            "reviewType TEXT" \
    ")"

with con:
    cur = con.cursor()
    cur.execute(tblGame)
    cur.execute(tblMovie)
    cur.execute(tblTVShow)
    cur.execute(tblReview)