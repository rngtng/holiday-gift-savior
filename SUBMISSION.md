# Holiday Gift Savior (HGS)

No worries, Santa's Secret Budget Tool helps with thoughtful, budget-compliant holiday gift recommendations.

## About

AI-Driven Concierge Workflow using Multi-Agent Orchestration, Custom Tools (**Santa's Secret Budget Tool**), and Long-Term Memory to generate thoughtful, budget-compliant holiday gift recommendations.

### Problem: The Thoughtful Gift Bottleneck

Holiday gift-giving is often hindered by two primary constraints: time and personalization. Users spend hours manually searching for gifts that meet specific criteria (hobbies, past successful gifts, dislikes) while struggling to stay within strict budget limits for each person. **The ultimate fear? Buying a boring or duplicative gift (e.g., the dreaded 'Socks Clause'),** leading to wasted effort and money.

### Solution: HGS - The Smart Gifting Assistant

The **Holiday Gift Savior (HGS)** is a specialized multi-agent system built on Google's Agent Development Kit (ADK) and powered by Gemini. HGS converts a simple list of recipients and budgets into a curated, executable gift plan.

The solution streamlines the process into three core automated steps:

1. **Profile-Driven Context:** Automatically loads long-term recipient data (interests, past gifts, dislikes) via custom tool from a persistent database, so users never have to re-state preferences.
2. **Parallel Research:** Launches 3 concurrent researcher agents to find gifts for multiple recipients simultaneously, drastically reducing planning time.
3. **Budget Validation:** Uses a custom tool, affectionately called **"Santa's Secret Budget Tool,"** to perform a final, deterministic compliance check (with 5% grace margin) before delivery.

### Core Concept & Value Proposition

The agentic architecture is necessary because the task requires **delegation, coordination, real-time external data access, and non-generative validation**:

* **Parallel Efficiency (Multi-Agent):** For a list of three family members, the system spins up three specialized researcher agents to work simultaneously, an efficiency impossible for a single LLM call.
* **Deterministic Validation (Custom Tool):** Budget compliance is a binary, mathematical check. The custom Python function ensures 100% accurate validation—it is the reliable ledger used by Santa's workshop, a critical process that cannot be reliably performed by the LLM's reasoning alone.
* **Persistent Context (Profile Database):** The system maintains persistent recipient profiles (interests, past gifts, dislikes) in a database, accessed via custom tool, enabling personalized recommendations without users having to repeat preferences across sessions.

## The Implementation

### Technical Architecture: Sequential/Parallel Workflow

The HGS uses a two-stage orchestration: a **Sequential Workflow** for control flow and a **Parallel Workflow** for efficiency.

#### Agents and Roles

| Agent Name | Agent Type | Primary Responsibility | Key Features Used |
| :---- | :---- | :---- | :---- |
| **1. HGS Concierge Agent (Router)** | LLM Agent with Error Handling | The Entry Point. Greets the user, loads persistent recipient profiles from the **profile database** via custom tool, and delegates the task to the main workflow. If the request is not about gifts, it offers a witty redirection back to the task. Includes graceful error handling for model overload (503 errors). | Custom Tool: Profile Loading, Error Recovery |
| **2. Preference Collector** | LLM Agent | Structures the user's input (Recipient, Budget, **Currency**) with persistent profile data into a clean, searchable brief for each recipient. | Context Engineering |
| **3. Gift Researcher Agent** | LLM Agent | **The Research Workhorse.** Launched in **Parallel** for each recipient (3 concurrent instances). Uses **Google Search** to find products, prices, and links in the *specified currency*. | Multi-Agent System (Parallel), Google Search |
| **4. Aggregator Agent** | LLM Agent | Collects all research, performs final budget validation using **"Santa's Secret Budget Tool,"** and formats the delivery. **CRITICAL:** Explicitly filters out items from disliked categories (e.g., 'socks' for Dad) based on loaded profiles and adds a celebratory tone to the final output. | Custom Tool: Budget Validation |

### Features

| Feature | Concept Demonstrated | ADK Implementation Detail |
| :---- | :---- | :---- |
| **Multi-Agent System** | Orchestration & Parallelism | Implemented the GiftPlanningWorkflow using a ParallelAgent (3 concurrent researchers) inside a SequentialAgent, ensuring efficient, concurrent research for multiple recipients. |
| **Custom Tools** | Deterministic Logic & Data Access | **Two custom Python functions**: (1) check_budget_compliance acts as **Santa's final budget ledger**, mathematically validating gift prices against budgets with 5% grace margin. (2) get_recipient_profiles loads persistent RecipientProfile data from a simulated database (USER_PROFILES_DB) containing interests, past gifts, and dislikes for each person. |
| **Persistent Profiles** | Stateful Personalization | The Concierge Agent calls get_recipient_profiles at session start to load user-specific recipient data. This simulates persistent storage that would connect to Firestore in production. Profiles include interests, successful past gifts, and disliked categories. |
| **Built-in Tool** | Grounding/RAG | Google Search is provided to the GiftResearcherAgent for access to real-time product prices, availability, and retail links in the specified currency. |
| **Effective Use of Gemini** | Core Reasoning | Gemini (gemini-2.5-flash-preview-09-2025) powers all agents for complex tasks like synthesizing preferences (Collector), filtering search results (Researcher), and budget validation coordination (Aggregator). |

## Demo

See: https://youtu.be/GC4PvqrQmxg

## The Build

The HGS was built using a combination of Python, Google ADK and Gemini for planning as well as Claude Code for code generation. Key technologies include:

- **Google ADK**: For building the multi-agent system and managing interactions between agents.
- **Google Search API**: To enable real-time product searches and price comparisons.
- **Custom Python Functions**: For budget validation and profile loading.
- **Simulated Database**: To mimic persistent user profiles and preferences.
- **Docker**: For containerizing the application and ensuring consistent development and deployment environments.

Code was mostly generated using Gemini, with manual adjustments for logic and integration.

## If I had more time, this is what I'd do

- connect to real persistent storage (e.g., Firestore) for recipient profiles.
- allow users to add/edit recipient profiles via a user interface.
- enhance error handling and recovery mechanisms.
- expand gift research to include more diverse sources and retailers.
- add user interface for better interaction, expose thumbnails and shopping links of gift options.
- performance testing and optimization.

## Attachments

* [GitHub Repository](https://github.com/rngtng/holiday-gift-savior)
* [Kaggle Notebook](https://www.kaggle.com/competitions/agents-intensive-capstone-project/writeups/holiday-gift-savior-hgs)
