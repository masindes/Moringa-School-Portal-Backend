import sqlite3
from werkzeug.security import generate_password_hash

# Database file
DB_FILE = "moringa_portal.db"

def seed_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        print("Seeding database...")

        # Drop tables if they exist (reset database)
        cursor.executescript('''
            DROP TABLE IF EXISTS users;
            DROP TABLE IF EXISTS students;
            DROP TABLE IF EXISTS courses;
            DROP TABLE IF EXISTS enrollments;
            DROP TABLE IF EXISTS grades;
            DROP TABLE IF EXISTS payments;
            DROP TABLE IF EXISTS notifications;
        ''')

        # Recreate tables
        cursor.executescript('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                phase TEXT NOT NULL,
                fee_balance REAL NOT NULL DEFAULT 0.00,
                status TEXT NOT NULL DEFAULT 'active',
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL
            );

            CREATE TABLE enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
            );

            CREATE TABLE grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_id INTEGER NOT NULL,
                grade TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE
            );

            CREATE TABLE payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT NOT NULL,
                transaction_id TEXT UNIQUE NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
            );

            CREATE TABLE notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'unread',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        ''')

        # Seed users
        cursor.executemany('''
            INSERT INTO users (first_name, last_name, email, password_hash, role) VALUES (?, ?, ?, ?, ?);
        ''', [
            ('John', 'Doe', 'john.doe@example.com', generate_password_hash('password123'), 'student'),
            ('Jane', 'Smith', 'jane.smith@example.com', generate_password_hash('password123'), 'student'),
            ('Admin', 'User', 'admin@example.com', generate_password_hash('adminpass'), 'admin')
        ])

        # Seed students
        cursor.executemany('''
            INSERT INTO students (user_id, phase, fee_balance) VALUES (?, ?, ?);
        ''', [
            (1, 'Phase 1', 1000.00),
            (2, 'Phase 2', 500.00)
        ])

        # Seed courses
        cursor.executemany('''
            INSERT INTO courses (name, description) VALUES (?, ?);
        ''', [
            ('Mathematics', 'Basic Math Course'),
            ('Science', 'Basic Science Course')
        ])

        # Seed enrollments
        cursor.executemany('''
            INSERT INTO enrollments (student_id, course_id) VALUES (?, ?);
        ''', [
            (1, 1),
            (2, 2)
        ])

        # Seed grades
        cursor.executemany('''
            INSERT INTO grades (enrollment_id, grade) VALUES (?, ?);
        ''', [
            (1, 'A'),
            (2, 'B+')
        ])

        # Seed payments
        cursor.executemany('''
            INSERT INTO payments (student_id, amount, payment_method, transaction_id) VALUES (?, ?, ?, ?);
        ''', [
            (1, 500.00, 'M-Pesa', 'MPESA001'),
            (2, 250.00, 'Credit Card', 'CC002')
        ])

        # Seed notifications
        cursor.executemany('''
            INSERT INTO notifications (user_id, message, status) VALUES (?, ?, ?);
        ''', [
            (1, 'Welcome to Moringa Portal!', 'unread'),
            (2, 'Your payment has been received.', 'unread')
        ])

        conn.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_db()
