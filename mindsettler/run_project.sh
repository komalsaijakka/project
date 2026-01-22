#!/bin/bash

# Navigate to the project directory (ensure we are in the right place)
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "Installing dependencies..."
    ./venv/bin/pip install -r requirements.txt
    # Fallback if requirements.txt doesn't exist or is incomplete for our new packages
    ./venv/bin/pip install django django-allauth google-api-python-client PyJWT cryptography oauthlib requests-oauthlib openai
fi

# Apply migrations
echo "Applying database migrations..."
./venv/bin/python manage.py migrate

# Create superuser (interactive, only if needed by user, so we skip auto-creation here but prompt user in echo)
echo "----------------------------------------------------------------"
echo "To create an admin account, run in a separate terminal:"
echo "source venv/bin/activate && python manage.py createsuperuser"
echo "----------------------------------------------------------------"

# Run server
echo "Starting MindSettler server at http://127.0.0.1:8000/"
./venv/bin/python manage.py runserver
