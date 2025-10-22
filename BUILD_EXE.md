# 📦 Building EXE Files

This guide shows how to compile the Python scripts into standalone `.exe` files that can run without Python installed.

## 🛠️ Prerequisites

Install PyInstaller:
```bash
pip install pyinstaller
```

---

## 🎯 Quick Build (Recommended)

### Build Main Application

**With Console (Recommended for first time):**
```bash
pyinstaller --onefile --add-data "web_client.html;." --name "ScreenShare" main.py
```

**Without Console (Clean UI):**
```bash
pyinstaller --onefile --noconsole --add-data "web_client.html;." --name "ScreenShare" main.py
```

**With Custom Icon:**
```bash
pyinstaller --onefile --noconsole --add-data "web_client.html;." --icon=icon.ico --name "ScreenShare" main.py
```

**Options explained:**
- `--onefile` - Creates a single `.exe` file (not a folder)
- `--add-data "web_client.html;."` - **REQUIRED** - Includes the HTML file
- `--noconsole` - No console window (remove this if you want to see logs)
- `--name` - Name of the output `.exe`
- `--icon` - Custom icon (optional, remove if you don't have one)

**Output:** `dist\ScreenShare.exe`

---

## 🌐 Build ngrok Helper (Optional)

```bash
pyinstaller --onefile --name "ngrok-helper" ngrok_helper.py
```

**Output:** `dist\ngrok-helper.exe`

---

## 📋 Step-by-Step Instructions

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Navigate to Project Directory
```bash
cd "d:\Programming\program exercise\Python\screen share"
```

### 3. Build Main Application

**With Console (Shows logs - Recommended):**
```bash
pyinstaller --onefile --add-data "web_client.html;." --name "ScreenShare" main.py
```

**Without Console (Clean):**
```bash
pyinstaller --onefile --noconsole --add-data "web_client.html;." --name "ScreenShare" main.py
```

### 4. Find Your EXE
```
dist\ScreenShare.exe
```

---

## 🎨 Add Custom Icon (Optional)

1. **Get an icon file** (`.ico` format)
   - Create one at: https://www.favicon-generator.org/
   - Or use any `.ico` file

2. **Save as `icon.ico`** in project folder

3. **Build with icon:**
```bash
pyinstaller --onefile --noconsole --name "ScreenShare" --icon=icon.ico main.py
```

---

## 📦 Build All Components

Create a batch file `build.bat`:

```batch
@echo off
echo Building Screen Share EXE files...
echo.

echo [1/2] Building main application...
pyinstaller --onefile --add-data "web_client.html;." --name "ScreenShare" main.py
echo.

echo [2/2] Building ngrok helper...
pyinstaller --onefile --name "ngrok-helper" ngrok_helper.py
echo.

echo ✅ Build complete!
echo.
echo Output files:
echo   - dist\ScreenShare.exe
echo   - dist\ngrok-helper.exe
echo.
pause
```

**Run:** Double-click `build.bat`

---

## 🚀 Distribution Package

### What to Include:

```
📦 ScreenShare-Package/
├── ScreenShare.exe          (Main application)
├── ngrok-helper.exe         (Optional - ngrok setup)
├── QUICK_START.md          (User guide)
├── README.md               (Documentation)
└── web_client.html         (Included in exe, but useful for reference)
```

### Create Distribution Folder:

**Windows PowerShell:**
```powershell
# Create distribution folder
New-Item -ItemType Directory -Path "ScreenShare-Package" -Force

# Copy EXE files
Copy-Item "dist\ScreenShare.exe" -Destination "ScreenShare-Package\"
Copy-Item "dist\ngrok-helper.exe" -Destination "ScreenShare-Package\"

# Copy documentation
Copy-Item "QUICK_START.md" -Destination "ScreenShare-Package\"
Copy-Item "README.md" -Destination "ScreenShare-Package\"

# Create ZIP
Compress-Archive -Path "ScreenShare-Package\*" -DestinationPath "ScreenShare-Package.zip" -Force

Write-Host "✅ Package created: ScreenShare-Package.zip"
```

---

## 📝 Important Notes

### ✅ Advantages of EXE:
- No Python installation required
- Easy to share with others
- Double-click to run
- Portable

### ⚠️ Things to Know:

1. **File Size:** EXE will be ~50-100 MB (includes Python + libraries)

2. **Antivirus Warning:** Some antivirus may flag it (false positive)
   - Solution: Sign the EXE or whitelist it

3. **First Run Slower:** Takes a few seconds to extract (one-time)

4. **Platform Specific:** Windows EXE only works on Windows
   - Build on Windows for Windows
   - Build on Mac for Mac
   - Build on Linux for Linux

5. **Updates:** Need to rebuild EXE for code changes

6. **Dependencies:** All Python dependencies are bundled automatically

---

## 🐛 Troubleshooting

### Problem: "Failed to execute script"
**Solution:** Build with console to see error:
```bash
pyinstaller --onefile --name "ScreenShare" main.py
```

### Problem: "ModuleNotFoundError"
**Solution:** Install missing package and rebuild:
```bash
pip install <package-name>
pyinstaller --onefile --name "ScreenShare" main.py
```

### Problem: EXE is too large
**Solution:** Use UPX compression:
```bash
pip install pyinstaller[encryption]
pyinstaller --onefile --upx-dir=upx --name "ScreenShare" main.py
```

### Problem: Antivirus blocks EXE
**Solutions:**
1. Whitelist the file in antivirus
2. Upload to VirusTotal to verify it's safe
3. Code sign the executable (advanced)

### Problem: web_client.html not found
**Solution:** PyInstaller needs to include it:
```bash
pyinstaller --onefile --add-data "web_client.html;." --name "ScreenShare" main.py
```

---

## 🔧 Advanced Build Options

### Include All Files:
```bash
pyinstaller --onefile ^
    --add-data "web_client.html;." ^
    --add-data "README.md;." ^
    --add-data "QUICK_START.md;." ^
    --name "ScreenShare" ^
    main.py
```

### Optimize Build:
```bash
pyinstaller --onefile ^
    --noconsole ^
    --optimize=2 ^
    --strip ^
    --name "ScreenShare" ^
    main.py
```

### Debug Build:
```bash
pyinstaller --onefile ^
    --debug=all ^
    --name "ScreenShare-Debug" ^
    main.py
```

---

## 📊 Build Comparison

| Method | Size | Speed | Ease | Recommended |
|--------|------|-------|------|-------------|
| `--onefile` | ~50MB | Medium | ⭐⭐⭐⭐⭐ | Yes |
| `--onedir` | ~150MB | Fast | ⭐⭐⭐ | No |
| No build (Python) | Small | Fast | ⭐⭐ | Development |

---

## ✅ Recommended Workflow

### For Development:
```bash
python main.py
```

### For Distribution:
```bash
pyinstaller --onefile --name "ScreenShare" main.py
```

### For Users:
```
Just run: ScreenShare.exe
```

---

## 📱 Quick Commands

**Build with console:**
```bash
pyinstaller --onefile main.py
```

**Build without console:**
```bash
pyinstaller --onefile --noconsole main.py
```

**Clean previous builds:**
```bash
rmdir /s /q build dist
del /q *.spec
```

**Build and clean:**
```bash
rmdir /s /q build dist 2>nul & pyinstaller --onefile --name "ScreenShare" main.py
```

---

## 🎯 Final Checklist

- [ ] Install PyInstaller: `pip install pyinstaller`
- [ ] Navigate to project folder
- [ ] Run build command
- [ ] Test the `.exe` file
- [ ] Check file size (~50-100 MB is normal)
- [ ] Test on another computer (without Python)
- [ ] Create distribution package
- [ ] Add documentation (QUICK_START.md)
- [ ] Share with users! 🎉

---

**Need help?** Check PyInstaller documentation: https://pyinstaller.org/
