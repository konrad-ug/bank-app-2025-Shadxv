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

    def test_remove_from_registry(self):
        acc = PersonalAccount("X", "Y", "01234567898")
        registry = AccountRegistry()
        registry.add_account(acc)
        assert registry.count() == 1
        registry.delete("01234567898")
        assert registry.count() == 0

    def test_clear_registry(self):
        acc1 = PersonalAccount("X", "Y", "01234567898")
        acc2 = PersonalAccount("X", "Y", "01234567897")
        registry = AccountRegistry()
        registry.add_account(acc1)
        registry.add_account(acc2)
        assert registry.count() == 2
        registry.clear()
        assert registry.count() == 0
        assert registry.all_accounts() == []
