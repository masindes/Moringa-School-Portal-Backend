from models import db, bcrypt, User, Student, Course, Enrollment, Grade, Payment, Notification, Report, ChatMessage, TokenBlocklist
from app import app
from datetime import datetime

def seed_data():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Create Users
        users = [
            User(
                first_name="nympha",
                last_name="pamba",
                email="nim@gmail.com",
                password_hash=bcrypt.generate_password_hash("123").decode('utf-8'),
                role="admin",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                first_name="lous",
                last_name="ogwal",
                email="louis@gmail.com",
                password_hash=bcrypt.generate_password_hash("123").decode('utf-8'),
                role="student",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                first_name="Stephen",
                last_name="waithumbi",
                email="stephen@gmail.com",
                password_hash=bcrypt.generate_password_hash("123").decode('utf-8'),
                role="student",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        db.session.add_all(users)
        db.session.commit()

        # Create Students
        students = [
            Student(
                user_id=users[1].id,
                phase="Phase 1",
                total_fee=500.00,
                amount_paid=150.00,
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Student(
                user_id=users[2].id,
                phase="Phase 2",
                total_fee=600.00,
                amount_paid=300.00,
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        db.session.add_all(students)
        db.session.commit()

        # Create Courses
        courses = [
            Course(
                name="Mathematics",
                description="Mathematics Course",
                created_at=datetime.utcnow()
            ),
            Course(
                name="Science",
                description="Science Course",
                created_at=datetime.utcnow()
            ),
            Course(
                name="History",
                description="History Course",
                created_at=datetime.utcnow()
            )
        ]
        db.session.add_all(courses)
        db.session.commit()

        # Create Enrollments
        enrollments = [
            Enrollment(
                student_id=students[0].id,
                course_id=courses[0].id,
                enrolled_at=datetime.utcnow()
            ),
            Enrollment(
                student_id=students[1].id,
                course_id=courses[1].id,
                enrolled_at=datetime.utcnow()
            )
        ]
        db.session.add_all(enrollments)
        db.session.commit()

        # Create Grades
        grades = [
            Grade(
                enrollment_id=enrollments[0].id,
                grade="A",
                created_at=datetime.utcnow()
            ),
            Grade(
                enrollment_id=enrollments[1].id,
                grade="B",
                created_at=datetime.utcnow()
            )
        ]
        db.session.add_all(grades)
        db.session.commit()

        # Create Payments
        payments = [
            Payment(
                student_id=students[0].id,
                amount=150.00,
                payment_date=datetime.utcnow(),
                payment_method="Credit Card",
                transaction_id="TXN12345"
            ),
            Payment(
                student_id=students[1].id,
                amount=300.00,
                payment_date=datetime.utcnow(),
                payment_method="Debit Card",
                transaction_id="TXN12346"
            )
        ]
        db.session.add_all(payments)
        db.session.commit()

        # Create Notifications
        notifications = [
            Notification(
                user_id=users[1].id,
                message="Welcome to the portal!",
                status="unread",
                created_at=datetime.utcnow()
            ),
            Notification(
                user_id=users[2].id,
                message="Fee payment reminder.",
                status="unread",
                created_at=datetime.utcnow()
            )
        ]
        db.session.add_all(notifications)
        db.session.commit()

        # Create Reports
        reports = [
            Report(
                admin_id=users[0].id,
                report_type="Attendance",
                report_data={"attendance_percentage": 95},
                created_at=datetime.utcnow()
            ),
            Report(
                admin_id=users[0].id,
                report_type="Performance",
                report_data={"average_grade": "B"},
                created_at=datetime.utcnow()
            )
        ]
        db.session.add_all(reports)
        db.session.commit()

        # Create ChatMessages
        chat_messages = [
            ChatMessage(
                sender_id=users[0].id,
                receiver_id=users[1].id,
                message="Hello, how can I help you?",
                sent_at=datetime.utcnow()
            ),
            ChatMessage(
                sender_id=users[1].id,
                receiver_id=users[0].id,
                message="I need help with my grades.",
                sent_at=datetime.utcnow()
            )
        ]
        db.session.add_all(chat_messages)
        db.session.commit()

        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()
