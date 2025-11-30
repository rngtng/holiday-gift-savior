"""Custom tools for the Holiday Gift Savior system."""

import json
import os
from google.adk.tools import FunctionTool
from .sample_data import USER_PROFILES_DB


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


@FunctionTool
def get_recipient_profiles(user_id: str = "") -> str:
    """
    Retrieve recipient profiles for the current user from the profile database.

    This tool loads personalized recipient profiles including interests,
    past successful gifts, and dislikes for each person the user shops for.

    Args:
        user_id: Optional user ID. If not provided, uses DEFAULT_USER_ID from environment.

    Returns:
        JSON string with list of recipient profiles for the user.
    """
    # Use provided user_id, fall back to environment variable
    if not user_id:
        user_id = os.getenv("CURRENT_USER_ID", "family_smith_123")

    profiles = USER_PROFILES_DB.get(user_id, [])

    if not profiles:
        return json.dumps({
            "error": f"No profiles found for user_id: {user_id}",
            "available_users": list(USER_PROFILES_DB.keys())
        })

    # Convert profiles to serializable format
    profiles_data = []
    for profile in profiles:
        profiles_data.append({
            "recipient_name": profile.recipient_name,
            "persistent_interests": profile.persistent_interests,
            "past_successful_gifts": profile.past_successful_gifts,
            "disliked_categories": profile.disliked_categories
        })

    return json.dumps({
        "user_id": user_id,
        "total_recipients": len(profiles),
        "profiles": profiles_data
    })
