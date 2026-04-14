-- Little Lemon Stored Procedures
-- Database: little_lemon

-- 1. GetMaxQuantity
-- Returns the maximum quantity ordered from the Orders table
DELIMITER //
CREATE PROCEDURE GetMaxQuantity()
BEGIN
    SELECT MAX(Quantity) AS 'Max Quantity in Order'
    FROM orders;
END //
DELIMITER ;

-- 2. ManageBooking
-- Checks whether a table is already booked on a given date
DELIMITER //
CREATE PROCEDURE ManageBooking(IN booking_date DATE, IN table_number INT)
BEGIN
    DECLARE booked INT;

    SELECT COUNT(*) INTO booked
    FROM Bookings
    WHERE BookingDate = booking_date AND TableNumber = table_number;

    IF booked > 0 THEN
        SELECT CONCAT('Table ', table_number, ' is already booked') AS 'Booking status';
    ELSE
        SELECT CONCAT('Table ', table_number, ' is available') AS 'Booking status';
    END IF;
END //
DELIMITER ;

-- 3. UpdateBooking
-- Updates the booking date for a given booking ID
DELIMITER //
CREATE PROCEDURE UpdateBooking(IN booking_id INT, IN booking_date DATE)
BEGIN
    UPDATE Bookings
    SET BookingDate = booking_date
    WHERE BookingID = booking_id;
    SELECT CONCAT('Booking ', booking_id, ' updated') AS Confirmation;
END //
DELIMITER ;

-- 4. AddBooking
-- Adds a new booking record
DELIMITER //
CREATE PROCEDURE AddBooking(IN booking_id INT, IN customer_id INT, IN table_number INT, IN booking_date DATE)
BEGIN
    INSERT INTO Bookings (BookingID, BookingDate, TableNumber, CustomerID)
    VALUES (booking_id, booking_date, table_number, customer_id);
    SELECT 'New booking added' AS Confirmation;
END //
DELIMITER ;

-- 5. CancelBooking
-- Deletes a booking record by booking ID
DELIMITER //
CREATE PROCEDURE CancelBooking(IN booking_id INT)
BEGIN
    DELETE FROM Bookings WHERE BookingID = booking_id;
    SELECT CONCAT('Booking ', booking_id, ' cancelled') AS Confirmation;
END //
DELIMITER ;
