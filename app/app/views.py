from flask import Flask, flash, redirect, render_template, request
from app import app
from random import randint

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/user/")
def hello():
    users = [ "Frank", "Steve", "Alice", "Bruce" ]
    return render_template('user.html', **locals())
