from src.account import PersonalAccount
import pytest
import requests

class TestCRUD:

    URL = "http://127.0.0.1:5000/api/accounts"

    @pytest.fixture
    def set_up(self):
        account_data = {
            "name": "Alice",
            "surname": "Smith",
            "pesel": "65012345678"
        }
        r = requests.post(self.URL, json=account_data)
        assert r.status_code == 201
        yield
        response = requests.get(self.URL)
        for acc in response.json():
            requests.delete(f"{self.URL}/{acc['pesel']}")

    def test_create_account(self, set_up):
        r = requests.get(self.URL + "/count")
        assert r.status_code == 200
        assert r.json()["count"] == 1

    def test_accounts_limit(self, set_up):
        account_data = {
            "name": "Bob",
            "surname": "Johnson",
            "pesel": "65012345679"
        }
        r1 = requests.post(self.URL, json=account_data)
        assert r1.status_code == 201
        r2 = requests.post(self.URL, json=account_data)
        assert r2.status_code == 409

    def test_find_account(self, set_up):
        r = requests.get(self.URL + "/65012345678")
        assert r.status_code == 200
        assert r.json()["name"] == "Alice"
        assert r.json()["surname"] == "Smith"
        assert r.json()["pesel"] == "65012345678"

    def test_find_account_404(self, set_up):
        r = requests.get(self.URL + "/00000000000")
        assert r.status_code == 404

    def test_update_account(self, set_up):
        update_data = {
            "name": "Bob",
            "surname": "Johnson",
            "pesel": "65012345679"
        }
        r = requests.patch(self.URL + "/65012345678", json=update_data)
        assert r.status_code == 200

        r = requests.get(self.URL + "/65012345679")
        assert r.status_code == 200
        assert r.json()["name"] == "Bob"
        assert r.json()["surname"] == "Johnson"
        assert r.json()["pesel"] == "65012345679"

    def test_delete_account(self, set_up):
        r = requests.delete(self.URL + "/65012345678")
        assert r.status_code == 200

        r = requests.get(self.URL + "/65012345678")
        assert r.status_code == 404
