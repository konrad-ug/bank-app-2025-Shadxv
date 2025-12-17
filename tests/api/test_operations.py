from src.account import PersonalAccount
import pytest
import requests

class TestOperations:

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

    def test_transfer_in_out(self, set_up):
        transfer_data = {
            "amount": 500,
            "type": "incomming"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 200

        r = requests.get(f"{self.URL}/65012345678")
        assert r.status_code == 200
        assert r.json()["balance"] == 500

        transfer_data = {
            "amount": 200,
            "type": "outgoing"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 200

        r = requests.get(f"{self.URL}/65012345678")
        assert r.status_code == 200
        assert r.json()["balance"] == 300

    def test_express_transfer(self, set_up):
        transfer_data = {
            "amount": 100,
            "type": "incomming"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 200

        transfer_data = {
            "amount": 50,
            "type": "express"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 200

        r = requests.get(f"{self.URL}/65012345678")
        assert r.status_code == 200
        assert r.json()["balance"] == 49

    def test_transfer_to_invalid_pesel(self, set_up):
        transfer_data = {
            "amount": 100,
            "type": "in"
        }
        r = requests.post(f"{self.URL}/00000000000/transfer", json=transfer_data)
        assert r.status_code == 404

    def test_invalid_amount_transfer(self, set_up):
        transfer_data = {
            "amount": -100,
            "type": "in"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 400

        transfer_data = {
            "amount": 0,
            "type": "out"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 400

        transfer_data = {
            "amount": -50,
            "type": "express"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 400

        transfer_data = {
            "type": "express"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 400

    def test_invalid_type_transfer(self, set_up):
        transfer_data = {
            "amount": 100,
            "type": "invalid_type"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 400

        transfer_data = {
            "amount": 100,
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 400

    def test_transfer_without_balance(self, set_up):
        transfer_data = {
            "amount": 50,
            "type": "express"
        }
        r = requests.post(f"{self.URL}/65012345678/transfer", json=transfer_data)
        assert r.status_code == 400
