from flask import flask, request, jsonify, session
from flasl_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask__restful import Api, Resource
from flask_cors import CORS
from flask_session import Session
from flask bcrypt import Bcrypt



app = Flask(__name__)
CORS(app,supports_credentials=True)
Bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '$y!v3$*123'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
Session(app)