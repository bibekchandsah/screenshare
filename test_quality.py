#!/usr/bin/env python3
"""Test script for web server quality functionality"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from web_server import ScreenShareWebServer
    print("✅ Web server imports successfully")
    
    # Test quality settings
    server = ScreenShareWebServer()
    print(f"✅ Default quality: {server.current_quality}")
    print(f"✅ Available qualities: {list(server.quality_settings.keys())}")
    
    # Test quality config
    for quality in server.quality_settings:
        config = server.quality_settings[quality]
        print(f"   {quality}: Scale {config['scale']}%, JPEG {config['jpeg_quality']}%")
        
    print("✅ Quality system ready!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()