# Use the official Python 3.13 slim image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose the port your application listens on (adjust if needed)
EXPOSE 8000

# Command to run your application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]  