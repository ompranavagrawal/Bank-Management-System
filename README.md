# Bank-Management-System
Certified by Infosys Limited, developed a comprehensive application built with Java and Spring Framework and an MS SQL database for robust management of checking and savings accounts, as well as debt management operations.


**Description**
This code is a Python script that simulates a basic banking system, utilizing the cx_Oracle library to interact with an Oracle database and the tabulate library to format output tables. It supports several operations:

**Sign Up**: Allows new users to create an account by entering details such as account type, holder name, address, password, and initial deposit amount. It inserts these details into a database table and generates unique customer and account numbers.

**Address Change**: Enables users to update their address information in the database for a given account number.

**Money Deposit**: Allows users to deposit money into their account. It updates the balance in the database after adding the deposited amount to the current balance.

**Money Withdrawal**: Enables users to withdraw money from their account if they have sufficient balance. It also updates the balance in the database.

**Print Statement**: Generates a statement of transactions within a specified date range for a given account number, displaying the date, transaction type, and balance.

**Transfer Money**: Allows users to transfer money from their account to another account if they have sufficient balance and the receiver account exists.

**Account Closure**: Marks an account as closed and records the closure date in the database.

**Fixed Deposit**: Users can create a fixed deposit account with a minimum amount and term.

**Loan Management**: Users can apply for a loan if they are eligible (based on their balance and existing loan amount) and view loan details.

**Admin Sign In**: Special functionality for admins to view reports and perform administrative tasks.

**Opening New Accounts**: Users can open additional saving, current, or fixed deposit accounts.

**Main Menu and Sign In**: The script provides a main menu for navigation and allows existing users to sign in and perform banking operations.

The script uses procedural programming to define functions for each feature and interacts with a database using SQL queries for data manipulation and retrieval. Each operation requires user input for various details, and the system provides feedback based on the actions performed.
