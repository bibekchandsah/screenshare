# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['mss', 'mss.windows', 'mss.linux', 'mss.darwin', 'PIL', 'PIL._imagingtk', 'PIL._tkinter_finder', 'cv2', 'flask', 'flask_cors', 'pyngrok', 'requests', 'threading', 'socket', 'json', 'base64', 'io', 'time', 'datetime']
hiddenimports += collect_submodules('mss')
hiddenimports += collect_submodules('flask')
hiddenimports += collect_submodules('cv2')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('cloudflared.exe', '.'), ('ngrok.exe', '.')],
    datas=[('server.py', '.'), ('client.py', '.'), ('web_server.py', '.'), ('ngrok_helper.py', '.'), ('cloudflare_helper.py', '.'), ('web_client.html', '.'), ('icon.ico', '.'), ('icon.png', '.')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'tkinter', '_tkinter', 'matplotlib'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ScreenShare_Console',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
