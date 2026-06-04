import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_fraud_model():
    """Train Random Forest model for fraud detection"""
    print("📊 Loading dataset...")
    df = pd.read_csv("dataset/insurance_claims.csv")

    features = [
        "claim_amount", "claim_frequency", "duplicate_claim",
        "suspicious_keywords", "policy_expired", "days_since_policy",
        "num_previous_claims", "amount_vs_avg_ratio", "incident_to_claim_days"
    ]
    target = "fraud_label"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("🤖 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model Accuracy: {acc * 100:.2f}%")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Genuine", "Fraudulent"]))

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/fraud_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(features, "models/features.pkl")
    print("💾 Model saved to models/fraud_model.pkl")

    return model, scaler, features

if __name__ == "__main__":
    train_fraud_model()
