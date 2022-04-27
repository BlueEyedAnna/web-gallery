from flask import Flask, render_template
import datetime
from app import app


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",
                           ver=datetime.datetime.now().timestamp())


@app.route("/exhibitions")
def exhibitions():
    return render_template("exhibitions.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("registration.html")


@app.route("/excursions")
def excursions():
    return render_template("excursions.html")


if __name__ == '__main__':
    app.run(debug=True)
