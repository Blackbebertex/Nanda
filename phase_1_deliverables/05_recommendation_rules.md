# Recommendation Rule Catalogue

This document defines the specific deterministic logic and suitability parameters driving the ARTHA AI wealth advisory service.

## 1. Dormant Asset Allocation Rule
- **ID:** `DORMANT_FD_REALLOCATION`
- **Objective:** Identify low-yield dormant assets and recommend higher-yielding suitability-matched alternatives.
- **Trigger Conditions:**
  - The customer holds an account of type `FD` (Fixed Deposit).
  - The asset has been untouched for more than 12 months (`lastTouchedAt` > 12 months ago).
  - The customer's risk profile is `Moderate` or `Growth`.
  - There exists a defined goal with a maturity horizon of less than 36 months (e.g. `First Car` goal).
- **Outcome Recommendation:** Reallocate dormant Fixed Deposit funds to a short-term hybrid mutual fund (target return: 9-11% p.a. vs current 6.1% yield).

## 2. Emergency Fund Sufficiency Rule
- **ID:** `INSUFFICIENT_EMERGENCY_FUND`
- **Objective:** Warn the customer if their liquid savings buffer falls below the recommended threshold.
- **Trigger Conditions:**
  - The customer's total balance in `SAVINGS` accounts is less than 3x average monthly expenses.
  - Average monthly expenses are calculated as the sum of all monthly DEBITS excluding investments.
- **Outcome Recommendation:** Advise increasing contributions to liquid savings buffers or sweep-in FDs before initiating new investment plans.

## 3. Suitability Agent Verification
- All generated recommendations must check customer-specific suitability factors:
  - **Risk Profile Alignment:** High-volatility equities must never be suggested to Conservative profiles.
  - **Liquidity Check:** Recommendation actions must ensure that minimum savings account liquidity is maintained.
  - **Goal Alignment:** Asset duration must match the target goal date.
