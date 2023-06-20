# Use the official Python image from the Docker Hub
FROM python:3.9-slim-buster

# Set the working directory in the Docker container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Set an environment variable with the default port to use
ENV PORT=5001 

# Expose the port the app runs in
EXPOSE $PORT

# Define the command that will be executed when the Docker container starts
CMD ["python", "app.py"]
