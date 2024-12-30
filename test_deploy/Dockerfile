M python:3.8-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . /app/

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]


