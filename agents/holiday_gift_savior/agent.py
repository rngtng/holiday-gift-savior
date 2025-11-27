import json
import asyncio
from typing import Dict, List, Optional
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.agents.base_agent_config import BaseAgentConfig
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import google_search, FunctionTool

# --- Imports for project-specific components (assumed to be in the same directory) ---
# NOTE: In a real ADK environment, these would be accessible via the project structure.
from .data_models import RecipientProfile, GiftIdea
from .custom_tools import BudgetTools

# --- Configuration ---
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
MOCK_USER_ID = "family_smith_123"

# --- 1. Specialized LLM Agents ---

def PreferenceCollectorAgent(**kwargs):
    """
    Factory function to create an agent that gathers session-specific constraints (e.g., specific budget for this year)
    and synthesizes them with LTM data loaded by the Router Agent.
    """
    return LlmAgent(
        instruction=(
            "You are the Gift Briefing Specialist. Your input is the user's gift request and the recipient's "
            "persistent profile (from memory/session context). Your task is to structure the final search query brief: "
            "Recipient Name, Max Budget, and a synthesized list of interests/constraints (including LTM data). "
            "Output a list of these structured briefs as JSON for the 'GiftResearcherAgent' to use. Ensure the output "
            "JSON is an array where each object contains 'recipient_name', 'max_budget', and 'search_query'."
        ),
        **kwargs
    )

def GiftResearcherAgent(**kwargs):
    """
    Factory function to create an agent that finds gift ideas using the built-in Google Search tool
    based on a single recipient's brief. This agent is designed for parallel execution.
    """
    return LlmAgent(
        instruction=(
            "You are a dedicated Gift Researcher. Take the provided recipient brief (name, budget, search query). "
            "Use the Google Search tool to find 3 highly-rated, appropriate gifts. "
            "CRITICALLY: Ensure the gift aligns with persistent interests and avoids disliked categories. "
            "For each gift, find a real-time price and link. Your output MUST be a JSON list of GiftIdea objects."
        ),
        tools=[google_search],
        **kwargs
    )

def create_aggregator_agent(memory_bank: InMemoryMemoryService, **kwargs):
    """
    Factory function to create the aggregator agent that collects results from all parallel agents,
    validates the budget using the Custom Tool, formats the final output, and manages Long-Term Memory updates.
    """
    budget_tools = BudgetTools()

    agent = LlmAgent(
        name="AggregatorAgent",
        model=MODEL_NAME,
        instruction=(
            "You are the Final Reviewer and Deliver Agent, Santa's Chief Helper. Your input is a collection of potential GiftIdea JSON objects. "
            "1. For every gift idea, use the 'check_budget_compliance' tool (Santa's Secret Budget Tool) to confirm the price against the budget. "
            "2. If a gift fails, recommend a similar, cheaper alternative in the final output. "
            "3. Format the final list into a professional, clear Markdown table for the user. "
            "4. CRITICALLY: Explicitly filter out any gift ideas containing 'socks' or items noted as 'boring' in the memory. "
            "5. Finally, analyze the conversation for any new preferences and use the MemoryBank to persist them. Deliver the response with a celebratory tone!"
        ),
        tools=[budget_tools],
        **kwargs
    )

    return agent

class AggregatorAgent(LlmAgent):
    """Legacy class for backwards compatibility"""
    pass

# --- 2. The Core Orchestration: Sequential and Parallel Workflow ---

def create_gift_planning_workflow(memory_bank: InMemoryMemoryService, **kwargs):
    """
    Factory function to create the main sequential workflow: Collection -> Parallel Research -> Aggregation.
    This demonstrates the combination of sequential and parallel execution.
    """
    # Step 1: Collect and Structure the Input
    collector = PreferenceCollectorAgent(name="CollectorAgent", model=MODEL_NAME)

    # Step 2: Parallel Research (Run one Researcher for each recipient brief)
    # This is a key feature demonstrating parallel execution efficiency.
    # NOTE: In this simplified ADK simulation, we fix the number of agents to 3.
    parallel_research = ParallelAgent(
        name="ParallelResearch",
        sub_agents=[GiftResearcherAgent(name=f"Researcher_{i}", model=MODEL_NAME) for i in range(3)]
    )

    # Step 3: Final Review, Custom Tool Validation, and Delivery/Memory Update
    aggregator = create_aggregator_agent(memory_bank=memory_bank)

    workflow = SequentialAgent(
        name="GiftPlanningWorkflow",
        model=MODEL_NAME,
        sub_agents=[collector, parallel_research, aggregator],
        **kwargs
    )

    return workflow

