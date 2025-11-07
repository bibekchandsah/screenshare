import os
import sys
import threading
import webbrowser
from pathlib import Path

# Try to import clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# Try to import pystray for system tray support
try:
    import pystray
    from PIL import Image
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("⚠️  Note: pystray not installed. System tray feature disabled.")
    print("   Install with: pip install pystray pillow")
    print()

# Global variables for tray control
tray_icon = None
console_visible = True
app_running = True

def copy_to_clipboard(text, description="text"):
    """Copy text to clipboard with user feedback"""
    if CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(text)
            print(f"📋 {description} copied to clipboard!")
            return True
        except Exception as e:
            print(f"⚠️  Could not copy {description} to clipboard: {e}")
            return False
    else:
        print(f"⚠️  Clipboard not available. Install pyperclip with: pip install pyperclip")
        return False

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def hide_console():
    """Hide the console window (Windows only)"""
    global console_visible
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        console_visible = False
        print("[*] Console hidden - Access via system tray icon")

def show_console():
    """Show the console window (Windows only)"""
    global console_visible
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        console_visible = True
        print("[*] Console visible")

def toggle_console():
    """Toggle console visibility"""
    if console_visible:
        hide_console()
    else:
        show_console()

def restart_app():
    """Restart the application"""
    print("\n[*] Restarting application...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def open_developer_website(icon=None, item=None):
    """Open developer website in browser"""
    try:
        webbrowser.open("https://www.bibekchandsah.com.np/")
        print("[*] Opening developer website...")
    except Exception as e:
        print(f"⚠️  Could not open website: {e}")

def open_contribute_page(icon=None, item=None):
    """Open GitHub repository in browser"""
    try:
        webbrowser.open("https://github.com/bibekchandsah/screenshare")
        print("[*] Opening GitHub repository...")
    except Exception as e:
        print(f"⚠️  Could not open repository: {e}")

def exit_app(icon=None, item=None):
    """Exit the application"""
    global app_running, tray_icon
    print("\n[*] Shutting down...")
    app_running = False
    
    # Stop tray icon if it's running
    if icon:
        # Called from tray menu - stop the icon
        icon.stop()
    elif tray_icon:
        # Called from elsewhere - stop global tray icon
        tray_icon.stop()
    
    # Use os._exit to avoid SystemExit exception in callback
    # This cleanly terminates the process without raising exceptions
    os._exit(0)

def create_tray_icon():
    """Create system tray icon with menu"""
    global tray_icon
    
    if not TRAY_AVAILABLE:
        return None
    
    # Try to load icon.ico
    icon_path = Path(__file__).parent / "icon.ico"
    
    try:
        if icon_path.exists():
            image = Image.open(str(icon_path))
        else:
            # Create a simple colored square as fallback
            from PIL import ImageDraw
            image = Image.new('RGB', (64, 64), color=(33, 150, 243))
            draw = ImageDraw.Draw(image)
            draw.rectangle([10, 10, 54, 54], fill=(255, 255, 255))
            draw.text((20, 20), "SS", fill=(33, 150, 243))
    except Exception as e:
        print(f"⚠️  Could not load icon: {e}")
        # Create a simple fallback icon
        from PIL import ImageDraw
        image = Image.new('RGB', (64, 64), color=(33, 150, 243))
        draw = ImageDraw.Draw(image)
        draw.rectangle([10, 10, 54, 54], fill=(255, 255, 255))
    
    # Create menu items with proper text handling
    def get_toggle_text(item):
        return 'Show Window' if not console_visible else 'Hide Window'
    
    # Create menu
    menu = pystray.Menu(
        pystray.MenuItem(
            get_toggle_text,
            toggle_console,
            default=True
        ),
        pystray.MenuItem('Restart', restart_app),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Developer', open_developer_website),
        pystray.MenuItem('Contribute', open_contribute_page),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Exit', exit_app)
    )
    
    # Create icon
    icon = pystray.Icon("ScreenShare", image, "Screen Share App", menu)
    
    return icon

def run_tray_icon():
    """Run the system tray icon in background"""
    global tray_icon
    
    if not TRAY_AVAILABLE:
        return
    
    try:
        tray_icon = create_tray_icon()
        if tray_icon:
            print("\n✅ System tray icon created!")
            print("   • Right-click the tray icon for menu")
            print("   • Show/Hide window, Restart, or Exit\n")
            # Run in background thread
            tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
            tray_thread.start()
    except Exception as e:
        print(f"\n⚠️  Could not create system tray icon: {e}")
        print("   Application will continue without tray support.\n")

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print(" " * 15 + "SCREEN SHARING APPLICATION")
    print("=" * 60)
    if TRAY_AVAILABLE and os.name != 'nt':
        print(" " * 10 + "📌 System Tray not available: Right-click icon for menu")
        print("=" * 60)
    print()

def main_menu():
    """Display main menu and get user choice"""
    while True:
        clear_screen()
        print_banner()
        
        print("Choose an option:\n")
        print("  [1] Share My Screen (Desktop App)")
        print("  [2] View Someone's Screen (Desktop App)")
        print("  [3] Share My Screen (Web Browser - Mobile Friendly)")
        print("  [4] Start Cloudflare Tunnel (Unlimited Bandwidth)")
        print("  [5] Share My Screen via Cloudflare Tunnel (Merged)")
        print("  [6] Share My Screen (Trusted Mode - No Security Code)")
        print("  [7] Share My Screen Trusted Mode via Cloudflare Tunnel (Merged)")
        print("  [8] Exit")
        print()
        print("-" * 60)
        print(" " * 39, end="𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓭 𝓫𝔂 𝓑𝓲𝓫𝓮𝓴...")
        print()
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            return 'server'
        elif choice == '2':
            return 'client'
        elif choice == '3':
            return 'web_server'
        elif choice == '4':
            return 'cloudflare'
        elif choice == '5':
            return 'cloudflare_merged'
        elif choice == '6':
            return 'web_server_trusted'
        elif choice == '7':
            return 'cloudflare_trusted_merged'
        elif choice == '8':
            # Confirm before exiting
            print()
            confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                print("\nGoodbye! 👋")
                sys.exit(0)
            # If 'no', loop continues and menu is shown again
        else:
            print("\n❌ Invalid choice! Please enter 1-8.")
            input("Press Enter to continue...")

def run_server():
    """Run the server (share screen) module"""
    clear_screen()
    print_banner()
    print("🖥️  SHARE MY SCREEN MODE")
    print("=" * 60)
    print()
    
    try:
        # Import and run server
        from server import ScreenShareServer
        
        server = ScreenShareServer()
        print("[*] Press Ctrl+C to stop sharing\n")
        server.start_sharing()
        
    except KeyboardInterrupt:
        print("\n\n[!] Sharing stopped by user")
        # Confirm before returning to menu
        print()
        input("Press Enter to return to main menu...")
    except ImportError as e:
        print(f"❌ Error: Could not import server module - {e}")
        print("Make sure server.py exists in the same directory.")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to continue...")

def run_client():
    """Run the client (view screen) module"""
    clear_screen()
    print_banner()
    print("👀 VIEW SOMEONE'S SCREEN MODE")
    print("=" * 60)
    print()
    
    try:
        # Import and run client
        from client import ScreenShareClient
        
        # Get connection details from user
        host = input("Enter server IP address (or 'localhost' for same PC): ").strip()
        if not host:
            host = 'localhost'
        
        port_input = input("Enter server port (default: 5555): ").strip()
        port = int(port_input) if port_input else 5555
        
        security_code = input("Enter the security code: ").strip().upper()
        
        if not security_code:
            print("❌ Security code is required!")
            input("\nPress Enter to return to main menu...")
            return
        
        print()
        print("-" * 60)
        
        # Create client and connect
        client = ScreenShareClient()
        
        if client.connect_to_server(host, port, security_code):
            client.receive_frames()
        else:
            print("❌ Failed to connect to server")
        
        input("\nPress Enter to return to main menu...")
            
    except KeyboardInterrupt:
        print("\n\n[!] Viewing stopped by user")
        input("\nPress Enter to return to main menu...")
    except ValueError:
        print("❌ Error: Invalid port number")
        input("\nPress Enter to return to main menu...")
    except ImportError as e:
        print(f"❌ Error: Could not import client module - {e}")
        print("Make sure client.py exists in the same directory.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def run_web_server():
    """Run the web server (browser-based screen sharing)"""
    clear_screen()
    print_banner()
    print("🌐 WEB BROWSER SCREEN SHARE MODE")
    print("=" * 60)
    print()
    
    try:
        # Import and run web server
        from web_server import ScreenShareWebServer
        
        server = ScreenShareWebServer()
        print("[*] This mode is mobile-friendly!")
        print("[*] You can view the screen from any device with a web browser\n")
        server.start_sharing()
        
    except KeyboardInterrupt:
        print("\n\n[!] Web server stopped by user")
        input("\nPress Enter to return to main menu...")
    except ImportError as e:
        print(f"❌ Error: Could not import web server module - {e}")
        print("Make sure web_server.py exists in the same directory.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def run_web_server_trusted():
    """Run the trusted web server (browser-based screen sharing without security code)"""
    clear_screen()
    print_banner()
    print("🌐 TRUSTED WEB BROWSER SCREEN SHARE MODE")
    print("=" * 60)
    print()
    
    try:
        # Import and run trusted web server
        from web_server_trusted import TrustedScreenShareWebServer
        
        server = TrustedScreenShareWebServer()
        print("⚠️  TRUSTED MODE - No security code required!")
        print("[*] All connections will be automatically accepted")
        print("[*] This mode is mobile-friendly!")
        print("[*] You can view the screen from any device with a web browser")
        print("[*] 📝 Connection details will be logged for your reference\n")
        server.start_sharing()
        
    except KeyboardInterrupt:
        print("\n\n[!] Trusted web server stopped by user")
        input("\nPress Enter to return to main menu...")
    except ImportError as e:
        print(f"❌ Error: Could not import trusted web server module - {e}")
        print("Make sure web_server_trusted.py exists in the same directory.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def run_cloudflare():
    """Run Cloudflare tunnel setup"""
    clear_screen()
    print_banner()
    print("🌐 LAUNCHING CLOUDFLARE TUNNEL")
    print("=" * 60)
    print()
    
    try:
        # Import cloudflare helper
        import subprocess
        import os
        import sys
        
        # When running as PyInstaller executable, check the temporary directory
        if getattr(sys, 'frozen', False):
            # Running as executable - files are in sys._MEIPASS
            bundle_dir = sys._MEIPASS
            cloudflare_helper_path = os.path.join(bundle_dir, 'cloudflare_helper.py')
        else:
            # Running as script - files are in current directory
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
            cloudflare_helper_path = os.path.join(bundle_dir, 'cloudflare_helper.py')
        
        # Check if cloudflare_helper.py exists
        if not os.path.exists(cloudflare_helper_path):
            print("❌ cloudflare_helper.py not found!")
            print(f"\nSearched in: {cloudflare_helper_path}")
            print("\nThis might be a build issue. Try rebuilding the executable with:")
            print("  python build_console_exe.py")
            input("\nPress Enter to return to main menu...")
            return
        
        print("[*] Starting Cloudflare Tunnel Helper...")
        print("[*] ♾️  Unlimited bandwidth • � Multiple users • ⚡ Enterprise performance")
        print()
        
        # Run cloudflare_helper.py directly
        try:
            # For PyInstaller executable, run the bundled cloudflare_helper
            if getattr(sys, 'frozen', False):
                # We need to run the helper directly since it's bundled
                # Import and run the main function
                sys.path.insert(0, bundle_dir)
                import cloudflare_helper
                cloudflare_helper.main()
            else:
                # Running as script, use subprocess
                subprocess.run([sys.executable, cloudflare_helper_path], check=True)
        except subprocess.CalledProcessError:
            print("\n⚠️  Cloudflare helper exited")
        except KeyboardInterrupt:
            print("\n\n[*] Returned from Cloudflare helper")
        except Exception as e:
            print(f"\n❌ Error running Cloudflare helper: {e}")
        
        input("\nPress Enter to return to main menu...")
        
    except ImportError as e:
        print(f"❌ Error: Import error - {e}")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def run_cloudflare_merged():
    """Run Cloudflare tunnel and then start web server in the same terminal"""
    clear_screen()
    print_banner()
    print("🌐 CLOUDFLARE TUNNEL + SCREEN SHARE (MERGED)")
    print("=" * 60)
    print()
    
    try:
        # Import required modules
        import subprocess
        import os
        import sys
        import time
        import threading
        from web_server import ScreenShareWebServer
        
        # Step 1: Start Cloudflare tunnel for Web Mode (port 5000)
        print("🚀 STEP 1: Starting Cloudflare Tunnel...")
        print("=" * 50)
        print()
        
        # When running as PyInstaller executable, check the temporary directory
        if getattr(sys, 'frozen', False):
            # Running as executable - files are in sys._MEIPASS
            bundle_dir = sys._MEIPASS
            cloudflare_helper_path = os.path.join(bundle_dir, 'cloudflare_helper.py')
        else:
            # Running as script - files are in current directory
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
            cloudflare_helper_path = os.path.join(bundle_dir, 'cloudflare_helper.py')
        
        # Check if cloudflare_helper.py exists
        if not os.path.exists(cloudflare_helper_path):
            print("❌ cloudflare_helper.py not found!")
            print(f"\nSearched in: {cloudflare_helper_path}")
            input("\nPress Enter to return to main menu...")
            return
        
        # Start Cloudflare tunnel programmatically
        print("[*] Setting up Cloudflare tunnel for Web Mode (Port 5000)...")
        
        # Import cloudflare helper functions directly
        try:
            if getattr(sys, 'frozen', False):
                sys.path.insert(0, bundle_dir)
            
            from cloudflare_helper import start_cloudflare_tunnel, check_cloudflared_installed
            
            # First check if cloudflared is available
            print("[*] Checking for cloudflared...")
            cloudflared_available, cloudflared_cmd = check_cloudflared_installed()
            
            if not cloudflared_available:
                print("❌ cloudflared not found!")
                print("Please make sure cloudflared.exe is available.")
                input("\nPress Enter to return to main menu...")
                return
            
            print(f"✅ Using cloudflared: {cloudflared_cmd}")
            print()
            
            # Start tunnel for web mode (port 5000)
            success, tunnel_url, tunnel_process = start_cloudflare_tunnel(
                port=5000, 
                protocol='http', 
                cloudflared_cmd=cloudflared_cmd
            )
            
            if success and tunnel_url:
                print(f"\n✅ CLOUDFLARE TUNNEL ACTIVE!")
                print(f"🌐 Public URL: {tunnel_url}")
                print(f"📡 Local: localhost:5000")
                
                # Copy URL to clipboard
                copy_to_clipboard(tunnel_url, "Cloudflare URL")
                
                print()
                print("-" * 50)
                print()
                
                # Step 2: Start web server
                print("🖥️  STEP 2: Starting Screen Share Server...")
                print("=" * 50)
                print()
                
                server = ScreenShareWebServer()
                print(f"[*] Screen share server starting on port 5000...")
                print(f"[*] Cloudflare tunnel URL: {tunnel_url}")
                print(f"[*] This mode is mobile-friendly!")
                print()
                
                # Display combined information
                print("🎯 READY TO SHARE!")
                print("=" * 50)
                print(f"🌐 Share this URL: {tunnel_url}")
                print("🔐 Security code will be shown below...")
                print("🚀 Unlimited bandwidth via Cloudflare!")
                print("=" * 50)
                print()
                
                # Start the web server
                server.start_sharing()

                # Prompt to copy security code to clipboard
                security_code = getattr(server, 'security_code', None)
                if security_code:
                    user_input = input("\nPress C to copy the security code to clipboard, or any other key to skip: ").strip().lower()
                    if user_input == 'c':
                        copy_to_clipboard(security_code, "Security code")
                        print("[✓] Security code copied to clipboard!")
                    else:
                        print("[!] Security code not copied. You can copy it manually above.")
                
            else:
                print("❌ Failed to start Cloudflare tunnel")
                input("\nPress Enter to return to main menu...")
                return
                
        except ImportError as e:
            print(f"❌ Error importing cloudflare_helper: {e}")
            input("\nPress Enter to return to main menu...")
            return
        except Exception as e:
            print(f"❌ Error starting Cloudflare tunnel: {e}")
            input("\nPress Enter to return to main menu...")
            return
        
    except KeyboardInterrupt:
        print("\n\n[!] Merged session stopped by user")
        input("\nPress Enter to return to main menu...")
    except ImportError as e:
        print(f"❌ Error: Could not import required modules - {e}")
        print("Make sure web_server.py and cloudflare_helper.py exist in the same directory.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def run_cloudflare_trusted_merged():
    """Run Cloudflare tunnel and then start trusted web server in the same terminal"""
    clear_screen()
    print_banner()
    print("🌐 CLOUDFLARE TUNNEL + TRUSTED SCREEN SHARE (MERGED)")
    print("=" * 60)
    print()
    
    try:
        # Import required modules
        import subprocess
        import threading
        import time
        import sys
        import os
        from web_server_trusted import TrustedScreenShareWebServer
        
        # Step 1: Start Cloudflare tunnel for Web Mode (port 5000)
        print("🚀 STEP 1: Starting Cloudflare Tunnel...")
        print("=" * 50)
        print()
        
        # When running as PyInstaller executable, check the temporary directory
        if getattr(sys, 'frozen', False):
            # Running as executable - files are in sys._MEIPASS
            bundle_dir = sys._MEIPASS
            cloudflare_helper_path = os.path.join(bundle_dir, 'cloudflare_helper.py')
        else:
            # Running as script - files are in current directory
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
            cloudflare_helper_path = os.path.join(bundle_dir, 'cloudflare_helper.py')
        
        # Check if cloudflare_helper.py exists
        if not os.path.exists(cloudflare_helper_path):
            print("❌ cloudflare_helper.py not found!")
            print(f"\nSearched in: {cloudflare_helper_path}")
            input("\nPress Enter to return to main menu...")
            return
        
        # Start Cloudflare tunnel programmatically
        print("[*] Setting up Cloudflare tunnel for Trusted Web Mode (Port 5000)...")
        
        # Import cloudflare helper functions directly
        try:
            if getattr(sys, 'frozen', False):
                sys.path.insert(0, bundle_dir)
            
            from cloudflare_helper import start_cloudflare_tunnel, check_cloudflared_installed
            
            # First check if cloudflared is available
            print("[*] Checking for cloudflared...")
            cloudflared_available, cloudflared_cmd = check_cloudflared_installed()
            
            if not cloudflared_available:
                print("❌ cloudflared not found!")
                print("Please make sure cloudflared.exe is available.")
                input("\nPress Enter to return to main menu...")
                return
            
            print(f"✅ Using cloudflared: {cloudflared_cmd}")
            print()
            
            # Start tunnel for web mode (port 5000)
            success, tunnel_url, tunnel_process = start_cloudflare_tunnel(
                port=5000, 
                protocol='http', 
                cloudflared_cmd=cloudflared_cmd
            )
            
            if success and tunnel_url:
                print(f"\n✅ CLOUDFLARE TUNNEL ACTIVE!")
                print(f"🌐 Public URL: {tunnel_url}")
                print(f"📡 Local: localhost:5000")
                
                # Copy URL to clipboard
                copy_to_clipboard(tunnel_url, "Cloudflare URL")
                
                print()
                print("-" * 50)
                print()
                
                # Step 2: Start trusted web server
                print("🖥️  STEP 2: Starting Trusted Screen Share Server...")
                print("=" * 50)
                print()
                
                server = TrustedScreenShareWebServer()
                print(f"[*] Trusted screen share server starting on port 5000...")
                print(f"[*] Cloudflare tunnel URL: {tunnel_url}")
                print(f"[*] This mode is mobile-friendly!")
                print()
                
                # Display combined information
                print("🎯 READY TO SHARE! (TRUSTED MODE)")
                print("=" * 50)
                print(f"🌐 Share this URL: {tunnel_url}")
                print("⚠️  TRUSTED MODE - No security code required!")
                print("🔓 All connections will be automatically accepted")
                print("🚀 Unlimited bandwidth via Cloudflare!")
                print("📝 Connection details will be logged for your reference")
                print("=" * 50)
                print()
                
                # Start the trusted web server
                server.start_sharing()
                
            else:
                print("❌ Failed to start Cloudflare tunnel")
                input("\nPress Enter to return to main menu...")
                return
                
        except ImportError as e:
            print(f"❌ Error importing cloudflare_helper: {e}")
            input("\nPress Enter to return to main menu...")
            return
        except Exception as e:
            print(f"❌ Error starting Cloudflare tunnel: {e}")
            input("\nPress Enter to return to main menu...")
            return
        
    except KeyboardInterrupt:
        print("\n\n[!] Trusted merged session stopped by user")
        input("\nPress Enter to return to main menu...")
    except ImportError as e:
        print(f"❌ Error: Could not import required modules - {e}")
        print("Make sure web_server_trusted.py and cloudflare_helper.py exist in the same directory.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def main():
    """Main application entry point"""
    global app_running
    
    # Initialize system tray icon
    if TRAY_AVAILABLE and os.name == 'nt':
        print("\n" + "="*60)
        print("🎯 Initializing system tray icon...")
        run_tray_icon()
        import time
        time.sleep(1)  # Give tray time to initialize
        print("="*60 + "\n")
    
    try:
        while app_running:
            choice = main_menu()
            
            if choice == 'server':
                run_server()
            elif choice == 'web_server':
                run_web_server()
            elif choice == 'web_server_trusted':
                run_web_server_trusted()
            elif choice == 'client':
                run_client()
            elif choice == 'cloudflare':
                run_cloudflare()
            elif choice == 'cloudflare_merged':
                run_cloudflare_merged()
            elif choice == 'cloudflare_trusted_merged':
                run_cloudflare_trusted_merged()
                
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        exit_app()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
