import os
import database as db
from flask import Flask, session, url_for, redirect, render_template, request, abort
from datetime import datetime

app = Flask(__name__)
# app.config.from_object('config')


# 400 − for Bad Request			401 − for Unauthenticated
# 403 − for Forbidden			404 − for Not Found
# 406 − for Not Acceptable		415 − for Unsupported Media Type
# 429 − Too Many Requests



# HOME PAGE
@app.route("/")
def root():
    return render_template("index.html")


# =====================
# CUSTOMER PAGES
# =====================

@app.route("/customers")
def customers(tab="add"):
    customer_table = db.get_customers_table()
    return render_template("customers.html", tab=tab,
                           customer_table=customer_table)


@app.route("/customers/add_customer", methods=['POST', 'GET'])
def add_customer():
    if request.method == 'POST':
        form = request.form
        db.add_customer(form['first_name'], form['last_name'],
                        form['email'], form['phone'], form['zip_code'])
        return customers("add")
    else:
        return customers("add")


@app.route("/customers/delete_customer", methods=['POST', 'GET'])
def delete_customer():
    if request.method == 'POST':
        id = request.form['customer_id']
        db.delete_customer(id)
        return customers("delete")
    else:
        return customers("delete")


@app.route("/customers/edit_customer", methods=['POST', 'GET'])
def edit_customer():
    if request.method == 'POST':
        id = request.form['customer_id']
        c_info = db.get_customer_info(id)
        if (c_info is None):
            abort(404)
        else:
            return render_template("edit_customer.html", c=c_info)
    else:
        return customers("edit")


@app.route("/customers/edit_customer/edit", methods=['POST', 'GET'])
def edit_customer_process():
    if request.method == 'POST':
        form = request.form
        db.edit_customer(form['customer_id'], form['first_name'],
                         form['last_name'], form['email'], form['phone'],
                         form['zip_code'])
        return customers("edit")
    else:
        return customers("edit")





# =====================
# RESORT PAGES
# =====================

@app.route("/resort")
def resort(tab="view"):
    db.update_available()
    room_table, floors = db.get_room_table()
    room_list = db.get_room_list()
    type_list = db.get_room_type_list()
    fee_list = db.get_fee_list()
    return render_template("resort.html", tab=tab, room_list=room_list,
                           type_list=type_list, fee_list=fee_list,
                           room_table=room_table, floors=floors)


@app.route("/resort/add_room", methods=['POST', 'GET'])
def add_room():
    if request.method == 'POST':
        form = request.form
        db.add_room(form['room_number'], form['floor'], form['room_type'])
        return resort("add_room")
    else:
        return resort("add_room")


@app.route("/resort/delete_room", methods=['POST', 'GET'])
def delete_room():
    if request.method == 'POST':
        db.delete_room(request.form['room_number'])
        return resort("delete_room")
    else:
        return resort("delete_room")


@app.route("/resort/add_room_type", methods=['POST', 'GET'])
def add_room_type():
    if request.method == 'POST':
        form = request.form
        db.add_room_type(form['name'], form['capacity'], form['price'])
        return resort("add_type")
    else:
        return resort("add_type")


@app.route("/resort/delete_room_type", methods=['POST', 'GET'])
def delete_room_type():
    if request.method == 'POST':
        db.delete_room_type(request.form['room_type'])
        return resort("delete_type")
    else:
        return resort("delete_type")


@app.route("/resort/add_fee", methods=['POST', 'GET'])
def add_fee():
    if request.method == 'POST':
        form = request.form
        db.add_fee(form['name'], form['price'])
        return resort("add_fee")
    else:
        return resort("add_fee")


@app.route("/resort/delete_fee", methods=['POST', 'GET'])
def delete_fee():
    if request.method == 'POST':
        db.delete_fee(request.form['fee'])
        return resort("delete_fee")
    else:
        return resort("delete_fee")




# =====================
# BOOKINGS PAGES
# =====================

@app.route("/bookings")
def bookings(tab="current"):
    active_bookings = db.get_active_bookings()
    past_bookings = db.get_past_bookings()
    upcoming_bookings = db.get_upcoming_bookings()
    customer_table = db.get_customers_table()
    return render_template("bookings.html", tab=tab,
                           customer_table=customer_table,
                           active_bookings=active_bookings,
                           past_bookings=past_bookings,
                           upcoming_bookings=upcoming_bookings)


