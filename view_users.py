#!/usr/bin/env python3
"""Display all available users and their recipient profiles."""

from agents.holiday_gift_savior.sample_data import USER_PROFILES_DB


def main():
    """Display all users and their profiles."""
    print("\n" + "=" * 80)
    print("Holiday Gift Savior - User Profile Database")
    print("=" * 80)
    print(f"\nTotal users in system: {len(USER_PROFILES_DB)}\n")

    for i, (user_id, profiles) in enumerate(USER_PROFILES_DB.items(), 1):
        print("-" * 80)
        print(f"\n{i}. User ID: {user_id}")
        print(f"   Total Recipients: {len(profiles)}\n")

        for profile in profiles:
            print(f"   👤 {profile.recipient_name}")
            print(f"      Interests: {', '.join(profile.persistent_interests)}")
            if profile.past_successful_gifts:
                print(f"      Past gifts: {', '.join(profile.past_successful_gifts)}")
            if profile.disliked_categories:
                print(f"      Avoid: {', '.join(profile.disliked_categories)}")
            print()

    print("=" * 80)
    print("\nTo use a specific user, set the DEFAULT_USER_ID in agent.py")
    print("Example: DEFAULT_USER_ID = \"user_johnson_456\"")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
