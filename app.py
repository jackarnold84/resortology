import os
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash

app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def root():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
    
