****Moringa School Portal****

The Moringa School Portal is a web application designed to manage student information, course enrollments, grades, payments, and notifications for Moringa School. The application provides functionalities for both students and administrators, including user registration, login, password reset, payment processing, and more.

# Features
User Authentication: Secure user registration, login, and logout with JWT-based authentication.

Password Reset: Users can request a password reset via OTP sent to their email.

Student Management: Admins can add, update, and deactivate student accounts.

Course Enrollment: Students can enroll in courses, and admins can manage enrollments.

Grade Management: Admins can add, update, and delete grades for students.

Payment Processing: Students can make payments via M-Pesa, and admins can view all payment records.

Notifications: Users receive notifications for important updates, such as payment confirmations.

Reports: Admins can generate and view reports on student attendance and performance.

Chat Messaging: Users can send and receive messages within the portal.

# Technologies Used

Backend: Flask (Python)

Database: PostgreSQL

Authentication: JWT (JSON Web Tokens)

Password Hashing: Flask-Bcrypt

Payment Integration: M-Pesa API

Email Notifications: Flask-Mail

API Documentation: Swagger (via Flask-RESTful)

Frontend: (Not included in this repository, but can be integrated with any frontend framework like React or Angular)

# Installation Prerequisites
Python 3.8 or higher

PostgreSQL

Flask

Flask-SQLAlchemy

Flask-Migrate

Flask-CORS

Flask-Bcrypt

Flask-JWT-Extended

Flask-Mail

dotenv for environment variable management

Steps
Clone the repository:

git clone https://github.com/yourusername/moringa-school-portal.git
cd moringa-school-portal
Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate
Install dependencies:


pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory and add the following variables:

.env files
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
DATABASE_URL=postgresql://username:password@localhost/moringa_school_portal_db
DEBUG=True
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password

