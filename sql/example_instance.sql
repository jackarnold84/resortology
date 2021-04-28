
INSERT into customer (first_name, last_name, email, phone, zip_code)
  VALUES
  ('James', 'McGill', 'goodman@hotmail.com', '2584268897', '50547'),
  ('Michael', 'Ehrmantraut', 'miketrout@outlook.com', '2589421354', '50541'),
  ('Kim', 'Wexler', 'kwex@hotmail.com ', '5511543551', '50541'),
  ('Charles', 'McGill', 'mcgill@hhm.org', '5154305440', '50541'),
  ('Howard', 'Hamlin', 'hamlin2@hhm.org', '4415400107', '50544'),
  ('Lalo', 'Salamanca', 'lalo@outlook.com', '4417860301', '22458')
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
  (210, 1, '2021-01-13', 2),
  (210, 2, '2021-01-11', 1),
  (225, 1, '2021-02-01', 4),
  (350, 3, '2021-02-08', 2),
  (210, 4, '2021-02-20', 1),
  (365, 5, '2021-02-13', 1),
  (225, 3, '2021-02-23', 3),
  (210, 6, '2021-03-02', 6),
  (225, 1, '2021-03-13', 2)
;


INSERT into booking_fee (booking_id, fee_id, quantity)
  VALUES
  (1, 1, 1),
  (1, 3, 3),
  (2, 2, 1),
  (3, 1, 1),
  (3, 2, 1),
  (5, 1, 1),
  (6, 1, 1),
  (6, 2, 2),
  (7, 2, 1),
  (8, 1, 1),
  (8, 3, 2)
;


INSERT into invoice (booking_id, amount, paid, paid_date)
  VALUES
  (1, 173.0, 1, '2021-01-14'),
  (2, 109.5, 1, '2021-01-11'),
  (3, 449.50, 1, '2021-02-03'),
  (4, 190.0, 1, '2021-02-09'),
  (5, 89.0, 1, '2021-02-21'),
  (6, 225.0, 1, '2021-02-14'),
  (7, 330.0, 1, '2021-02-23'),
  (8, 424.5, 1, '2021-03-04'),
  (9, 190.0, 1, '2021-03-13')
;
