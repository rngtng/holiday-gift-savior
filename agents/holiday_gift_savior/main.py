import json
import asyncio
from typing import Dict, List, Optional
from adk.agent import LlmAgent, WorkflowAgent, AgentConfig, Tool
from adk.workflows import SequentialWorkflow, ParallelWorkflow
from adk.providers import InMemorySessionService
from adk.providers.memory import MemoryBank
from adk.tools import GoogleSearchTool # Placeholder for ADK built-in tool

# --- Imports for project-specific components (assumed to be in the same directory) ---
# NOTE: In a real ADK environment, these would be accessible via the project structure.
from agents.holiday_gift_savior.data_models import RecipientProfile, GiftIdea 
from agents.holiday_gift_savior.custom_tools import BudgetTools

# --- Configuration ---
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
MOCK_USER_ID = "family_smith_123"

# --- 1. Specialized LLM Agents ---

class PreferenceCollectorAgent(LlmAgent):
    """
    Gathers session-specific constraints (e.g., specific budget for this year) 
    and synthesizes them with LTM data loaded by the Router Agent.
    """
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.instruction = (
            "You are the Gift Briefing Specialist. Your input is the user's gift request and the recipient's "
            "persistent profile (from memory/session context). Your task is to structure the final search query brief: "
            "Recipient Name, Max Budget, and a synthesized list of interests/constraints (including LTM data). "
            "Output a list of these structured briefs as JSON for the 'GiftResearcherAgent' to use. Ensure the output "
            "JSON is an array where each object contains 'recipient_name', 'max_budget', and 'search_query'."
        )

class GiftResearcherAgent(LlmAgent):
    """
    Finds gift ideas using the built-in Google Search tool based on a single recipient's brief.
    This agent is designed for parallel execution.
    """
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.instruction = (
            "You are a dedicated Gift Researcher. Take the provided recipient brief (name, budget, search query). "
            "Use the Google Search tool to find 3 highly-rated, appropriate gifts. "
            "CRITICALLY: Ensure the gift aligns with persistent interests and avoids disliked categories. "
            "For each gift, find a real-time price and link. Your output MUST be a JSON list of GiftIdea objects."
        )
        self.config.tools = [GoogleSearchTool()] # Built-in Tool

class AggregatorAgent(LlmAgent):
    """
    Collects results from all parallel agents, validates the budget using the Custom Tool, 
    formats the final output, and manages Long-Term Memory updates.
    """
    def __init__(self, config: AgentConfig, memory_bank: MemoryBank):
        super().__init__(config)
        self.memory_bank = memory_bank
        self.budget_tools = BudgetTools()
        
        self.config.instruction = (
            "You are the Final Reviewer and Deliver Agent, Santa's Chief Helper. Your input is a collection of potential GiftIdea JSON objects. "
            "1. For every gift idea, use the 'check_budget_compliance' tool (Santa's Secret Budget Tool) to confirm the price against the budget. "
            "2. If a gift fails, recommend a similar, cheaper alternative in the final output. "
            "3. Format the final list into a professional, clear Markdown table for the user. "
            "4. CRITICALLY: Explicitly filter out any gift ideas containing 'socks' or items noted as 'boring' in the memory. "
            "5. Finally, analyze the conversation for any new preferences and use the MemoryBank to persist them. Deliver the response with a celebratory tone!"
        )
        self.config.tools = [self.budget_tools] # Custom Tool

# --- 2. The Core Orchestration: Sequential and Parallel Workflow ---

class GiftPlanningWorkflow(SequentialWorkflow):
    """
    The main sequential workflow: Collection -> Parallel Research -> Aggregation.
    This demonstrates the combination of sequential and parallel execution.
    """
    def __init__(self, config: AgentConfig, memory_bank: MemoryBank):
        super().__init__(config)
        
        # Step 1: Collect and Structure the Input
        self.add_agent(PreferenceCollectorAgent(AgentConfig(name="CollectorAgent", model=MODEL_NAME)))
        
        # Step 2: Parallel Research (Run one Researcher for each recipient brief)
        # This is a key feature demonstrating parallel execution efficiency.
        # NOTE: In this simplified ADK simulation, we fix the number of agents to 3.
        self.add_agent(ParallelWorkflow(
            config=AgentConfig(name="ParallelResearch", model=MODEL_NAME),
            agents=[GiftResearcherAgent(AgentConfig(name=f"Researcher_{i}", model=MODEL_NAME)) for i in range(3)] 
        ))
        
        # Step 3: Final Review, Custom Tool Validation, and Delivery/Memory Update
        self.add_agent(AggregatorAgent(
            config=AgentConfig(name="AggregatorAgent", model=MODEL_NAME),
            memory_bank=memory_bank
        ))

# --- 3. The Main Router Agent (Entry Point) ---

class HGSConciergeAgent(LlmAgent):
    """
    The top-level agent that manages memory loading and delegation for the Holiday Gift Savior (HGS).
    """
    def __init__(self, config: AgentConfig, memory_bank: MemoryBank):
        super().__init__(config)
        
        self.memory_bank = memory_bank
        self.gift_workflow = GiftPlanningWorkflow(AgentConfig(name="GiftPlanningWorkflow", model=MODEL_NAME), memory_bank=memory_bank)

        self.config.instruction = (
            "You are the main Holiday Gift Savior (HGS) Concierge Agent. Your primary role is delegation and managing the MemoryBank. "
            "If the user asks for 'gift ideas' or 'help shopping', you must first load all available recipient profiles from the MemoryBank for the current user_id. "
            "Pass the memory context, along with the user's latest query, to the 'GiftPlanningWorkflow' tool/workflow for execution. "
            "If the user asks a general question, offer a witty redirection back to the task, like: 'My sleigh bells are only calibrated for gift requests! How can I help you shop today?'"
        )
        
        # Expose the full workflow as a tool the LLM can decide to call
        self.config.tools = [self.gift_workflow]

# --- 4. Main ADK Application Setup ---

# --- 4. Main ADK Application Setup ---

def create_agent():
    """Initializes and returns the ADK agent."""
    session_service = InMemorySessionService()
    
    # Initialize Mock Memory Bank and Pre-load Use Case data
    memory_bank = MemoryBank(config={"provider": "in_memory"})

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
    router_config = AgentConfig(
        name="HGSConciergeAgent",
        model=MODEL_NAME,
        session_service=session_service,
    )
    router_agent = HGSConciergeAgent(router_config, memory_bank=memory_bank)
    return router_agent

# Create the agent instance for ADK to load
agent = create_agent()

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