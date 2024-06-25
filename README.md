# Unifi Backup Automation

The Unifi API spec seems to be a bit **dense**..so I chose the worst route of them all and automated backups through Selenium.

## Overview

This project provides an automated solution for backing up your Unifi Controller using Selenium WebDriver. It logs into the Unifi Controller's web interface, initiates a backup, and saves the backup file. Optionally, the backup file can be uploaded to an S3 bucket.

## Prerequisites

- Docker
- Docker Compose

## Environment Variables

The following environment variables need to be set for the script to work:

- `USERNAME`: Username for logging into the Unifi Controller (optional)
- `PASSWORD`: Password for logging into the Unifi Controller
- `UNIFI_IP`: IP address of the Unifi Controller
- `BACKUP_INTERVAL`: Interval in hours between each backup (default: 24 hours)
- `OUTPUT_DIRECTORY`: Directory to save the backup files (default: `~/Downloads`)
- `AWS_ACCESS_KEY`: AWS access key (optional, required if uploading to S3)
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key (optional, required if uploading to S3)
- `AWS_REGION`: AWS region (optional, required if uploading to S3)
- `TARGET_BUCKET`: S3 bucket name to upload the backup file (optional)

## Usage

1. **Clone the repository**

   ```sh
   git clone https://github.com/kwehen/UnifiBackup.git
   cd UnifiBackup
   ```

2. **Build and run the Docker container**

   The repository includes a `docker-compose.yml` file and a `Dockerfile`:

   - **Docker Compose file**: Defines a service named `unifibackup` that uses the `jeffhardyski/unifibackup:0.1` image. It sets the environment variables required for the backup script and ensures the container restarts unless stopped.

   Run the Docker container:

   ```sh
   docker-compose up -d
   ```

## Dockerfile

The Dockerfile used to build the Docker image:

```dockerfile
# Use the official Python image as a base image
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Install required packages
RUN pip install selenium
RUN pip install webdriver_manager
RUN pip install boto3

# Set the working directory
WORKDIR /app

# Copy your Selenium WebDriver script into the container
COPY unifibackup.py .

# Define the command to execute your script
CMD ["python", "unifibackup.py"]
```

## Script Explanation

### unifibackup.py

This script performs the following steps:

1. Loads environment variables.
2. Sets up the Selenium WebDriver with Firefox in headless mode.
3. Logs into the Unifi Controller.
4. Initiates a backup and waits for the backup file to download.
5. Moves the backup file to the specified output directory.
6. Uploads the backup file to an S3 bucket (if configured).
7. Repeats the process at the specified interval.

### Logging

The script uses Python's built-in logging module to log information and errors.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## Issues

If you have an issue, or would like an additional backup target to be added, please create an issue.
