from flask import Flask, jsonify, request
from flask_cors import CORS
from db import supabase
from datetime import datetime
from functions import (
    get_amount_for_rule,
    get_country_for_rule,
    generate_transaction_ref,
    get_run_name
)

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
    Generate test AML transactions dynamically.
    Expects JSON:
    {
        "tenant_code": "SG",
        "transaction_date": "2025-10-16",
        "scenario": "POS" or "NEG",
        "rule_codes": ["AML-TRX-ALL-A-01", "AML-TRX-ALL-B-02"]
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

        # Fetch Tenant ID
        tenant = supabase.table("tenants").select("*").eq("tenant_code", tenant_code).execute().data
        if not tenant:
            return jsonify({"error": f"Tenant '{tenant_code}' not found"}), 404
        tenant_id = tenant[0]["id"]

        # Create Test Run
        run_name = get_run_name(tenant_code)
        test_run = supabase.table("test_runs").insert({
            "tenant_id": tenant_id,
            "run_name": run_name,
            "initiated_by": "webapp",
            "status": "running"
        }).execute().data[0]
        test_run_id = test_run["id"]

        # Generate Transactions per Rule
        generated = []
        for rule_code in rule_codes:
            transaction = {
                "tenant_code": tenant_code,
                "transaction_date": transaction_date,
                "transaction_ref": generate_transaction_ref(rule_code, scenario),
                "rule_code": rule_code,
                "amount": get_amount_for_rule(rule_code, positive=(scenario == "POS")),
                "currency_code": "SGD",
                "banking_source": "RBK", 
                "from_country": "SG",
                "to_country": get_country_for_rule(rule_code, positive=(scenario == "POS")),
                "test_run_id": test_run_id,
            }

            supabase.table("transactions").insert(transaction).execute()
            generated.append(transaction)

        # Mark Test Run as Complete
        supabase.table("test_runs").update({
            "status": "completed",
            "completed_at": datetime.now().isoformat()
        }).eq("id", test_run_id).execute()

        return jsonify({
            "message": f"✅ Generated {len(rule_codes)} {scenario} transactions for {tenant_code}",
            "test_run_id": test_run_id,
            "run_name": run_name,
            "scenario": scenario,
            "count": len(rule_codes),
            "transactions": generated
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask server connected and running at http://127.0.0.1:5000")
    app.run(debug=True)
