# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Holiday Gift Savior (HGS) is a multi-agent system built with Google's Agent Development Kit (ADK) that helps users find appropriate gifts for recipients based on persistent preferences, budgets, and constraints. The system demonstrates sequential and parallel agent orchestration, custom tools, and long-term memory management.

## Development Commands

- make sure to use `uv` to manage all dependencies
- use `uv` to run python files
- always use `uv` to run the server do not use pip directly

### Local Development (requires Python 3.11+ and uv)

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your_api_key_here"

# View available user profiles
uv run view_users.py

# Note: The agent runs via Docker/ADK Web UI (see below)
```

### Docker Development (recommended)
```bash
# Using Task (recommended)
task build    # Build the Docker image
task run      # Build and run the container
task dev      # Build and open interactive shell

# Using Docker directly
docker build -t holiday-gift-savior .
docker run -p 3011:3011 -e GEMINI_API_KEY="your_key" holiday-gift-savior
docker run -it -p 3011:3011 -e GEMINI_API_KEY="your_key" -v .:/app holiday-gift-savior bash
```

### ADK Web Interface
The agent is served via the ADK Web UI on port 3011 when running in Docker. Access at `http://localhost:3011`

## Architecture

### Multi-Agent Orchestration Pattern

The system uses a hierarchical agent architecture combining **sequential** and **parallel** execution:

```
HGSConciergeAgent (Sequential Router)
  └─> GiftPlanningWorkflow (Sequential)
       ├─> CollectorAgent (LLM) - Structures briefs from user query + memory
       ├─> ParallelResearch (Parallel) - Runs 3 concurrent GiftResearcherAgents
       │    └─> Each uses google_search tool to find gift ideas
       └─> AggregatorAgent (LLM) - Validates budget, filters results, updates memory
```

**Key insight**: The parallel research phase demonstrates ADK's ability to spawn multiple identical agents that process different inputs concurrently (one per recipient brief).

### Agent Factory Pattern

All agents use **factory functions** rather than direct instantiation:
- `PreferenceCollectorAgent(**kwargs)` - Creates the collector
- `GiftResearcherAgent(**kwargs)` - Creates a researcher (for parallel execution)
- `create_aggregator_agent(memory_bank, **kwargs)` - Creates the aggregator with memory access
- `create_gift_planning_workflow(memory_bank, **kwargs)` - Creates the sequential workflow
- `create_concierge_agent(memory_bank, **kwargs)` - Creates the top-level router

This pattern allows ADK to properly configure and instantiate agents with shared resources (like memory services).

### Custom Tools

The system includes one custom tool in [custom_tools.py](agent/custom_tools.py):
- `check_budget_compliance()` - A `@FunctionTool` decorated function that validates gift prices against budgets with a 5% grace margin

Custom tools must:
1. Be decorated with `@FunctionTool`
2. Have clear type hints for parameters
3. Have comprehensive docstrings (used for tool selection)
4. Return string values (typically JSON for structured data)

### Data Models

[data_models.py](agent/data_models.py) defines two core schemas:
- `RecipientProfile` - Long-term memory schema for persistent preferences (interests, past gifts, dislikes)
- `GiftIdea` - Inter-agent communication schema for passing gift recommendations between agents

### Memory Management

The system uses `InMemoryMemoryService` for long-term memory simulation. In production, this would connect to Firestore or another persistent store. Memory is:
1. Pre-loaded with recipient profiles in `create_agent()`
2. Read by the CollectorAgent to enrich search queries
3. Updated by the AggregatorAgent based on new preferences learned from conversations

## Entry Point

The ADK expects a module-level `root_agent` variable:
```python
# In agent/__init__.py
from .agent import root_agent
__all__ = ['root_agent']
```

The `root_agent` is created via `create_agent()` in [agent.py](agent/agent.py), which initializes services and returns the configured concierge agent.

## Configuration

- **Model**: Uses `gemini-2.5-flash-preview-09-2025` (defined in `agent.py`)
- **Port**: ADK Web UI runs on port 3011 (configurable in Dockerfile)
- **API Key**: Required via `GEMINI_API_KEY` environment variable

## Dependencies

Core dependencies in [requirements.txt](requirements.txt):
- `google-adk[eval]` - Agent Development Kit with evaluation tools
- `google-genai` - Gemini API client
- `pydantic` - Data validation for models

## GCP Deployment

The agent can be deployed to Google Cloud Run:
```bash
# Tag and push to GCR
docker tag holiday-gift-savior:latest gcr.io/YOUR_PROJECT_ID/hgs-agent:latest
docker push gcr.io/YOUR_PROJECT_ID/hgs-agent:latest

# Deploy to Cloud Run
gcloud run deploy hgs-agent-service \
    --image gcr.io/YOUR_PROJECT_ID/hgs-agent:latest \
    --platform managed \
    --region europe-west4 \
    --allow-unauthenticated \
    --set-env-vars GEMINI_API_KEY="your_key" \
    --max-instances 5 \
    --memory 1Gi \
    --cpu 1
```

## Important Implementation Details

1. **Parallel Agent Count**: The system is hardcoded to 3 parallel researchers. This should match the expected number of recipient briefs from the collector.

2. **JSON Output Requirements**: Agents that pass structured data must explicitly instruct the LLM to output valid JSON. See the instruction strings in agent factory functions.

3. **Memory Filtering**: The AggregatorAgent is explicitly instructed to filter out items marked as "boring" or "socks" - this demonstrates using memory data for negative constraints.

4. **Budget Compliance**: All gifts must pass through `check_budget_compliance` before final delivery. The aggregator should suggest alternatives for failed items.

5. **Legacy Classes**: Empty classes like `AggregatorAgent(LlmAgent)` and `GiftPlanningWorkflow(SequentialAgent)` exist for backwards compatibility but should not be instantiated directly.
