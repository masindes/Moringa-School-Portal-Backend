# Moringa School Portal

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

git clone git@github.com:masindes/Task_Managent_Backend.git
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

# Initialize the database:

flask db init
flask db migrate
flask db upgrade
Seed the database with sample data:
python seed.py

# Run the application:

flask run
Access the application:
The application will be running at http://127.0.0.1:5000/.

# API EndpointsAuthentication
POST /register: Register a new user.

POST /login: Log in and receive a JWT token.

POST /logout: Log out and invalidate the JWT token.

Password Reset
POST /request_password_reset: Request a password reset OTP.

POST /reset_password: Reset password using the OTP.

Student Management
GET /students: Get all students (Admin only).

POST /students: Add a new student (Admin only).

PATCH /students/int:student_id: Update student details (Admin only).

DELETE /students/int:student_id: Delete a student (Admin only).

Course Management
GET /courses: Get all courses.

POST /courses: Add a new course (Admin only).

Grade Management
POST /enrollments/int:enrollment_id/grades: Add a grade for a student (Admin only).

PATCH /grades/int:grade_id: Update a grade (Admin only).

DELETE /grades/int:grade_id: Delete a grade (Admin only).

Payment Management
POST /mpesa/payment: Initiate an M-Pesa payment.

POST /mpesa/callback: M-Pesa payment callback (used internally).

Notifications
GET /notifications/int:user_id: Get notifications for a user.

Reports
GET /reports: Get all reports (Admin only).

Chat Messaging
POST /chat: Send a chat message.

GET /chat/int:user_id: Get chat messages for a user.

Configuration
The application can be configured for different environments (development, production) by setting the appropriate environment variables in the .env file.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments
Moringa School for the inspiration.

Flask and the Python community for the tools and libraries used in this project.
# Contributors
LouisOgwal
Nympha Pamba
Stephen Waithumbi
Masinde Sylvester

# Contact
For any questions or issues, please contact yienlouis470@gmail.com,