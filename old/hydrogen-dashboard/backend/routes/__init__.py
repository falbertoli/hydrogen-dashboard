"""Initialize all API route blueprints."""
from flask import Flask

def register_routes(app: Flask):
    """Register all route blueprints with the Flask app."""
    from .hydrogen_demand import hydrogen_demand_bp
    from .storage import storage_bp
    from .economic import economic_bp
    
    app.register_blueprint(hydrogen_demand_bp, url_prefix='/api/hydrogen-demand')
    app.register_blueprint(storage_bp, url_prefix='/api/storage')
    app.register_blueprint(economic_bp, url_prefix='/api/economic')