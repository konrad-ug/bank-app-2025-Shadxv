from flask import Flask, request, jsonify
from src.registry import AccountRegistry
from src.account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    searchResault = registry.find_account(data["pesel"])
    if searchResault is not None:
        return jsonify({"message": "Account with this PESEL already exists"}), 409
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    return jsonify({"count": registry.count()}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc = registry.find_account(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    acc = registry.find_account(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    if "name" in data:
        acc.first_name = data["name"]
    if "surname" in data:
        acc.last_name = data["surname"]
    if "pesel" in data:
        acc.pesel = data["pesel"]

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    registry.delete(pesel)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    acc = registry.find_account(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    transfer_type = data.get("type", "invalid")

    match transfer_type.lower():
        case 'incomming':
            amount = data.get("amount", 0)
            if not acc.transfer_in(amount):
                return jsonify({"error": "Invalid transfer amount"}), 400
            return jsonify({"message": "Transfer successful", "new_balance": acc.balance}), 200
        case 'outgoing':
            amount = data.get("amount", 0)
            if not acc.transfer_out(amount):
                return jsonify({"error": "Invalid transfer amount"}), 400
            return jsonify({"message": "Transfer successful", "new_balance": acc.balance}), 200
        case 'express':
            amount = data.get("amount", 0)

            if not acc.express_transfer(amount):
                return jsonify({"error": "Invalid transfer amount"}), 400
            return jsonify({"message": "Express transfer successful", "new_balance": acc.balance}), 200

    return jsonify({"error": "Invalid transfer type"}), 400
