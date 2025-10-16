from flask import Flask, jsonify, request
from flask_cors import CORS
from db import supabase
from datetime import datetime, timedelta
from functions import (
    get_amount_for_rule,
    get_country_for_rule,
    generate_transaction_ref,
    get_random_banking_source
)
import random, os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({"message": "✅ Flask server connected successfully"})

# ---------------------------
# RULES ENDPOINTS
# ---------------------------
@app.route("/rules", methods=["GET"])
def get_rules():
    """
    Returns all AML rules.
    """
    data = supabase.table("rules").select("*").execute()
    return jsonify(data.data)

@app.route("/rules", methods=["POST"])
def add_rule():
    """
    Add a new AML rule (optional, admin use).
    """
    payload = request.json
    result = supabase.table("rules").insert(payload).execute()
    return jsonify(result.data), 201

# ---------------------------
# TENANTS ENDPOINTS
# ---------------------------
@app.route("/tenants", methods=["GET"])
def get_tenants():
    """
    Returns all tenants for dropdown selection.
    """
    data = supabase.table("tenants").select("*").execute()
    return jsonify(data.data)

@app.route("/tenants", methods=["POST"])
def add_tenant():
    """
    Add a new tenant (optional, admin use).
    """
    payload = request.json
    result = supabase.table("tenants").insert(payload).execute()
    return jsonify(result.data), 201

# ---------------------------
# TRANSACTIONS ENDPOINTS
# ---------------------------
@app.route("/transactions", methods=["GET"])
def get_transactions():
    '''
    Returns all transactions.
    '''
    data = supabase.table("transactions").select("*").limit(20).execute()
    return jsonify(data.data)

@app.route("/transactions", methods=["POST"])
def add_transaction():
    """
    Add a new transaction (optional, admin use).
    """
    payload = request.json
    result = supabase.table("transactions").insert(payload).execute()
    return jsonify(result.data), 201

# Generate Transactions
@app.route("/generate_transactions", methods=["POST"])
def generate_transactions():
    """
    Generate test AML transactions dynamically for POS and NEG scenarios.
    Exports results to a .txt file that mimics the 'Response' layout.
    Expects JSON:
    {
        "tenant_code": "SG",
        "transaction_date": "2025-10-16",
        "scenario": "POS" or "NEG",
        "rule_codes": ["AML-TRX-ALL-A-01", "AML-TRX-ALL-B-02", ...]
    }
    """
    try:
        data = request.get_json()
        tenant_code = data.get("tenant_code")
        transaction_date = data.get("transaction_date") or datetime.now().strftime("%Y-%m-%d")
        scenario = data.get("scenario", "POS").upper()
        rule_codes = data.get("rule_codes", [])

        if not tenant_code or not rule_codes:
            return jsonify({"error": "tenant_code and rule_codes are required"}), 400

        # create output folder
        os.makedirs("exports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exports/transactions_{tenant_code}_{timestamp}.txt"

        transactions = []

        with open(filename, "w") as file:
            for rule_code in rule_codes:
                txn_id = generate_transaction_ref()
                amount = get_amount_for_rule(rule_code, scenario)
                to_country = get_country_for_rule(rule_code, scenario)
                from_country = "SG"
                currency = "SGD"
                source_system = get_random_banking_source()

                block = (
                    f"{tenant_code}\n"
                    f"{transaction_date}\n"
                    f"{txn_id}\n"
                    f"{rule_code}\n"
                    f"{amount}\n"
                    f"{currency}\n"
                    f"{source_system}\n"
                    f"{from_country}-{to_country}\n"
                    + "-" * 40 + "\n"
                )

                file.write(block)
                transactions.append({
                    "tenant_code": tenant_code,
                    "transaction_date": transaction_date,
                    "transaction_ref": txn_id,
                    "rule_code": rule_code,
                    "amount": amount,
                    "currency_code": currency,
                    "banking_source": source_system,
                    "from_country": from_country,
                    "to_country": to_country
                })

        return jsonify({
            "message": f"✅ Generated {len(transactions)} transactions for {tenant_code} ({scenario})",
            "export_file": filename,
            "transactions": transactions
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask server connected and running at http://127.0.0.1:5000")
    app.run(debug=True)