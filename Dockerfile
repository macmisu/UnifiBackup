# Use the official Python image as a base image
FROM python:3.8-slim

RUN apt-get update \
    && apt-get install -y firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Install required packages
RUN pip install selenium
RUN pip install webdriver_manager

# Set the working directory
WORKDIR /app

# Copy your Selenium WebDriver script into the container
COPY unifibackup.py .

# Define the command to execute your script
CMD ["python", "unifibackup.py"]
