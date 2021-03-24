import os
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash

app = Flask(__name__)
# app.config.from_object('config')


# HOME PAGE
@app.route("/")
def root():
    return render_template("index.html")



# CUSTOMER PAGES
@app.route("/customers")
def customers():
    return render_template("customers.html")


@app.route("/customers/add_customer", methods=['POST', 'GET'])
def add_customer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone']
        zip_code = request.form['zip_code']

        print(first_name, last_name, email, phone_number, zip_code)

        return 'added'
    else:
        abort(400)



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
