from src.account import PersonalAccount
from src.registry import AccountRegistry
import pytest

class TestRegistry:

   def test_registry(self):
        acc1 = PersonalAccount("X", "Y", "01234567898")
        acc2 = PersonalAccount("X", "Y", "01234567897")

        registry = AccountRegistry()
        registry.add_account(acc1)
        registry.add_account(acc2)
        assert registry.count() == 2
        assert registry.find_account("01234567898") == acc1
        assert registry.find_account("01234567899") == None
        assert registry.all_accounts() == [acc1, acc2]
