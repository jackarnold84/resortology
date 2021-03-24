DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    first_name varchar(30),
    last_name varchar(30),
    email varchar(50),
    phone varchar(12),
    zip_code varchar(5),

	PRIMARY KEY (customer_id)
);
