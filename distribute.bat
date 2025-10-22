@echo off
REM Universal Windows installer
REM distribute.bat

echo 📦 Screen Share Application Installer
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed.
    echo    Download from: https://python.org
    pause
    exit /b 1
)

REM Create directory
if not exist ScreenShare mkdir ScreenShare
cd ScreenShare

REM Download application
echo 📥 Downloading application...
curl -L https://github.com/bibekchandsah/screenshare/archive/main.zip -o screenshare.zip
powershell -command "Expand-Archive screenshare.zip -DestinationPath ."
move screenshare-main\* .
rmdir /s /q screenshare-main
del screenshare.zip

REM Install requirements
echo 📦 Installing requirements...
pip install -r requirements.txt

echo ✅ Installation complete!
echo.
echo 🚀 To run the application:
echo    python main.py
echo.
echo 📖 Choose option:
echo    1 - Share your screen
echo    3 - View someone's screen
echo    4 - Enable internet sharing (ngrok)

pause