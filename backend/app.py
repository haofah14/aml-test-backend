from flask import Flask, jsonify, request
from flask_cors import CORS
from db import supabase
from functions import (
    get_amount_for_rule,
    get_country_for_rule,
    generate_transaction_ref,
    get_run_name
)
from datetime import datetime
import random

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
    data = supabase.table("rules").select("*").execute()
    return jsonify(data.data)

@app.route("/rules", methods=["POST"])
def add_rule():
    payload = request.json
    result = supabase.table("rules").insert(payload).execute()
    return jsonify(result.data), 201

# ---------------------------
# TENANTS ENDPOINTS
# ---------------------------
@app.route("/tenants", methods=["GET"])
def get_tenants():
    data = supabase.table("tenants").select("*").execute()
    return jsonify(data.data)

@app.route("/tenants", methods=["POST"])
def add_tenant():
    payload = request.json
    result = supabase.table("tenants").insert(payload).execute()
    return jsonify(result.data), 201

# ---------------------------
# TRANSACTIONS ENDPOINTS
# ---------------------------
@app.route("/transactions", methods=["GET"])
def get_transactions():
    data = supabase.table("transactions").select("*").limit(20).execute()
    return jsonify(data.data)

@app.route("/transactions", methods=["POST"])
def add_transaction():
    payload = request.json
    result = supabase.table("transactions").insert(payload).execute()
    return jsonify(result.data), 201

# Generate Transactions
@app.route("/generate_transactions", methods=["POST"])
def generate_transactions():
    tenant_code = "SG"
    today = datetime.now().strftime("%Y-%m-%d")

    # Get tenant
    tenant = supabase.table("tenants").select("*").eq("tenant_code", tenant_code).execute().data
    if not tenant:
        return jsonify({"error": f"Tenant '{tenant_code}' not found"}), 404
    tenant_id = tenant[0]["id"]

    # Create new test_run
    run_name = get_run_name(tenant_code)
    test_run = supabase.table("test_runs").insert({
        "tenant_id": tenant_id,
        "run_name": run_name,
        "initiated_by": "system",
        "status": "running"
    }).execute().data[0]
    test_run_id = test_run["id"]

    # Fetch rules
    rules = supabase.table("rules").select("*").execute().data
    if not rules:
        return jsonify({"error": "No rules found"}), 404

    generated = []

    for rule in rules:
        rule_code = rule["rule_code"]

        pos_txn = {
            "tenant_code": tenant_code,
            "transaction_date": today,
            "transaction_ref": generate_transaction_ref(rule_code, "POS"),
            "rule_code": rule_code,
            "amount": get_amount_for_rule(rule_code, True),
            "currency_code": "SGD",
            "banking_source": "RBK",
            "from_country": "SG",
            "to_country": get_country_for_rule(rule_code, True),
            "test_run_id": test_run_id,
        }

        neg_txn = {
            "tenant_code": tenant_code,
            "transaction_date": today,
            "transaction_ref": generate_transaction_ref(rule_code, "NEG"),
            "rule_code": rule_code,
            "amount": get_amount_for_rule(rule_code, False),
            "currency_code": "SGD",
            "banking_source": "RBK",
            "from_country": "SG",
            "to_country": get_country_for_rule(rule_code, False),
            "test_run_id": test_run_id,
        }

        supabase.table("transactions").insert([pos_txn, neg_txn]).execute()
        generated.append({"rule": rule_code, "POS": pos_txn, "NEG": neg_txn})

    # Mark run completed
    supabase.table("test_runs").update({
        "status": "completed",
        "completed_at": datetime.now().isoformat()
    }).eq("id", test_run_id).execute()

    return jsonify({
        "message": f"✅ Generated POS & NEG transactions for {tenant_code}",
        "test_run_id": test_run_id,
        "run_name": run_name,
        "count": len(rules) * 2,
        "transactions": generated
    })

if __name__ == "__main__":
    print("✅ Flask server connected and running at http://127.0.0.1:5000")
    app.run(debug=True)
