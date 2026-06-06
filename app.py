from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_development_key' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

try:
    pipeline = joblib.load('sentiment_pipeline.joblib')
    print("Model pipeline loaded successfully!")
except Exception as e:
    print("Error loading model.")
    pipeline = None

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    age_group = db.Column(db.String(20), nullable=False) 
    
    # --- NEW USER DETAILS ---
    email = db.Column(db.String(120), unique=True, nullable=True)
    full_name = db.Column(db.String(100), nullable=True)
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    age_group = data.get('age_group')
    
    # Extract the new details from the request
    email = data.get('email')
    full_name = data.get('full_name')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    
    # Save EVERYTHING to the SQLite database
    new_user = User(
        username=username, 
        password_hash=hashed_password, 
        age_group=age_group,
        email=email,
        full_name=full_name
    )
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()

    if user and check_password_hash(user.password_hash, data.get('password')):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful!", "username": user.username})
    
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully!"})

@app.route('/predict', methods=['POST'])
def predict():
    if not pipeline:
        return jsonify({'error': 'Model pipeline not loaded.'}), 500

    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized. Please log in.'}), 401

    try:
        current_user = User.query.get(session['user_id'])
        
        data = request.json
        text_input = data.get('text', '')

        # REMOVED Time of Tweet here, keeping only text and Age
        input_df = pd.DataFrame([{
            'text': text_input,
            'Age of User': current_user.age_group 
        }])

        predicted_score = pipeline.predict(input_df)[0]
        final_score = max(-1.0, min(1.0, float(predicted_score)))

        return jsonify({
            'status': 'success',
            'mood_score': round(final_score, 2),
            'age_used': current_user.age_group 
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/')
def serve_frontend():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)