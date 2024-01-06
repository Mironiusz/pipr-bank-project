import csv
from itertools import count
from client import Client
from datetime import datetime, timedelta


def time_forward(total_months):
    """
    Ta funkcja służy do przesuwania czasu do przodu. Wykonuje się tyle razy,
    o ile miesięcy użytkownik postanowi przesunąć czas. Wykonuje także
    wszystkie operacje, jakie wiążą się z przesuwaniem czasu (poprzez
    wywołanie odpowiednich funkcji) - płatności, zmiana stanu aktywów banku.
    """
    for i in range(int(total_months)):
        add_month()
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
                bank_file.write(str(round(bank_balance, 2)))

        with open("loans.txt", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(loans)


def update_bank(amount_to_subtract):
    """
    Ta funkcja ma na celu zmianę stanu aktywów banku o podaną wartość
    """
    with open("bank.txt", "r") as file:
        current_amount = float(file.read())

    new_amount = current_amount - amount_to_subtract

    if new_amount < 0:
        with open("bank.txt", "w") as file:
            file.write(str(round(current_amount, 2)))
        return 0

    with open("bank.txt", "w") as file:
        file.write(str(round(new_amount, 2)))

    return 1


def add_client_write(client):
    """
    Ta funkcja zapisuje nowo utworzonego klienta do pliku csv
    """
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
    """
    Ta funkcja zapisuje nowo utworzony kredyt do pliku csv
    """
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
                round(loan.installment_amount, 2)])


def refresh_cwl_write():
    """
    Ta funkcja odświeża listę klientów z kredytami. Pobiera
    ich z pliku csv i zmienia w format listy
    """
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
    """
    Ta funkcja odświeża listę wszystkich klientów zarejestrowanych
    w banku
    """
    clients = []

    with open('clients.txt', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                client = Client(int(row[0]), row[1], row[2])
                clients.append(f"{client.client_id}. "
                               f"{client.first_name} {client.last_name}")
    return clients


def read_date_from_file(file_name):
    """
    Ta funkcja odczytuje datę z pliku time.txt
    """
    with open(file_name, "r") as file:
        date_str = file.read().strip()
        return datetime.strptime(date_str, "%Y-%m-%d")


def write_date_to_file(file_name, date):
    """
    Ta funkcja zapisuje datę do pliku time.txt
    """
    with open(file_name, "w") as file:
        file.write(date.strftime("%Y-%m-%d"))


def add_month():
    """
    Ta funkcja dodaje miesiąc (30 dni) do daty pobranej z pliku csv
    """
    date_from_file = read_date_from_file("time.txt")
    new_date = date_from_file + timedelta(days=30)
    write_date_to_file("time.txt", new_date)
