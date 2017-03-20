from flask import Flask, flash, redirect, render_template, request
from app import app
from random import randint
import sqlite3 as lite

@app.route("/")
def index():
    con = lite.connect('D:/capstone-v2.db')
    cur = con.cursor()

    rows = cur.execute('SELECT DISTINCT developer FROM tblGame ORDER BY developer ASC;')
    devs = []
    [devs.append({
        'developer': row[0]
    }) for row in rows
    ]

    rows = cur.execute('SELECT name, link, developer FROM tblGame LIMIT 20')
    games = []
    [games.append({
        'name': row[0],
        'link': row[1],
        'developer': row[2]
    }) for row in rows
    ]

    return render_template('index.html', games=games, devs=devs)

@app.route("/user/")
def hello():
    users = [ "Frank", "Steve", "Alice", "Bruce" ]
    return render_template('user.html', **locals())
