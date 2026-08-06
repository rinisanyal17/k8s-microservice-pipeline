# Use a lightweight official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency definition first (takes advantage of Docker layer caching)
COPY requirements.txt .

# Install dependencies inside the container image
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Expose the port Flask listens on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
