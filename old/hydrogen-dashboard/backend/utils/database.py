"""Database connection utilities."""
import os
import sqlite3
from flask import Flask, g

def get_db_connection(database_name):
    """Get a connection to the specified database."""
    database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', database_name)
    conn = sqlite3.connect(database_path)
    return conn

def init_db(app: Flask):
    """Initialize database connections for the Flask app."""
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()