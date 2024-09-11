# Find and kill the process running on port 8000
sudo kill -9 $(lsof -t -i:8000)

# Pull the latest code from the GitHub repository
git pull origin master

# Use virtual environment for packages already created when setup
source venv/bin/activate

# Install project dependencies (new code might have new dependencies)
pip install -r requirements.txt

# Autogenerate migrations (new code might contain DB changes)
alembic revision --autogenerate -m "RPi_HAS"

# Run migrations
alembic upgrade head

# Start the FastAPI server
fastapi run server.py
#uvicorn server:app --reload --host 0.0.0.0 --port 8000

