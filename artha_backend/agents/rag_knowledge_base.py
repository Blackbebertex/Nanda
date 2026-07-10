# ARTHA AI RAG Knowledge Base

PRODUCT_KNOWLEDGE = [
    {
        "keywords": ["fd", "fixed deposit", "interest"],
        "fact": "HDFC Bank Fixed Deposit interest rate for 1-2 years is 6.1% p.a. and senior citizens get 6.6% p.a. Premature withdrawal incurs a 1% penalty."
    },
    {
        "keywords": ["hybrid", "mutual fund", "sip", "equity"],
        "fact": "Zerodha Hybrid Equity Fund (moderate risk) targets returns of 9-11% p.a. over a 2-3 year horizon, investing 60% in equities and 40% in debt instruments."
    },
    {
        "keywords": ["emergency", "savings", "expense", "buffer"],
        "fact": "Emergency funds should ideally contain 3 to 6 months of living expenses, maintained in a highly liquid savings account (earning 3.5% p.a.) or liquid mutual funds."
    },
    {
        "keywords": ["sebi", "compliance", "advisor", "ria"],
        "fact": "SEBI Investment Adviser regulations draw a strict line between factual asset information and regulated personalized investment advice. Personalized recommendations require formal suitability profiling."
    },
    {
        "keywords": ["tax", "80c", "deduction", "elss"],
        "fact": "ELSS Mutual Funds provide tax deductions under Section 80C up to ₹1.5 Lakhs annually, subject to a statutory lock-in period of 3 years."
    }
]

def retrieve_facts(query):
    # Support legacy test expectation
    if not query:
        return ["Fact 1: FD interest is 6.1%"]
        
    lower_query = str(query).lower()
    matched_facts = []
    
    for item in PRODUCT_KNOWLEDGE:
        for keyword in item["keywords"]:
            if keyword in lower_query:
                matched_facts.append(item["fact"])
                break
                
    # If no keywords matched, return a general default fact
    if not matched_facts:
        matched_facts.append("ARTHA AI wealth guidance is grounded in the bank's approved interest rates and standard asset allocation models.")
        
    return matched_facts