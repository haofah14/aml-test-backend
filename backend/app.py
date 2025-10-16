from flask import Flask, jsonify, request
from flask_cors import CORS
from db import supabase
from datetime import datetime, timedelta
from functions import (
    get_amount_for_rule,
    get_country_for_rule,
    generate_transaction_id
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

@app.route("/generate_transactions", methods=["POST"])
def generate_transactions():
    """
    Generate AML transactions dynamically for POS and NEG scenarios.
    Export results to a .txt file in Actimize-style format.
    JSON body:
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
        transaction_date = data.get("transaction_date") 
        scenario = data.get("scenario", "POS").upper()
        rule_codes = data.get("rule_codes", [])

        if not tenant_code or not rule_codes:
            return jsonify({"error": "tenant_code and rule_codes are required"}), 400
        
        os.makedirs("transactions", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transactions/transactions_{tenant_code}_{timestamp}.txt"

        tenant_data = supabase.table("tenants").select("currency_code").eq("tenant_code", tenant_code).execute().data
        currency = tenant_data[0]["currency_code"] if tenant_data and tenant_data[0].get("currency_code") else "SGD"

        sources_data = supabase.table("banking_sources").select("id").execute().data
        banking_sources = [s["id"] for s in sources_data] if sources_data else ["RBK"]

        txn_time = datetime.now().strftime("%H%M%S")

        transactions = []

        with open(filename, "w", encoding="utf-8") as file:
            for rule_code in rule_codes:
                txn_id = generate_transaction_id()
                amount = get_amount_for_rule(rule_code, scenario)
                to_country = get_country_for_rule(rule_code, scenario)
                from_country = tenant_code
                source_system = random.choice(banking_sources)
                dynamic_tag = f"{from_country}{to_country}TXN{random.randint(10,99)}"
                rand6 = str(random.randint(100000, 999999)).zfill(6)

                line = (
                    f"{tenant_code}{transaction_date}{txn_id}"
                    f"~##~{tenant_code}"
                    f"~##~{tenant_code}{txn_time}{rand6}{currency}"
                    f"~##~{amount}"
                    f"~##~~##~{scenario.lower()}{rule_code}{transaction_date}"
                    + "~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~TCOECDGEN"
                    + f"~##~~##~~##~{dynamic_tag}"
                    + f"~##~~##~{transaction_date.replace('-', '')}{txn_time}"
                    + f"~##~UOB~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~{amount}"
                    f"~##~{currency}~##~~##~~##~~##~~##~~##~1~##~~##~~##~~##~~##~~##~~##~{source_system}~##~~##~110~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~{from_country}-{to_country}~##~~##~~##~~##~~##~~##~{random.randint(4000,9999)}~##~~##~~##~~##~~##~C~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~~##~"
                )

                file.write(line + "\n")

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
        print(f"❌ Error generating transactions: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask server connected and running at http://127.0.0.1:5000")
    app.run(debug=True)