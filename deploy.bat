@echo off
echo Starting XRay Federation System Deployment...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r backend\requirements.txt

:: Initialize database
echo Initializing database...
cd backend
python -c "from app import init_db; init_db()"

echo.
echo ✅ Deployment completed successfully!
echo.
echo To start the system:
echo   cd backend
echo   python app.py
echo.
echo Access points:
echo   - Web Dashboard: http://localhost:5000/dashboard
echo   - Orthanc DICOM: http://localhost:8042
echo.
pause
