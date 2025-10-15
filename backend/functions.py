import random
from datetime import datetime

def get_amount_for_rule(rule_code: str, positive: bool = True) -> float:
    """
    Generate realistic transaction amounts for AML rules.
    positive=True means the transaction is meant to trigger (POS case).
    """
    if "A-01" in rule_code:  # High-Value Transaction
        return 150000 if positive else 80000
    elif "B-02" in rule_code:  # Sanctioned Country
        return 5000
    elif "C-03" in rule_code:  # ATM 3-Day Pattern
        return 6000 if positive else 2000
    elif "D-04" in rule_code:  # Frequent Low-Value Transfers
        return 50 if positive else 150
    return random.randint(100, 5000)

def get_country_for_rule(rule_code: str, positive: bool = True) -> str:
    """
    Return destination country based on rule type.
    """
    if "B-02" in rule_code:
        return "IR" if positive else "SG"  # Iran for POS (sanctioned)
    return "SG"

def generate_transaction_ref(rule_code: str, scenario: str) -> str:
    """
    Generate readable transaction reference IDs.
    """
    return f"{scenario}_{rule_code}_{random.randint(1000, 9999)}"

def get_run_name(tenant_code: str) -> str:
    """
    Create a timestamped run name for test_runs.
    """
    return f"Run_{tenant_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"