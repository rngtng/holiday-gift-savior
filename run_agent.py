#!/usr/bin/env python3
"""CLI entrypoint for running the Holiday Gift Savior agent locally."""

import asyncio
from agents.holiday_gift_savior.agent import MODEL_NAME, NUM_PARALLEL_RESEARCHERS


async def main():
    """Run the agent in simulation mode for local testing."""
    print("\n" + "=" * 70)
    print("Holiday Gift Savior (HGS) - Multi-Agent Gift Recommendation System")
    print("=" * 70)
    print(f"Model: {MODEL_NAME}")
    print(f"Features: Sequential workflow, {NUM_PARALLEL_RESEARCHERS}x parallel research, budget validation")
    print("=" * 70 + "\n")

    print("Example queries:")
    print("  - 'I need gifts for Dad ($55) and Brother ($40) for Christmas.'")
    print("  - 'Help me find a gift for Mom who loves gardening, budget $30'")
    print("\nAccess the web UI at http://localhost:3011 when running in Docker\n")


if __name__ == "__main__":
    asyncio.run(main())
