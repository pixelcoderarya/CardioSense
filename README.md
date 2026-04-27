# CardioSense AI 🩺

CardioSense is a state-of-the-art AI-driven heart sound analysis system. It leverages machine learning models (Random Forest, XGBoost, and LightGBM) to analyze heart sound features and provide diagnostic support.

## 🌟 Key Features
- **Multi-Model Ensemble**: Combines multiple ML models for high-accuracy predictions.
- **FastAPI Backend**: Robust and scalable API for real-time analysis.
- **Streamlit Frontend**: A premium, interactive UI for visualization and data input.
- **Docker Ready**: Full stack containerization for easy deployment.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- MySQL
- Docker (optional)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Running the App
You can run the full stack using Docker:
```bash
docker-compose up --build
```
Or manually:
1. Initialize the database: `python init_db.py`
2. Start the backend: `uvicorn backend.main:app --reload`
3. Start the frontend: `streamlit run frontend/app.py`

## 📂 Project Structure
- `backend/`: FastAPI application and database logic.
- `frontend/`: Streamlit user interface.
- `ml/`: Training scripts and serialized models.
- `data/`: Dataset and feature files.

## 📄 Deployment
See [README_DEPLOY.md](README_DEPLOY.md) for detailed deployment instructions.

---
Built with ❤️ for better heart health.
