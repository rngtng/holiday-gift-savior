"""Holiday Gift Savior - Multi-agent gift recommendation system."""

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search

from .custom_tools import check_budget_compliance, get_recipient_profiles

# Configuration
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
NUM_PARALLEL_RESEARCHERS = 3

# Default user for demo purposes (can be overridden via CURRENT_USER_ID environment variable)
DEFAULT_USER_ID = "family_smith_123"

# ============================================================================
# Agent Factory Functions
# ============================================================================

def create_collector_agent(**kwargs) -> LlmAgent:
    """
    Creates the Collector Agent that structures user requests into recipient briefs.

    Takes user input + recipient memory profiles and outputs structured JSON briefs
    containing recipient_name, max_budget, and search_query for each person.
    """
    return LlmAgent(
        instruction=(
            "You are the Gift Briefing Specialist. For each gift request:\n"
            "1. Query MemoryBank to retrieve the recipient's profile (interests, past gifts, dislikes)\n"
            "2. Combine the user's budget and preferences with the stored memory profile\n"
            "3. Create structured search briefs as a JSON array where each object contains:\n"
            "   - 'recipient_name': The person's name\n"
            "   - 'max_budget': Budget from user's request\n"
            "   - 'search_query': Synthesized query using interests from memory + user preferences\n\n"
            "IMPORTANT: Use ACTUAL data from MemoryBank, not hallucinated information."
        ),
        **kwargs
    )


def create_researcher_agent(**kwargs) -> LlmAgent:
    """
    Creates a Gift Researcher Agent that finds gifts using Google Search.

    Designed for parallel execution - each instance handles one recipient brief.
    Returns 3 gift ideas as JSON with titles, prices, and links.
    """
    return LlmAgent(
        instruction=(
            "You are a Gift Researcher. Take the recipient brief (name, budget, search query) "
            "and use Google Search to find 3 highly-rated, appropriate gifts. Ensure gifts "
            "align with interests and avoid disliked categories. Output a JSON list of GiftIdea objects "
            "with fields: recipient, gift_title, description, estimated_price, product_link, currency."
        ),
        tools=[google_search],
        **kwargs
    )


def create_aggregator_agent(**kwargs) -> LlmAgent:
    """
    Creates the Aggregator Agent that validates and delivers final recommendations.

    Validates budgets using check_budget_compliance tool, filters unwanted items,
    formats output as markdown table, and updates long-term memory with new preferences.
    """
    return LlmAgent(
        name="AggregatorAgent",
        model=MODEL_NAME,
        instruction=(
            "You are the Final Reviewer. Process the gift ideas from researchers:\n"
            "1. Use 'check_budget_compliance' tool to validate each gift price vs budget\n"
            "2. If a gift fails budget check, suggest a cheaper alternative\n"
            "3. Check the recipient profiles (available in context) for disliked_categories\n"
            "4. Filter out items that match disliked categories from the profiles\n"
            "5. Format approved gifts as a clear Markdown table\n"
            "6. Note any new preferences learned from the conversation"
        ),
        tools=[check_budget_compliance],
        **kwargs
    )

# ============================================================================
# Workflow Orchestration
# ============================================================================

def create_gift_planning_workflow(**kwargs) -> SequentialAgent:
    """
    Creates the main sequential workflow: Collection -> Parallel Research -> Aggregation.

    Architecture:
        1. Collector structures user input into recipient briefs
        2. Parallel researchers (3 instances) find gifts concurrently
        3. Aggregator validates budgets and formats final output

    Args:
        **kwargs: Additional agent configuration

    Returns:
        SequentialAgent configured with the three-stage workflow
    """
    # Stage 1: Structure input into recipient briefs
    collector = create_collector_agent(
        name="CollectorAgent",
        model=MODEL_NAME
    )

    # Stage 2: Parallel research - one researcher per recipient
    parallel_research = ParallelAgent(
        name="ParallelResearch",
        sub_agents=[
            create_researcher_agent(
                name=f"Researcher_{i}",
                model=MODEL_NAME
            )
            for i in range(NUM_PARALLEL_RESEARCHERS)
        ]
    )

    # Stage 3: Aggregate, validate, and deliver results
    aggregator = create_aggregator_agent()

    return SequentialAgent(
        name="GiftPlanningWorkflow",
        sub_agents=[collector, parallel_research, aggregator],
        **kwargs
    )

# ============================================================================
# Main Entry Point Agent
# ============================================================================

def create_concierge_agent(**kwargs) -> LlmAgent:
    """
    Creates the top-level Concierge Agent that routes requests and manages memory.

    This is the main entry point for the system. It dynamically loads recipient profiles
    based on the user_id from the session and delegates gift planning to the workflow sub-agent.

    Args:
        **kwargs: Additional agent configuration

    Returns:
        LlmAgent configured as the system's main router
    """
    gift_workflow = create_gift_planning_workflow()

    return LlmAgent(
        name="HGSConciergeAgent",
        model=MODEL_NAME,
        instruction=(
            "You are the Holiday Gift Savior Concierge - a warm, helpful assistant specializing in gift recommendations.\n\n"

            "IMPORTANT - LOAD USER PROFILES:\n"
            "At the START of every conversation, you MUST call the 'get_recipient_profiles' tool to load the user's recipient data.\n"
            "Pass an empty string or the user's ID to load their personalized profiles.\n"
            "Do NOT proceed with recommendations until you have loaded the profiles.\n\n"

            "FIRST INTERACTION (at conversation start):\n"
            "1. Call 'get_recipient_profiles' tool to load user data\n"
            "2. Greet the user warmly and introduce yourself as their Holiday Gift Savior 🎁\n"
            "3. Summarize the loaded recipient profiles:\n"
            "   - Total number of recipients\n"
            "   - Each person's name with 2-3 key interests\n"
            "   - Any important dislikes to avoid\n"
            "4. Ask who they're shopping for and their budget\n\n"

            "Example greeting format:\n"
            "\"Welcome! 🎁 I'm your Holiday Gift Savior.\n\n"
            "I have profiles for [N] people:\n"
            "- [Name] (loves [Interest1], [Interest2], but avoid [Dislike1])\n"
            "- [Name] (enjoys [Interest1], [Interest2], no [Dislike1])\n\n"
            "Who are you shopping for today, and what's your budget?\"\n\n"

            "FOR GIFT REQUESTS:\n"
            "- Acknowledge the request positively\n"
            "- Delegate to the 'GiftPlanningWorkflow' sub-agent\n"
            "- The workflow will use the loaded profile data for personalized recommendations\n\n"

            "FOR OTHER QUESTIONS:\n"
            "- Politely redirect: 'My sleigh bells are only calibrated for gift requests! How can I help you find the perfect gift today?'"
        ),
        tools=[get_recipient_profiles],
        sub_agents=[gift_workflow],
        **kwargs
    )

def create_agent() -> LlmAgent:
    """
    Initializes and returns the root agent for the ADK system.

    This is the entry point called by the ADK framework.
    The agent will dynamically load user profiles at runtime using the get_recipient_profiles tool.

    Returns:
        The root LlmAgent (concierge) ready to handle user requests
    """
    print("\n🎁 Initializing Holiday Gift Savior (profiles will be loaded dynamically per session)")
    return create_concierge_agent()


# Root agent instance - ADK framework expects this variable
root_agent = create_agent()
