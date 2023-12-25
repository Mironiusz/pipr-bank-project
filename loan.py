class Loan:
    def __init__(self, loan_id="", client_id="", amount="", percentage="",
                 installments="", remaining_installments="",
                 installment_amount=""):
        self.loan_id = loan_id
        self.client_id = client_id
        self.amount = amount
        self.percentage = percentage
        self.installments = installments
        self.remaining_installments = remaining_installments
        self.installment_amount = installment_amount
