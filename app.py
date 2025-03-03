#app.py 
import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, decode_token
from models import db, bcrypt, User, Student, Course, Enrollment, Grade, Payment, Notification, Report, ChatMessage, TokenBlocklist
from datetime import datetime
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KE")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 


import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)

# M-Pesa API credentials
CONSUMER_KEY = "RgXJq5gNAcVfObTMmXVAvOIcV28bsvCh3dqUVJuG7pSzAR0x"
CONSUMER_SECRET = "npzeXWjsTqPVcQoeGGmGUvBPUxG4lZiyHGYaGJ94yseYOgwrAn9gSemZ4RKKJqGa"
SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
CALLBACK_URL = "https://moringa-school-portal-backend.onrender.com/mpesa/callback"

CORS(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Generate M-Pesa access token
def generate_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    token_data = response.json()
    
    # Debugging: Log the token response
    print("Access Token Response:", token_data)

    return token_data.get("access_token")

# Generate Lipa Na M-Pesa password
def generate_password():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data_to_encode = SHORTCODE + PASSKEY + timestamp
    encoded_password = base64.b64encode(data_to_encode.encode()).decode()
    return encoded_password, timestamp

# Initiate STK Push
def stk_push(phone_number, amount, account_reference, transaction_desc):
    access_token = generate_access_token()
    if not access_token:
        return {"error": "Failed to generate access token"}
    
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    password, timestamp = generate_password()
    
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Debugging: Log the STK Push response
    print("STK Push Response:", response.json())

    return response.json()

# Payment route
@app.route("/mpesa/payment", methods=["POST"])
def initiate_payment():
    data = request.json
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    account_reference = "MoringaPortal"
    transaction_desc = "Student Payment"
    
    if not phone_number or not amount:
        return jsonify({"error": "Phone number and amount are required"}), 400
    
    response = stk_push(phone_number, amount, account_reference, transaction_desc)
    return jsonify(response)

# Callback route to process payment response
@app.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    data = request.json
    print("M-Pesa Callback Data:", data)

    # Extract relevant fields from M-Pesa response
    try:
        result_code = data["Body"]["stkCallback"]["ResultCode"]
        if result_code == 0:
            transaction_id = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
            amount = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
            phone_number = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
            
            # Process the payment in the database (Example)
            # new_payment = Payment(student_id=some_student_id, amount=amount, transaction_id=transaction_id, status="Completed")
            # db.session.add(new_payment)
            # db.session.commit()

            return jsonify({"message": "Payment successful", "transaction_id": transaction_id, "amount": amount, "phone_number": phone_number}), 200
        else:
            return jsonify({"error": "Payment failed"}), 400
    except KeyError:
        return jsonify({"error": "Invalid callback data"}), 400


# check if the current user is an admin
def admin_required():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({"message": "Admin access required"}), 403

#Checks whether the students status is active
def student_active_required(student_id):
    student = Student.query.get(student_id)
    if not student or student.status != 'active':
        return jsonify({"message": "Your account is inactive"}), 403
    return None
    
# Create a callback to check if the token is blacklisted
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

@app.route('/')
def home():
    return {"message": "Hello, Welcome Moringa Students Portal!"}

# User registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if the email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        role=data['role'],
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": new_user.to_dict()}), 201

# User login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        identity = str(user.id)  # Ensure identity is a string
        access_token = create_access_token(identity=identity, additional_claims={"role": user.role})
        return jsonify({"message": "Logged in successfully", "access_token": access_token}), 200
    return jsonify({"message": "Invalid email or password"}), 401

# Logout route to add the token to the blacklist
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    new_token_block = TokenBlocklist(jti=jti, created_at=datetime.utcnow())
    db.session.add(new_token_block)
    db.session.commit()
    return jsonify({"message": "Successfully logged out"}), 200


# Route to change student password
@app.route('/students/<int:student_id>/change_password', methods=['PATCH'])
@jwt_required()
def change_student_password(student_id):
    current_user_id = int(get_jwt_identity())
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    # Ensure only the student can change their password
    if current_user_id != user.id:
        return jsonify({"message": "Unauthorized access"}), 403
    data = request.get_json()
    if 'new_password' not in data:
        return jsonify({"message": "New password is required"}), 400
    # Hash and update the new password
    user.password_hash = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
    db.session.commit()
    return jsonify({"message": "Password changed successfully"}), 200


# Get user info route
@app.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    
    # Manually serialize the user data
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }
    
    return jsonify(user_data), 200


