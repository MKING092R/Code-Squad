from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbon_credits.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model Definitions
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    activities = db.relationship('Activity', backref='user', lazy=True)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    verified = db.Column(db.Boolean, default=False)

class CarbonCredit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

class Marketplace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carbon_credit_id = db.Column(db.Integer, db.ForeignKey('carbon_credit.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

# User Management Routes
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json['username']
    password = request.json['password']
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

# Activity Submission
@app.route('/submit_activity', methods=['POST'])
def submit_activity():
    user_id = request.json['user_id']
    description = request.json['description']
    new_activity = Activity(user_id=user_id, description=description)
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({'message': 'Activity submitted successfully!'}), 201

# Carbon Credit Generation
@app.route('/generate_credit', methods=['POST'])
def generate_credit():
    activity_id = request.json['activity_id']
    quantity = request.json['quantity']
    new_credit = CarbonCredit(activity_id=activity_id, quantity=quantity)
    db.session.add(new_credit)
    db.session.commit()
    return jsonify({'message': 'Carbon credit generated successfully!'}), 201

# Marketplace Trading
@app.route('/trade_credit', methods=['POST'])
def trade_credit():
    carbon_credit_id = request.json['carbon_credit_id']
    price = request.json['price']
    new_trade = Marketplace(carbon_credit_id=carbon_credit_id, price=price)
    db.session.add(new_trade)
    db.session.commit()
    return jsonify({'message': 'Carbon credit put on marketplace!'}), 201

# Run server
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)