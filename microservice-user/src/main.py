"""
User Microservice API - Simple version with in-memory storage
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models.user import User
from utils import hash_password, verify_password, generate_token, token_required

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL for Swagger UI
API_URL = '/static/swagger.yaml'  # URL to access swagger.yaml

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "User Microservice API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# In-memory storage (simple dictionary)
# Format: {"username": User object}
users_db = {}


@app.route('/')
def index():
    """Redirect to Swagger UI"""
    from flask import redirect
    return redirect('/api/docs')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "user-microservice"
    }), 200


@app.route('/static/swagger.yaml')
def swagger_file():
    """Serve swagger.yaml file"""
    from flask import send_file
    import os
    swagger_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'swagger.yaml')
    return send_file(swagger_path, mimetype='text/yaml')


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "username" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields: username, email, password"}), 400

    # Check if user already exists
    if data["username"] in users_db:
        return jsonify({"error": "Username already exists"}), 409

    # Hash password
    password_hash = hash_password(data["password"])

    # Create user
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=password_hash,
        role=data.get("role", "user")
    )

    # Validate user
    is_valid, errors = user.validate()
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    # Save to dictionary
    users_db[user.username] = user

    return jsonify({
        "message": "User created successfully",
        "user": user.to_dict()
    }), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Login and get JWT token"""
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    # Get user
    user = users_db.get(data["username"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Verify password
    if not verify_password(data["password"], user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate token
    token = generate_token(user.user_id, user.username, user.role)

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    }), 200


@app.route('/api/v1/users', methods=['GET'])
#@token_required
def get_users():
    """Get all users"""
    users_list = [user.to_dict() for user in users_db.values()]

    return jsonify({
        "count": len(users_list),
        "users": users_list
    }), 200


@app.route('/api/v1/users/<user_id>', methods=['GET'])
#@token_required
def get_user(user_id):
    """Get user by ID"""
    # Find user by user_id
    user = None
    for u in users_db.values():
        if u.user_id == user_id:
            user = u
            break

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """Update user details"""
    # Find user
    user = None
    for u in users_db.values():
        if u.user_id == user_id:
            user = u
            break

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check permissions
    current_user = request.current_user
    if current_user["user_id"] != user_id and current_user["role"] != "admin":
        return jsonify({"error": "Permission denied"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update email
    if "email" in data:
        user.email = data["email"]

    # Update role (admin only)
    if "role" in data:
        if current_user["role"] != "admin":
            return jsonify({"error": "Only admins can change roles"}), 403
        user.role = data["role"]

    # Update password
    if "password" in data:
        if current_user["user_id"] == user_id:
            user.password_hash = hash_password(data["password"])

    return jsonify({
        "message": "User updated successfully",
        "user": user.to_dict()
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
