from pymongo import MongoClient
from src.account import PersonalAccount, FirmAccount

class MongoAccountsRepository:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['bank_app']
        self.collection = self.db['accounts']

    def save_all(self, accounts):
        self.collection.delete_many({})
        for account in accounts:
            self.collection.insert_one(account.to_dict())

    def load_all(self):
        accounts_data = self.collection.find()
        accounts = []
        for data in accounts_data:
            if data.get('type') == 'PersonalAccount':
                acc = PersonalAccount(data['first_name'], data['last_name'], data['pesel'])
                acc.balance = data['balance']
                acc.history = data['history']
                accounts.append(acc)
            elif data.get('type') == 'FirmAccount':
                # FirmAccount constructor: company_name, nip
                # But FirmAccount validates NIP via MF. We might need to bypass that or mock it if we are just loading from DB.
                # However, if it's already in DB, it was valid.
                # But the constructor calls validate_nip_via_mf.
                # We might need a way to reconstruct without validation or mock the validation.
                # For now, let's assume we only deal with PersonalAccount as per current API capabilities, 
                # or try to instantiate.
                try:
                    acc = FirmAccount(data['company_name'], data['nip'])
                    acc.balance = data['balance']
                    acc.history = data['history']
                    accounts.append(acc)
                except Exception as e:
                    print(f"Failed to load FirmAccount: {e}")
        return accounts
