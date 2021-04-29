from mysql import connector
import json
import sys
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
matplotlib.use('Agg')


# =====================
# Connect to DB
# =====================

# path to json file with connection info (private)
connect_file_path = "C:/Users/jacka/Desktop/Dump/db_connect_info.json"
with open(connect_file_path) as f:
    conn_info = json.load(f)

db_uri = 'mysql+mysqlconnector://%s:%s@%s/%s' % (conn_info['user'],
                conn_info['password'], conn_info['host'], conn_info['database'])

# connection global variables
session = None


def connect_sqlalchemy():
    engine = sqlalchemy.create_engine(db_uri, echo=False, encoding='utf-8')

    global session
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                          bind=engine))

    global Base
    Base.query = session.query_property()

    Base.metadata.create_all(bind=engine)


def connect():
    try:
        cnx = connector.connect(user=conn_info['user'],
                                password=conn_info['password'],
                                host=conn_info['host'],
                                database=conn_info['database'])
        return cnx
    except:
        print("---> ERROR: could not connect to database")
        return None



# =====================
# INITIALIZATION
# =====================

def source_file(path):
    f = open(path, 'r')
    sql_file = f.read()
    f.close()
    sql_commands = sql_file.split(';')

    cnx = connect()
    cursor = cnx.cursor()
    for command in sql_commands:
        if command.strip() != '':
            cursor.execute(command)

    cursor.close()
    cnx.commit()
    cnx.close()


# create tables from sql build file
def build_tables(reset=False, example_instance=False):

    build_file_path = "sql/build_tables.sql"
    example_instance_path = "sql/example_instance.sql"

    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    if (not reset and len(tables) > 0):
        print("---> tables already exist")
        cnx.close()
        return # don't change tables

    source_file(build_file_path)
    print("---> created tables")

    if example_instance:
        connect()
        source_file(example_instance_path)
        print("---> initialized example instance")

    cnx.close()


def setup_indexes():
    idx1 = """CREATE INDEX bid_index ON booking (booking_id, arrival)
              USING HASH"""
    idx2 = """CREATE INDEX cid_index ON customer (customer_id) USING HASH"""
    idx3 = """CREATE INDEX fid_index ON fee (fee_id) USING HASH"""

    # create if does not already exist
    cnx = connect()
    cursor = cnx.cursor()
    try:
        cursor.execute(idx1)
    except:
        pass
    try:
        cursor.execute(idx2)
    except:
        pass
    try:
        cursor.execute(idx3)
    except:
        pass
    cursor.close()
    cnx.commit()
    cnx.close()


# TRANSACTIONS
def set_transaction_isolation(cnx, level="REPEATABLE READ"):
    if level not in ["REPEATABLE READ", "READ COMMITTED",
                     "READ UNCOMMITTED", "SERIALIZABLE"]:
        return
    query = """SET TRANSACTION ISOLATION LEVEL %s""" % level;

    cursor = cnx.cursor()
    cursor.execute(query)
    cursor.close()


def commit_transaction():
    cnx.commit()
    connect()


def rollback_transaction():
    connect()



# =====================
# CUSTOMER TABLE
# =====================

def get_customers_table():
    connect_sqlalchemy()
    return Customer.query.all()


def add_customer(first_name, last_name, email, phone, zip_code):
    new = Customer(first_name=first_name, last_name=last_name, email=email,
                   phone=phone, zip_code=zip_code)
    session.add(new)
    session.commit()
    connect()


def edit_customer(id, first_name, last_name, email, phone, zip_code):
    customer = Customer.query.filter_by(customer_id=id).first()
    customer.first_name = first_name
    customer.last_name = last_name
    customer.email = email
    customer.phone = phone
    customer.zip_code = zip_code

    session.commit()
    connect()



def delete_customer(id):
    Customer.query.filter_by(customer_id=id).delete()
    session.commit()
    connect()


def get_customer_info(id):
    return Customer.query.filter_by(customer_id=id).first()



# =====================
# RESORT TABLE
# =====================

