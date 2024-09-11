# Find and kill the process running on port 8000
sudo kill -9 $(lsof -t -i:8000)

# Pull the latest code from the GitHub repository
git pull origin master

# Use virtual environment for packages already created when setup
source venv/bin/activate

# Install project dependencies (new code might have new dependencies)
pip install -r requirements.txt

# Remove the current migration version
rm -f alembic/versions/*

# Generate a new base migration
alembic revision --autogenerate -m "RPi_HAS_BASE_MIGRATIONS"

# Mark the base migration as the current version in the database
alembic stamp head

# Generate a new migration for current changes
alembic revision --autogenerate -m "RPi_HAS_CURRENT_SCHEMA"

# Apply the new migration
alembic upgrade head

# Start the FastAPI server
fastapi run server.py
#uvicorn server:app --reload --host 0.0.0.0 --port 8000

