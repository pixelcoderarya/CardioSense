Write-Host "🚀 Starting CardioSense AI System..." -ForegroundColor Cyan

# Set environment variables for the session
$env:DB_HOST = "localhost"
$env:DB_USER = "root"
$env:DB_PASSWORD = "masteradmin"
$env:DB_NAME = "cardiosense"
$env:API_URL = "http://localhost:8000/predict"

# Start Backend in a new window
Write-Host "-> Launching Backend (FastAPI on port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn backend.main:app --host 0.0.0.0 --port 8000"

# Wait for backend to warm up
Write-Host "-> Waiting for backend to initialize..."
Start-Sleep -Seconds 3

# Start Frontend in a new window
Write-Host "-> Launching Frontend (Streamlit on port 8501)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "streamlit run frontend/app.py"

Write-Host "`n✅ All services are now running!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:8501"
Write-Host "`nNote: Check the new terminal windows for logs."
