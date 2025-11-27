import json
from google.adk.tools import FunctionTool

@FunctionTool
def check_budget_compliance(gift_price: float, recipient_budget: float, currency: str) -> str:
    """
    Performs a deterministic check to see if a gift price is compliant with the budget.

    It is assumed that both gift_price and recipient_budget are in the same currency,
    as enforced by the preceding agents' search queries.

    Args:
        gift_price: The estimated price of the gift.
        recipient_budget: The maximum budget allocated for the recipient.
        currency: The ISO currency code (e.g., "USD" or "EUR").

    Returns:
        A JSON string indicating the compliance status and the exact difference.
    """
    currency = currency.upper()
    symbol = "€" if currency == "EUR" else "$" # Display symbol for clarity
    status: str

    # Calculate the difference: positive means under budget, negative means over
    difference: float = round(recipient_budget - gift_price, 2)

    if gift_price <= recipient_budget:
        status = "Pass"
        message = f"Compliance SUCCESS: Gift price is {symbol}{gift_price:.2f}, which is {symbol}{difference:.2f} under the budget of {symbol}{recipient_budget:.2f}. Approved by the Head Elf!"
    elif gift_price <= recipient_budget * 1.05:
        # Allows a small grace margin (5%) before a hard fail
        status = "Warning"
        message = f"Compliance WARNING: Gift price is {symbol}{gift_price:.2f}, exceeding the budget of {symbol}{recipient_budget:.2f} by less than 5%. Requires parental review before sending to the workshop."
    else:
        status = "Fail"
        message = f"Compliance FAILURE: Gift price is {symbol}{gift_price:.2f}, exceeding the budget of {symbol}{recipient_budget:.2f} by more than {symbol}{abs(difference):.2f}. Must find a cheaper alternative immediately."

    result = {
        "compliance_status": status,
        "gift_price": round(gift_price, 2),
        "recipient_budget": round(recipient_budget, 2),
        "currency": currency,
        "budget_difference": difference,
        "compliance_message": message
    }

    return json.dumps(result)
