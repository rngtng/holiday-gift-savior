# Holiday Gift Savior

Google ADK based AI-Agentic Demo project for Kaggle Capstone Project




## **Local Development and Running Instructions**

### **Prerequisites**

* [Python 3.11+](https://www.python.org/downloads/)
* [uv](https://github.com/astral-sh/uv) (fast Python package installer)
* [Task](https://taskfile.dev/) (optional, for simplified commands)
* [Docker](https://www.docker.com/) (optional, for dependency management and containerization)
* Your Gemini API Key (set as an environment variable)

### Local Setup (Without Docker)

For quick testing and debugging outside of a container:

1. **Install uv:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set API Key:**
   ```bash
   export GEMINI_API_KEY="YOUR_API_KEY_HERE"
   ```

4. **View Available User Profiles:**

   ```bash
   uv run view_users.py
   ```

   This displays all demo users and their recipient profiles.

   Available user IDs: `family_smith_123`, `user_johnson_456`, `corporate_hr_789`, `student_alex_321`

   **Note:** The agent runs via the ADK Web UI (see Containerized Execution section below) and automatically loads user profiles based on the `userId` parameter in the session URL.

### Containerized Execution with ADK Web UI (Recommended)

This method packages the application with all dependencies and serves the agent via ADK's web interface.

#### Using Task (Recommended)

```bash
# Build the Docker image
task build

# Build and run the container
task run

# Build and open interactive shell for debugging
task dev
```

#### Using Docker directly

1. **Build the Docker Image:**

   ```bash
   docker build -t holiday-gift-savior .
   ```

2. **Run the Container:**

   ```bash
   docker run -p 8000:8000 -e GEMINI_API_KEY="YOUR_API_KEY_HERE" holiday-gift-savior
   ```

3. **Access the Web UI:**

   Open your browser to [http://localhost:8000](http://localhost:8000)

   The ADK Web UI provides an interactive interface to chat with the agent and see the multi-agent workflow in action.

   **User Profile Loading:** The agent automatically loads recipient profiles based on the `userId` parameter in the session URL (e.g., `?userId=user_johnson_456`). The agent will call the `get_recipient_profiles` tool at the start of each conversation to load personalized data.
