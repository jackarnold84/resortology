import os
import database as db
from flask import Flask, session, url_for, redirect, render_template, request, abort

app = Flask(__name__)
# app.config.from_object('config')


# HOME PAGE
@app.route("/")
def root():
    return render_template("index.html")



# CUSTOMER PAGES
@app.route("/customers")
def customers():

    customer_list = db.get_all_customers()

    return render_template("customers.html", customer_list=customer_list)


@app.route("/customers/add_customer", methods=['POST', 'GET'])
def add_customer():
    if request.method == 'POST':
        form = request.form
        db.add_customer(form['first_name'], form['last_name'],
                        form['email'], form['phone'], form['zip_code'])

        return 'added'
    else:
        abort(400)



if __name__ == "__main__":

    db.connect()
    db.build_tables(reset=True)

    app.run(debug=True, host="127.0.0.1", port=5000)
