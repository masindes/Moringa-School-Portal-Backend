
from app import app, db
from models import User, Student, Course, Enrollment, Grade, Payment, Notification, Report, ChatMessage
from datetime import datetime
import random

# Sample data
user_data = [
    {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "password", "role": "student"},
    {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com", "password": "password", "role": "student"},
]

student_data = [
    {"user_id": 1, "phase": "Phase 1", "fee_balance": 100.00, "status": "active"},
    {"user_id": 2, "phase": "Phase 2", "fee_balance": 200.00, "status": "active"},
]

course_data = [
    {"name": "Course 1", "description": "Description of Course 1"},
    {"name": "Course 2", "description": "Description of Course 2"},
]

enrollment_data = [
    {"student_id": 1, "course_id": 1},
    {"student_id": 2, "course_id": 2},
]

grade_data = [
    {"enrollment_id": 1, "grade": "A"},
    {"enrollment_id": 2, "grade": "B"},
]

payment_data = [
    {"student_id": 1, "amount": 100.00, "payment_method": "Credit Card", "transaction_id": "txn_1"},
    {"student_id": 2, "amount": 200.00, "payment_method": "Credit Card", "transaction_id": "txn_2"},
]

notification_data = [
    {"user_id": 1, "message": "You have a new grade."},
    {"user_id": 2, "message": "Your fee balance has been updated."},
]

report_data = [
    {"admin_id": 1, "report_type": "performance", "report_data": {"course": "Course 1", "average_grade": "B+"}},
    {"admin_id": 1, "report_type": "fees", "report_data": {"total_fees_collected": 300.00}},
]

chat_message_data = [
    {"sender_id": 1, "receiver_id": 2, "message": "Hello, how are you?"},
    {"sender_id": 2, "receiver_id": 1, "message": "I'm good, thank you!"},
]

def seed_data():
    with app.app_context():
        db.create_all()
    
        for data in user_data:
            user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                role=data["role"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            user.set_password(data["password"])
            db.session.add(user)
        
        for data in student_data:
            student = Student(
                user_id=data["user_id"],
                phase=data["phase"],
                fee_balance=data["fee_balance"],
                status=data["status"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(student)
        
        for data in course_data:
            course = Course(
                name=data["name"],
                description=data["description"],
                created_at=datetime.utcnow()
            )
            db.session.add(course)
        
        # Insert sample enrollments
        for data in enrollment_data:
            enrollment = Enrollment(
                student_id=data["student_id"],
                course_id=data["course_id"],
                enrolled_at=datetime.utcnow()
            )
            db.session.add(enrollment)
        
        # Insert sample grades
        for data in grade_data:
            grade = Grade(
                enrollment_id=data["enrollment_id"],
                grade=data["grade"],
                created_at=datetime.utcnow()
            )
            db.session.add(grade)
        
        # Insert sample payments
        for data in payment_data:
            payment = Payment(
                student_id=data["student_id"],
                amount=data["amount"],
                payment_date=datetime.utcnow(),
                payment_method=data["payment_method"],
                transaction_id=data["transaction_id"]
            )
            db.session.add(payment)
        
        # Insert sample notifications
        for data in notification_data:
            notification = Notification(
                user_id=data["user_id"],
                message=data["message"],
                status="unread",
                created_at=datetime.utcnow()
            )
            db.session.add(notification)
        
        # Insert sample reports
        for data in report_data:
            report = Report(
                admin_id=data["admin_id"],
                report_type=data["report_type"],
                report_data=data["report_data"],
                created_at=datetime.utcnow()
            )
            db.session.add(report)
        
        # Insert sample chat messages
        for data in chat_message_data:
            chat_message = ChatMessage(
                sender_id=data["sender_id"],
                receiver_id=data["receiver_id"],
                message=data["message"],
                sent_at=datetime.utcnow()
            )
            db.session.add(chat_message)
        
        db.session.commit()

if __name__ == "__main__":
    seed_data()
    print("Sample data inserted successfully.")
