"""
Main application entry point for the hydrogen dashboard API.
Initializes the Flask app and registers all routes.
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from routes import register_routes
from utils.database import init_db
from utils.error_handlers import register_error_handlers

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize database connections
    init_db(app)
    
    # Register blueprints for all routes
    register_routes(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    @app.route('/data/<path:filename>', methods=['GET'])
    def download_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'data'), filename)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)