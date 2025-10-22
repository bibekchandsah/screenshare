"""
Simple test script to verify system tray icon functionality
"""
import sys
import os
import webbrowser
from pathlib import Path

# Try to import required libraries
try:
    import pystray
    from PIL import Image, ImageDraw
    print("✅ pystray and PIL imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Install with: pip install pystray pillow")
    sys.exit(1)

def test_icon_creation():
    """Test creating a system tray icon"""
    print("\n🔍 Testing icon creation...")
    
    # Try to load icon.ico
    icon_path = Path(__file__).parent / "icon.ico"
    
    if icon_path.exists():
        print(f"✅ Found icon.ico at: {icon_path}")
        try:
            image = Image.open(str(icon_path))
            print(f"✅ Loaded icon.ico successfully (size: {image.size})")
        except Exception as e:
            print(f"⚠️  Could not load icon.ico: {e}")
            image = create_fallback_icon()
    else:
        print(f"⚠️  icon.ico not found at: {icon_path}")
        print("   Creating fallback icon...")
        image = create_fallback_icon()
    
    return image

def create_fallback_icon():
    """Create a simple fallback icon"""
    image = Image.new('RGB', (64, 64), color=(33, 150, 243))
    draw = ImageDraw.Draw(image)
    draw.rectangle([10, 10, 54, 54], fill=(255, 255, 255))
    draw.text((20, 20), "SS", fill=(33, 150, 243))
    print("✅ Created fallback icon")
    return image

def on_quit(icon, item):
    """Quit the application"""
    print("\n👋 Exiting...")
    icon.stop()
    # Use os._exit to avoid SystemExit exception in callback
    os._exit(0)

def on_show(icon, item):
    """Show a message"""
    print("📌 Show clicked!")

def on_developer(icon, item):
    """Open developer website"""
    print("📌 Opening developer website...")
    try:
        webbrowser.open("https://www.bibekchandsah.com.np/")
    except Exception as e:
        print(f"⚠️  Error: {e}")

def on_contribute(icon, item):
    """Open GitHub repository"""
    print("📌 Opening GitHub repository...")
    try:
        webbrowser.open("https://github.com/bibekchandsah/screenshare")
    except Exception as e:
        print(f"⚠️  Error: {e}")

def test_menu_creation():
    """Test creating the menu"""
    print("\n🔍 Testing menu creation...")
    
    try:
        menu = pystray.Menu(
            pystray.MenuItem('Show', on_show, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Developer', on_developer),
            pystray.MenuItem('Contribute', on_contribute),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', on_quit)
        )
        print("✅ Menu created successfully")
        return menu
    except Exception as e:
        print(f"❌ Error creating menu: {e}")
        return None

def main():
    """Main test function"""
    print("="*60)
    print("       SYSTEM TRAY ICON TEST")
    print("="*60)
    
    # Test icon creation
    image = test_icon_creation()
    
    # Test menu creation
    menu = test_menu_creation()
    
    if not menu:
        print("\n❌ Menu creation failed. Exiting.")
        sys.exit(1)
    
    # Create the tray icon
    print("\n🔍 Creating system tray icon...")
    try:
        icon = pystray.Icon("TestTray", image, "Test System Tray", menu)
        print("✅ System tray icon object created")
        
        print("\n" + "="*60)
        print("📌 Look for the tray icon in your taskbar!")
        print("   • Right-click it to see the menu")
        print("   • Click 'Exit' to close this test")
        print("="*60 + "\n")
        
        # Run the icon (this blocks until icon.stop() is called)
        icon.run()
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error running tray icon: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
