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

# Student Signup
@app.route('/students/signup', methods=['POST'])
def student_signup():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password_hash=hashed_password,
        role='student'
    )
    db.session.add(new_user)
    db.session.commit()
    new_student = Student(user_id=new_user.id, phase=data['phase'], fee_balance=0.00, status='active')
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student account created successfully"}), 201

# Student Login
@app.route('/students/login', methods=['POST'])
def student_login():
    data = request.json
    user = User.query.filter_by(email=data['email'], role='student').first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = create_access_token(identity={"id": user.id, "role": "student"})
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401
  
  # CRUD Routes
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted"})
    return jsonify({"message": "Student not found"}), 404

@app.route('/courses', methods=['GET', 'POST'])
def manage_courses():
    if request.method == 'POST':
        data = request.json
        new_course = Course(name=data['name'], description=data['description'])
        db.session.add(new_course)
        db.session.commit()
        return jsonify({"message": "Course added"})
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@app.route('/enrollments', methods=['POST'])
def enroll_student():
    data = request.json
    new_enrollment = Enrollment(student_id=data['student_id'], course_id=data['course_id'])
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify({"message": "Student enrolled successfully"})
  
  # M-Pesa Integration Placeholder
@app.route('/payments/mpesa', methods=['POST'])
def mpesa_payment():
    data = request.json
    return jsonify({"message": "M-Pesa payment successful", "transaction_id": "MPESA123456"}), 200

if __name__ == '__main__':
    app.run(debug=True)
