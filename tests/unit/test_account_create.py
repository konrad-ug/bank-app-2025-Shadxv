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
