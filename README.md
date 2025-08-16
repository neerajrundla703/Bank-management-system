# Bank Managements System

## First download python and mysql 

create a database and create table 
<br>
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(100),
    pin INT NOT NULL,
    account_no VARCHAR(10) UNIQUE NOT NULL,
    balance DECIMAL(10,2) DEFAULT 0.00
);

and connect to python file 
