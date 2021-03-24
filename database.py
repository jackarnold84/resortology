from mysql import connector
import json

# path to json file with connection info (private)
connect_file_path = "C:/Users/jacka/Desktop/Dump/db_connect_info.json"

build_file_path = "sql/build_tables.sql"

cnx = None


# INITIALIZE DB

# set up connection
def connect():
    with open(connect_file_path) as f:
        conn_info = json.load(f)

    try:
        global cnx
        cnx = connector.connect(user=conn_info['user'],
                                password=conn_info['password'],
                                host=conn_info['host'],
                                database=conn_info['database'])
        print("-->connected to database")
    except:
        print("-->ERROR: could not connect to database")


# create tables from sql build file
def build_tables(reset=False):
    # needs fixed

    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()

    if (not reset and len(tables) > 0):
        return # don't reset

    with open(build_file_path, "r") as f:
        query = f.read()

    cursor = cnx.cursor()
    cursor.execute(query, multi=True)
    cnx.commit()
    cursor.close()

    print("-->table build success")



# CUSTOMERS

def get_all_customers(limit=100):

    query = "SELECT * FROM customers LIMIT %d" % limit

    cursor = cnx.cursor()
    cursor.execute(query)
    customers = cursor.fetchall()
    cursor.close()

    return customers


def add_customer(first_name, last_name, email, phone, zip_code):
    query = """
      INSERT INTO customers (first_name, last_name, email, phone, zip_code)
      VALUES (%s, %s, %s, %s, %s);
    """
    values = (first_name, last_name, email, phone, zip_code)

    cursor = cnx.cursor()
    cursor.execute(query, values)
    cnx.commit()
    cursor.close()
