from src.account import PersonalAccount, is_born_after_1960


class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", None)
        assert account.first_name == "John"
        assert account.last_name == "Doe"

    def test_account_balance(self):
        account = PersonalAccount("John", "Doe", None)
        assert account.balance == 0

    def test_account_pesel(self):
        account = PersonalAccount("John", "Doe", "01010101010")
        assert account.pesel == "01010101010"

    def test_validate_pesel(self):
        account1 = PersonalAccount("John", "Doe", "123456789098765")
        assert account1.pesel == "Invalid"
        account2 = PersonalAccount("John", "Smith", "1234")
        assert account2.pesel == "Invalid"
        account3 = PersonalAccount("John", "Baker", "12345678909")
        assert account3.pesel == "12345678909"

    def test_promo_code(self):
        account1 = PersonalAccount("John", "Doe", None, None)
        assert account1.balance == 0
        account2 = PersonalAccount("John", "Doe", "12345678901", "PROM_ABC")
        assert account2.balance == 50
        account3 = PersonalAccount("John", "Doe", None, "PROM-ABC")
        assert account3.balance == 0
        account4 = PersonalAccount("John", "Doe", None, "PROM_ABCD")
        assert account4.balance == 0
        account5 = PersonalAccount("John", "Doe", None, "PROM_AB")
        assert account5.balance == 0
        account6 = PersonalAccount("John", "Doe", None, "PRO-ABC")
        assert account6.balance == 0

    def test_birth_year(self):
        account1 = PersonalAccount("John", "Doe", None, "PROM_ABC")
        assert is_born_after_1960(account1.pesel) is False
        assert account1.balance == 0
        account2 = PersonalAccount("John", "Doe", "12345678901", "PROM_ABC")
        assert is_born_after_1960(account2.pesel) is True
        assert account2.balance == 50
