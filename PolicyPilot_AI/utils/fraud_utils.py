import pandas as pd
import numpy as np
import joblib
import os
from models.train_model import train_fraud_model

def load_model():
    """Load trained model or train if not exists"""
    model_path = "models/fraud_model.pkl"
    scaler_path = "models/scaler.pkl"
    features_path = "models/features.pkl"

    if not os.path.exists(model_path):
        train_fraud_model()

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    return model, scaler, features

def calculate_fraud_features(claim_amount, claim_frequency, duplicate_claim,
                               has_suspicious_keywords, policy_expired,
                               days_since_policy, num_previous_claims,
                               avg_claim_amount=58000, incident_to_claim_days=5):
    """Calculate features for fraud prediction"""
    amount_vs_avg_ratio = claim_amount / avg_claim_amount if avg_claim_amount > 0 else 1.0

    return {
        "claim_amount": claim_amount,
        "claim_frequency": claim_frequency,
        "duplicate_claim": int(duplicate_claim),
        "suspicious_keywords": int(has_suspicious_keywords),
        "policy_expired": int(policy_expired),
        "days_since_policy": days_since_policy,
        "num_previous_claims": num_previous_claims,
        "amount_vs_avg_ratio": amount_vs_avg_ratio,
        "incident_to_claim_days": incident_to_claim_days,
    }

def predict_fraud(features_dict):
    """Predict fraud probability and class"""
    try:
        model, scaler, feature_names = load_model()

        feature_values = [[features_dict[f] for f in feature_names]]
        feature_scaled = scaler.transform(feature_values)

        prediction = model.predict(feature_scaled)[0]
        probabilities = model.predict_proba(feature_scaled)[0]

        fraud_prob = probabilities[1] * 100
        genuine_prob = probabilities[0] * 100

        if fraud_prob >= 70:
            risk_label = "🔴 Fraudulent Claim"
            risk_level = "High"
        elif fraud_prob >= 40:
            risk_label = "🟡 Suspicious Claim"
            risk_level = "Medium"
        else:
            risk_label = "🟢 Genuine Claim"
            risk_level = "Low"

        return {
            "prediction": int(prediction),
            "risk_label": risk_label,
            "risk_level": risk_level,
            "fraud_probability": round(fraud_prob, 2),
            "genuine_probability": round(genuine_prob, 2),
            "confidence_score": round(max(fraud_prob, genuine_prob), 2),
        }

    except Exception as e:
        return {
            "prediction": 0,
            "risk_label": "⚠️ Analysis Error",
            "risk_level": "Unknown",
            "fraud_probability": 0,
            "genuine_probability": 0,
            "confidence_score": 0,
            "error": str(e)
        }

def get_fraud_indicators(features_dict, fraud_prob):
    """Generate list of fraud indicators"""
    indicators = []

    if features_dict.get("claim_amount", 0) > 300000:
        indicators.append("💰 Unusually high claim amount")
    if features_dict.get("claim_frequency", 0) >= 3:
        indicators.append("📋 High claim frequency detected")
    if features_dict.get("duplicate_claim", 0):
        indicators.append("🔄 Possible duplicate claim")
    if features_dict.get("suspicious_keywords", 0):
        indicators.append("⚠️ Suspicious keywords in description")
    if features_dict.get("policy_expired", 0):
        indicators.append("❌ Policy was expired at claim time")
    if features_dict.get("days_since_policy", 365) < 60:
        indicators.append("🆕 Claim filed very soon after policy start")
    if features_dict.get("num_previous_claims", 0) >= 3:
        indicators.append("📊 Multiple previous claims on file")
    if features_dict.get("amount_vs_avg_ratio", 1) > 5:
        indicators.append("📈 Amount far exceeds policy average")
    if features_dict.get("incident_to_claim_days", 10) <= 2:
        indicators.append("⏱️ Claim filed suspiciously fast after incident")

    return indicators if indicators else ["✅ No significant fraud indicators detected"]

def check_duplicate_claims(claim_id, customer_name, claim_amount):
    """Check for duplicate claims in CSV"""
    try:
        df = pd.read_csv("claims.csv")
        duplicates = df[
            (df["customer_name"].str.lower() == customer_name.lower()) &
            (abs(df["claim_amount"] - claim_amount) < 5000) &
            (df["claim_id"] != claim_id)
        ]
        return len(duplicates) > 0, len(duplicates)
    except:
        return False, 0
