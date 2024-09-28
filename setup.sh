#!/bin/bash
sudo kill -9 `sudo lsof -t -i:8000`
# Update system packages
# sudo apt-get update -y
# sudo apt-get upgrade -y

# Uninstall PostgreSQL in case present (it will delete all the existing postgresql databases from system)
sudo apt-get --purge remove postgresql postgresql-*

# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib libpq-dev python3-dev lsof -y

# Start PostgreSQL service
sudo service postgresql start

# Set up PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER rpi_has WITH PASSWORD 'rpi_has';"
sudo -u postgres psql -c "CREATE DATABASE rpi_has OWNER rpi_has;"

# Install Python3 and pip
sudo apt-get install python3 python3-pip -y 

# Install Python virtual environment
sudo apt install python3-venv

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

pip install "fastapi[standard]"

# Install project dependencies
pip install -r requirements.txt

# Regenerate and apply new migrations
alembic revision --autogenerate -m "RPi_HAS"

# Apply the new migration
alembic upgrade head

# Start the Python server
# fastapi run server.py 
uvicorn server:app --host 0.0.0.0 --port 8000 --ws websockets
