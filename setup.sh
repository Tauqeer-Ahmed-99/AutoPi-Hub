#!/bin/bash

# Update system packages
# sudo apt-get update -y
# sudo apt-get upgrade -y

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

# Remove the current migration version
psql -h localhost -U rpi_has -d rpi_has

# In psql:
DROP TABLE IF EXISTS alembic_version;

# Exit psql
\q

# Remove old migration files
rm -rf migrations/versions/*

# Start the Python server
fastapi run server.py 
