from tkinter import *
from tkinter import ttk
from tkinter import font

class App(Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title("Bank Simulator 2002")
        self.geometry("1600x900")
        self.style = ttk.Style(self)
        self.style.theme_use("classic")

        retro_font = "Tahoma" #MS Sans Serif
        font_style = ttk.Style()
        font_style.configure('.', font=(retro_font, 12))

        #notebook
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

        #dodawanie klientów
        add_client_center = ttk.Frame(add_client_page)
        add_client_center.pack(expand=True, fill="y", pady=(50,0))

        add_client_header = ttk.Label(add_client_center, text="Dodaj klienta do listy kredytobiorców", font=(retro_font, 45))
        add_client_header.grid(column=0, row=0, columnspan=2)

        add_client_first_name_label = ttk.Label(add_client_center, text="Imię klienta", font=(retro_font, 20))
        add_client_first_name_label.grid(column=0, row=1, pady=(50,50))
        add_client_first_name_entry = ttk.Entry(add_client_center, font=(retro_font, 20))
        add_client_first_name_entry.grid(column=1, row=1)

        add_client_last_name_label = ttk.Label(add_client_center, text="Nazwisko klienta", font=(retro_font, 20))
        add_client_last_name_label.grid(column=0, row=2)
        add_client_last_name_entry = ttk.Entry(add_client_center, font=(retro_font, 20))
        add_client_last_name_entry.grid(column=1, row=2)

        add_client_submit = ttk.Button(add_client_center, text="Dodaj Klienta", width=30)
        add_client_submit.grid(column=0, row=3, columnspan=2, pady=(50,0))

        #strona główna
        main_page_center = ttk.Frame(main_page)
        main_page_center.pack(expand=True, fill="y", pady=(50,0))

        main_page_header = ttk.Label(main_page_center, text="Witaj w aplikacji banku!", font=(retro_font, 60))
        main_page_header.grid(column=0, row=0)
        main_page_text = ttk.Label(main_page_center,
                                   text="Lorem ispum "
                                   "Dolor sit amet",
                                   font=(retro_font, 20),
                                   wraplength=800)
        main_page_text.grid(column=0, row=1)

        #dodawanie kredytów
        clients = ["Klient 1", "Klient 2", "Klient 3"]

        loan_page_center = ttk.Frame(add_loan_page)
        loan_page_center.pack(expand=True, fill="y")

        loan_page_header = ttk.Label(loan_page_center, text="Udziel kredytu klientowi", font=(retro_font, 45))
        loan_page_header.grid(column=0, row=0, columnspan=2, pady=(50, 0))

        loan_client_label = ttk.Label(loan_page_center, text="Imię klienta", font=(retro_font, 20))
        loan_client_label.grid(column=0, row=1, pady=(50, 0))
        loan_client_entry = ttk.Combobox(loan_page_center, font=(retro_font, 20), values=clients, state="readonly")
        loan_client_entry.grid(column=1, row=1, pady=(50, 0))

        loan_amount_label = ttk.Label(loan_page_center, text="Kwota Kredytu", font=(retro_font, 20))
        loan_amount_label.grid(column=0, row=2, pady=(50, 0))
        loan_amount_entry = ttk.Entry(loan_page_center, font=(retro_font, 20))
        loan_amount_entry.grid(column=1, row=2, pady=(50, 0))

        loan_percentage_label = ttk.Label(loan_page_center, text="Oprocentowanie", font=(retro_font, 20))
        loan_percentage_label.grid(column=0, row=3, pady=(50, 0))
        loan_percentage_entry = ttk.Entry(loan_page_center, font=(retro_font, 20))
        loan_percentage_entry.grid(column=1, row=3, pady=(50, 0))

        loan_installment_label = ttk.Label(loan_page_center, text="Ilość rat", font=(retro_font, 20))
        loan_installment_label.grid(column=0, row=4, pady=(50, 0))
        loan_installment_entry = ttk.Entry(loan_page_center, font=(retro_font, 20))
        loan_installment_entry.grid(column=1, row=4, pady=(50, 0))

        loan_submit = ttk.Button(loan_page_center, text="Zaakceptuj Kredyt", width=30)
        loan_submit.grid(column=0, row=5, columnspan=2, pady=(50, 0))

        #podgląd kredytów
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

        check_budget_label = ttk.Label(check_budget_frame, text="Bank ma na koncie 2137690 zł", font=(retro_font, 20))
        check_budget_label.pack()

        select_client_label = ttk.Label(select_client_frame, text="Wybierz klienta", font=(retro_font, 20))
        select_client_label.grid(column=0, row=0)
        select_client_entry = ttk.Combobox(select_client_frame, font=(retro_font, 20), values=clients, state="readonly")
        select_client_entry.grid(column=1, row=0)

        check_loan_label = ttk.Label(check_loan_frame, text="Oto parametry kredytu", font=(retro_font, 20))
        check_loan_label.grid(column=0, row=0)
        check_loan_label2 = ttk.Label(check_loan_frame, text="Wypożyczona Kwota: 10000 zł", font=(retro_font, 20))
        check_loan_label2.grid(column=0, row=1, pady=(25, 0))
        check_loan_label3 = ttk.Label(check_loan_frame, text="Pozostało do spłaty: 9000 zł w 10 miesięcy", font=(retro_font, 20))
        check_loan_label3.grid(column=0, row=2, pady=(25, 0))

        time_forward_label = ttk.Label(time_forward_frame, text="Przewiń czas o miesiąc do przodu", font=(retro_font, 20))
        time_forward_label.grid(column=0, row=0)
        time_forward_button = ttk.Button(time_forward_frame, text="Przewiń", width=30)
        time_forward_button.grid(column=0, row=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
