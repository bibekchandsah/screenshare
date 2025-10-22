# Quick Build Script for Screen Sharing Application
# For PowerShell on Windows

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       SCREEN SHARING APPLICATION - BUILD TOOL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python detected: $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from: https://www.python.org/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if PyInstaller is installed
$pyinstallerCheck = python -c "import PyInstaller" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ PyInstaller not found. Installing dependencies..." -ForegroundColor Yellow
    Write-Host ""
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "✗ ERROR: Failed to install dependencies!" -ForegroundColor Red
        Write-Host "Please run manually: pip install -r requirements.txt" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Choose build type:" -ForegroundColor Cyan
Write-Host "  [1] Regular EXE (No console window - Clean)" -ForegroundColor White
Write-Host "  [2] Console EXE (With console - For debugging)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1 or 2)"

Write-Host ""
if ($choice -eq "1") {
    Write-Host "Building regular EXE..." -ForegroundColor Yellow
    Write-Host ""
    python build_exe.py
} elseif ($choice -eq "2") {
    Write-Host "Building console EXE..." -ForegroundColor Yellow
    Write-Host ""
    python build_console_exe.py
} else {
    Write-Host "Invalid choice! Building regular EXE by default..." -ForegroundColor Yellow
    Write-Host ""
    python build_exe.py
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Build complete! Check the dist\ folder for your EXE file." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
