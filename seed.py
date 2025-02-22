from models import db, User, Student, Course, Enrollment, Grade, Payment, Notification
from werkzeug.security import generate_password_hash

def seed_db():
    # Clear existing data
    db.session.query(Notification).delete()
    db.session.query(Payment).delete()
    db.session.query(Grade).delete()
    db.session.query(Enrollment).delete()
    db.session.query(Course).delete()
    db.session.query(Student).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Seed users (students)
    student1 = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password_hash=generate_password_hash("password123"),
        role="student"
    )
    student2 = User(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        password_hash=generate_password_hash("password456"),
        role="student"
    )
    db.session.add_all([student1, student2])
    db.session.commit()

    # Seed students table
    student1_data = Student(user_id=student1.id, phase="Phase 1", fee_balance=500.00, status="active")
    student2_data = Student(user_id=student2.id, phase="Phase 2", fee_balance=0.00, status="active")
    db.session.add_all([student1_data, student2_data])
    db.session.commit()

    # Seed courses
    course1 = Course(name="Web Development", description="Learn HTML, CSS, JavaScript")
    course2 = Course(name="Data Science", description="Python, Machine Learning, and AI")
    db.session.add_all([course1, course2])
    db.session.commit()

    # Seed enrollments
    enrollment1 = Enrollment(student_id=student1_data.id, course_id=course1.id)
    enrollment2 = Enrollment(student_id=student2_data.id, course_id=course2.id)
    db.session.add_all([enrollment1, enrollment2])
    db.session.commit()

    # Seed grades
    grade1 = Grade(enrollment_id=enrollment1.id, grade="A")
    grade2 = Grade(enrollment_id=enrollment2.id, grade="B+")
    db.session.add_all([grade1, grade2])
    db.session.commit()

    # Seed payments
    payment1 = Payment(student_id=student1_data.id, amount=500.00, payment_method="M-Pesa", transaction_id="MPESA001")
    db.session.add(payment1)
    db.session.commit()

    # Seed notifications
    notification1 = Notification(user_id=student1.id, message="Your payment has been received.", status="unread")
    db.session.add(notification1)
    db.session.commit()

    print("Database seeded successfully!")
