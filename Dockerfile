# Use a lightweight Python base image
FROM python:3.11-slim

# Install system dependencies required by OpenCV
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (including uploads folder if it exists)
COPY . .

# Ensure uploads folder exists inside the container
RUN mkdir -p /app/uploads

# Expose the port Flask/Gunicorn will run on
ENV PORT=8080

# Start the Flask app using Gunicorn (production server)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
