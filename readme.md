
# Credit Bank Simulator

## Description
This is my first object-oriented program, written in the first semester of my studies.

The program is a simulator of a bank granting loans to its clients. It allows clients to take loans of various amounts and with different interest rates. The loan is simplified - the only variables are: interest rate, number of installments, and installment amount. The program is graphical and interactive. The simulator allows for time acceleration - you can see the debt status of clients and the bank's assets after a few months.

## Program Structure
The program is divided into classes located in files with the same names:

- `Client` - contains client data. Unique id, first and last name.
- `Loan` - contains loan data. Unique id, id of the client taking the loan, loan amount, interest rate, number of installments, remaining installments, installment amount.
- `App` - contains the main part of the code. The entire GUI and logic.

The program is run from the `main.py` file.

The program includes the `functions.py` file, responsible for all repetitive functions within the code.

Functions and all variables are named so that their functionality is known - even at the cost of a long name. They are also described with appropriate comments.

## Key Text Files
The key part of the program consists of three text files - `bank.txt`, `clients.txt`, and `loans.txt`.

- `bank.txt` - holds information about the bank's account balance.
- `clients.txt` - is a database of all clients, in .csv format.
- `loans.txt` - is a database of all loans, in .csv format.

In the `bank.txt` file, we can set the initial state of the bank's account. This is done manually by changing the content of the file. The default value is one million złotych.

In the `loans.txt` and `clients.txt` files, we can manually remove loans and clients. It is not recommended to manually add new values or modify existing ones.

The `test_Bank.py` file contains unit tests for functions from the `functions.py` file.

## Author
Program written by: Rafał Mironko
