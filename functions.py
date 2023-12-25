import csv
from itertools import count
from client import Client


def time_forward():
    months_to_skip = 1
    loans = []
    with open("loans.txt", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            loans.append(row)

    for loan in loans:
        remaining_months = int(loan[5]) - months_to_skip
        if remaining_months < 0:
            remaining_months = 0
            continue

        loan[5] = str(remaining_months)

        amount_paid = float(loan[6])
        with open("bank.txt", "r") as bank_file:
            bank_balance = float(bank_file.read())

        bank_balance += amount_paid
        with open("bank.txt", "w") as bank_file:
            bank_file.write(str(bank_balance))

    with open("loans.txt", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(loans)


def update_bank(amount_to_subtract):
    with open("bank.txt", "r") as file:
        current_amount = float(file.read())

    new_amount = current_amount - amount_to_subtract

    if new_amount < 0:
        with open("bank.txt", "w") as file:
            file.write(str(current_amount))
        return 0

    with open("bank.txt", "w") as file:
        file.write(str(new_amount))

    return 1


def add_client_write(client):
    with open('clients.txt', mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        counter = count(start=1)

        with open('clients.txt', mode='r') as f:
            existing_ids = set(int(row[0]) for row in csv.reader(f))

        client.client_id = next(
            id_num for id_num in counter if id_num not in existing_ids)
        writer.writerow(
            [client.client_id, client.first_name, client.last_name])
    return client


def add_loan_write(loan):
    with open('loans.txt', mode='a', newline='') as file:
        writer = csv.writer(file)
        counter = count(start=1)

        with open('loans.txt', mode='r') as f:
            existing_ids = set(int(row[0]) for row in csv.reader(f))

        loan_id = next(
            id_num for id_num in counter if id_num not in existing_ids)

        writer.writerow(
            [loan_id, loan.client_id, loan.amount, loan.percentage,
                loan.installments, loan.installments,
                loan.installment_amount])


def refresh_cwl_write():
    clients_with_loans = set()
    clients_with_loans_list = []

    with open("loans.txt", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            client_id = row[1]
            clients_with_loans.add(client_id)

    with open("clients.txt", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            client = Client(row[0], row[1], row[2])

            if client.client_id in clients_with_loans:
                client_name = f"{client.client_id}. " \
                    f"{client.first_name} {client.last_name}"
                clients_with_loans_list.append(client_name)
    return clients_with_loans_list


def refresh_c_write():
    clients = []

    with open('clients.txt', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                client = Client(int(row[0]), row[1], row[2])
                clients.append(f"{client.client_id}. "
                               f"{client.first_name} {client.last_name}")
    return clients
