from flask import Flask, jsonify, request
from flask_cors import CORS
from db import supabase
from datetime import datetime, timedelta
from functions import (
    get_amount_for_rule,
    get_country_for_rule,
    generate_transaction_ref,
    get_run_name
)
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

        # 1️. Fetch Tenant ID
        tenant = supabase.table("tenants").select("*").eq("tenant_code", tenant_code).execute().data
        if not tenant:
            return jsonify({"error": f"Tenant '{tenant_code}' not found"}), 404
        tenant_id = tenant[0]["id"]

        # 2. Create Test Run
        run_name = get_run_name(tenant_code)
        test_run = supabase.table("test_runs").insert({
            "tenant_id": tenant_id,
            "run_name": run_name,
            "initiated_by": "webapp",
            "status": "running"
        }).execute().data[0]
        test_run_id = test_run["id"]

        generated = []

        # 3. Generate transactions for each rule
        for rule_code in rule_codes:
            # Default number of transactions
            num_txn = 1

            # --- Rule 3: ATM withdrawals pattern ---
            if rule_code == "AML-ATM-ALL-C-03":
                if scenario == "POS":
                    num_txn = 3  # exactly 3 consecutive days
                    base_amount = 5500  # > $5K
                else:
                    num_txn = random.randint(1, 2)  # fewer for NEG
                    base_amount = 3000  # < $5K

                for i in range(num_txn):
                    txn_date = (datetime.strptime(transaction_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
                    amount = base_amount + random.uniform(100, 800)

                    transaction = {
                        "tenant_code": tenant_code,
                        "transaction_date": txn_date,
                        "transaction_ref": generate_transaction_ref(rule_code, scenario),
                        "rule_code": rule_code,
                        "amount": round(amount, 2),
                        "currency_code": "SGD",
                        "banking_source": "RBK",
                        "from_country": "SG",
                        "to_country": "SG",
                        "test_run_id": test_run_id,
                    }

                    supabase.table("transactions").insert(transaction).execute()
                    generated.append(transaction)
                continue  # move to next rule

            # --- Rule 4: Frequent low-value transfers ---
            elif rule_code == "AML-XFER-ALL-D-04":
                if scenario == "POS":
                    num_txn = random.randint(10, 12)
                    base_amount = 60  # <$100
                else:
                    num_txn = random.randint(3, 5)
                    base_amount = 80  # also <$100 but fewer

                for i in range(num_txn):
                    txn_date = (datetime.strptime(transaction_date, "%Y-%m-%d") + timedelta(days=i % 5)).strftime("%Y-%m-%d")
                    amount = base_amount + random.uniform(-10, 10)

                    transaction = {
                        "tenant_code": tenant_code,
                        "transaction_date": txn_date,
                        "transaction_ref": generate_transaction_ref(rule_code, scenario),
                        "rule_code": rule_code,
                        "amount": round(amount, 2),
                        "currency_code": "SGD",
                        "banking_source": "RBK",
                        "from_country": "SG",
                        "to_country": get_country_for_rule(rule_code, positive=(scenario == "POS")),
                        "test_run_id": test_run_id,
                    }

                    supabase.table("transactions").insert(transaction).execute()
                    generated.append(transaction)
                continue

            # --- Rules 1 & 2 (single transactions) ---
            else:
                amount = get_amount_for_rule(rule_code, positive=(scenario == "POS"))
                transaction = {
                    "tenant_code": tenant_code,
                    "transaction_date": transaction_date,
                    "transaction_ref": generate_transaction_ref(rule_code, scenario),
                    "rule_code": rule_code,
                    "amount": round(amount, 2),
                    "currency_code": "SGD",
                    "banking_source": "RBK",
                    "from_country": "SG",
                    "to_country": get_country_for_rule(rule_code, positive=(scenario == "POS")),
                    "test_run_id": test_run_id,
                }

                supabase.table("transactions").insert(transaction).execute()
                generated.append(transaction)

        # 4. Mark test run complete
        supabase.table("test_runs").update({
            "status": "completed",
            "completed_at": datetime.now().isoformat()
        }).eq("id", test_run_id).execute()

        # 5. Return JSON response
        return jsonify({
            "message": f"✅ Generated {len(generated)} {scenario} transactions for {tenant_code}",
            "test_run_id": test_run_id,
            "run_name": run_name,
            "scenario": scenario,
            "count": len(generated),
            "transactions": generated
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask server connected and running at http://127.0.0.1:5000")
    app.run(debug=True)