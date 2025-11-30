# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Holiday Gift Savior is a multi-agent system built with Google's Agent Development Kit (ADK) that helps users find appropriate gifts for recipients based on persistent preferences, budgets, and constraints. The system demonstrates sequential and parallel agent orchestration, custom tools, and long-term memory management.

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

# Agent Development Kit (ADK)

Agent Development Kit (ADK)

## ADK Python Repository

Agent Development Kit (ADK)

An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control.

Agent Development Kit (ADK) is a flexible and modular framework for developing and deploying AI agents. While optimized for Gemini and the Google ecosystem, ADK is model-agnostic, deployment-agnostic, and is built for compatibility with other frameworks. ADK was designed to make agent development feel more like software development, to make it easier for developers to create, deploy, and orchestrate agentic architectures that range from simple tasks to complex workflows.


✨ Key Features

Rich Tool Ecosystem
: Utilize pre-built tools, custom functions,
  OpenAPI specs, or integrate existing tools to give agents diverse
  capabilities, all for tight integration with the Google ecosystem.

Code-First Development
: Define agent logic, tools, and orchestration
  directly in Python for ultimate flexibility, testability, and versioning.

Modular Multi-Agent Systems
: Design scalable applications by composing
  multiple specialized agents into flexible hierarchies.

Deploy Anywhere
: Easily containerize and deploy agents on Cloud Run or
  scale seamlessly with Vertex AI Agent Engine.

🤖 Agent2Agent (A2A) Protocol and ADK Integration

For remote agent-to-agent communication, ADK integrates with the A2A protocol. See this  example for how they can work together.


🚀 Installation


Stable Release (Recommended)


You can install the latest stable version of ADK using pip:


pip install google-adk



The release cadence is weekly.


This version is recommended for most users as it represents the most recent official release.


Development Version


Bug fixes and new features are merged into the main branch on GitHub first. If you need access to changes that haven't been included in an official PyPI release yet, you can install directly from the main branch:


pip install git+https://github.com/google/adk-python.git@main



Note: The development version is built directly from the latest code commits. While it includes the newest fixes and features, it may also contain experimental changes or bugs not present in the stable release. Use it primarily for testing upcoming changes or accessing critical fixes before they are officially released.


📚 Documentation


Explore the full documentation for detailed guides on building, evaluating, and
deploying agents:




Documentation




🏁 Feature Highlight


Define a single agent:


from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.5-flash", # Or your preferred Gemini model
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search]
)



Define a multi-agent system:


Define a multi-agent system with coordinator agent, greeter agent, and task execution agent. Then ADK engine and the model will guide the agents works together to accomplish the task.


from google.adk.agents import LlmAgent, BaseAgent

# Define individual agents
greeter = LlmAgent(name="greeter", model="gemini-2.5-flash", ...)
task_executor = LlmAgent(name="task_executor", model="gemini-2.5-flash", ...)

# Create parent agent and assign children via sub_agents
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.5-flash",
    description="I coordinate greetings and tasks.",
    sub_agents=[ # Assign sub_agents here
        greeter,
        task_executor
    ]
)



Development UI


A built-in development UI to help you test, evaluate, debug, and showcase your agent(s).




Evaluate Agents


adk eval \
    samples_for_testing/hello_world \
    samples_for_testing/hello_world/hello_world_eval_set_001.evalset.json



Happy Agent Building!

