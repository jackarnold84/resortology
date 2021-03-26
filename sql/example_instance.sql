
INSERT into customer (first_name, last_name, email, phone, zip_code)
  VALUES
  ('James', 'Sullivan', 'jps@hotmail.com', '2584268897', '22547'),
  ('Mike', 'Wazowski', 'mike@hotmail.com', '2589421354', '22547'),
  ('Randall', 'Boggs', 'randy1@yahoo.com', '4475268847', '22366')
;


INSERT into room_type (name, capacity, price)
  VALUES
  ('Single', 1, 64.50),
  ('Double', 2, 95.00),
  ('Single Suite', 1, 110.50)
;


INSERT into room (room_number, floor, room_type_id, available)
  VALUES
  (210, 2, 1, 1),
  (215, 2, 1, 1),
  (225, 2, 2, 1),
  (350, 3, 2, 1),
  (365, 3, 3, 1)
;


INSERT into fee (name, price)
  VALUES
  ('Pool Access', 24.50),
  ('Parking Permit', 45.00),
  ('Towel Service', 6.50)
;


INSERT into booking (room_number, customer_id, arrival, nights)
  VALUES
  (210, 1, '2021-03-01', 3),
  (215, 1, '2021-03-12', 2),
  (210, 2, '2021-03-12', 3)
;


INSERT into booking_fee (booking_id, fee_id, quantity)
  VALUES
  (1, 1, 1),
  (1, 3, 3),
  (2, 2, 1),
  (3, 1, 1),
  (3, 2, 1)
;


-- INSERT into invoice (booking_id, amount, paid, paid_date)
--   VALUES
--   ()
-- ;
