"""Error handling utilities for the Flask application."""
from flask import Flask, jsonify

def register_error_handlers(app: Flask):
    """Register error handlers for the Flask app."""
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "Not Found", "message": str(e)}), 404
    
    @app.errorhandler(500)
    def handle_server_error(e):
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500