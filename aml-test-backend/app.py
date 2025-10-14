from flask import Flask, jsonify, request
from flask_cors import CORS
from db import supabase

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "✅ AML Test API Connected Successfully!"}

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

if __name__ == "__main__":
    app.run(debug=True)
