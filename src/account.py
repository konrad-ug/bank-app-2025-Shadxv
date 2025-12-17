import os
import requests
from datetime import date
from abc import ABC, abstractmethod
class Account(ABC):
    def __init__(self):
        self.balance = 0
        self.history = []

    def transfer_in(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)
            return True
        return False

    def transfer_out(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)
            return True
        return False

    def express_transfer(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance:
            return False
        self.balance -= amount + self.get_express_transfer_cost()
        self.history.append(-amount)
        self.history.append(-self.get_express_transfer_cost())
        return True

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

# pragma: no cover
class FirmAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            if not self.validate_nip_via_mf(nip):
                raise ValueError("Company not registered!!")
            self.nip = nip
        else:
            self.nip = "Invalid"

    def get_express_transfer_cost(self):
        return 5

    def validate_nip_via_mf(self, nip):
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().strftime("%Y-%m-%d")
        endpoint = f"{base_url}/api/search/nip/{nip}?date={today}"

        try:
            response = requests.get(endpoint, timeout=5)
            data = response.json()

            print(f"\nNIP: {nip}, Response: {data}")

            if "result" in data and data["result"].get("subject"):
                status_vat = data["result"]["subject"].get("statusVat")
                return status_vat == "Czynny"

            return False
        except Exception as e:
            print(f"MF Error: {str(e)}")
            return False

    def take_loan(self, amount):
        if amount <= 0:
            return False
        if self.balance < 2*amount:
            return False
        if self.history.count(-1775) == 0:
            return False
        self.balance += amount
        return True
