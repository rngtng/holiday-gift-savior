"""Custom tools for the Holiday Gift Savior system."""

import json
from google.adk.tools import FunctionTool


@FunctionTool
def check_budget_compliance(
    gift_price: float,
    recipient_budget: float,
    currency: str
) -> str:
    """
    Check if a gift price is within budget (allows 5% grace margin).

    Args:
        gift_price: The estimated price of the gift.
        recipient_budget: The maximum budget allocated for the recipient.
        currency: The ISO currency code (e.g., "USD" or "EUR").

    Returns:
        JSON string with compliance status and details.
    """
    currency = currency.upper()
    symbol = "€" if currency == "EUR" else "$"
    difference = round(recipient_budget - gift_price, 2)

    # Determine compliance status
    if gift_price <= recipient_budget:
        status = "Pass"
        message = (
            f"Compliance SUCCESS: Gift price is {symbol}{gift_price:.2f}, "
            f"which is {symbol}{difference:.2f} under budget of {symbol}{recipient_budget:.2f}."
        )
    elif gift_price <= recipient_budget * 1.05:
        status = "Warning"
        message = (
            f"Compliance WARNING: Gift price is {symbol}{gift_price:.2f}, "
            f"exceeding budget of {symbol}{recipient_budget:.2f} by less than 5%."
        )
    else:
        status = "Fail"
        message = (
            f"Compliance FAILURE: Gift price is {symbol}{gift_price:.2f}, "
            f"exceeding budget of {symbol}{recipient_budget:.2f} by {symbol}{abs(difference):.2f}."
        )

    return json.dumps({
        "compliance_status": status,
        "gift_price": round(gift_price, 2),
        "recipient_budget": round(recipient_budget, 2),
        "currency": currency,
        "budget_difference": difference,
        "compliance_message": message
    })
