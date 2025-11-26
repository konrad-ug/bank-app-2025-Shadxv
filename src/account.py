from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self):
        self.balance = 0
        self.history = []

    def transfer_in(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)

    def transfer_out(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)

    def express_transfer(self, amount):
        if amount <= 0:
            return
        if amount > self.balance:
            return
        self.balance -= amount + self.get_express_transfer_cost()
        self.history.append(-amount)
        self.history.append(-self.get_express_transfer_cost())

    @abstractmethod
    def get_express_transfer_cost(self):
        """Abstract get express transfer costs. Implemented in subclasses"""

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        if isinstance(pesel, str) and len(pesel) == 11 and pesel.isdigit():
            self.pesel = pesel
        else:
            self.pesel = "Invalid"
        if isinstance(promo_code, str) and promo_code.startswith("PROM_") and len(promo_code) == 8 and is_born_after_1960(self.pesel):
            self.balance += 50

    def get_express_transfer_cost(self):
        return 1

    def submit_for_loan(self, amount):
        if amount <= 0:
            return False
        if self.are_last_three_income() or (len(self.history) >= 5 and sum(self.history[-5:]) > amount):
            self.balance += amount
            return True
        return False

    def are_last_three_income(self):
        if len(self.history) < 3:
            return False
        return all(x > 0 for x in self.history[-3:])


def is_born_after_1960(pesel):
    birth_year_str = pesel[0:2]
    try:
        birth_year = int(birth_year_str)
        return birth_year > 60 or (birth_year < 25)
    except:
        return False

class FirmAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        if nip and len(nip) == 10 and nip.isdigit():
            self.nip = nip
        else:
            self.nip = "Invalid"

    def get_express_transfer_cost(self):
        return 5
