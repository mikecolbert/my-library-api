-- Check the version of MySQL. This syntax is valid for version 8.
SELECT VERSION();

-- See all databases on this server.
SHOW DATABASES;

-- See all users on this server.
SELECT user FROM mysql.user GROUP BY user; 

-- Create a database named colbert.
CREATE DATABASE my_library;

-- In MySQL, you must "use" the database you want to modify.
USE my_library;

-- Drop a table (delete it).
DROP TABLE books;

-- Create a new table.
CREATE TABLE books ( 
book_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, -- Create a field named 'id'. It is a required field. It is the primary key. It will auto-increment.
library_user varchar(128) NOT NULL, -- Create a field named 'user'. It is a required field.
title varchar(128) NOT NULL, -- It is a required field.
author varchar (128), 
pages int,
isbn varchar(128),
book_type varchar(128),
date_read date,
genre varchar(128),
format varchar(128),
source varchar(128),
evaluation varchar(128),
created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) 
ENGINE=InnoDB AUTO_INCREMENT=1; 

-- Show the tables in the database you are 'using'.
SHOW TABLES;

-- Insert data into the books table.
-- Notice 'id' field isn't populated from the query. It is automatically filled with the next integer when the record is committed.
-- User should be your hawkid.
INSERT INTO books(library_user, title, author, pages, isbn, book_type, date_read, genre, format, source, evaluation) VALUES ('colbert', 'Where the Wild Things Are', 'Maurice Sendak', 48, '978-0-06-025492-6', 'fiction', '2023-02-02', 'Children', 'Hardcover', 'Library', 'Good');
INSERT INTO books(library_user, title, author, pages, isbn, book_type, date_read, genre, format, source, evaluation) VALUES ('colbert', 'Llama Llama Red Pajama', 'Anna Dewdney', 20, '978-0-670-05983-6', 'fiction', '2023-04-01', 'Children', 'Hardcover', 'Library', 'Good');
INSERT INTO books(library_user, title, author, pages, isbn, book_type, date_read, genre, format, source, evaluation) VALUES ('colbert', 'The Very Hungry Caterpillar', 'Eric Carle', 32, '978-0-399-22690-8', 'fiction', '2022-03-20', 'Children', 'Hardcover', 'Library', 'Good');
INSERT INTO books(library_user, title, author, pages, isbn, book_type, date_read, genre, format, source, evaluation) VALUES ('colbert', 'The Giving Tree', 'Shel Silverstein', 64, '978-0-06-025665-4', 'fiction', '2021-04-14', 'Children', 'Hardcover', 'Library', 'Good');
INSERT INTO books(library_user, title, author, pages, isbn, book_type, date_read, genre, format, source, evaluation) VALUES ('colbert', 'The Cat in the Hat', 'Dr. Seuss', 45, '978-0-394-80001-1', 'fiction', '2020-06-29', 'Children', 'Hardcover', 'Library', 'Good');
INSERT INTO books(library_user, title, author, pages, isbn, book_type, date_read, genre, format, source, evaluation) VALUES ('colbert', 'The Lorax', 'Dr. Seuss', 72, '978-0-394-82337-9', 'fiction', '2019-10-01', 'Children', 'Hardcover', 'Library', 'Good');



-- View all the fields in the books table. You should see 5 books.
SELECT * FROM books;

-- View the title and author fields from the books table
SELECT author, title FROM books;

-- Update a database record - changed # of pages
UPDATE books
    SET pages=33 
    WHERE book_id=2; -- Only change this one record with the primary key (id) of 2.

-- You should see the number of pages for book id = 2 updated to 33.
SELECT * FROM books;

-- Delete the record with an id = 4.
DELETE FROM books WHERE book_id=4;

-- You should not see book #4 - Where the Wild Things Are.
SELECT * FROM books;

-- _mgr account has full permissions for all tables inside my_library.
CREATE USER 'my_library_mgr'@'%' IDENTIFIED BY 'VI3XFsJkghxfMOZd0KvqfmGPxG3IqGGqtsUJRf7b8L';
GRANT ALL PRIVILEGES ON my_library.* TO 'my_library_mgr'@'%';
FLUSH PRIVILEGES;

-- _app account has simple CRUD permissions for the books tables inside my_library.
CREATE USER 'my_library_app'@'%' IDENTIFIED BY 'N3kundjVLbUy049WxJ8nS4OskPzrQoBXBFet';
GRANT SELECT, INSERT, DELETE, UPDATE ON my_library.books TO 'my_library_app'@'%';
FLUSH PRIVILEGES;

-- _ro account only has SELECT permissions for the books tables inside my_library.
CREATE USER 'my_library_ro'@'%' IDENTIFIED BY 'E1rdsWMFFSvJlz90R6vipGe7qF9C3V';
GRANT SELECT ON my_library.books TO 'my_library_ro'@'%';
FLUSH PRIVILEGES;



