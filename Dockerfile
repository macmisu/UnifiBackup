# Use the official Python image as a base image
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y firefox-esr \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/unifi -s /bin/sh unifi

# Install Python packages
RUN pip install selenium \
    webdriver_manager \
    boto3

# Set the working directory
WORKDIR /app

COPY unifibackup.py .
RUN chown -R unifi:unifi /app

USER unifi

ENTRYPOINT ["python", "unifibackup.py"]