**Source:** [adk-python repository](https://github.com/google/adk-python)

## Documentation

- [Custom agents](https://github.com/google/adk-docs/blob/main/docs/agents/custom-agents.md)
- [Agents](https://github.com/google/adk-docs/blob/main/docs/agents/index.md)
- [LLM Agent](https://github.com/google/adk-docs/blob/main/docs/agents/llm-agents.md)
- [Using Different Models with ADK](https://github.com/google/adk-docs/blob/main/docs/agents/models.md)
- [Multi-Agent Systems in ADK](https://github.com/google/adk-docs/blob/main/docs/agents/multi-agents.md)
- [Workflow Agents](https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/index.md)
- [Loop agents](https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/loop-agents.md)
- [Parallel agents](https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/parallel-agents.md)
- [Sequential agents](https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/sequential-agents.md)
- [API Reference](https://github.com/google/adk-docs/blob/main/docs/api-reference/index.md)
- [Artifacts](https://github.com/google/adk-docs/blob/main/docs/artifacts/index.md)
- [Design Patterns and Best Practices for Callbacks](https://github.com/google/adk-docs/blob/main/docs/callbacks/design-patterns-and-best-practices.md)
- [Callbacks: Observe, Customize, and Control Agent Behavior](https://github.com/google/adk-docs/blob/main/docs/callbacks/index.md)
- [Types of Callbacks](https://github.com/google/adk-docs/blob/main/docs/callbacks/types-of-callbacks.md)
- [Community Resources](https://github.com/google/adk-docs/blob/main/docs/community.md)
- [Context](https://github.com/google/adk-docs/blob/main/docs/context/index.md)
- [1. [`google/adk-python`](https://github.com/google/adk-python)](https://github.com/google/adk-docs/blob/main/docs/contributing-guide.md)
- [Deploy to Vertex AI Agent Engine](https://github.com/google/adk-docs/blob/main/docs/deploy/agent-engine.md)
- [Deploy to Cloud Run](https://github.com/google/adk-docs/blob/main/docs/deploy/cloud-run.md)
- [Deploy to GKE](https://github.com/google/adk-docs/blob/main/docs/deploy/gke.md)
- [Deploying Your Agent](https://github.com/google/adk-docs/blob/main/docs/deploy/index.md)
- [Why Evaluate Agents](https://github.com/google/adk-docs/blob/main/docs/evaluate/index.md)
- [Events](https://github.com/google/adk-docs/blob/main/docs/events/index.md)
- [Agent Development Kit (ADK)](https://github.com/google/adk-docs/blob/main/docs/get-started/about.md)
- [Get Started](https://github.com/google/adk-docs/blob/main/docs/get-started/index.md)
- [Installing ADK](https://github.com/google/adk-docs/blob/main/docs/get-started/installation.md)
- [Quickstart](https://github.com/google/adk-docs/blob/main/docs/get-started/quickstart.md)
- [Streaming Quickstarts](https://github.com/google/adk-docs/blob/main/docs/get-started/streaming/index.md)
- [Quickstart (Streaming / Java) {#adk-streaming-quickstart-java}](https://github.com/google/adk-docs/blob/main/docs/get-started/streaming/quickstart-streaming-java.md)
- [Quickstart (Streaming / Python) {#adk-streaming-quickstart}](https://github.com/google/adk-docs/blob/main/docs/get-started/streaming/quickstart-streaming.md)
- [Testing your Agents](https://github.com/google/adk-docs/blob/main/docs/get-started/testing.md)
- [What is Agent Development Kit?](https://github.com/google/adk-docs/blob/main/docs/index.md)
- [Model Context Protocol (MCP)](https://github.com/google/adk-docs/blob/main/docs/mcp/index.md)
- [Agent Observability with Arize AX](https://github.com/google/adk-docs/blob/main/docs/observability/arize-ax.md)
- [Agent Observability with Phoenix](https://github.com/google/adk-docs/blob/main/docs/observability/phoenix.md)
- [Runtime](https://github.com/google/adk-docs/blob/main/docs/runtime/index.md)
- [Runtime Configuration](https://github.com/google/adk-docs/blob/main/docs/runtime/runconfig.md)
- [Safety & Security for AI Agents](https://github.com/google/adk-docs/blob/main/docs/safety/index.md)
- [Introduction to Conversational Context: Session, State, and Memory](https://github.com/google/adk-docs/blob/main/docs/sessions/index.md)
- [Memory: Long-Term Knowledge with `MemoryService`](https://github.com/google/adk-docs/blob/main/docs/sessions/memory.md)
- [Session: Tracking Individual Conversations](https://github.com/google/adk-docs/blob/main/docs/sessions/session.md)
- [State: The Session's Scratchpad](https://github.com/google/adk-docs/blob/main/docs/sessions/state.md)
- [Configurating streaming behaviour](https://github.com/google/adk-docs/blob/main/docs/streaming/configuration.md)
- [Custom Audio Streaming app (WebSocket) {#custom-streaming-websocket}](https://github.com/google/adk-docs/blob/main/docs/streaming/custom-streaming-ws.md)
- [Custom Audio Streaming app (SSE) {#custom-streaming}](https://github.com/google/adk-docs/blob/main/docs/streaming/custom-streaming.md)
- [ADK Bidi-streaming development guide: Part 1 - Introduction](https://github.com/google/adk-docs/blob/main/docs/streaming/dev-guide/part1.md)
- [Bidi-streaming(live) in ADK](https://github.com/google/adk-docs/blob/main/docs/streaming/index.md)
- [Streaming Tools](https://github.com/google/adk-docs/blob/main/docs/streaming/streaming-tools.md)
- [Authenticating with Tools](https://github.com/google/adk-docs/blob/main/docs/tools/authentication.md)
- [Built-in tools](https://github.com/google/adk-docs/blob/main/docs/tools/built-in-tools.md)
- [Function tools](https://github.com/google/adk-docs/blob/main/docs/tools/function-tools.md)
- [Google Cloud Tools](https://github.com/google/adk-docs/blob/main/docs/tools/google-cloud-tools.md)
- [Tools](https://github.com/google/adk-docs/blob/main/docs/tools/index.md)
- [Model Context Protocol Tools](https://github.com/google/adk-docs/blob/main/docs/tools/mcp-tools.md)
- [OpenAPI Integration](https://github.com/google/adk-docs/blob/main/docs/tools/openapi-tools.md)
- [Third Party Tools](https://github.com/google/adk-docs/blob/main/docs/tools/third-party-tools.md)
- [Build Your First Intelligent Agent Team: A Progressive Weather Bot with ADK](https://github.com/google/adk-docs/blob/main/docs/tutorials/agent-team.md)
- [ADK Tutorials!](https://github.com/google/adk-docs/blob/main/docs/tutorials/index.md)
- [Python API Reference](https://github.com/google/adk-docs/blob/main/docs/api-reference/python/)
