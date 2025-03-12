# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
import os
import logging
from routes import register_routes
from utils.database import init_db, teardown_db
from utils.error_handlers import register_error_handlers
from config import get_config, init_logging

def create_app(config_name=os.environ.get('FLASK_ENV', 'default')):
    """
    Application factory function that creates and configures the Flask app.
    
    Args:
        config_name (str): Name of the configuration to use (default, development, testing, production)
    
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    try:
        # Load configuration
        config = get_config(config_name)
        app.config.from_object(config)
        
        # Initialize logging
        init_logging(app)
        logger = logging.getLogger(__name__)
        logger.info(f"Starting application with {config_name} configuration")
        
        # Configure CORS
        CORS(app, resources={r"/*": {"origins": "*"}})
        
        # Initialize database connections
        init_db(app)
        logger.info("Database initialized successfully")
        
        # Register teardown function
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if exception:
                logger.error(f"Error during request: {str(exception)}")
            teardown_db()
        
        # Register blueprints for all routes
        register_routes(app)
        logger.info("Routes registered successfully")
        
        # Register error handlers
        register_error_handlers(app)
        logger.info("Error handlers registered successfully")
        
        # Health check endpoint
        @app.route('/health')
        def health_check():
            return jsonify({
                "status": "healthy",
                "version": app.config.get('API_VERSION', 'v1'),
                "environment": config_name
            })
        
        # Add basic info to app context
        @app.context_processor
        def inject_globals():
            return {
                'app_name': 'Hydrogen Dashboard',
                'version': app.config.get('API_VERSION', 'v1')
            }
        
        return app
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.critical(f"Failed to create application: {str(e)}")
        raise

def run_app():
    """
    Development server function to run the application.
    Usage: if __name__ == '__main__': run_app()
    """
    app = create_app('development')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )

if __name__ == '__main__':
    run_app()




# To use this setup:

# For development:

# # Set environment
# export FLASK_ENV=development
# # Run the app
# python app.py
# For production (using gunicorn):

# # Set environment
# export FLASK_ENV=production
# # Run with gunicorn
# gunicorn wsgi:app