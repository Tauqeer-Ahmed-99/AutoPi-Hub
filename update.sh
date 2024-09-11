# Find and kill the process running on port 8000
sudo kill -9 $(lsof -t -i:8000)

# Pull the latest code from the GitHub repository
git pull origin master

# Use virtual environment for packages already created when setup
source venv/bin/activate

# Install project dependencies (new code might have new dependencies)
pip install -r requirements.txt

# Set the password for psql command
export PGPASSWORD='rpi_has'

# Remove the current migration version
sudo -u postgres psql -h localhost -U rpi_has -d rpi_has -c "DROP TABLE IF EXISTS alembic_version;"


# UnSet the password for psql command
unset PGPASSWORD

# Remove old migration files
rm -rf migrations/versions/*

# Regenerate and apply new migrations
alembic revision --autogenerate -m "RPi_HAS"

# Apply the new migration
alembic upgrade head

# Start the FastAPI server
fastapi run server.py
#uvicorn server:app --reload --host 0.0.0.0 --port 8000

