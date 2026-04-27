FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for MySQL client and build tools
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and ML models
# Note: We copy ml/models specifically as the backend expects it at ../ml/models
COPY backend/ /app/backend/
COPY ml/ /app/ml/

# Set environment variables
ENV PYTHONPATH=/app
ENV DB_HOST=db
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_NAME=cardiosense

EXPOSE 8000

# Run FastAPI using uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
