# Use the official Python image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /src

# Copy the application code from the host machine
COPY src/ /src

# Copy the requirements file from the host machine
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5009

# Run the application
CMD ["python3", "app.py"]
