e an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose any necessary ports (not required unless you have a web service running)
# EXPOSE 5000

# Set the entry point to the main script that runs your pipeline
CMD ["python", "main.py"]

