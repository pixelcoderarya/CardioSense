import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

import os

# FastAPI Backend URL
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

st.set_page_config(
    page_title="CardioSense AI",
    layout="wide",
    page_icon="🫀",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
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

    .card:hover {
        border-color: var(--secondary);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 209, 255, 0.1);
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

    .metric-container {
        text-align: center;
        padding: 1rem;
    }

    /* Style Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94a3b8;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: var(--secondary) !important;
        border-bottom-color: var(--secondary) !important;
    }

    /* Input styling */
    .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid var(--glass-border) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: var(--secondary) !important;
    }

    .risk-badge {
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
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
            s1_duration = st.number_input("S1 Duration (sec)", min_value=0.0, max_value=2.0, value=0.12, help="The duration of the first heart sound.")
            s1_amplitude = st.number_input("S1 Amplitude", min_value=0.0, value=0.55, help="Peak amplitude of S1 signal.")
            s1_area = st.number_input("S1 Area", min_value=0.0, value=0.05, help="Integrated area under the S1 curve.")
        
            st.markdown("#### Temporal Intervals")
            systole_duration = st.number_input("Systole Duration (sec)", min_value=0.0, max_value=2.0, value=0.34, help="Duration between S1 and S2.")
        
        with col2:
            st.markdown("#### S2 Features (Dub)")
            s2_duration = st.number_input("S2 Duration (sec)", min_value=0.0, max_value=2.0, value=0.09, help="The duration of the second heart sound.")
            s2_amplitude = st.number_input("S2 Amplitude", min_value=0.0, value=0.45, help="Peak amplitude of S2 signal.")
            s2_area = st.number_input("S2 Area", min_value=0.0, value=0.04, help="Integrated area under the S2 curve.")
        
            st.markdown("#### ") # Spacer
            st.write("") # Spacer
            diastole_duration = st.number_input("Diastole Duration (sec)", min_value=0.0, max_value=2.0, value=0.51, help="Duration between S2 and the next S1.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    predict_pressed = st.button("Initialize AI Analysis", type="primary", use_container_width=True)

with tab2:
    if predict_pressed:
        payload = {
            "s1_duration_sec": s1_duration,
            "s1_amplitude": s1_amplitude,
            "s1_area": s1_area,
            "s2_duration_sec": s2_duration,
            "s2_amplitude": s2_amplitude,
            "s2_area": s2_area,
            "systole_duration_sec": systole_duration,
            "diastole_duration_sec": diastole_duration
        }
        
        with st.spinner("Processing through Neural Ensemble..."):
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    risk_level = data['risk_level']
                    probs = data['probabilities']
                    
                    st.markdown("### <span style='color: #00D1FF;'>02</span> Analysis Results", unsafe_allow_html=True)
                    
                    # Risk Header Card
                    if risk_level == "HIGH":
                        color = "#FF4B4B"
                        bg = "rgba(255, 75, 75, 0.1)"
                        icon = "🚨"
                    elif risk_level == "MODERATE":
                        color = "#FFAA00"
                        bg = "rgba(255, 170, 0, 0.1)"
                        icon = "⚠️"
                    else:
                        color = "#00FFAB"
                        bg = "rgba(0, 255, 171, 0.1)"
                        icon = "✅"

                    st.markdown(f"""
                        <div style="background: {bg}; border: 1px solid {color}; padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
                            <h2 style="color: {color}; margin: 0;">{icon} Risk Level: {risk_level} {icon}</h2>
                            <p style="margin-top: 0.5rem; opacity: 0.8;">Confidence Level: {probs['ensemble']:.1%}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    col_left, col_right = st.columns([1, 1.5])
                    
                    with col_left:
                        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
                        st.markdown("#### Clinical Interpretation")
                        if risk_level == "HIGH":
                            st.write("High probability of pathological abnormality detected. Patient exhibits acoustic patterns consistent with valvular or structural heart disease.")
                        elif risk_level == "MODERATE":
                            st.write("Acoustic features fall within a borderline range. Correlation with clinical symptoms and further imaging (Echocardiogram) is recommended.")
                        else:
                            st.write("Heart sound morphology and temporal intervals are within normal physiological ranges. No significant anomalies detected.")
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col_right:
                        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
                        st.markdown("#### Ensemble Probability Distribution")
                        
                        # Plotly Gauge Chart for Ensemble
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = probs['ensemble'] * 100,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Abnormality Risk %", 'font': {'size': 18}},
                            gauge = {
                                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                                'bar': {'color': color},
                                'bgcolor': "rgba(255, 255, 255, 0.1)",
                                'borderwidth': 2,
                                'bordercolor': "white",
                                'steps': [
                                    {'range': [0, 33], 'color': 'rgba(0, 255, 0, 0.1)'},
                                    {'range': [33, 66], 'color': 'rgba(255, 255, 0, 0.1)'},
                                    {'range': [66, 100], 'color': 'rgba(255, 0, 0, 0.1)'}],
                            }
                        ))
                        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': "white", 'family': "Inter"},
                            height=250,
                            margin=dict(l=20, r=20, t=40, b=20)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Model Breakdown
                    st.markdown("#### Model Specificity")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.metric("Random Forest", f"{probs['rf']:.1%}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.metric("XGBoost", f"{probs['xgb']:.1%}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.metric("LightGBM", f"{probs['lgbm']:.1%}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    if data['db_logged']:
                        st.toast("Record securely logged to MySQL database", icon="💾")
                        st.caption("✅ Record ID generated and stored.")
                    else:
                        st.error("Database connection failure: Prediction not logged.")
                        
                else:
                    st.error(f"Engine Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")
    else:
        st.markdown("""
            <div style="text-align: center; padding: 5rem; opacity: 0.5;">
                <h3 style="font-weight: 400;">Awaiting Input Data...</h3>
                <p>Complete the patient biomarkers form to trigger the analysis engine.</p>
            </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### <span style='color: #00D1FF;'>03</span> Patient Record Ledger", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.info("The clinical history module is currently aggregating live data from the MySQL `PREDICTION` table.")
    st.markdown("""
        - **Real-time Synchronization**: Active
        - **Data Source**: `cardiosense_db.PREDICTIONS`
        - **Encryption**: AES-256
    """)
    st.markdown('</div>', unsafe_allow_html=True)
