class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        if isinstance(pesel, str) and len(pesel) == 11 and pesel.isdigit():
            self.pesel = pesel
        else:
            self.pesel = "Invalid"
        if isinstance(promo_code, str) and promo_code.startswith("PROM_") and len(promo_code) == 8 and self.is_born_after_1960(self.pesel):
            self.balance += 50

    def is_born_after_1960(self, pesel):
        birth_year_str = pesel[0:2]
        try:
            birth_year = int(birth_year_str)
            return birth_year > 60 or (birth_year < 25)
        except:
            return False
