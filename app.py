import tkinter as tk
from tkinter import ttk
from client import Client
from loan import Loan
import csv
import functions


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # dodawanie klientów - zmienne
        self.new_client_first_name = tk.StringVar()
        self.new_client_last_name = tk.StringVar()

        # dodawanie kredytów - zmienne
        self.loan_client = tk.StringVar()
        self.loan_amount = tk.StringVar()
        self.loan_percentage = tk.StringVar()
        self.loan_installment = tk.StringVar()

        # listy wyświetlane w ComboBoxach
        self.clients = []
        self.clients_with_loans = []

        # wybór klienta do sprawdzenia
        self.current_client = tk.StringVar()

        # ilość miesięcy do przesunięcia czasu
        self.months_forward = 0

        # root window
        self.title("Bank Simulator 95")
        self.geometry("1600x900")
        self.style = ttk.Style(self)
        self.style.theme_use("classic")

        retro_font = "Tahoma"  # MS Sans Serif
        font_style = ttk.Style()
        font_style.configure('.', font=(retro_font, 12))

        # notebook
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        main_page = ttk.Frame(notebook)
        add_client_page = ttk.Frame(notebook)
        add_loan_page = ttk.Frame(notebook)
        check_data_page = ttk.Frame(notebook)

        notebook.add(main_page, text="Strona Główna")
        notebook.add(add_client_page, text="Dodaj Klienta")
        notebook.add(add_loan_page, text="Dodaj Kredyt")
        notebook.add(check_data_page, text="Podgląd Danych")

        notebook.bind("<<NotebookTabChanged>>", self.refresh_data)

        # strona zwierająca dodawanie klientów
        add_client_center = ttk.Frame(add_client_page)
        add_client_center.pack(expand=True, fill="y", pady=(50, 0))

        add_client_header = ttk.Label(
            add_client_center,
            text="Dodaj klienta do "
            "listy kredytobiorców",
            font=(retro_font, 45))
        add_client_header.grid(column=0, row=0, columnspan=2)

        add_client_first_name_label = ttk.Label(
            add_client_center,
            text="Imię klienta",
            font=(retro_font, 20))
        add_client_first_name_label.grid(column=0, row=1, pady=(50, 50))

        self.add_client_first_name_entry = ttk.Entry(
            add_client_center,
            font=(retro_font, 20),
            textvariable=self.new_client_first_name)
        self.add_client_first_name_entry.grid(column=1, row=1)

        add_client_last_name_label = ttk.Label(
            add_client_center,
            text="Nazwisko klienta",
            font=(retro_font, 20))
        add_client_last_name_label.grid(column=0, row=2)

        self.add_client_last_name_entry = ttk.Entry(
            add_client_center,
            font=(retro_font, 20),
            textvariable=self.new_client_last_name)
        self.add_client_last_name_entry.grid(column=1, row=2)

        add_client_submit = ttk.Button(
            add_client_center,
            text="Dodaj Klienta",
            width=30,
            command=self.add_client)
        add_client_submit.grid(column=0, row=3, columnspan=2, pady=(50, 0))

        self.add_client_error_label = ttk.Label(
            add_client_center,
            text="",
            font=(retro_font, 20))
        self.add_client_error_label.grid(
            column=0, row=4, columnspan=2, pady=(50, 0))

        # strona główna
        main_page_center = ttk.Frame(main_page)
        main_page_center.pack(expand=True, fill="y", pady=(50, 0))

        main_page_header = ttk.Label(
            main_page_center,
            text="Witaj w Bank Simulator 95!",
            font=(retro_font, 60))
        main_page_header.grid(column=0, row=0)

        main_page_text = ttk.Label(
            main_page_center,
            text="Witaj w Bank Simulator 95! \n\n"
                 "Aplikacja symuluje udzielanie kredytów klientom banku."
                 " Ponieważ posiada tylko podstawowe funkcje, jest utrzymana "
                 "w stylistyce klasycznych systemów Windows. \n\n"
                 "W zakładce „Dodaj Klienta” możesz dodawać klientów "
                 "do bazy danych banku. \n\n"
                 "W zakładce „Dodaj Kredyt” możesz udzielić kredytu "
                 "użytkownikowi uprzednio dodanemu do bazy danych. \n\n"
                 "W zakładce „Podgląd Danych” masz dostęp do najważniejszej "
                 "części aplikacji – możesz zobaczyć, ile pieniędzy bank ma "
                 "na koncie oraz ile czasu klienci będą spłacać "
                 "swoje zobowiązania. Masz też tutaj dostęp do przewijania"
                 " czasu – możesz dzięki temu sprawdzić "
                 "stan konta po upłynięciu kilku miesięcy",
            font=(retro_font, 20),
            wraplength=800)
        main_page_text.grid(column=0, row=1)

        # strona zawierająca dodawanie kredytów
        loan_page_center = ttk.Frame(add_loan_page)
        loan_page_center.pack(expand=True, fill="y")

        loan_page_header = ttk.Label(
            loan_page_center,
            text="Udziel kredytu klientowi",
            font=(retro_font, 45))
        loan_page_header.grid(column=0, row=0, columnspan=2, pady=(50, 0))

        loan_client_label = ttk.Label(
            loan_page_center,
            text="Imię klienta",
            font=(retro_font, 20))
        loan_client_label.grid(column=0, row=1, pady=(50, 0))

        self.loan_client_entry = ttk.Combobox(
            loan_page_center,
            font=(retro_font, 20),
            values=self.clients,
            state="readonly",
            textvariable=self.loan_client)
        self.loan_client_entry.grid(column=1, row=1, pady=(50, 0))

        loan_amount_label = ttk.Label(
            loan_page_center,
            text="Kwota Kredytu",
            font=(retro_font, 20))
        loan_amount_label.grid(column=0, row=2, pady=(50, 0))

        self.loan_amount_entry = ttk.Entry(
            loan_page_center,
            font=(retro_font, 20),
            textvariable=self.loan_amount)
        self.loan_amount_entry.grid(column=1, row=2, pady=(50, 0))

        loan_percentage_label = ttk.Label(
            loan_page_center,
            text="Oprocentowanie",
            font=(retro_font, 20))
        loan_percentage_label.grid(column=0, row=3, pady=(50, 0))

        self.loan_percentage_entry = ttk.Entry(
            loan_page_center,
            font=(retro_font, 20),
            textvariable=self.loan_percentage)
        self.loan_percentage_entry.grid(column=1, row=3, pady=(50, 0))

        loan_installment_label = ttk.Label(
            loan_page_center,
            text="Ilość rat",
            font=(retro_font, 20))
        loan_installment_label.grid(column=0, row=4, pady=(50, 0))

        self.loan_installment_entry = ttk.Entry(
            loan_page_center,
            font=(retro_font, 20),
            textvariable=self.loan_installment)
        self.loan_installment_entry.grid(column=1, row=4, pady=(50, 0))

        loan_submit = ttk.Button(
            loan_page_center,
            text="Udziel Kredytu",
            width=30,
            command=self.add_loan)
        loan_submit.grid(column=0, row=5, columnspan=2, pady=(50, 0))

        self.loan_add_error = ttk.Label(
            loan_page_center,
            text="",
            font=(retro_font, 20))
        self.loan_add_error.grid(column=0, row=6, pady=(50, 0), columnspan=2)

        # strona zwierająca podgląd kredytów
        check_data_center = ttk.Frame(check_data_page)
        check_data_center.pack(expand=True, fill="y", pady=(50, 0))

        check_budget_frame = ttk.Frame(check_data_center)
        check_budget_frame.grid(column=0, row=0, columnspan=2, pady=(0, 75))
        select_client_frame = ttk.Frame(check_data_center)
        select_client_frame.grid(column=0, row=1, pady=(0, 50))
        check_loan_frame = ttk.Frame(check_data_center)
        check_loan_frame.grid(column=0, row=2, pady=(0, 75))
        time_forward_frame = ttk.Frame(check_data_center)
        time_forward_frame.grid(column=0, row=3)

        self.check_budget_label = ttk.Label(
            check_budget_frame,
            text="Bank ma na koncie 0 zł",
            font=(retro_font, 20))
        self.check_budget_label.pack()

        select_client_label = ttk.Label(
            select_client_frame,
            text="Wybierz klienta: ",
            font=(retro_font, 20))
        select_client_label.grid(column=0, row=0)

        self.select_client_entry = ttk.Combobox(
            select_client_frame,
            font=(retro_font, 20),
            values=self.clients_with_loans,
            state="readonly",
            textvariable=self.current_client)

        self.select_client_entry.bind(
            "<<ComboboxSelected>>",
            self.refresh_data)
        self.select_client_entry.grid(column=1, row=0)

        check_loan_label = ttk.Label(
            check_loan_frame,
            text="Oto parametry kredytu",
            font=(retro_font, 20))
        check_loan_label.grid(column=0, row=0)

        self.check_loan_label2 = ttk.Label(
            check_loan_frame,
            text="Wypożyczona Kwota: 0 zł",
            font=(retro_font, 20))
        self.check_loan_label2.grid(column=0, row=1, pady=(25, 0))

        self.check_loan_label3 = ttk.Label(
            check_loan_frame,
            text="Pozostało do spłaty: 0 zł w 0 miesięcy",
            font=(retro_font, 20))
        self.check_loan_label3.grid(column=0, row=2, pady=(25, 0))

        self.time_forward_label = ttk.Label(
            time_forward_frame,
            text="Ilość miesięcy do przewinięcia: 0",
            font=(retro_font, 20))
        self.time_forward_label.grid(column=0, row=0)

        self.time_forward_silder = ttk.Scale(
            time_forward_frame,
            from_=0, to=1,
            length=300,
            orient="horizontal", command=self.change_months)
        self.time_forward_silder.grid(column=0, row=1, pady=(25, 25))

        time_forward_button = ttk.Button(
            time_forward_frame,
            text="Przewiń",
            width=30,
            command=self.time_forward)
        time_forward_button.grid(column=0, row=2)

    # funkcja odświeżająca wyświetlane wartości dotyczące klientów
    def refresh_clients(self):
        self.clients = functions.refresh_c_write()
        self.loan_client_entry.configure(values=self.clients)
        self.select_client_entry.configure(values=self.clients)

    # funkcja odświeżająca klientów, którzy mają kredyt
    def refresh_clients_with_loans(self):
        self.clients_with_loans = functions.refresh_cwl_write()
        self.select_client_entry.configure(values=self.clients_with_loans)

    # funkcja odświeżająca informacje o kredytach
    def refresh_loans(self):
        loans = []
        client_id = self.select_client_entry.get()
        client_id = client_id.split(".")[0]

        with open("loans.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == client_id:
                    loans.append(row)

        for loan in loans:
            self.check_loan_label2.configure(
                text=f"Wypożyczona Kwota: {loan[2]} zł")
            rem_amount = round(float(loan[6]), 2) * round(float(loan[5]), 2)
            self.check_loan_label3.configure(
                text=f"Pozostało do spłaty: {round(rem_amount, 2)} zł w"
                f" {float(loan[5])} miesięcy")
            self.time_forward_silder.configure(to=int(loan[5]))

    # funkcja odświeżająca stan konta banku
    def refresh_bank(self):
        bank = 0
        with open("bank.txt", "r") as file:
            bank = float(file.read())
        self.check_budget_label.configure(
            text=f"Bank ma na koncie {bank:,} zł")

    # funkcja odświeżająca wszystko
    def refresh_data(self, event):
        self.refresh_clients()
        self.refresh_loans()
        self.refresh_bank()
        self.refresh_clients_with_loans()

    # funkcja dodająca klienta
    def add_client(self):
        client = Client()
        client.first_name = self.new_client_first_name.get()
        client.last_name = self.new_client_last_name.get()

        if client.first_name == "" or client.last_name == "":
            error = "Nieprawidłowa wartość"
            self.add_client_error_label.configure(text=error)
            print(error)
            return

        functions.add_client_write(client)
        self.add_client_first_name_entry.delete(0, "end")
        self.add_client_last_name_entry.delete(0, "end")

        error = "Udało się dodać klienta"
        self.add_client_error_label.configure(text=error)
        print(error)

    # funkcja dodająca kredyt, zawiera zabezpieczenia
    def add_loan(self):
        loan = Loan()
        loan.client_id = self.loan_client.get()
        loan.client_id = loan.client_id.split(".")[0]
        loan.amount = self.loan_amount.get()
        loan.percentage = self.loan_percentage.get()
        loan.installments = self.loan_installment.get()

        if not loan.client_id:
            error = "Nieprawidłowy ID klienta"
            print(error)
            self.loan_add_error.configure(text=error)
            return

        try:
            amount = float(loan.amount)
            percentage = float(loan.percentage)
        except ValueError:
            error = "Nieprawidłowa kwota lub oprocentowanie"
            print(error)
            self.loan_add_error.configure(text=error)
            return

        try:
            installments = int(loan.installments)
        except ValueError:
            error = "Liczba rat musi być liczbą całkowitą"
            self.loan_add_error.configure(text=error)
            print(error)
            return

        if amount == 0 or installments == 0:
            return

        interest_rate = percentage / 100 + 1
        installment_amount = amount * interest_rate / installments

        if self.update_bank(amount):
            loan.amount = amount
            loan.percentage = percentage
            loan.installments = installments
            loan.installment_amount = installment_amount
            functions.add_loan_write(loan)
            error = "Kredyt dodany prawidłowo"
            print(error)
            self.loan_add_error.configure(text=error)

            self.loan_amount_entry.delete(0, "end")
            self.loan_installment_entry.delete(0, "end")
            self.loan_percentage_entry.delete(0, "end")

        else:
            error = "Nie udało się udzielić kredytu. Bank jest zbyt biedny"
            print(error)
            self.loan_add_error.configure(text=error)

    # funkcja zmieniająca stan konta banku
    def update_bank(self, amount_to_subtract):
        return functions.update_bank(amount_to_subtract)

    # funkcja odpowiedzialna za przyspieszenie czasu
    def time_forward(self):
        functions.time_forward(self.months_forward)
        self.refresh_data(1)

    def change_months(self, value):
        self.months_forward = round(float(value))
        self.time_forward_label.configure(
                text=f"Ilość miesięcy do przewinięcia: {self.months_forward}")
