# ARTHA AI Compliance & Safety Guardrails

PROHIBITED_INPUT_PATTERNS = [
    r"\bignore\s+(?:all\s+)?previous\s+instructions\b",
    r"\boverride\s+rules\b",
    r"\bsystem\s+prompt\b",
    r"\bjailbreak\b",
    r"\bignore\s+safety\b"
]

PROHIBITED_OUTPUT_PATTERNS = [
    r"\bguarantee",
    r"\bassured\s+return\b",
    r"\bzero\s+risk\b",
    r"\bno\s+risk\b",
    r"\b100%\s+safe\b"
]

import re

def check_safety(text):
    # Base compatibility check
    if not text:
        return True
        
    lower_text = str(text).lower()
    
    # 1. Input Shield: Search for injection attempts
    for pattern in PROHIBITED_INPUT_PATTERNS:
        if re.search(pattern, lower_text):
            print(f"[GUARDRAIL ALERT] Prompt Injection blocked: '{pattern}'")
            return False
            
    # 2. Output Shield: Search for compliance violations
    for pattern in PROHIBITED_OUTPUT_PATTERNS:
        if re.search(pattern, lower_text):
            print(f"[GUARDRAIL ALERT] Non-compliant statement blocked: '{pattern}'")
            return False
            
    return True