#!/bin/bash

# Update system packages
sudo apt-get update -y
sudo apt-get upgrade -y


# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib -y

# Start PostgreSQL service
sudo service postgresql start

# Set up PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER your_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "CREATE DATABASE your_db OWNER your_user;"

# Install Python3 and pip
sudo apt-get install python3 python3-pip -y

# Install Python virtual environment
sudo pip3 install virtualenv

# Create and activate a virtual environment
virtualenv venv
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Run migrations (assuming you use a migration tool like Alembic)
alembic upgrade head  # or other migration commands

# Start the Python server (adjust the command based on your setup)
python server.py  # or the entry point of your project
