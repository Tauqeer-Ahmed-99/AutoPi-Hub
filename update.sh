#!/bin/bash

# Save House Data to ./data directory
sudo venv/bin/python save_house_data.py

# PostgreSQL Setup
# Uninstall PostgreSQL
sudo apt-get --purge remove postgresql postgresql-*
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib libpq-dev python3-dev
# Start PostgreSQL service
sudo service postgresql start
# Set up PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER autopi_hub WITH PASSWORD 'autopi_hub';"
sudo -u postgres psql -c "CREATE DATABASE autopi_hub OWNER autopi_hub;"

# Pull the latest code from the GitHub repository forcefully and delete local uncommitted changes.
git fetch origin
git reset --hard origin/master

# Use virtual environment for packages already created when setup
source venv/bin/activate

# Install packages which cant be installed in requirements.txt
pip install "fastapi[standard]"
sudo apt-get install python3-rpi.gpio # Install RPi.GPIO package
python3 -m pip install RPi.GPIO # Install RPi.GPIO package

# Install project dependencies (new code might have new dependencies)
pip install -r requirements.txt

# Databse 
alembic revision --autogenerate -m "AutoPi-Hub" # Regenerate and apply new migrations
alembic upgrade head # Apply the new migration

# Load House Data from ./data directory
sudo venv/bin/python load_house_data.py

# Find and kill the process running on port 8000
sudo kill -9 `sudo lsof -t -i:8000`

# Start the FastAPI server
fastapi run server.py
#uvicorn server:app --reload --host 0.0.0.0 --port 8000

