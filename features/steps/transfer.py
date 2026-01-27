from behave import *
import requests

URL = "http://localhost:5000"

@given('an account with balance {balance:d}')
def step_impl(context, balance):
    context.pesel = "12345678901"
    requests.delete(URL + f"/api/accounts/{context.pesel}")
    
    json_body = { "name": "Test", "surname": "User", "pesel": context.pesel }
    create_resp = requests.post(URL + "/api/accounts", json = json_body)
    assert create_resp.status_code == 201
    
    if balance > 0:
        transfer_body = { "type": "incomming", "amount": balance }
        resp = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=transfer_body)
        assert resp.status_code == 200

@when('I receive a transfer of {amount:d}')
def step_impl(context, amount):
    transfer_body = { "type": "incomming", "amount": amount }
    context.response = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=transfer_body)

@then('the account balance should be {balance:d}')
def step_impl(context, balance):
    response = requests.get(URL + f"/api/accounts/{context.pesel}")
    assert response.status_code == 200
    assert response.json()["balance"] == balance

@when('I send a transfer of {amount:d}')
def step_impl(context, amount):
    transfer_body = { "type": "outgoing", "amount": amount }
    context.response = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=transfer_body)

@when('I try to send a transfer of {amount:d}')
def step_impl(context, amount):
    transfer_body = { "type": "outgoing", "amount": amount }
    context.response = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=transfer_body)

@then('the transfer should fail')
def step_impl(context):
    assert context.response.status_code != 200

@then('the account balance should remain {balance:d}')
def step_impl(context, balance):
    response = requests.get(URL + f"/api/accounts/{context.pesel}")
    assert response.status_code == 200
    assert response.json()["balance"] == balance

@when('I make an express transfer of {amount:d}')
def step_impl(context, amount):
    transfer_body = { "type": "express", "amount": amount }
    context.response = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=transfer_body)
