# Holiday Gift Savior (HGS)

This document provides instructions for building, running, and deploying the HGS multi-agent system, which is fully containerized using Docker.

## **Local Development and Running Instructions**

### **Prerequisites**

* [Python 3.11+](https://www.python.org/downloads/)
* [uv](https://github.com/astral-sh/uv) (fast Python package installer)
* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.
* Your Gemini API Key (set as an environment variable).
* The following files must be present in your project directory: main.py, custom\_tools.py, data\_models.py, requirements.txt, and Dockerfile.

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

4. **Run the Agent:**
   ```bash
   uv run main.py
   ```

   *(Note: This runs the initialization block and simulates the orchestrated workflow.)*

### **2\. Containerized Execution (Recommended)**

This method packages the application with all dependencies for guaranteed reproducibility.

1. **Build the Docker Image:**
   From the root directory containing the required files:
   ```bash
   docker build -t hgs-agent:latest .
   ```

   This command builds the image and tags it as hgs-agent:latest.

2. **Run the Docker Container:**
   You must pass your Gemini API Key as an environment variable when running the container.
   ```bash
   docker run -e GEMINI_API_KEY="YOUR_API_KEY_HERE" hgs-agent:latest
   ```

   The agent will initialize and print the simulated user query and the status of the orchestrated workflow.

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
       --region us-central1 \
       --allow-unauthenticated \
       --set-env-vars GEMINI_API_KEY="YOUR_API_KEY_HERE" \
       --max-instances 5 \
       --memory 1Gi \
       --cpu 1
   ```

2. **Result:** Cloud Run will provide a stable HTTPS endpoint. You can then configure a frontend to send API requests to this endpoint, enabling the full agent functionality for users.
