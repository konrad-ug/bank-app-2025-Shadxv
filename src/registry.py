class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def find_account(self, pesel):
        matches = [acc for acc in self.accounts if acc.pesel == pesel]
        return matches[0] if matches else None

    def all_accounts(self):
        return self.accounts

    def count(self):
        return len(self.accounts)

    def delete(self, pesel):
        self.accounts = [acc for acc in self.accounts if acc.pesel != pesel]
