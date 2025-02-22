import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from models import db, User, Student, Course, Enrollment, Grade, Payment, Notification
from seed import seed_db

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///moringa_portal.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecretkey")

jwt = JWTManager(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    seed_db()