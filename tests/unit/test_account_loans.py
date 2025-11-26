from src.account import PersonalAccount
import pytest

class TestLoans:

    @pytest.fixture
    def account(self):
        return PersonalAccount("Alice", "Smith", "65012345678")

    @pytest.mark.parametrize("history,amount,expected",
                             [
                                 ([100, 150, 200], -100, 0),
                                 ([100, 150, 200], 500, 500),
                                 ([1000, -50, 30, -20, 10], 300, 300),
                                 ([100, -50], 100, 0),
                                 ([1000, -800, 20, 200, -100, -200], 400, 0),
                             ])
    def test_loans(self, account, history, amount, expected):
        account.history = history
        account.submit_for_loan(amount)
        assert account.balance == expected

    # def test_negative_loan(self, account):
    #     account.history = [100, 150, 200]
    #     assert account.submit_for_loan(-100) == False
    #     assert account.balance == 0

    # def test_3_income(self, account):
    #     account.history = [100, 150, 200]
    #     assert account.are_last_three_income() == True
    #     assert account.submit_for_loan(500) == True
    #     assert account.balance == 500

    # def test_5_transactions_higher_than_loan(self, account):
    #     account.history = [1000, -50, 30, -20, 10]
    #     assert account.are_last_three_income() == False
    #     assert account.submit_for_loan(300) == True
    #     assert account.balance == 300

    # def test_2_transactions(self, account):
    #     account.history = [100, -50]
    #     assert account.are_last_three_income() == False
    #     assert account.submit_for_loan(100) == False
    #     assert account.balance == 0

    # def test_last_5_transactions_lower_than_loan(self, account):
    #     account.history = [1000, -800, 20, 200, -100, -200]
    #     assert account.are_last_three_income() == False
    #     assert account.submit_for_loan(400) == False
    #     assert account.balance == 0
