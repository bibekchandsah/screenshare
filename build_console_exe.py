"""
Build Script for Screen Sharing Application (WITH CONSOLE)
Compiles the Python application to a standalone EXE file with visible console
Use this version if you want to see debug output and error messages
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("=" * 60)
    print(" " * 5 + "BUILDING SCREEN SHARE EXE (CONSOLE MODE)")
    print("=" * 60)
    print()
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if all required files exist
    required_files = [
        'main.py',
        'server.py',
        'client.py',
        'web_server.py',
        'ngrok_helper.py',
        'cloudflare_helper.py',
        'web_client.html'
    ]
    
    print("Checking required files...")
    missing_files = []
    for file in required_files:
        file_path = os.path.join(script_dir, file)
        if os.path.exists(file_path):
            print(f"  ✓ Found: {file}")
        else:
            print(f"  ✗ Missing: {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Error: Missing required files: {', '.join(missing_files)}")
        print("Please ensure all files are in the same directory.")
        sys.exit(1)
    
    # Check for ngrok binary
    print("\n" + "=" * 60)
    print("Checking for ngrok binary...")
    print("=" * 60)
    
    ngrok_paths = [
        os.path.join(os.path.expanduser('~'), 'ngrok.exe'),
        os.path.join(script_dir, 'ngrok.exe'),
        'C:\\ngrok\\ngrok.exe',
    ]
    
    # Also check in pyngrok cache
    try:
        from pyngrok import conf
        pyngrok_dir = conf.get_default().ngrok_path
        if pyngrok_dir and os.path.exists(pyngrok_dir):
            ngrok_paths.insert(0, pyngrok_dir)
    except:
        pass
    
    ngrok_binary = None
    for path in ngrok_paths:
        if os.path.exists(path):
            ngrok_binary = path
            print(f"  ✓ Found ngrok at: {path}")
            break
    
    if not ngrok_binary:
        print("  ⚠ ngrok binary not found (optional)")
        print("   Run: .\\install_ngrok.ps1 to add ngrok support")
    
    print("\n" + "=" * 60)
    print("Starting PyInstaller build...")
    print("=" * 60)
    print()
    
    # PyInstaller arguments (CONSOLE VERSION)
    pyinstaller_args = [
        'main.py',                              # Entry point
        '--name=ScreenShare_Console',           # Executable name
        '--onefile',                            # Single executable file
        '--console',                            # SHOW CONSOLE (for debugging)
        '--icon=icon.ico',                          # No icon (you can add one later)
        
        # Add all Python modules
        '--add-data=server.py;.',
        '--add-data=client.py;.',
        '--add-data=web_server.py;.',
        '--add-data=ngrok_helper.py;.',
        '--add-data=web_client.html;.',
    ]
    
    # Add ngrok binary if found
    if ngrok_binary:
        print(f"[*] Including ngrok binary in EXE: {ngrok_binary}")
        pyinstaller_args.append(f'--add-binary={ngrok_binary};.')
        print("  ✓ ngrok will be bundled with EXE")
    else:
        print("  ⚠ Building without ngrok")
    
    # Continue with other arguments
    pyinstaller_args.extend([
        # Exclude Qt bindings (we don't use Qt, only OpenCV)
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        '--exclude-module=PySide2',
        '--exclude-module=PySide6',
        '--exclude-module=tkinter',
        '--exclude-module=_tkinter',
        '--exclude-module=matplotlib',
        
        # Hidden imports (modules imported dynamically)
        '--hidden-import=mss',
        '--hidden-import=mss.windows',
        '--hidden-import=mss.linux',
        '--hidden-import=mss.darwin',
        '--hidden-import=PIL',
        '--hidden-import=PIL._imagingtk',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=cv2',
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=pyngrok',
        '--hidden-import=requests',
        '--hidden-import=threading',
        '--hidden-import=socket',
        '--hidden-import=json',
        '--hidden-import=base64',
        '--hidden-import=io',
        '--hidden-import=time',
        '--hidden-import=datetime',
        
        # Collect submodules
        '--collect-submodules=mss',
        '--collect-submodules=flask',
        '--collect-submodules=cv2',
        
        # Clean build
        '--clean',
        
        # Output directory
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
    ])
    
    # Note: On Windows, use semicolon (;) as separator
    # On Linux/Mac, use colon (:) as separator
    if sys.platform != 'win32':
        # Replace semicolons with colons for non-Windows platforms
        pyinstaller_args = [arg.replace(';', ':') for arg in pyinstaller_args]
    
    try:
        # Run PyInstaller
        PyInstaller.__main__.run(pyinstaller_args)
        
        print("\n" + "=" * 60)
        print("✅ BUILD SUCCESSFUL!")
        print("=" * 60)
        print()
        print("Your executable is ready:")
        print(f"  📦 Location: {os.path.join(script_dir, 'dist', 'ScreenShare_Console.exe')}")
        print()
        print("You can now:")
        print("  1. Copy ScreenShare_Console.exe to any Windows PC")
        print("  2. Run it without Python installed")
        print("  3. See console output for debugging")
        print()
        print("⚠️  IMPORTANT NOTES:")
        print("  • This version SHOWS the console window (good for debugging)")
        print("  • Use build_exe.py for a version WITHOUT console (cleaner)")
        print("  • The EXE file is quite large (~200-300 MB) due to bundled libraries")
        print("  • First run may be slow as Windows scans the file")
        print("  • Windows Defender might flag it (false positive - it's safe)")
        print("  • For web_client.html, keep it in the same folder as the EXE")
        print()
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ BUILD FAILED!")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure all dependencies are installed:")
        print("     pip install -r requirements.txt")
        print("  2. Try running as administrator")
        print("  3. Check if antivirus is blocking PyInstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
