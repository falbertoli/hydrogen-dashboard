# backend/wsgi.py
import os
from app import create_app

# Get environment from FLASK_ENV environment variable, default to 'production'
app = create_app(os.environ.get('FLASK_ENV', 'production'))