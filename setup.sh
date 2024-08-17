#!/bin/bash

# Update system packages
sudo apt-get update -y
sudo apt-get upgrade -y


# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib -y

# Start PostgreSQL service
sudo service postgresql start

# Set up PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER rpi_has WITH PASSWORD 'rpi_has';"
sudo -u postgres psql -c "CREATE DATABASE rpi_has OWNER rpi_has;"

# Install Python3 and pip
sudo apt-get install python3 python3-pip -y

# Install Python virtual environment
sudo pip3 install virtualenv

# Create and activate a virtual environment
virtualenv venv
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

#Autogenerate Migrations
alembic revision --autogenerate -m "RPi_HAS"

# Run migrations
alembic upgrade head

# Start the Python server
fastapi run server.py 
