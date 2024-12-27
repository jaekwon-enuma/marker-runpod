FROM python:3.11-slim-bullseye

ENV TORCH_DEVICE="cuda"

RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    libgl1 \
    gcc \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install marker-pdf fastapi uvicorn python-multipart runpod

COPY marker_server.py /app/marker_server.py

WORKDIR /app

CMD ["python", "marker_server"]
