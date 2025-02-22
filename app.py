import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
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

# Admin login
ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "admin@example.com").split(',')
ADMIN_PASSWORDS = os.getenv("ADMIN_PASSWORDS", "password123").split(',')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email in ADMIN_EMAILS and password in ADMIN_PASSWORDS:
        token = create_access_token(identity={"email": email, "role": "admin"})
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Invalid admin credentials"}), 401

# M-Pesa Integration Placeholder
@app.route('/payments/mpesa', methods=['POST'])
def mpesa_payment():
    data = request.json
    return jsonify({"message": "M-Pesa payment successful", "transaction_id": "MPESA123456"}), 200

if __name__ == '__main__':
    app.run(debug=True)