from src.account import PersonalAccount, FirmAccount

class TestHistory:

    def test_personal_account_history(self):
        account = PersonalAccount("John", "Doe", "12345678901", "PROM_ABC")
        account.transfer_in(200)
        account.transfer_out(50)
        account.express_transfer(30)
        expected_history = [200, -50, -30, -1]
        assert account.history == expected_history

    def test_firm_account_history(self):
        account = FirmAccount("Apple Inc.", "1234567890")
        account.transfer_in(500)
        account.transfer_out(200)
        account.express_transfer(100)
        expected_history = [500, -200, -100, -5]
        assert account.history == expected_history
