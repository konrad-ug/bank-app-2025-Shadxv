from src.account import PersonalAccount, FirmAccount

class TestOperations:
    def test_transfer_in(self):
        account = PersonalAccount("John", "Doe", None)
        account.transfer_in(1000)
        assert account.balance == 1000
        account.transfer_in(-1000)
        assert account.balance == 1000
        account.transfer_in(0)
        assert account.balance == 1000
        account.transfer_in(100)
        assert account.balance == 1100

    def test_transfer_out(self):
        account = PersonalAccount("John", "Doe", None)
        account.transfer_in(1000)
        account.transfer_out(100)
        assert account.balance == 900
        account.transfer_out(-100)
        assert account.balance == 900
        account.transfer_out(0)
        assert account.balance == 900
        account.transfer_out(1000)
        assert account.balance == 900
        account.transfer_out(100)
        assert account.balance == 800

    def test_firm_account(self):
        account = FirmAccount("Apple Inc.", "1234567890")
        assert account.company_name == "Apple Inc."
        assert account.nip == "1234567890"
        assert account.balance == 0
        account2 = FirmAccount("Apple Inc.", "123")
        assert account2.nip == "Invalid"
        account3 = FirmAccount("Apple Inc.", "123456789098")
        assert account3.nip == "Invalid"
        account4 = FirmAccount("Apple Inc.", None)
        assert account4.nip == "Invalid"
        account5 = FirmAccount("Apple Inc.", "abcdefghij")
        assert account5.nip == "Invalid"
