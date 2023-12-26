import functions
import csv
from client import Client
from loan import Loan


def test_time_forward():
    bank_start = 0
    lines = 0

    with open("loans.txt", 'r') as file:
        lines = file.readlines()

    with open('loans.txt', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['1', '1', '1000', '5', '12', '12', '100'])

    with open('bank.txt', 'r') as file:
        bank_start = float(file.read())

    with open('bank.txt', 'w') as file:
        file.write('1000')

    functions.time_forward(2)

    with open('loans.txt', 'r', newline='') as file:
        reader = csv.reader(file)
        last_row = None
        for row in reader:
            last_row = row

        assert last_row == ['1', '1', '1000', '5', '12', '10', '100']

    with open('bank.txt', 'r') as file:
        balance = float(file.read())

        assert balance == 1200.0

    with open("bank.txt", 'w') as file:
        file.write(str(bank_start))

    with open("loans.txt", 'w') as file:
        file.writelines(lines)


def test_update_bank():
    bank_start = 0
    bank_temp = 0
    with open('bank.txt', 'r') as file:
        bank_start = float(file.read())

    functions.update_bank(-300)
    with open('bank.txt', 'r') as file:
        bank_temp = float(file.read())

    assert bank_start + 300 == bank_temp

    with open("bank.txt", 'w') as file:
        file.write(str(bank_start))


def test_add_client():
    lines = ""
    with open("clients.txt", 'r') as file:
        lines = file.readlines()

    client = Client("", "Test1", "Test2")
    functions.add_client_write(client)

    with open('clients.txt', 'r', newline='') as file:
        reader = csv.reader(file)
        last_row = None
        for row in reader:
            last_row = row

        assert last_row[1] == "Test1"
        assert last_row[2] == "Test2"

    with open("clients.txt", 'w') as file:
        file.writelines(lines)


def test_add_loan():
    lines = ""
    with open("loans.txt", 'r') as file:
        lines = file.readlines()

    loan = Loan('1', '1', '1000', '5', '12', '12', 100)
    functions.add_loan_write(loan)

    with open('loans.txt', 'r', newline='') as file:
        reader = csv.reader(file)
        last_row = None
        for row in reader:
            last_row = row

        assert last_row[1] == "1"
        assert last_row[2] == "1000"
        assert last_row[3] == "5"
        assert last_row[4] == "12"
        assert last_row[5] == "12"
        assert last_row[6] == "100"

    with open("loans.txt", 'w') as file:
        file.writelines(lines)


def test_refresh_cwl():
    clients_lines = ""
    with open("clients.txt", 'r') as file:
        clients_lines = file.readlines()
    loans_lines = ""
    with open("loans.txt", 'r') as file:
        loans_lines = file.readlines()

    client = Client("", "Nowy", "Klient")
    client = functions.add_client_write(client)
    loan = Loan("", client.client_id, "1000", "5", "12", "12", 100)
    functions.add_loan_write(loan)

    cwl = functions.refresh_cwl_write()

    client_listed = f"{client.client_id}. "\
        f"{client.first_name} {client.last_name}"
    assert client_listed in cwl

    with open("clients.txt", 'w') as file:
        file.writelines(clients_lines)
    with open("loans.txt", 'w') as file:
        file.writelines(loans_lines)
