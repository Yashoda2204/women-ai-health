"""
model.py — AI Health Risk Prediction
Uses rule-based scoring (simulates Random Forest + Logistic Regression output).
You can replace predict_risk() with a real trained sklearn model later.

Research paper methods used:
  - Random Forest (ensemble decision trees)
  - Logistic Regression (probability output)
  - Predictive Analytics (multi-parameter risk scoring)
"""


def predict_risk(data: dict) -> dict:
    """
    Input:  data dict with keys:
            age, pregnancies, glucose, blood_pressure,
            bmi, insulin, skin_thickness, dpf
    Output: dict with label, percentage, color, tips
    """

    score = 0

    # ── Glucose Analysis ───────────────────────────────────
    glucose = data.get('glucose', 0)
    if glucose > 140:
        score += 30
    elif glucose > 110:
        score += 18
    elif glucose > 99:
        score += 8

    # ── BMI Analysis ───────────────────────────────────────
    bmi = data.get('bmi', 0)
    if bmi > 35:
        score += 22
    elif bmi > 30:
        score += 15
    elif bmi > 25:
        score += 8

    # ── Blood Pressure ─────────────────────────────────────
    bp = data.get('blood_pressure', 0)
    if bp > 100:
        score += 15
    elif bp > 90:
        score += 10
    elif bp > 80:
        score += 5

    # ── Age Factor ─────────────────────────────────────────
    age = data.get('age', 0)
    if age > 50:
        score += 15
    elif age > 40:
        score += 10
    elif age > 30:
        score += 5

    # ── Insulin ────────────────────────────────────────────
    insulin = data.get('insulin', 0)
    if insulin > 200:
        score += 10
    elif insulin > 100:
        score += 5

    # ── Diabetes Pedigree Function (family history) ────────
    dpf = data.get('dpf', 0)
    if dpf > 1.0:
        score += 10
    elif dpf > 0.5:
        score += 6

    # ── Pregnancies ────────────────────────────────────────
    pregnancies = data.get('pregnancies', 0)
    if pregnancies > 5:
        score += 8
    elif pregnancies > 2:
        score += 4

    # ── Skin Thickness ─────────────────────────────────────
    skin = data.get('skin_thickness', 0)
    if skin > 35:
        score += 5

    # ── Cap at 99 ──────────────────────────────────────────
    score = min(int(score), 99)

    # ── Classify ───────────────────────────────────────────
    if score >= 60:
        label = 'High Risk'
        color = 'danger'
        tips  = [
            'Consult a doctor as soon as possible.',
            'Reduce sugar and high-carb foods.',
            'Monitor blood pressure daily.',
            'Begin a medically supervised exercise plan.',
        ]
    elif score >= 30:
        label = 'Moderate Risk'
        color = 'warning'
        tips  = [
            'Schedule a health check-up within a month.',
            'Reduce processed foods and increase vegetables.',
            'Aim for 30 minutes of walking daily.',
            'Monitor your glucose levels regularly.',
        ]
    else:
        label = 'Low Risk'
        color = 'success'
        tips  = [
            'Keep maintaining your healthy lifestyle!',
            'Annual health check-ups are still recommended.',
            'Stay hydrated and sleep 7–8 hours daily.',
            'Continue regular physical activity.',
        ]

    return {
        'label':      label,
        'color':      color,
        'percentage': score,
        'tips':       tips,
    }
