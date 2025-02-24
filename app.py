
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, decode_token
from models import db, bcrypt, User, Student, Course, Enrollment, Grade, Payment, Notification, Report, ChatMessage, TokenBlocklist
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///moringa_students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "03a0eae755348efcd38aa36594fa75c40da931ea19823351e88f893c4337cf48"
app.config["JWT_SECRET_KEY"] = "0399c5c9f2b940c607e7f11c9f86de41bcf59ec6fdfe1c51f5d87abfaf0a2664"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  

CORS(app)
bcrypt.init_app(app)
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# check if the current user is an admin
def admin_required():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({"message": "Admin access required"}), 403
    
# Create a callback to check if the token is blacklisted
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

@app.route('/')
def home():
    return {"message": "Hello, Moringa Students Portal!"}

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
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
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
    return jsonify(user.to_dict()), 200

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
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
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
    return jsonify({"message": "Student deactivated successfully", "student": student.to_dict()}), 200

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
        created_at=datetime.utcnow()
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
    student = Student.query.get_or_404(student_id)
    return jsonify({"fee_balance": student.fee_balance}), 200

# Student: Get current phase
@app.route('/students/<int:student_id>/current_phase', methods=['GET'])
@jwt_required()
def get_current_phase(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({"current_phase": student.phase}), 200

# Student: Make a payment
@app.route('/students/<int:student_id>/payments', methods=['POST'])
@jwt_required()
def make_payment(student_id):
    data = request.get_json()
    student = Student.query.get_or_404(student_id)
    
    # Create a new payment
    new_payment = Payment(
        student_id=student_id,
        amount=data['amount'],
        payment_date=datetime.utcnow(),
        payment_method=data['payment_method'],
        transaction_id=data['transaction_id']
    )
    
    # Update student's amount_paid
    student.amount_paid += data['amount']
    
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({"message": "Payment made successfully", "payment": new_payment.to_dict()}), 201


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
