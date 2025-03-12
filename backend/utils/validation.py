# backend/utils/validation.py
from pydantic import ValidationError
from flask import jsonify

def validate_input(schema, data):
    try:
        return schema(**data)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400