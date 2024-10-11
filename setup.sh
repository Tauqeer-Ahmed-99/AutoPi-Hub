#!/bin/bash

# Update system packages
# sudo apt-get update -y
# sudo apt-get upgrade -y

# PostgreSQL Setup
# Uninstall PostgreSQL in case present (it will delete all the existing postgresql databases from system)
sudo apt-get --purge remove postgresql postgresql-*
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib libpq-dev python3-dev 
# Start PostgreSQL service
sudo service postgresql start
# Set up PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER autopi_hub WITH PASSWORD 'autopi_hub';"
sudo -u postgres psql -c "CREATE DATABASE autopi_hub OWNER autopi_hub;"

# Install Global Packages Python3 and pip
sudo apt-get install python3 python3-pip -y  # Install Python and Pip
sudo apt-get install lsof -y # Install lsof to kill process on a specific port
sudo apt install python3-venv # Install Python virtual environment

# Create and Activate Virtual Env
python3 -m venv venv # Create a virtual environment
source venv/bin/activate # Activate virtual environment

# Install packages which cant be installed in requirements.txt
pip install --upgrade pip # Upgrade pip to the latest version
pip install "fastapi[standard]"
sudo apt-get install python3-rpi.gpio # Install RPi.GPIO package
python3 -m pip install RPi.GPIO # Install RPi.GPIO package

# Install project dependencies
pip install -r requirements.txt

# Database 
alembic revision --autogenerate -m "AutoPi-Hub" # Regenerate and apply new migrations
alembic upgrade head # Apply the new migration

# Reister HomeAutomationSystem Service to start automatically on boot

# Define the service file path
SERVICE_FILE="/etc/systemd/system/autopihub.service"
# Get the current username
USER_NAME=$(whoami)
# Create the autopihub.service file
sudo bash -c "cat > $SERVICE_FILE" << EOL
[Unit]
Description=AutoPi Hubs's Home Automation System with FastAPI Application
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=/home/$USER_NAME/AutoPi-Hub
ExecStart=/home/$USER_NAME/AutoPi-Hub/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000 --ws websockets
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOL

# Reload the systemd manager configuration
sudo systemctl daemon-reload
# Enable the FastAPI service to start on boot
sudo systemctl enable autopihub
# Start the FastAPI service
# sudo systemctl start autopihub
# Check the status of the FastAPI service
# sudo systemctl status autopihub

# Kill any process on port 8000
sudo kill -9 `sudo lsof -t -i:8000`

# Start the Python server
fastapi run server.py 
# uvicorn server:app --host 0.0.0.0 --port 8000 --ws websockets
