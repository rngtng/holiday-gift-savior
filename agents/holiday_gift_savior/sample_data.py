"""Sample user profiles for demo purposes.

In production, this data would be stored in a database like Firestore
and retrieved via API calls. This file simulates that persistent storage
with different example datasets for various user types.
"""

from .data_models import RecipientProfile

# ============================================================================
# User Profile Database (simulates persistent storage)
# ============================================================================

USER_PROFILES_DB = {
    # Family use case - traditional family gift shopping
    "family_smith_123": [
        RecipientProfile(
            recipient_name="Dad",
            persistent_interests=["Coffee", "Gadgets"],
            past_successful_gifts=["Smart Speaker"],
            disliked_categories=["Socks", "Tie"]
        ),
        RecipientProfile(
            recipient_name="Mom",
            persistent_interests=["Gardening", "Reading"],
            past_successful_gifts=[],
            disliked_categories=["Heavy Jewelry", "Anything Red"]
        ),
        RecipientProfile(
            recipient_name="Brother",
            persistent_interests=["Baking", "Sci-Fi"],
            past_successful_gifts=[],
            disliked_categories=["Video Games"]
        )
    ],

    # Personal use case - spouse and children
    "user_johnson_456": [
        RecipientProfile(
            recipient_name="Wife",
            persistent_interests=["Yoga", "Photography", "Travel"],
            past_successful_gifts=["Camera Lens", "Yoga Mat"],
            disliked_categories=["Jewelry", "Perfume"]
        ),
        RecipientProfile(
            recipient_name="Daughter",
            persistent_interests=["Art", "Music", "Anime"],
            past_successful_gifts=["Drawing Tablet"],
            disliked_categories=["Clothes", "Makeup"]
        ),
        RecipientProfile(
            recipient_name="Son",
            persistent_interests=["Gaming", "Robotics", "Coding"],
            past_successful_gifts=["Raspberry Pi"],
            disliked_categories=["Books", "Sports Equipment"]
        )
    ],

    # Corporate use case - office gift exchange
    "corporate_hr_789": [
        RecipientProfile(
            recipient_name="Team Lead Sarah",
            persistent_interests=["Leadership Books", "Coffee", "Wellness"],
            past_successful_gifts=["Planner"],
            disliked_categories=["Generic Mugs", "Candy"]
        ),
        RecipientProfile(
            recipient_name="Developer Mike",
            persistent_interests=["Mechanical Keyboards", "Tech Gadgets"],
            past_successful_gifts=["USB Hub"],
            disliked_categories=["Office Supplies", "Gift Cards"]
        ),
        RecipientProfile(
            recipient_name="Designer Lisa",
            persistent_interests=["Art Supplies", "Plants", "Stationery"],
            past_successful_gifts=["Succulent Set"],
            disliked_categories=["Tech Gadgets", "Books"]
        )
    ],

    # Student use case - friends and roommates
    "student_alex_321": [
        RecipientProfile(
            recipient_name="Best Friend Emma",
            persistent_interests=["K-pop", "Skincare", "Boba Tea"],
            past_successful_gifts=["BTS Album"],
            disliked_categories=["Books", "Formal Wear"]
        ),
        RecipientProfile(
            recipient_name="Roommate Jordan",
            persistent_interests=["Cooking", "Board Games", "Hiking"],
            past_successful_gifts=["Cast Iron Skillet"],
            disliked_categories=["Electronics", "Candles"]
        )
    ]
}
