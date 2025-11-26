# Holiday Gift Savior (HGS)

AI-Driven Concierge Workflow using Multi-Agent Orchestration, Custom Tools (**Santa's Secret Budget Tool**), and Long-Term Memory to generate thoughtful, budget-compliant holiday gift recommendations.

## Submission Track

**Concierge Agents** (Focus: Automating complex personal and family coordination tasks.)

## Category 1: The Pitch (Problem, Solution, Value)

### 1. Problem Statement: The Thoughtful Gift Bottleneck

Holiday gift-giving is often hindered by two primary constraints: time and personalization. Users spend hours manually searching for gifts that meet specific criteria (hobbies, past successful gifts, dislikes) while struggling to stay within strict budget limits for each person. **The ultimate fear? Buying a boring or duplicative gift (e.g., the dreaded 'Socks Clause'),** leading to wasted effort and money.

### 2. Solution Statement: HGS \- The Smart Gifting Assistant

The **Holiday Gift Savior (HGS)** is a specialized multi-agent system built on Google's Agent Development Kit (ADK) and powered by Gemini. HGS converts a simple list of recipients and budgets into a curated, executable gift plan.

The solution streamlines the process into three core automated steps:

1. **Memory-Driven Context:** Automatically recalls long-term recipient interests (e.g., "Dad loves vintage cameras") so the user never has to re-state them.  
2. **Parallel Research:** Launches concurrent agents to research gifts for multiple recipients at once, drastically reducing planning time.  
3. **Budget Validation:** Uses a custom tool, affectionately called **"Santa's Secret Budget Tool,"** to perform a final, deterministic compliance check before delivery.

### 3. Core Concept & Value (Why Agents?)

The agentic architecture is necessary because the task requires **delegation, coordination, real-time external data access, and non-generative validation**:

* **Parallel Efficiency (Multi-Agent):** For a list of five family members, the system spins up five specialized researcher agents to work simultaneously, an efficiency impossible for a single LLM call.  
* **Deterministic Validation (Custom Tool):** Budget compliance is a binary, mathematical check. The custom Python function ensures 100% accurate validation—it is the reliable ledger used by Santa's workshop, a critical process that cannot be reliably performed by the LLM's reasoning alone.  
* **Adaptation (Memory):** The agent learns and adapts by storing recipient profiles, making the quality of the recommendations better with every passing holiday season.

## Category 2: The Implementation

### 1. Technical Architecture: Sequential/Parallel Workflow

The HGS uses a two-stage orchestration: a **Sequential Workflow** for control flow and a **Parallel Workflow** for efficiency.

#### **Agents and Roles:**

| Agent Name | Agent Type | Primary Responsibility | Key Features Used |
| :---- | :---- | :---- | :---- |
| **1\. Router Agent (The Concierge)** | LLM Agent | The Entry Point. Greets the user, loads persistent recipient profiles from **Memory Bank**, and delegates the task to the main workflow. If the request is not about gifts, it offers a witty redirection back to the task. | **Sessions & Memory Retrieval** |
| **2\. Preference Collector** | LLM Agent | Structures the user's input (Recipient, Budget, **Currency**) with persistent memory data into a clean, searchable brief. | Context Engineering |
| **3\. Gift Researcher Agent** | LLM Agent | **The Research Workhorse.** Launched in **Parallel** for each recipient. Uses **Google Search** to find products, prices, and links in the *specified currency*. | **Multi-Agent System (Parallel)**, **Built-in Tool: Google Search** |
| **4\. Aggregator Agent** | LLM Agent | Collects all research, performs final budget validation using **"Santa's Secret Budget Tool,"** updates the memory, and formats the delivery. **CRITICAL:** Explicitly filters out 'socks' or items noted as 'boring' in the memory and adds a celebratory tone to the final output. | **Custom Tool**, **Memory Update** |

### **2\. Mandatory Features Included**

(Min. 3 required, 5 achieved)

| Feature | Concept Demonstrated | ADK Implementation Detail |
| :---- | :---- | :---- |
| **Multi-Agent System** | Orchestration & Parallelism | Implemented the GiftPlanningWorkflow using a ParallelWorkflow inside a SequentialWorkflow, ensuring efficient, concurrent research. |
| **Custom Tool** | Deterministic Logic | The AggregatorAgent calls a Python function, check\_budget\_compliance, which acts as **Santa's final budget ledger**, to mathematically validate that the real-time gift price does not exceed the allocated budget. |
| **Sessions & Memory** | Persistent Personalization | The Router Agent retrieves RecipientProfile data (e.g., interests, dislikes) from the Memory Bank at the start of the session for personalization. The Aggregator Agent saves new preferences. |
| **Built-in Tool** | Grounding/RAG | Google Search is provided to the GiftResearcherAgent for access to real-time product prices, availability, and retail links. |
| **Effective Use of Gemini** | Core Reasoning | Gemini powers all agents for complex tasks like synthesizing preferences (Collector) and filtering search results (Researcher). |

### **3\. Documentation**

All code for the HGS (including main.py, custom\_tools.py, and data\_models.py) is provided in the linked repository. The system is containerized for easy deployment. For setup instructions, refer to **TECHNICAL\_README.md**.

## **Bonus Criteria**

* **Effective Use of Gemini:** Gemini (gemini-2.5-flash-preview-09-2025) is the reasoning engine across all specialized agents, driving complex delegation and synthesis tasks.  
* **Agent Deployment:** The architecture is designed for scalability and deployment via containerization (Docker) to **Cloud Run** or **Vertex AI Agent Engine**. **(See TECHNICAL\_README.md for deployment guide.)**  
* **YouTube Video Submission:** A video will demonstrate the full user flow:  
  1. **Memory Setup:** User states a new preference ("My brother now loves baking").  
  2. **Workflow Trigger:** User requests gifts for three recipients with budgets.  
  3. **Result:** The HGS successfully recommends a baking-related gift for the brother, uses the Custom Tool to confirm the price is under budget, and outputs the final curated list with a celebratory tone.

**Attachments:**

* \[GitHub Repository Link: Your-Repository-URL-Here\]  
* \[Kaggle Notebook Link: Your-Kaggle-Notebook-URL-Here\]