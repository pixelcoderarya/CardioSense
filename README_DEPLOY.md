# 🚀 Making CardioSense Live

This document provides instructions on how to deploy the CardioSense AI system to a live production environment.

## 📦 Containerization with Docker

The project is now equipped with Docker configurations for a seamless "one-click" deployment of the entire stack (Database, Backend, and Frontend).

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 1. Launching the Full Stack Locally
To test the production environment locally, run the following command in the project root:

```powershell
docker-compose up --build
```

This will:
1.  **Initialize MySQL**: Create the `cardiosense` database and run `backend/schema.sql`.
2.  **Start Backend**: Launch the FastAPI server on `http://localhost:8000`.
3.  **Start Frontend**: Launch the Streamlit UI on `http://localhost:8501`.

---

## 🌐 Cloud Deployment Options

To make the project accessible over the public internet, you can use several platforms:

### Option A: Render (Recommended for Simplicity)
1.  **Database**: Create a "Managed MySQL" instance on Render.
2.  **Backend**:
    - Create a "Web Service" connected to your GitHub repo.
    - Set the **Root Directory** to `./`.
    - Set **Build Command**: `pip install -r requirements.txt`.
    - Set **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
    - Add **Environment Variables**: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (pointing to your Render MySQL).
3.  **Frontend**:
    - Create another "Web Service".
    - Set **Start Command**: `streamlit run frontend/app.py --server.port $PORT`.
    - Add **Environment Variable**: `API_URL` (pointing to your Render Backend URL).

### Option B: Railway / Fly.io
These platforms support `docker-compose.yml` or Dockerfiles directly, making the deployment extremely straightforward. Simply connect your repository and they will detect the configuration.

---

## 🛠️ Production Checklist
- [ ] **Security**: Change the default `DB_PASSWORD` in `docker-compose.yml` and `Dockerfile` before pushing to a public repository.
- [ ] **Persistence**: Ensure the `db_data` volume is correctly mapped in your production environment to avoid data loss on restarts.
- [ ] **SSL**: Use a platform that provides automatic HTTPS (like Render or Vercel/Streamlit Cloud).

---

### API Reference
Once live, your backend will expose the following endpoints:
- `GET /`: Health check.
- `POST /predict`: Submit heart sound features for AI analysis.
- `POST /feedback`: (Optional) Submit clinical feedback for future training.
