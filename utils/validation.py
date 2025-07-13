from marshmallow import Schema, fields, validate, ValidationError
from flask import jsonify

class ProductSchema(Schema):
    """Schema for product validation."""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock = fields.Integer(required=True, validate=validate.Range(min=0))
    image_url = fields.Str(validate=validate.Length(max=255))
    category_id = fields.Integer(required=True)

class UserRegistrationSchema(Schema):
    """Schema for user registration validation."""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class CartItemSchema(Schema):
    """Schema for cart item validation."""
    product_id = fields.Integer(required=True, validate=validate.Range(min=1))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1, max=100))

def validate_json_input(schema_class):
    """Decorator to validate JSON input using Marshmallow schema."""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            from flask import request
            try:
                schema = schema_class()
                validated_data = schema.load(request.get_json())
                request.validated_data = validated_data
                return f(*args, **kwargs)
            except ValidationError as err:
                return jsonify({
                    'error': 'Validation failed',
                    'messages': err.messages
                }), 400
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator
