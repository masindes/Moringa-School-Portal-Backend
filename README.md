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

