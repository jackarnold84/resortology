from mysql import connector
import json

# path to json file with connection info (private)
connect_file_path = "C:/Users/jacka/Desktop/Dump/db_connect_info.json"

build_file_path = "sql/build_tables.sql"
example_instance_path = "sql/example_instance.sql"

cnx = None



# HELPER FUNCTIONS

def source_file(path):
    f = open(path, 'r')
    sql_file = f.read()
    f.close()
    sql_commands = sql_file.split(';')

    cursor = cnx.cursor()
    for command in sql_commands:
        if command.strip() != '':
            cursor.execute(command)

    cursor.close()
    cnx.commit()



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
        print("---> connected to database")
    except:
        print("---> ERROR: could not connect to database")


# create tables from sql build file
def build_tables(reset=False, example_instance=False):

    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    if (not reset and len(tables) > 0):
        return # don't change tables

    source_file(build_file_path)
    print("---> created tables")

    if example_instance:
        source_file(example_instance_path)
        print("---> initialized example instance")



# CUSTOMERS

def get_customers_table(limit=100):
    query = "SELECT * FROM customer LIMIT %d" % limit

    cursor = cnx.cursor()
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()

    return table


def get_customer_list():
    query = """SELECT customer_id, first_name, last_name FROM customer"""

    cursor = cnx.cursor()
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()

    c_list = [(x[0], '(%d) %s %s' % (x[0], x[1], x[2])) for x in table]
    return c_list


def add_customer(first_name, last_name, email, phone, zip_code):
    query = """
      INSERT INTO customer (first_name, last_name, email, phone, zip_code)
      VALUES (%s, %s, %s, %s, %s);
    """
    values = (first_name, last_name, email, phone, zip_code)

    cursor = cnx.cursor()
    cursor.execute(query, values)
    cursor.close()
    cnx.commit()


def delete_customer(id):
    query = "DELETE FROM customer WHERE customer_id = %s" % (str(id))

    cursor = cnx.cursor()
    cursor.execute(query)
    cursor.close()
    cnx.commit()