@app.route("/bookings/add_booking", methods=['POST', 'GET'])
def add_booking():
    if request.method == 'POST':
        err = ""
        form = request.form
        if 'room_number' in form:
            added = db.add_booking(form['room_number'], form['customer_id'],
                                   form['arrival'], form['nights'])
            if added:
                return bookings("add")
            else:
                err = "Room %s is already booked during this timeframe" % (form['room_number'])

        c_info = db.get_customer_info(request.form['customer_id'])
        room_table = db.get_room_table(by_floor=False)
        return render_template("add_booking.html", c=c_info,
                               room_table=room_table, err_message=err)
    else:
        return bookings("add")


@app.route("/bookings/delete_booking", methods=['POST', 'GET'])
def delete_booking():
    if request.method == 'POST':
        db.delete_booking(request.form['booking_id'])
        return bookings("current")
    else:
        return bookings("current")


@app.route("/bookings/fees", methods=['POST', 'GET'])
def manage_fees():
    if request.method == 'POST':
        booking_id = request.form['booking_id']

        fees = db.get_fee_ids();
        if (len(list(request.form.keys())) > 2):
            for f in fees:
                db.update_fee(booking_id, f, request.form[f])
            return bookings("current")

        fees = db.get_fees(booking_id)
        b_info = db.get_booking_info(booking_id)
        return render_template("manage_fees.html", b=b_info, fees=fees)
    else:
        return bookings("current")




# =====================
# INVOICES PAGES
# =====================

@app.route("/invoices")
def invoices(tab="unpaid"):
    current_invoices = db.get_current_invoices()
    overdue_invoices = db.get_overdue_invoices()
    paid_invoices = db.get_paid_invoices()
    return render_template("invoices.html", tab=tab,
                           current_invoices=current_invoices,
                           overdue_invoices=overdue_invoices,
                           paid_invoices=paid_invoices)


@app.route("/invoices/pay", methods=['POST', 'GET'])
def invoice_pay():
    if request.method == 'POST':
        booking_id = request.form['booking_id']
        db.mark_as_paid(booking_id)
        return invoices("unpaid")
    else:
        return invoices("unpaid")


@app.route("/invoices/unpay", methods=['POST', 'GET'])
def invoice_unpay():
    if request.method == 'POST':
        booking_id = request.form['booking_id']
        db.mark_as_unpaid(booking_id)
        return invoices("paid")
    else:
        return invoices("paid")



# =====================
# ANALYTICS PAGES
# =====================

@app.route("/analytics")
def analytics(tab="bookings"):
    s1 = db.update_bookings_by_month()
    s2 = db.update_revenue_by_month()
    s3 = db.update_revenue_by_fee()
    bookings_tot = db.get_total_bookings()
    revenue_tot = db.get_total_revenue()
    unpaid_tot = db.get_total_revenue(unpaid=True)
    return render_template("analytics.html", tab=tab, bookings_tot=bookings_tot,
                           revenue_tot=revenue_tot, unpaid_tot=unpaid_tot,
                           book_by_mo=s1, rev_by_mo=s2, rev_by_fee=s3)


@app.route("/analytics/refresh")
def analytics_refresh():
    db.update_bookings_by_month()
    db.update_revenue_by_month()
    db.update_revenue_by_fee()
    return redirect(url_for('analytics'))



# =====================
# SETTINGS PAGE
# =====================

@app.route("/settings")
def settings(tab="clear"):
    return render_template("settings.html", tab=tab,
                           date=db.get_date())


@app.route("/settings/admin", methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        command = request.form['command']

        if command == "clear_all":
            db.build_tables(reset=True, example_instance=False)
            return settings("clear")

        elif command == "clear_example":
            db.build_tables(reset=True, example_instance=True)
            return settings("clear")

        elif command == "change_date":
            return "<h2>Feature not yet available</h2>"

        return settings("clear")
    else:
        return settings("clear")




# MAIN FUNCTION
# connect to DB, and start the app
if __name__ == "__main__":

    cnx = db.connect()
    if cnx is None:
        exit(0)

    db.connect_sqlalchemy()
    db.setup_indexes()
    print("--> database connected")

    app.run(debug=True, host="127.0.0.1", port=5000)
