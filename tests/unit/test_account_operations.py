from src.account import Account

class TestOperations:
    def test_transfer_in(self):
        account = Account("John", "Doe", None)
        account.transfer_in(1000)
        assert account.balance == 1000
        account.transfer_in(-1000)
        assert account.balance == 1000
        account.transfer_in(0)
        assert account.balance == 1000
        account.transfer_in(100)
        assert account.balance == 1100

    def test_transfer_out(self):
        account = Account("John", "Doe", None)
        account.transfer_in(1000)
        account.transfer_out(100)
        assert account.balance == 900
        account.transfer_out(-100)
        assert account.balance == 900
        account.transfer_out(0)
        assert account.balance == 900
        account.transfer_out(100)
        assert account.balance == 800
