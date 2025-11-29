# Holiday Gift Savior (HGS)

This document provides instructions for building, running, and deploying the HGS multi-agent system, which is fully containerized using Docker.

## **Local Development and Running Instructions**

### **Prerequisites**

* [Python 3.11+](https://www.python.org/downloads/)
* [uv](https://github.com/astral-sh/uv) (fast Python package installer)
* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
* [Task](https://taskfile.dev/) (optional, for simplified commands)
* Your Gemini API Key (set as an environment variable)

### **1\. Local Setup (Without Docker)**

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

### **2\. Containerized Execution with ADK Web UI (Recommended)**

This method packages the application with all dependencies and serves the agent via ADK's web interface.

#### **Using Task (Recommended):**

```bash
# Build the Docker image
task build

# Build and run the container
task run

# Build and open interactive shell for debugging
task dev
```

#### **Using Docker directly:**

1. **Build the Docker Image:**

   ```bash
   docker build -t holiday-gift-savior .
   ```

2. **Run the Container:**

   ```bash
   docker run -p 3011:3011 -e GEMINI_API_KEY="YOUR_API_KEY_HERE" holiday-gift-savior
   ```

3. **Access the Web UI:**

   Open your browser to [http://localhost:3011](http://localhost:3011)

   The ADK Web UI provides an interactive interface to chat with the agent and see the multi-agent workflow in action.

   **User Profile Loading:** The agent automatically loads recipient profiles based on the `userId` parameter in the session URL (e.g., `?userId=user_johnson_456`). The agent will call the `get_recipient_profiles` tool at the start of each conversation to load personalized data.

## **Deployment to Google Cloud (GCP)**

The HGS agent is production-ready and can be deployed as a highly scalable service using **Cloud Run**. This satisfies the **Agent Deployment** bonus criteria.

### **1\. Push Image to Google Container Registry (GCR)**

Assuming you have the Google Cloud CLI (gcloud) installed and authenticated:

1. **Tag the Image for GCR:** Replace YOUR\_PROJECT\_ID with your actual GCP project ID.
   ```bash
   docker tag hgs-agent:latest gcr.io/YOUR_PROJECT_ID/hgs-agent:latest
   ```

2. **Push the Image:**
   ```bash
   docker push gcr.io/YOUR_PROJECT_ID/hgs-agent:latest
   ```

### **2\. Deploy to Cloud Run**

Cloud Run is the ideal choice for deploying containerized ADK agents as serverless, scalable endpoints.

1. **Deploy the Service:**
   ```bash
   gcloud run deploy hgs-agent-service \
       --image gcr.io/YOUR_PROJECT_ID/hgs-agent:latest \
       --platform managed \
       --region europe-west4 \
       --allow-unauthenticated \
       --set-env-vars GEMINI_API_KEY="YOUR_API_KEY_HERE" \
       --max-instances 5 \
       --memory 1Gi \
       --cpu 1
   ```

2. **Result:** Cloud Run will provide a stable HTTPS endpoint. You can then configure a frontend to send API requests to this endpoint, enabling the full agent functionality for users.
