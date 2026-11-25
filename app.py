from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import db, User, MedicalRecord
from model import predict_risk
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import webbrowser
import threading
import os

app = Flask(__name__)
app.secret_key = 'womenhealthai_secret_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///womenhealthai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ─── HOME ─────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('base.html', page='home')

# ─── REGISTER ─────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = generate_password_hash(request.form['password'])
        role     = request.form.get('role', 'patient')
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('base.html', page='register')

# ─── LOGIN ────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user     = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id']   = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            return redirect(url_for('dashboard'))
        flash('Invalid email or password!', 'danger')
    return render_template('base.html', page='login')

# ─── LOGOUT ───────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ─── DASHBOARD ────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('user_role') == 'doctor':
        patients = User.query.filter_by(role='patient').all()
        records  = MedicalRecord.query.order_by(MedicalRecord.created_at.desc()).all()
        return render_template('dashboard.html', view='doctor', patients=patients, records=records)
    else:
        records = MedicalRecord.query.filter_by(
            user_id=session['user_id']
        ).order_by(MedicalRecord.created_at.desc()).all()
        return render_template('dashboard.html', view='patient', records=records)

# ─── PREDICT ──────────────────────────────────────────────────
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    result = None
    if request.method == 'POST':
        try:
            data = {
                'age':            float(request.form['age']),
                'pregnancies':    float(request.form['pregnancies']),
                'glucose':        float(request.form['glucose']),
                'blood_pressure': float(request.form['blood_pressure']),
                'bmi':            float(request.form['bmi']),
                'insulin':        float(request.form['insulin']),
                'skin_thickness': float(request.form['skin_thickness']),
                'dpf':            float(request.form['dpf']),
            }
            result = predict_risk(data)
            record = MedicalRecord(
                user_id        = session['user_id'],
                age            = int(data['age']),
                pregnancies    = int(data['pregnancies']),
                glucose        = data['glucose'],
                blood_pressure = data['blood_pressure'],
                bmi            = data['bmi'],
                insulin        = data['insulin'],
                skin_thickness = data['skin_thickness'],
                dpf            = data['dpf'],
                risk_result    = result['label'],
                risk_percentage= result['percentage'],
            )
            db.session.add(record)
            db.session.commit()
            flash('Prediction complete and saved!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('prdedict.html', result=result)

# ─── RECORDS ──────────────────────────────────────────────────
@app.route('/records')
def records():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_records = MedicalRecord.query.filter_by(
        user_id=session['user_id']
    ).order_by(MedicalRecord.created_at.desc()).all()
    return render_template('records.html', records=user_records)

# ─── AUTO OPEN CHROME OR FIREFOX ──────────────────────────────
def open_browser():
    url = 'http://127.0.0.1:5000'
    # Try Chrome first, then Firefox, then default browser
    chrome_paths = [
        'C:/Program Files/Google/Chrome/Application/chrome.exe %s',
        'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s',
    ]
    firefox_paths = [
        'C:/Program Files/Mozilla Firefox/firefox.exe %s',
        'C:/Program Files (x86)/Mozilla Firefox/firefox.exe %s',
    ]
    opened = False
    for path in chrome_paths:
        try:
            webbrowser.get(path).open(url)
            opened = True
            break
        except:
            pass
    if not opened:
        for path in firefox_paths:
            try:
                webbrowser.get(path).open(url)
                opened = True
                break
            except:
                pass
    if not opened:
        webbrowser.open(url)

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, host='127.0.0.1', port=5000)
