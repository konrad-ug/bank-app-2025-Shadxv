import requests
import pytest

class TestPerformance():

    URL = "http://127.0.0.1:5000/api/accounts"

    @pytest.fixture
    def acc_data(self):
        return {
            "name": "Perf",
            "surname": "Test",
            "pesel": "99012345678"
        }

    def test_create_delete_time(self, acc_data):
        for _ in range(100):
            r = requests.post(self.URL, json=acc_data, timeout=0.5)
            assert r.status_code == 201
            r = requests.delete(f"{self.URL}/{acc_data['pesel']}", timeout=0.5)
            assert r.status_code == 200

    def test_transactions_time(self, acc_data):
        r = requests.post(self.URL, json=acc_data)
        assert r.status_code == 201

        for _ in range(100):
            transfer_data = {
                "amount": 100,
                "type": "incomming"
            }
            r = requests.post(f"{self.URL}/{acc_data['pesel']}/transfer", json=transfer_data, timeout=0.5)
            assert r.status_code == 200

        r = requests.get(f"{self.URL}/{acc_data['pesel']}")
        assert r.status_code == 200
        assert r.json()["balance"] == 10000

        r = requests.delete(f"{self.URL}/{acc_data['pesel']}")
        assert r.status_code == 200
