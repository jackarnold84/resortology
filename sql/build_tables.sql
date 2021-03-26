DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS invoice;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS room_type;
DROP TABLE IF EXISTS booking_fee;
DROP TABLE IF EXISTS fee;


CREATE TABLE customer (
  customer_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(30),
  last_name VARCHAR(30),
  email VARCHAR(50),
  phone VARCHAR(15),
  zip_code VARCHAR(5),

	PRIMARY KEY (customer_id)
);


CREATE TABLE booking (
  booking_id INT NOT NULL AUTO_INCREMENT,
  room_number INT,
  customer_id INT,
  arrival DATE,
  nights INT,

  PRIMARY KEY (booking_id)
);


CREATE TABLE invoice (
  invoice_id INT NOT NULL AUTO_INCREMENT,
  booking_id INT,
  amount DECIMAL(10,2),
  paid INT,
  paid_date DATE,

  PRIMARY KEY (invoice_id)
);


CREATE TABLE room (
  room_number INT NOT NULL UNIQUE,
  floor INT,
  room_type_id INT,
  available INT,

  PRIMARY KEY (room_number)
);


CREATE TABLE room_type (
  room_type_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50),
  capacity INT,
  price DECIMAL(10,2),

  PRIMARY KEY (room_type_id)
);


CREATE TABLE booking_fee (
  booking_id INT NOT NULL,
  fee_id INT NOT NULL,
  quantity INT,

  PRIMARY KEY (booking_id, fee_id)
);


CREATE TABLE fee (
  fee_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50),
  price DECIMAL(10,2),

  PRIMARY KEY (fee_id)
);
