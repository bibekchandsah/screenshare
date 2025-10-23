@echo off
echo =====================================================================
echo 🚀 CLOUDFLARE TUNNEL SETUP HELPER
echo =====================================================================
echo.
echo This script will help you set up cloudflared for the screen share app.
echo.
echo 📁 Current directory: %cd%
echo.
echo 🔍 SETUP OPTIONS:
echo.
echo 1. Copy existing cloudflared.exe to this folder
echo 2. Download cloudflared.exe directly
echo 3. Exit
echo.
set /p choice="Choose option (1-3): "

if "%choice%"=="1" goto copy_existing
if "%choice%"=="2" goto download
if "%choice%"=="3" goto exit
goto invalid

:copy_existing
echo.
echo 📂 Please follow these steps:
echo 1. Find your cloudflared.exe file
echo 2. Copy it to this folder: %cd%
echo 3. Press any key when done
echo.
pause
if exist "cloudflared.exe" (
    echo ✅ cloudflared.exe found!
    echo 🚀 You can now run: python cloudflare_helper.py
) else (
    echo ❌ cloudflared.exe not found in this folder
    echo Please copy the file and try again
)
goto end

:download
echo.
echo 🌐 Opening Cloudflare releases page...
echo Download: cloudflared-windows-amd64.exe
echo Rename it to: cloudflared.exe
echo Place it in: %cd%
echo.
start https://github.com/cloudflare/cloudflared/releases/latest
echo 📥 Download started in your browser
echo 📁 Save the file as 'cloudflared.exe' in this folder
echo.
pause
if exist "cloudflared.exe" (
    echo ✅ cloudflared.exe found!
    echo 🚀 You can now run: python cloudflare_helper.py
) else (
    echo ❌ cloudflared.exe not found
    echo Please download and rename the file, then try again
)
goto end

:invalid
echo ❌ Invalid choice
goto end

:exit
echo 👋 Goodbye!
goto end

:end
echo.
echo Press any key to exit...
pause > nul