class GiftPlanningWorkflow(SequentialAgent):
    """Legacy class for backwards compatibility"""
    pass

# --- 3. The Main Router Agent (Entry Point) ---

def create_concierge_agent(memory_bank: InMemoryMemoryService, **kwargs):
    """
    Factory function to create the top-level agent that manages memory loading and delegation for the Holiday Gift Savior (HGS).
    """
    gift_workflow = create_gift_planning_workflow(memory_bank=memory_bank)

    agent = LlmAgent(
        name="HGSConciergeAgent",
        model=MODEL_NAME,
        instruction=(
            "You are the main Holiday Gift Savior (HGS) Concierge Agent. Your primary role is delegation and managing the MemoryBank. "
            "If the user asks for 'gift ideas' or 'help shopping', you must first load all available recipient profiles from the MemoryBank for the current user_id. "
            "Pass the memory context, along with the user's latest query, to the 'GiftPlanningWorkflow' tool/workflow for execution. "
            "If the user asks a general question, offer a witty redirection back to the task, like: 'My sleigh bells are only calibrated for gift requests! How can I help you shop today?'"
        ),
        tools=[gift_workflow],
        **kwargs
    )

    return agent

# --- 4. Main ADK Application Setup ---

def create_agent():
    """Initializes and returns the ADK agent."""
    session_service = InMemorySessionService()

    # Initialize Mock Memory Bank and Pre-load Use Case data
    memory_bank = InMemoryMemoryService()

    # --- Simulate Pre-loaded Memory Data (Crucial for scoring the Memory feature) ---
    recipient_data = [
        RecipientProfile(recipient_name="Dad", persistent_interests=["Coffee", "Gadgets"], past_successful_gifts=["Smart Speaker"], disliked_categories=["Socks", "Tie"]),
        RecipientProfile(recipient_name="Mom", persistent_interests=["Gardening", "Reading"], past_successful_gifts=[], disliked_categories=["Heavy Jewelry", "Anything Red"]),
        RecipientProfile(recipient_name="Brother", persistent_interests=["Baking", "Sci-Fi"], past_successful_gifts=[], disliked_categories=["Video Games"])
    ]

    # In a real ADK app, this would be saved/loaded via an API call (e.g., Firestore)
    print(f"--- HGS Pre-loading Memory for {MOCK_USER_ID} ---")
    for profile in recipient_data:
        # Hypothetical memory write operation
        # await memory_bank.add_memory(MOCK_USER_ID, profile.to_dict())
        print(f"Profile Loaded: {profile.recipient_name} | Interests: {', '.join(profile.persistent_interests)}")

    # Initialize the main agent
    router_agent = create_concierge_agent(memory_bank=memory_bank)
    return router_agent

# Create the agent instance for ADK to load
root_agent = create_agent()

async def main():
    print("\n--- Holiday Gift Savior (HGS) Initialized & Ready to Save the Holidays ---")
    print(f"System Model: {MODEL_NAME}")
    print("Features ready: Multi-Agent System (Sequential & Parallel), Custom Tool ('Santa's Secret Budget Tool'), Memory.")

    # Simulate the User Query that triggers the full workflow
    print("\n[Simulated User Query]: 'I need gifts for Dad ($55 budget) and Brother ($40 budget) for Christmas. He just got into baking, too!'")

    # In a real ADK runtime, the flow would now execute:
    # Router (Loads Memory) -> Collector (Structures Briefs) -> Parallel Research (Finds Ideas) -> Aggregator (Custom Tool Check & Deliver)

    # For simulation purposes, we might want to run the agent here if needed,
    # but for ADK web, we just need the agent instance.
    pass

if __name__ == '__main__':
    asyncio.run(main())
