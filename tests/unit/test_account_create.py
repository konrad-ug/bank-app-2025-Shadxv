from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", None)
        assert account.first_name == "John"
        assert account.last_name == "Doe"

    def test_account_balance(self):
        account = Account("John", "Doe", None)
        assert account.balance == 0

    def test_account_pesel(self):
        account = Account("John", "Doe", "01010101010")
        assert account.pesel == "01010101010"

    def test_validate_pesel(self):
        account1 = Account("John", "Doe", "123456789098765")
        assert account1.pesel == "Invalid"
        account2 = Account("John", "Smith", "1234")
        assert account2.pesel == "Invalid"
        account3 = Account("John", "Baker", "12345678909")
        assert account3.pesel == "12345678909"