def get_room_table(by_floor=True):
    query = """SELECT r.room_number, r.floor, r.available, rt.name, rt.capacity
               FROM room r
               JOIN room_type rt ON r.room_type_id = rt.room_type_id
               ORDER BY r.room_number
            """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    if not by_floor:
        return table

    if len(table) == 0:
        return table, []

    floors = sorted(set([x[1] for x in table]))
    t = {f : [] for f in floors}
    for x in table:
        t[x[1]].append( (x[0], x[2], x[3], x[4]) )

    return t, floors


def get_room_list():
    return Room.query.with_entities(Room.room_number).order_by(Room.room_number).all()


def get_room_type_list():
    return RoomType.query.with_entities(RoomType.room_type_id, RoomType.name).all()


def get_fee_list():
    return Fee.query.all()


def add_room(room_number, floor, room_type_id):
    new = Room(room_number=room_number, floor=floor, room_type_id=room_type_id,
               available=1)
    session.add(new)
    session.commit()


def add_room_type(name, capacity, price):
    new = RoomType(name=name, capacity=capacity, price=price)
    session.add(new)
    session.commit()


def add_fee(name, price):
    new = Fee(name=name, price=price)
    session.add(new)
    session.commit()


def delete_room(room_number):
    Room.query.filter_by(room_number=room_number).delete()
    session.commit()


def delete_room_type(id):
    RoomType.query.filter_by(room_type_id=id).delete()
    session.commit()


def delete_fee(id):
    Fee.query.filter_by(fee_id=id).delete()
    session.commit()


def update_available():
    query1 = """
    UPDATE room
    SET available = 1;
    """

    query2 = """
    UPDATE room AS r
    JOIN booking b on b.room_number = r.room_number
    SET r.available = 0
    WHERE DATE_ADD(b.arrival, INTERVAL nights DAY) >= CURRENT_DATE()
          AND b.arrival <= CURRENT_DATE();
    """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.close()
    cnx.commit()
    cnx.close()


# =====================
# BOOKINGS TABLE
# =====================

def get_active_bookings():
    query = """SELECT b.booking_id, CONCAT(c.first_name, " ", c.last_name) AS name,
                      b.arrival, b.nights, b.room_number
               FROM booking b
               JOIN customer c on b.customer_id = c.customer_id
               WHERE DATE_ADD(arrival, INTERVAL nights DAY) >= CURRENT_DATE()
                     AND arrival <= CURRENT_DATE()
               ORDER BY arrival
            """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table


def get_upcoming_bookings():
    query = """SELECT b.booking_id, CONCAT(c.first_name, " ", c.last_name) AS name,
                      b.arrival, b.nights, b.room_number
               FROM booking b
               JOIN customer c on b.customer_id = c.customer_id
               WHERE arrival > CURRENT_DATE()
               ORDER BY arrival
            """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table


def get_past_bookings():
    query = """SELECT b.booking_id, CONCAT(c.first_name, " ", c.last_name) AS name,
                      b.arrival, b.nights, b.room_number
               FROM booking b
               JOIN customer c on b.customer_id = c.customer_id
               WHERE DATE_ADD(arrival, INTERVAL nights DAY) < CURRENT_DATE()
               ORDER BY arrival
            """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table


def is_valid_booking(cnx, room_number, arrival, nights):
    query = """SELECT COUNT(*) FROM booking
               WHERE room_number = %s AND (
                 (%s >= arrival AND %s < DATE_ADD(arrival, INTERVAL nights DAY)) OR
                 (DATE_ADD(%s, INTERVAL %s DAY) > arrival AND
                    DATE_ADD(%s, INTERVAL %s DAY) <= DATE_ADD(arrival, INTERVAL nights DAY)) OR
                 (%s < arrival AND
                    DATE_ADD(%s, INTERVAL %s DAY) > DATE_ADD(arrival, INTERVAL nights DAY))
               )
            """
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query, (room_number, arrival, arrival, arrival, nights,
                           arrival, nights, arrival, arrival, nights))
    table = cursor.fetchall()
    cursor.close()

    return False if table[0][0] > 0 else True


def add_booking(room_number, customer_id, arrival, nights):
    # transaction
    cnx = connect()
    set_transaction_isolation(cnx, "REPEATABLE READ")

    if not is_valid_booking(cnx, room_number, arrival, nights):
        # rollback
        cnx.close()
        return False

    query = """INSERT INTO booking (room_number, customer_id, arrival, nights)
               VALUES (%s, %s, %s, %s)"""

    cursor = cnx.cursor(prepared=True)
    cursor.execute(query, (room_number, customer_id, arrival, nights))

    query = """SELECT LAST_INSERT_ID()"""
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()

    setup_invoice(cnx, table[0][0])
    # commit
    cnx.commit()
    cnx.close()
    return True


