# ngrok Installation Helper Script
# This script helps you download and install ngrok manually

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "              NGROK INSTALLATION HELPER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will help you install ngrok manually." -ForegroundColor Yellow
Write-Host "We need to do this because of SSL certificate issues." -ForegroundColor Yellow
Write-Host ""

# Check if ngrok is already installed
$ngrokPaths = @(
    "$env:USERPROFILE\ngrok.exe",
    "C:\ngrok\ngrok.exe",
    "C:\Program Files\ngrok\ngrok.exe"
)

$ngrokFound = $false
foreach ($path in $ngrokPaths) {
    if (Test-Path $path) {
        Write-Host "✓ ngrok found at: $path" -ForegroundColor Green
        $ngrokFound = $true
        
        # Test if it works
        Write-Host ""
        Write-Host "Testing ngrok..." -ForegroundColor Yellow
        $version = & $path version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ ngrok is working! Version: $version" -ForegroundColor Green
        } else {
            Write-Host "⚠ ngrok found but may not be working properly" -ForegroundColor Yellow
        }
        break
    }
}

if (-not $ngrokFound) {
    Write-Host "✗ ngrok not found on system" -ForegroundColor Red
    Write-Host ""
    Write-Host "INSTALLATION STEPS:" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "OPTION 1: Automatic Download (Recommended)" -ForegroundColor Green
    Write-Host "-------------------------------------------" -ForegroundColor Green
    Write-Host ""
    
    $download = Read-Host "Do you want to download ngrok now? (y/n)"
    
    if ($download -eq "y" -or $download -eq "Y") {
        Write-Host ""
        Write-Host "Downloading ngrok..." -ForegroundColor Yellow
        
        # Create temp directory
        $tempDir = "$env:TEMP\ngrok_download"
        New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
        
        # Download URL (Windows 64-bit)
        $ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        $zipPath = "$tempDir\ngrok.zip"
        $extractPath = "$env:USERPROFILE"
        
        try {
            # Disable SSL verification for download (only for this download)
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
            
            Write-Host "Downloading from: $ngrokUrl" -ForegroundColor Gray
            
            # Use WebClient with SSL verification disabled
            $webClient = New-Object System.Net.WebClient
            $webClient.DownloadFile($ngrokUrl, $zipPath)
            
            Write-Host "✓ Download complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Extracting to: $extractPath" -ForegroundColor Yellow
            
            # Extract zip
            Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
            
            Write-Host "✓ Extraction complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "✓ ngrok installed at: $extractPath\ngrok.exe" -ForegroundColor Green
            
            # Test it
            Write-Host ""
            Write-Host "Testing ngrok..." -ForegroundColor Yellow
            $version = & "$extractPath\ngrok.exe" version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ ngrok is working! Version: $version" -ForegroundColor Green
            }
            
            # Cleanup
            Remove-Item -Recurse -Force $tempDir
            
            Write-Host ""
            Write-Host "============================================================" -ForegroundColor Green
            Write-Host "✓ INSTALLATION SUCCESSFUL!" -ForegroundColor Green
            Write-Host "============================================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Cyan
            Write-Host "1. (Optional) Get free authtoken from: https://dashboard.ngrok.com/signup" -ForegroundColor White
            Write-Host "2. (Optional) Add authtoken: ngrok config add-authtoken YOUR_TOKEN" -ForegroundColor White
            Write-Host "3. Try running your screen share app again!" -ForegroundColor White
            Write-Host ""
            
        } catch {
            Write-Host "✗ Download failed: $_" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please try OPTION 2 (Manual Download) below." -ForegroundColor Yellow
        }
        
    } else {
        Write-Host ""
        Write-Host "OPTION 2: Manual Download" -ForegroundColor Yellow
        Write-Host "-------------------------" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "1. Open browser and go to:" -ForegroundColor White
        Write-Host "   https://ngrok.com/download" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "2. Download 'Windows (64-bit)' version" -ForegroundColor White
        Write-Host ""
        Write-Host "3. Extract the zip file" -ForegroundColor White
        Write-Host ""
        Write-Host "4. Copy ngrok.exe to one of these locations:" -ForegroundColor White
        Write-Host "   • $env:USERPROFILE\ngrok.exe (Recommended)" -ForegroundColor Cyan
        Write-Host "   • C:\ngrok\ngrok.exe" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "5. Run this script again to verify installation" -ForegroundColor White
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "✓ ngrok is already installed!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    
    # Check if authtoken is configured
    Write-Host "Checking ngrok configuration..." -ForegroundColor Yellow
    $configPath = "$env:USERPROFILE\AppData\Local\ngrok\ngrok.yml"
    if (Test-Path $configPath) {
        $config = Get-Content $configPath -Raw
        if ($config -match "authtoken:") {
            Write-Host "✓ Auth token is configured" -ForegroundColor Green
        } else {
            Write-Host "⚠ No auth token found" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Optional: Add auth token for better features:" -ForegroundColor White
            Write-Host "1. Sign up at: https://dashboard.ngrok.com/signup" -ForegroundColor Cyan
            Write-Host "2. Get your authtoken" -ForegroundColor White
            Write-Host "3. Run: ngrok config add-authtoken YOUR_TOKEN" -ForegroundColor White
        }
    } else {
        Write-Host "⚠ ngrok not configured yet" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Optional: Configure ngrok:" -ForegroundColor White
        Write-Host "1. Sign up at: https://dashboard.ngrok.com/signup" -ForegroundColor Cyan
        Write-Host "2. Get your authtoken" -ForegroundColor White
        Write-Host "3. Run: ngrok config add-authtoken YOUR_TOKEN" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "You can now use ngrok in your screen share app!" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
