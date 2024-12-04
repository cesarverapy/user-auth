from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
from routes import register_routes

app = Flask(__name__)

app.config.from_object(Config)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