def delete_booking(id):
    Booking.query.filter_by(booking_id=id).delete()
    Invoice.query.filter_by(booking_id=id).delete()
    session.commit()


def get_booking_info(id):
    return Booking.query.filter_by(booking_id=id).join(Customer).\
           with_entities(Booking.booking_id, Customer.first_name,
                         Customer.last_name, Booking.room_number).first()


def get_fee_ids():
    table = Fee.query.with_entities(Fee.fee_id).all()
    return [str(f.fee_id) for f in table]



def get_fees(id):
    query = """
    SELECT * FROM ((
      SELECT f.fee_id, f.name, bf.quantity
      FROM booking b
      JOIN booking_fee bf ON b.booking_id = bf.booking_id
      JOIN fee f ON f.fee_id = bf.fee_id
      WHERE b.booking_id = %s
    ) UNION (
        SELECT fee_id, name, 0 as quantity
        FROM fee f
        WHERE fee_id NOT IN (
          SELECT f.fee_id
          FROM booking b
          JOIN booking_fee bf ON b.booking_id = bf.booking_id
          JOIN fee f ON f.fee_id = bf.fee_id
          WHERE b.booking_id = %s
        )
      )) t
    ORDER BY fee_id;
    """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query, (id, id))
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table


def update_fee(booking_id, fee_id, quantity):

    cnx = connect()
    set_transaction_isolation(cnx, "READ COMMITTED")

    bf = BookingFee.query.filter_by(booking_id=booking_id, fee_id=fee_id).first()
    quantity = int(quantity)

    if bf and quantity > 0:
        bf.quantity = quantity
    elif bf and quantity == 0:
        BookingFee.query.filter_by(booking_id=booking_id, fee_id=fee_id).delete()
    elif not bf and quantity > 0:
        new = BookingFee(booking_id=booking_id, fee_id=fee_id, quantity=quantity)
        session.add(new)

    session.commit()

    update_invoice_amount(cnx, booking_id)
    cnx.commit()
    cnx.close()



# =====================
# INVOICES PAGES
# =====================

def setup_invoice(cnx, booking_id):
    query = """INSERT INTO invoice (booking_id, amount, paid, paid_date)
               VALUES (%s, 0.0, 0, NULL)"""
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query, (booking_id, ))
    cursor.close()

    update_invoice_amount(cnx, booking_id)



def update_invoice_amount(cnx, booking_id):
    query = """
    UPDATE invoice
    SET amount = (
        SELECT MAX(rt.price)*MAX(b.nights) + IFNULL(SUM(f.price * bf.quantity), 0)
        FROM booking b
        JOIN room r ON b.room_number = r.room_number
        JOIN room_type rt ON r.room_type_id = rt.room_type_id
        LEFT OUTER JOIN booking_fee bf ON b.booking_id = bf.booking_id
        LEFT OUTER JOIN fee f ON bf.fee_id = f.fee_id
        GROUP BY b.booking_id
        HAVING b.booking_id = %s
    )
    WHERE booking_id = %s;
    """

    cursor = cnx.cursor(prepared=True)
    cursor.execute(query, (booking_id, booking_id))
    cursor.close()


def mark_as_paid(booking_id):
    invoice = Invoice.query.filter_by(booking_id=booking_id).first()
    invoice.paid = 1
    invoice.paid_date = date.datetime.today().strftime('%Y-%m-%d')
    session.commit()


def mark_as_unpaid(booking_id):
    invoice = Invoice.query.filter_by(booking_id=booking_id).first()
    invoice.paid = 0
    invoice.paid_date = None
    session.commit()


def get_current_invoices():
    query = """SELECT b.booking_id, i.invoice_id, CONCAT(c.first_name, " ", c.last_name),
               b.room_number, i.amount,
               DATE_ADD(b.arrival, INTERVAL b.nights DAY) AS due_date
               FROM invoice i
               JOIN booking b ON i.booking_id = b.booking_id
               JOIN customer c ON b.customer_id = c.customer_id
               WHERE i.paid = 0
               HAVING due_date >= CURRENT_DATE()
               ORDER BY due_date;
            """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table


