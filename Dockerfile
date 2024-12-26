# -------------------------------------
# Dockerfile to run marker on RunPod
# -------------------------------------
FROM python:3.10-slim-bullseye

# (Optional) Set environment variables for controlling Torch device
ENV TORCH_DEVICE="cuda"

# Install system dependencies
# We install git (for pip install from git) and others that might be needed
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    libgl1 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# (Option A) Install marker from PyPI
# If you want the latest stable release from PyPI:
RUN pip install marker-pdf

# (Option B) OR install marker from GitHub
# If you want to install from the main branch on GitHub, uncomment below:
# RUN pip install git+https://github.com/VikParuchuri/marker.git@master

# Install optional dependencies for the server
RUN pip install fastapi uvicorn python-multipart

# Copy over a simple server script
COPY marker_server.py /app/marker_server.py

WORKDIR /app

# Expose the port that uvicorn will run on (e.g., 8000)
EXPOSE 8000

# Command to run when container starts
# This starts a simple FastAPI server with marker
CMD ["uvicorn", "marker_server:app", "--host", "0.0.0.0", "--port", "8000"]
