from src.account import FirmAccount
import pytest

class TestFirmLoans:

    @pytest.fixture
    def account(self):
        return FirmAccount("Apple", None)

    @pytest.mark.parametrize("history,balance,amount,expected,condition_expected",
                             [
                                 ([100, 150, 200], 450, 100, 450, False),
                                 ([100, 150, 200], 450, 0, 450, False),
                                 ([100, 150, 200], 450, -1, 450, False),
                                 ([2000, -1775], 225, 125, 225, False),
                                 ([3000, -1775], 1225, 125, 1350, True),
                                 ([3000, -1775, 3000, -1775, -450], 2000, 1000, 3000, True),
                             ])
    def test_loans(self, account, history, balance, amount, expected, condition_expected):
        account.history = history
        account.balance = balance
        assert account.take_loan(amount) == condition_expected
        assert account.balance == expected
