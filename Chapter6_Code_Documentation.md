# CHAPTER 6
# FRONT-END AND BACK-END CODE OF CARDIOSENSE

This chapter provides a detailed overview of the implementation logic for both the front-end interface and the back-end database connectivity of the CardioSense AI system.

## 6.1 Front–End Module Codes

The front-end of CardioSense is built using **Streamlit**, a high-performance Python framework for building data-driven web applications. The interface is designed with a premium, medical-grade aesthetic utilizing custom CSS (Glassmorphism) and Plotly for interactive diagnostic visualizations.

### 6.1.1 Implementation (frontend/app.py)

```python
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os

# FastAPI Backend URL Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")
if not API_URL.endswith("/predict"):
    API_URL = f"{API_URL.rstrip('/')}/predict"

st.set_page_config(
    page_title="CardioSense AI",
    layout="wide",
    page_icon="🫀",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Medical Interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    :root {
        --primary: #FF4B4B;
        --secondary: #00D1FF;
        --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        --card-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    .stApp {
        background: var(--bg-gradient);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .main-header {
        background: rgba(255, 255, 255, 0.03);
        padding: 3rem;
        border-radius: 24px;
        border: 1px solid var(--glass-border);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    .card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }

    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF7E7E 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.4);
        border: none;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
    <div class="main-header">
        <h1 style='font-size: 3.5rem; margin-bottom: 0.5rem;'>🫀 CardioSense <span style='color: #00D1FF;'>AI</span></h1>
        <p style='font-size: 1.2rem; color: #94a3b8; max-width: 700px; margin: 0 auto;'>
            Next-generation cardiac decision support utilizing multi-model ensemble analysis 
            for precision heart sound interpretation.
        </p>
    </div>
""", unsafe_allow_html=True)

# Tabs Setup
tab1, tab2, tab3 = st.tabs(["🩺 Prediction System", "📊 Diagnostic Analytics", "🕒 Clinical History"])

with tab1:
    st.markdown("### <span style='color: #00D1FF;'>01</span> Patient Biomarkers", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### S1 Features (Lub)")
            s1_duration = st.number_input("S1 Duration (sec)", min_value=0.0, value=0.12)
            s1_amplitude = st.number_input("S1 Amplitude", min_value=0.0, value=0.55)
            s1_area = st.number_input("S1 Area", min_value=0.0, value=0.05)
            systole_duration = st.number_input("Systole Duration (sec)", min_value=0.0, value=0.34)
        
        with col2:
            st.markdown("#### S2 Features (Dub)")
            s2_duration = st.number_input("S2 Duration (sec)", min_value=0.0, value=0.09)
            s2_amplitude = st.number_input("S2 Amplitude", min_value=0.0, value=0.45)
            s2_area = st.number_input("S2 Area", min_value=0.0, value=0.04)
            diastole_duration = st.number_input("Diastole Duration (sec)", min_value=0.0, value=0.51)
        
        st.markdown('</div>', unsafe_allow_html=True)

    predict_pressed = st.button("Initialize AI Analysis", type="primary")

with tab2:
    if predict_pressed:
        payload = {
            "s1_duration_sec": s1_duration, "s1_amplitude": s1_amplitude,
            "s1_area": s1_area, "s2_duration_sec": s2_duration,
            "s2_amplitude": s2_amplitude, "s2_area": s2_area,
            "systole_duration_sec": systole_duration, "diastole_duration_sec": diastole_duration
        }
        
        with st.spinner("Processing through Neural Ensemble..."):
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                risk_level = data['risk_level']
                probs = data['probabilities']
                
                # Visual Feedback based on Risk
                color = "#FF4B4B" if risk_level == "HIGH" else "#FFAA00" if risk_level == "MODERATE" else "#00FFAB"
                
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); border: 1px solid {color}; padding: 2rem; border-radius: 20px; text-align: center;">
                        <h2 style="color: {color};">Risk Level: {risk_level}</h2>
                        <p>Confidence: {probs['ensemble']:.1%}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = probs['ensemble'] * 100,
                    title = {'text': "Abnormality Risk %"},
                    gauge = {'bar': {'color': color}}
                ))
                st.plotly_chart(fig)
```

---

## 6.2 Database Connectivity

CardioSense utilizes a relational database management system (**MySQL**) to ensure clinical data persistence and auditability. The connectivity layer is implemented using the `mysql-connector-python` library, featuring atomic transactions and structured error handling.

### 6.2.1 Database Schema (backend/schema.sql)

The schema follows the **Third Normal Form (3NF)** to ensure data integrity and minimize redundancy.

