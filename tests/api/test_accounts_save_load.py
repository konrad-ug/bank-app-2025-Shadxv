import pytest
import requests

URL = "http://localhost:5000"

def test_save_and_load_accounts():
    requests.get(URL + "/api/accounts")
    
    acc_data = {"name": "Test", "surname": "User", "pesel": "12345678901"}
    requests.post(URL + "/api/accounts", json=acc_data)

    resp = requests.post(URL + "/api/accounts/save")
    assert resp.status_code == 200
    
    requests.delete(URL + "/api/accounts/12345678901")
    
    resp = requests.get(URL + "/api/accounts/12345678901")
    assert resp.status_code == 404
    
    resp = requests.post(URL + "/api/accounts/load")
    assert resp.status_code == 200
    
    resp = requests.get(URL + "/api/accounts/12345678901")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test"
    assert data["surname"] == "User"
