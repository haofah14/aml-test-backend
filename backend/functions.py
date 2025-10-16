import random
from datetime import datetime
from db import supabase

def get_thresholds(rule_code):
    """Fetch threshold values for a rule from the thresholds table."""
    rule = supabase.table("rules").select("id").eq("rule_code", rule_code).execute().data
    if not rule:
        return {}
    rule_id = rule[0]["id"]
    data = supabase.table("thresholds").select("*").eq("rule_id", rule_id).execute().data
    return data[0] if data else {}

def get_amount_for_rule(rule_code, scenario="POS"):
    """Derive transaction amount based on threshold and scenario."""
    thresholds = get_thresholds(rule_code)
    if not thresholds:
        return random.randint(100, 5000)

    if scenario == "POS" and thresholds.get("amount_gt"):
        return thresholds["amount_gt"] + random.randint(1000, 5000)
    elif scenario == "NEG" and thresholds.get("amount_gt"):
        return thresholds["amount_gt"] - random.randint(1000, 5000)
    elif thresholds.get("amount_lt"):
        if scenario == "POS":
            return thresholds["amount_lt"] - random.randint(10, 20)
        else:
            return thresholds["amount_lt"] + random.randint(10, 50)
    return random.randint(100, 5000)

def get_country_for_rule(rule_code, scenario="POS"):
    """Return random country based on rule and scenario."""
    thresholds = get_thresholds(rule_code)
    is_sanctioned = thresholds.get("is_sanctioned", False)

    if rule_code == "AML-TRX-ALL-B-02" and scenario == "POS" and is_sanctioned:
        sanctioned = supabase.table("countries").select("code").eq("is_sanctioned", True).execute().data
        if sanctioned:
            return random.choice(sanctioned)["code"]
    return "SG"

def get_random_banking_source():
    """
    Fetch all banking sources from Supabase and pick one randomly.
    Returns the 'id' (e.g., 'RBK', 'REM', etc.)
    """
    sources = supabase.table("banking_sources").select("id").execute().data
    if not sources:
        return "RBK"  
    return random.choice(sources)["id"]

def generate_transaction_ref():
    """Generate transaction ID: ATC + DDMMYYYY + HHMM"""
    now = datetime.now()
    return "ATC" + now.strftime("%d%m%Y%H%M")
