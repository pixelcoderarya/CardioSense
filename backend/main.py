from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
import sys

# Add current directory to path for relative imports if run directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import insert_prediction_transaction

app = FastAPI(title="CardioSense API", description="AI Heart Sound Analysis API")

# 1. Define Input Schema
class HeartSoundFeatures(BaseModel):
    s1_duration_sec: float
    s1_amplitude: float
    s1_area: float
    s2_duration_sec: float
    s2_amplitude: float
    s2_area: float
    systole_duration_sec: float
    diastole_duration_sec: float

# 2. Global Model Variables
models = {}
scaler = None

@app.on_event("startup")
def load_models():
    """Loads the scaler and machine learning models on API startup."""
    global models, scaler
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models')
    
    try:
        scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        models['rf'] = joblib.load(os.path.join(model_dir, 'random_forest_model.pkl'))
        models['xgb'] = joblib.load(os.path.join(model_dir, 'xgboost_model.pkl'))
        models['lgbm'] = joblib.load(os.path.join(model_dir, 'lightgbm_model.pkl'))
        print("✅ Models loaded successfully into FastAPI.")
    except Exception as e:
        print(f"⚠️ Warning: Could not load models. Make sure train_models.py has been run. Error: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CardioSense API!"}

@app.post("/predict")
def predict_heart_sound(features: HeartSoundFeatures):
    """
    Receives acoustic features, scales them, runs through the 3-model ensemble,
    saves the transaction to MySQL, and returns the risk level.
    """
    if not scaler or not models:
        raise HTTPException(status_code=500, detail="Machine learning models are not loaded.")

    # Convert incoming JSON payload to numpy array for prediction
    feature_values = np.array([[
        features.s1_duration_sec, features.s1_amplitude, features.s1_area,
        features.s2_duration_sec, features.s2_amplitude, features.s2_area,
        features.systole_duration_sec, features.diastole_duration_sec
    ]])
    
    # Scale the features using the fitted StandardScaler
    X_scaled = scaler.transform(feature_values)
    
    # Generate probabilities from all 3 models
    prob_rf = float(models['rf'].predict_proba(X_scaled)[0, 1])
    prob_xgb = float(models['xgb'].predict_proba(X_scaled)[0, 1])
    prob_lgbm = float(models['lgbm'].predict_proba(X_scaled)[0, 1])
    
    # Calculate Soft Voting Ensemble Probability
    ensemble_prob = (prob_rf + prob_xgb + prob_lgbm) / 3.0
    
    # Risk Classification Thresholds
    if ensemble_prob >= 0.70:
        risk_level = "HIGH"
    elif ensemble_prob >= 0.40:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"
        
    probabilities = {
        'rf': prob_rf,
        'xgb': prob_xgb,
        'lgbm': prob_lgbm,
        'ensemble': ensemble_prob
    }
    
    # Store everything in the MySQL Database (Atomic Transaction)
    db_success = insert_prediction_transaction(
        patient_id=None, 
        features=features.model_dump(), # Using model_dump() instead of dict() for Pydantic V2
        probabilities=probabilities,
        final_risk=risk_level
    )
    
    return {
        "status": "success",
        "probabilities": probabilities,
        "risk_level": risk_level,
        "db_logged": db_success
    }
