# Kill the process on port 8000
sudo kill -9 8000

git pull origin master

# Autogenerate Migrations (New code might contain db changes)
alembic revision --autogenerate -m "RPi_HAS"

# Run migrations (New code might contain db changes)
alembic upgrade head

# Use virtual environment for packages already created when setup
source venv/bin/activate

# Install project dependencies (new code might have new dependencies)
pip install -r requirements.txt

# Start the Python server
fastapi run server.py