# Admin: Add a new student
@app.route('/students', methods=['POST'])
@jwt_required()
def add_student():
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check

    data = request.get_json()
    new_student = Student(
        user_id=data['user_id'],
        phase=data['phase'],
        fee_balance=data['fee_balance'],
        status=data['status'],
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully", "student": new_student.to_dict()}), 201

# Admin: Update student details
@app.route('/students/<int:student_id>', methods=['PATCH'])
@jwt_required()
def update_student(student_id):
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check

    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    if 'phase' in data:
        student.phase = data['phase']
    if 'fee_balance' in data:
        student.fee_balance = data['fee_balance']
    if 'status' in data:
        student.status = data['status']
    db.session.commit()
    return jsonify({"message": "Student updated successfully", "student": student.to_dict()}), 200

# Admin: View all students
@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check
    
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200

# Admin: Deactivate student account
@app.route('/students/<int:student_id>/deactivate', methods=['PATCH'])
@jwt_required()
def deactivate_student(student_id):
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check
    
    student = Student.query.get_or_404(student_id)
    student.status = 'inactive'
    db.session.commit()
    
    # Manually serialize the student data
    student_data = {
        "id": student.id,
        "user_id": student.user_id,
        "phase": student.phase,
        "total_fee": float(student.total_fee),
        "amount_paid": float(student.amount_paid),
        "fee_balance": student.fee_balance,
        "status": student.status,
        "created_at": student.created_at.isoformat(),
        "updated_at": student.updated_at.isoformat(),
    }
    
    return jsonify({"message": "Student deactivated successfully", "student": student_data}), 200

# Create a new grade for a student enrollment
@app.route('/enrollments/<int:enrollment_id>/grades', methods=['POST'])
@jwt_required()
def add_grade(enrollment_id):
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check

    data = request.get_json()
    new_grade = Grade(
        enrollment_id=enrollment_id,
        grade=data['grade'],
        created_at = datetime.utcnow()
    )
    db.session.add(new_grade)
    db.session.commit()
    return jsonify({"message": "Grade added successfully", "grade": new_grade.to_dict()}), 201

# Update an existing grade
@app.route('/grades/<int:grade_id>', methods=['PATCH'])
@jwt_required()
def update_grade(grade_id):
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check

    grade = Grade.query.get_or_404(grade_id)
    data = request.get_json()
    if 'grade' in data:
        grade.grade = data['grade']
    db.session.commit()
    return jsonify({"message": "Grade updated successfully", "grade": grade.to_dict()}), 200

# Delete a grade
@app.route('/grades/<int:grade_id>', methods=['DELETE'])
@jwt_required()
def delete_grade(grade_id):
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check

    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    return jsonify({"message": "Grade deleted successfully"}), 200


# Student: Get grades
@app.route('/students/<int:student_id>/grades', methods=['GET'])
@jwt_required()
def get_grades(student_id):
    # Check if student account is active
    active_check = student_active_required(student_id)
    if active_check:
        return active_check

    student = Student.query.get_or_404(student_id)
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()
    grades = []
    for enrollment in enrollments:
        grade = Grade.query.filter_by(enrollment_id=enrollment.id).first()
        if grade:
            grades.append({"course": enrollment.course.name, "grade": grade.grade})
    return jsonify(grades), 200

# Student: Get fee balance
@app.route('/students/<int:student_id>/fee_balance', methods=['GET'])
@jwt_required()
def get_fee_balance(student_id):

    # Check if student account is active
    active_check = student_active_required(student_id)
    if active_check:
        return active_check
    
    student = Student.query.get_or_404(student_id)
    return jsonify({"fee_balance": student.fee_balance}), 200

# Student: Get current phase
@app.route('/students/<int:student_id>/current_phase', methods=['GET'])
@jwt_required()
def get_current_phase(student_id):
    # Check if student account is active
    active_check = student_active_required(student_id)
    if active_check:
        return active_check
    
    student = Student.query.get_or_404(student_id)
    return jsonify({"current_phase": student.phase}), 200

# Student: Make a payment
@app.route('/students/<int:student_id>/payments', methods=['POST'])
@jwt_required()
def make_payment(student_id):
    # Check if student account is active
    active_check = student_active_required(student_id)
    if active_check:
        return active_check

    data = request.get_json()
    student = Student.query.get_or_404(student_id)
    
    # Create a new payment
    new_payment = Payment(
        student_id=student_id,
        amount=data['amount'],
        payment_date = datetime.utcnow(),
        payment_method=data['payment_method'],
        transaction_id=data['transaction_id']
    )
    
    # Update student's amount_paid
    student.amount_paid += data['amount']
    
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({"message": "Payment made successfully", "payment": new_payment.to_dict()}), 201


    # Student: Get all details
@app.route('/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_details(student_id):
    # Check if student account is active
    active_check = student_active_required(student_id)
    if active_check:
        return active_check
    
    student = Student.query.get_or_404(student_id)
    user = student.user
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()
    grades = []
    for enrollment in enrollments:
        grade = Grade.query.filter_by(enrollment_id=enrollment.id).first()
        if grade:
            grades.append({
                "course": enrollment.course.name,
                "grade": grade.grade,
                "enrolled_at": enrollment.enrolled_at.isoformat()
            })
    payments = Payment.query.filter_by(student_id=student.id).all()
    payment_list = [payment.to_dict() for payment in payments]

    # Collect all details
    student_details = {
        "student_id": student.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phase": student.phase,
        "total_fee": student.total_fee,
        "amount_paid": student.amount_paid,
        "fee_balance": student.fee_balance,
        "status": student.status,
        "created_at": student.created_at.isoformat(),
        "updated_at": student.updated_at.isoformat(),
        "grades": grades,
        "payments": payment_list
    }
    
    return jsonify(student_details), 200



# Admin: View all payments
@app.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    # Check for admin role
    admin_check = admin_required()
    if admin_check:
        return admin_check
    
    payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments]), 200

# Notifications: Get notifications for a user
@app.route('/notifications/<int:user_id>', methods=['GET'])
@jwt_required()
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([notification.to_dict() for notification in notifications]), 200

if __name__ == '__main__':
    app.run(debug=True)