```sql
-- 1. PATIENT Table: Stores demographic and entry metadata
CREATE TABLE PATIENT (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file VARCHAR(50),
    notes TEXT
);

-- 2. HEART_SOUND Table: Stores acoustic biomarkers extracted from audio
CREATE TABLE HEART_SOUND (
    sound_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    s1_duration_sec FLOAT,
    s1_amplitude FLOAT,
    s1_area FLOAT,
    s2_duration_sec FLOAT,
    s2_amplitude FLOAT,
    s2_area FLOAT,
    systole_duration_sec FLOAT,
    diastole_duration_sec FLOAT,
    FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id) ON DELETE CASCADE
);

-- 3. PREDICTION Table: Stores AI model outputs and risk classification
CREATE TABLE PREDICTION (
    pred_id INT AUTO_INCREMENT PRIMARY KEY,
    sound_id INT NOT NULL,
    rf_probability FLOAT,
    xgb_probability FLOAT,
    lgbm_probability FLOAT,
    ensemble_probability FLOAT,
    final_risk_level VARCHAR(20),
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sound_id) REFERENCES HEART_SOUND(sound_id) ON DELETE CASCADE
);
```

### 6.2.2 Connectivity Logic (backend/database.py)

The Python backend manages the connection lifecycle and executes complex multi-table inserts within a single transaction to maintain atomicity.

```python
import mysql.connector
from mysql.connector import Error
import os

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "masteradmin")
DB_NAME = os.getenv("DB_NAME", "cardiosense")

def get_db_connection():
    """Establish and return a MySQL connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def insert_prediction_transaction(patient_id, features, probabilities, final_risk):
    """
    Inserts data into PATIENT, HEART_SOUND, and PREDICTION tables atomically.
    Ensures data consistency across the entire schema.
    """
    conn = get_db_connection()
    if not conn: return False
        
    try:
        conn.autocommit = False # Start transaction
        cursor = conn.cursor()
        
        # Step 1: Insert Patient Record
        cursor.execute("INSERT INTO PATIENT (source_file) VALUES (%s)", ('api_input',))
        actual_patient_id = cursor.lastrowid
        
        # Step 2: Insert Extracted Biomarkers
        hs_query = "INSERT INTO HEART_SOUND (patient_id, ...) VALUES (%s, ...)"
        # ... logic for executing insert ...
        
        # Step 3: Insert AI Prediction Results
        pred_query = "INSERT INTO PREDICTION (sound_id, ensemble_probability, final_risk_level) VALUES (%s, %s, %s)"
        cursor.execute(pred_query, (sound_id, probabilities['ensemble'], final_risk))
        
        conn.commit() # Commit all changes
        return True
        
    except Error as e:
        conn.rollback() # Rollback on failure
        return False
    finally:
        if conn: conn.close()

---

## 6.3 Machine Learning Module Codes

CardioSense employs a **Multi-Model Soft-Voting Ensemble** architecture to achieve high precision in heart sound classification. The pipeline includes data normalization, class imbalance handling, and a comparative training framework using Random Forest, XGBoost, and LightGBM.

### 6.3.1 Model Training Pipeline (ml/train_models.py)

The training script handles the end-to-end lifecycle from raw data ingestion to model serialization.

```python
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

def train_ensemble_models():
    # 1. Load and Clean Acoustic Data
    df_all = pd.read_csv('acoustic_biomarkers.csv').drop_duplicates()

    # 2. Handle Class Imbalance
    # Undersample normal class to manage medical dataset skewness
    df_normal = df_all[df_all['label'] == 0]
    df_abnormal = df_all[df_all['label'] == 1]
    df_balanced = pd.concat([df_normal.sample(n=len(df_abnormal)*2), df_abnormal])

    # 3. Feature Scaling
    X = df_balanced.drop(columns=['label'])
    y = df_balanced['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    joblib.dump(scaler, 'scaler.pkl')

    # 4. Ensemble Model Definitions
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=15, class_weight='balanced'),
        'XGBoost': XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05),
        'LightGBM': LGBMClassifier(n_estimators=300, num_leaves=63, learning_rate=0.05)
    }

    # 5. Training and Serialization
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        # Serialize for production use in FastAPI
        joblib.dump(model, f"{name.lower().replace(' ', '_')}_model.pkl")

if __name__ == "__main__":
    train_ensemble_models()
```

### 6.3.2 Production Inference Logic (backend/main.py snippet)

The backend utilizes the serialized models to perform real-time ensemble inference.

```python
@app.post("/predict")
def predict_heart_sound(features: HeartSoundFeatures):
    # Scale incoming real-time features
    X_scaled = scaler.transform(feature_values)
    
    # Generate probabilities from all 3 models
    prob_rf = float(models['rf'].predict_proba(X_scaled)[0, 1])
    prob_xgb = float(models['xgb'].predict_proba(X_scaled)[0, 1])
    prob_lgbm = float(models['lgbm'].predict_proba(X_scaled)[0, 1])
    
    # Calculate Soft Voting Ensemble Probability
    ensemble_prob = (prob_rf + prob_xgb + prob_lgbm) / 3.0
    
    # Classify Risk based on Ensemble Confidence
    if ensemble_prob >= 0.70: risk_level = "HIGH"
    elif ensemble_prob >= 0.40: risk_level = "MODERATE"
    else: risk_level = "LOW"
    
    return {"risk_level": risk_level, "ensemble_probability": ensemble_prob}
```

```
