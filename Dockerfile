# Use an official Python runtime as a parent image
FROM python:3.11

COPY google-cloud-cli-linux-x86_64.tar.gz .
RUN tar -xf google-cloud-cli-linux-x86_64.tar.gz && \
    ./google-cloud-sdk/install.sh --quiet && \
    rm google-cloud-cli-linux-x86_64.tar.gz

# Update PATH environment variable to include Google Cloud SDK
ENV PATH="/google-cloud-sdk/bin:${PATH}"

# Install uv for faster dependency resolution
RUN pip install --upgrade pip uv

# Set the working directory in the container
WORKDIR /app
RUN mkdir -p /app/agent

# Copy the requirements file into the container
COPY agent/requirements.txt agent/requirements.txt

# Install Python dependencies using uv (much faster than pip)
RUN uv pip install --system --no-cache -r agent/requirements.txt

# Copy the rest of the application source code into the container
COPY . .

# Set environment variable for the model API key (REQUIRED for runtime)
# NOTE: This must be provided when running the container (e.g., via -e GEMINI_API_KEY=...)
ENV GEMINI_API_KEY=""

# Expose port 3011 for ADK Web UI
EXPOSE 3011

# Command to run the application when the container starts
# We run adk web to serve the agent
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "3011", "."]
