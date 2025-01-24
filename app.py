from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_session import Session
from flask_bcrypt import Bcrypt

# Initialize Flask application
app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

# Configure application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '$y!v3$*123'
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
Session(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Resource for user signup
class Signup(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

# Resource for user login
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            return jsonify({'message': 'Logged in successfully'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

# Resource for user logout
class Logout(Resource):
    def post(self):
        session.pop('user_id', None)
        return jsonify({'message': 'Logged out successfully'}), 200

# Resource to check login status
class IsLoggedIn(Resource):
    def get(self):
        if 'user_id' in session:
            return jsonify({'message': 'User is logged in'}), 200
        return jsonify({'message': 'User is not logged in'}), 401

# Add API resources
api.add_resource(Signup, "/Signup")
api.add_resource(Login, "/Login")
api.add_resource(Logout, "/Logout")
api.add_resource(IsLoggedIn, "/IsLoggedIn")

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
