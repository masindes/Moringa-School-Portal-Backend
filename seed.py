from models import db, bcrypt, User, Student, Course, Enrollment, Grade, Payment, Notification, Report, ChatMessage
from app import app
from datetime import datetime

def seed_data():
    with app.app_context():
        
        db.drop_all()
        db.create_all()


        users = [
            User(
                first_name="louis",
                last_name="ogwal",
                email="louis@gmail.com",
                password_hash=bcrypt.generate_password_hash("password").decode('utf-8'),
                role="admin",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                first_name="nympha",
                last_name="nim",
                email="nim@gmail.com",
                password_hash=bcrypt.generate_password_hash("password").decode('utf-8'),
                role="student",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        db.session.add_all(users)
        db.session.commit()

        student1 = Student(
            user_id=users[2].id,
            phase="Phase 1",
            total_fee=500.00,
            amount_paid=150.00,
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(student1)
        db.session.commit()

        
        courses = [
            Course(name="Mathematics", description="Mathematics Course", created_at=datetime.utcnow()),
            Course(name="Science", description="Science Course", created_at=datetime.utcnow())
        ]
        db.session.add_all(courses)
        db.session.commit

        enrollment1 = Enrollment(
            student_id=student1.id,
            course_id=courses[1].id,
            enrolled_at=datetime.utcnow()
        )
        db.session.add(enrollment1)
        db.session.commit()

    
        grade1 = Grade(
            enrollment_id=enrollment1.id,
            grade="A",
            created_at=datetime.utcnow()
        )
        db.session.add(grade1)
        db.session.commit()

    
        payment1 = Payment(
            student_id=student1.id,
            amount=150.00,
            payment_date=datetime.utcnow(),
            payment_method="Credit Card",
            transaction_id="TXN12345"
        )
        db.session.add(payment1)
        db.session.commit()

    
        notification1 = Notification(
            user_id=users[2].id,
            message="Welcome to the portal!",
            status="unread",
            created_at=datetime.utcnow()
        )
        db.session.add(notification1)
        db.session.commit()


        report1 = Report(
            admin_id=users[1].id,
            report_type="Attendance",
            report_data={"attendance_percentage": 95},
            created_at=datetime.utcnow()
        )
        db.session.add(report1)
        db.session.commit()


        chat_message1 = ChatMessage(
            sender_id=users[1].id,
            receiver_id=users[2].id,
            message="Hello, how can I help you?",
            sent_at=datetime.utcnow()
        )
        db.session.add(chat_message1)
        db.session.commit()

        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
