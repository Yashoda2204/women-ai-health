from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ─── USER TABLE ──────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    role       = db.Column(db.String(20), default='patient')   # 'patient' or 'doctor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    records    = db.relationship('MedicalRecord', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'


# ─── MEDICAL RECORD TABLE ────────────────────────────────────
class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Health Parameters
    age             = db.Column(db.Integer)
    pregnancies     = db.Column(db.Integer)
    glucose         = db.Column(db.Float)
    blood_pressure  = db.Column(db.Float)
    bmi             = db.Column(db.Float)
    insulin         = db.Column(db.Float)
    skin_thickness  = db.Column(db.Float)
    dpf             = db.Column(db.Float)   # Diabetes Pedigree Function

    # AI Result
    risk_result     = db.Column(db.String(50))
    risk_percentage = db.Column(db.Float)

    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Record user={self.user_id} risk={self.risk_result}>'
