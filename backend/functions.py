import random
from datetime import datetime

def get_amount_for_rule(rule_code, positive=True):
    if rule_code == "AML-TRX-ALL-A-01":  
        return 150000 if positive else 80000
    elif rule_code == "AML-TRX-ALL-B-02":  
        return 10000 if positive else 10000
    elif rule_code == "AML-ATM-ALL-B-03":  
        return 6000 if positive else 3000
    elif rule_code == "AML-XFER-ALL-C-04":  
        return 80 if positive else 150
    else:
        return random.randint(100, 5000)

def get_country_for_rule(rule_code, positive=True):
    if rule_code == "AML-TRX-ALL-B-02":  
        return "IR" if positive else "SG"  
    else:
        return "SG"

def generate_transaction_ref(rule_code, scenario):
    return f"{scenario}_{rule_code}_{random.randint(1000,9999)}"

def get_run_name(tenant_code):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"Run_{tenant_code}_{timestamp}"