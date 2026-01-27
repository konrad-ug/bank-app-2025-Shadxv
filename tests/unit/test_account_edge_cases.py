import pytest
from src.account import PersonalAccount, is_born_after_1960

class TestAccountEdgeCases:

    def test_invalid_transfers(self):
        account = PersonalAccount("Test", "User", "12345678901")
        account.balance = 100
        
        assert not account.transfer_in(0), "transfer_in should fail for zero amount"
        assert not account.transfer_in(-50), "transfer_in should fail for negative amount"
        assert account.balance == 100, "Balance should not change after failed transfer_in"

        assert not account.transfer_out(0), "transfer_out should fail for zero amount"
        assert not account.transfer_out(-50), "transfer_out should fail for negative amount"
        assert account.balance == 100, "Balance should not change after failed transfer_out"

        assert not account.express_transfer(0), "express_transfer should fail for zero amount"
        assert not account.express_transfer(-50), "express_transfer should fail for negative amount"
        assert account.balance == 100, "Balance should not change after failed express_transfer"

    def test_loan_submission_insufficient_history(self):
        account = PersonalAccount("Test", "User", "12345678901")
        account.history = [100, 100, -50, 100] # Only 4 items
        assert not account.submit_for_loan(50), "Loan should not be granted with insufficient history"

    def test_are_last_three_income_not_enough_history(self):
        account = PersonalAccount("Test", "User", "12345678901")
        account.history = [100, 100]
        assert not account.are_last_three_income(), "Should be false if history has less than 3 items"

    def test_account_creation_edge_cases(self):
        account_invalid_pesel = PersonalAccount("Test", "User", "123")
        assert account_invalid_pesel.pesel == "Invalid"
        assert account_invalid_pesel.balance == 0, "Balance should be 0 for invalid PESEL with promo"

        account_invalid_promo = PersonalAccount("Test", "User", "90010112345", promo_code="INVALID")
        assert account_invalid_promo.balance == 0, "Balance should be 0 for invalid promo code"
        
        account_old_person = PersonalAccount("Test", "User", "50010112345", promo_code="PROM_ABC")
        assert account_old_person.balance == 0, "Balance should be 0 for person born before 1960"

    def test_is_born_after_1960_error_handling(self):
        assert not is_born_after_1960("not_a_num"), "Should handle non-numeric PESEL gracefully"

    def test_initial_history_is_empty(self):
        account = PersonalAccount("Test", "User", "12345678901")
        assert account.history == [], "Account history should be empty on creation"
        
    def test_send_history_not_implemented(self, mocker):
        account = PersonalAccount("Test", "User", "12345678901")
        mock_send = mocker.patch("lib.smtp.SMTPClient.send", return_value=False)
        result = account.send_history_via_email("test@test.com")
        assert result is False
