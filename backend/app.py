# backend/app.py
from flask import Flask, send_from_directory  # Import send_from_directory
from flask_cors import CORS
import os
from routes import register_routes
from utils.database import init_db
from utils.error_handlers import register_error_handlers
from config import get_config

def create_app(config_name=os.environ.get('FLASK_ENV', 'default')):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
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