# password_reset.py

from flask import Blueprint, request, jsonify
from models import db, User
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import random
import string

password_reset_bp = Blueprint('password_reset', __name__)
mail = Mail()

# Generate a random OTP
def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

# Send OTP email
def send_otp_email(email, otp):
    msg = Message('Password Reset OTP', sender='noreply@example.com', recipients=[email])
    msg.body = f'Your OTP for password reset is: {otp}'
    mail.send(msg)

# Request password reset
@password_reset_bp.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user:
        otp = generate_otp()
        user.password_reset_otp = otp
        user.password_reset_otp_expiry = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()
        
        send_otp_email(user.email, otp)
        return jsonify({"message": "OTP sent to your email address"}), 200
    return jsonify({"message": "User not found"}), 404

# Verify OTP and reset password
@password_reset_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email'], password_reset_otp=data['otp']).first()
    
    if user and user.password_reset_otp_expiry > datetime.utcnow():
        user.set_password(data['new_password'])
        user.password_reset_otp = None
        user.password_reset_otp_expiry = None
        db.session.commit()
        return jsonify({"message": "Password reset successfully"}), 200
    return jsonify({"message": "Invalid OTP or OTP has expired"}), 400
