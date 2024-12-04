from flask import jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import add_user, get_user

def register_routes(app):
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'Usuario')

        if get_user(email):
            return jsonify({
                'message': 'user already exists'
            }), 400

        password_hash = generate_password_hash(password).decode('utf-8')
        add_user(email, password_hash, role)
        return jsonify({
            'message': 'user succesfully registered'
        }), 201
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = get_user(email)
        if not user or not check_password_hash(user['password'], password):
            return jsonify({
                'message': 'invalid credentials'
            }), 401

        access_token = create_access_token(identity={
            'email': email,
            'role': user['role']
        })
        return jsonify({
            'acces token': access_token
        }), 200

    @app.route('/auth/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify({
            'message': f'welcome, {current_user['email']}'
        }), 200

    @app.route('/auth/admin', methods=['GET'])
    def admin_route():
        current_user = get_jwt_identity()

        if current_user['role'] != 'Administrador':
            return jsonify({
                'message': 'acces denied'
            }), 403

        return jsonify({
            'message': 'welcome, administrator'
        }), 200