def get_overdue_invoices():
    query = """
    SELECT b.booking_id, i.invoice_id, CONCAT(c.first_name, " ", c.last_name),
           b.room_number, i.amount,
           DATE_ADD(b.arrival, INTERVAL b.nights DAY) AS due_date
    FROM invoice i
    JOIN booking b ON i.booking_id = b.booking_id
    JOIN customer c ON b.customer_id = c.customer_id
    WHERE i.paid = 0
    HAVING due_date < CURRENT_DATE()
    ORDER BY due_date;
    """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table


def get_paid_invoices():
    query = """
    SELECT b.booking_id, i.invoice_id, CONCAT(c.first_name, " ", c.last_name),
           b.room_number, i.amount,
           DATE_ADD(b.arrival, INTERVAL b.nights DAY) AS due_date
    FROM invoice i
    JOIN booking b ON i.booking_id = b.booking_id
    JOIN customer c ON b.customer_id = c.customer_id
    WHERE i.paid = 1
    ORDER BY due_date DESC
    LIMIT 100;
    """

    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table



# =====================
# ANALYTICS PAGES
# =====================

def get_total_bookings():
    query = """SELECT IFNULL(COUNT(*), 0)
               FROM booking;
            """
    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return table[0][0]


def get_total_revenue(unpaid=False):
    query = """SELECT IFNULL(SUM(amount), 0) FROM invoice
               WHERE paid = 1;
            """
    if unpaid:
        query = """SELECT IFNULL(SUM(amount), 0) FROM invoice
                   WHERE paid = 0;
                """
    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    return "$%.2f" % float(table[0][0])


def update_bookings_by_month():
    query = """SELECT MONTH(arrival), MONTHNAME(arrival), COUNT(*)
               FROM booking
               WHERE YEAR(arrival) = YEAR(CURRENT_DATE())
               GROUP BY MONTH(arrival), MONTHNAME(arrival)
               ORDER BY MONTH(arrival);
            """
    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    df = pd.DataFrame(table, columns=["M", "Month", "Bookings"])
    return str(df[['Month', 'Bookings']].values.tolist())



def update_revenue_by_month():
    query = """SELECT MONTH(paid_date), MONTHNAME(paid_date), SUM(amount)
               FROM invoice
               WHERE YEAR(paid_date) = YEAR(CURRENT_DATE())
                 AND paid = 1
               GROUP BY MONTH(paid_date), MONTHNAME(paid_date)
               ORDER BY MONTH(paid_date);
            """
    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    df = pd.DataFrame(table, columns=["M", "Month", "Revenue"])
    df["Revenue"] = pd.to_numeric(df["Revenue"])
    return str(df[['Month', 'Revenue']].values.tolist())



def update_revenue_by_fee():
    query = """SELECT name, SUM(quantity) * MAX(price) AS revenue
               FROM fee f
               JOIN booking_fee bf ON f.fee_id = bf.fee_id
               GROUP BY name
               ORDER BY revenue DESC;
            """
    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()

    df = pd.DataFrame(table, columns=["Fee", "Revenue"])
    df["Revenue"] = pd.to_numeric(df["Revenue"])
    return str(df[['Fee', 'Revenue']].values.tolist())



# =====================
# SETTINGS PAGES
# =====================

def get_date():
    query = """SELECT NOW()"""
    cnx = connect()
    cursor = cnx.cursor(prepared=True)
    cursor.execute(query)
    table = cursor.fetchall();
    cursor.close()
    cnx.close()
    return table[0][0]



# MAIN FUNCTION
# (to initialize DB from the command line)
if __name__ == "__main__":

    connect()

    if "-example" in sys.argv:
        build_tables(reset=True, example_instance=True)
    elif "-reset" in sys.argv:
        build_tables(reset=True, example_instance=False)
    elif "-build" in sys.argv:
        build_tables(reset=False, example_instance=False)
    else:
        print("\nAdd arguments:")
        print("To build tables: -build")
        print("To build tables and reset instance: -reset")
        print("To build with example instance: -example")
