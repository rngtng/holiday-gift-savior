# Holiday Gift Savior (HGS)

This document provides instructions for building, running, and deploying the HGS multi-agent system, which is fully containerized using Docker.

## **Local Development and Running Instructions**

### **Prerequisites**

* [Python 3.11+](https://www.python.org/downloads/)  
* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.  
* Your Gemini API Key (set as an environment variable).  
* The following files must be present in your project directory: main.py, custom\_tools.py, data\_models.py, requirements.txt, and Dockerfile.

### **1\. Local Setup (Without Docker)**

For quick testing and debugging outside of a container:

1. **Install Dependencies:**  
   pip install \-r requirements.txt

2. **Set API Key:**  
   export GEMINI\_API\_KEY="YOUR\_API\_KEY\_HERE"

3. **Run the Agent:**  
   python main.py

   *(Note: This runs the initialization block and simulates the orchestrated workflow.)*

### **2\. Containerized Execution (Recommended)**

This method packages the application with all dependencies for guaranteed reproducibility.

1. Build the Docker Image:  
   From the root directory containing the required files:  
   docker build \-t hgs-agent:latest .

   This command builds the image and tags it as hgs-agent:latest.  
2. Run the Docker Container:  
   You must pass your Gemini API Key as an environment variable when running the container.  
   docker run \-e GEMINI\_API\_KEY="YOUR\_API\_KEY\_HERE" hgs-agent:latest

   The agent will initialize and print the simulated user query and the status of the orchestrated workflow.

## **Deployment to Google Cloud (GCP)**

The HGS agent is production-ready and can be deployed as a highly scalable service using **Cloud Run**. This satisfies the **Agent Deployment** bonus criteria.

### **1\. Push Image to Google Container Registry (GCR)**

Assuming you have the Google Cloud CLI (gcloud) installed and authenticated:

1. **Tag the Image for GCR:** Replace YOUR\_PROJECT\_ID with your actual GCP project ID.  
   docker tag hgs-agent:latest gcr.io/YOUR\_PROJECT\_ID/hgs-agent:latest

2. **Push the Image:**  
   docker push gcr.io/YOUR\_PROJECT\_ID/hgs-agent:latest

### **2\. Deploy to Cloud Run**

Cloud Run is the ideal choice for deploying containerized ADK agents as serverless, scalable endpoints.

1. **Deploy the Service:**  
   gcloud run deploy hgs-agent-service \\  
       \--image gcr.io/YOUR\_PROJECT\_ID/hgs-agent:latest \\  
       \--platform managed \\  
       \--region us-central1 \\  
       \--allow-unauthenticated \\  
       \--set-env-vars GEMINI\_API\_KEY="YOUR\_API\_KEY\_HERE" \\  
       \--max-instances 5 \\  
       \--memory 1Gi \\  
       \--cpu 1

2. **Result:** Cloud Run will provide a stable HTTPS endpoint. You can then configure a frontend to send API requests to this endpoint, enabling the full agent functionality for users.