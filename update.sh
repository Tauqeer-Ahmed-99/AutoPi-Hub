# Find and kill the process running on port 8000
sudo kill -9 `sudo lsof -t -i:8000`

# Save House Data to ./data directory
sudo venv/bin/python services/save_house_data.py

# PostgreSQL Setup
# Uninstall PostgreSQL
sudo apt-get --purge remove postgresql postgresql-*
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib libpq-dev python3-dev
# Start PostgreSQL service
sudo service postgresql start
# Set up PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER rpi_has WITH PASSWORD 'rpi_has';"
sudo -u postgres psql -c "CREATE DATABASE rpi_has OWNER rpi_has;"

# Pull the latest code from the GitHub repository forcefully and delete local uncommitted changes.
git fetch origin
git reset --hard origin/master

# Use virtual environment for packages already created when setup
source venv/bin/activate

# Install packages which cant be installed in requirements.txt
# Install RPi.GPIO package
sudo apt-get install python3-rpi.gpio
python3 -m pip install RPi.GPIO

# Install project dependencies (new code might have new dependencies)
pip install -r requirements.txt

# Regenerate and apply new migrations
alembic revision --autogenerate -m "RPi_HAS"

# Apply the new migration
alembic upgrade head

# Load House Data from ./data directory
sudo venv/bin/python services/load_house_data.py

# Start the FastAPI server
fastapi run server.py
#uvicorn server:app --reload --host 0.0.0.0 --port 8000

