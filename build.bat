@echo off
REM Quick Build Script for Screen Sharing Application
REM Double-click this file to compile to EXE (Windows)

echo ============================================================
echo          SCREEN SHARING APPLICATION - BUILD TOOL
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python detected!
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing dependencies...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please run manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo Choose build type:
echo   [1] Regular EXE (No console window - Clean)
echo   [2] Console EXE (With console - For debugging)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Building regular EXE...
    echo.
    python build_exe.py
) else if "%choice%"=="2" (
    echo.
    echo Building console EXE...
    echo.
    python build_console_exe.py
) else (
    echo.
    echo Invalid choice! Building regular EXE by default...
    echo.
    python build_exe.py
)

echo.
echo ============================================================
echo.
echo Build complete! Check the dist\ folder for your EXE file.
echo.
pause
