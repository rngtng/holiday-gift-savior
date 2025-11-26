# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to minimize image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container
COPY . .

# Set environment variable for the model API key (REQUIRED for runtime)
# NOTE: This must be provided when running the container (e.g., via -e GEMINI_API_KEY=...)
ENV GEMINI_API_KEY=""

# Command to run the application when the container starts
# We run the main async function in main.py
CMD ["python", "main.py"]