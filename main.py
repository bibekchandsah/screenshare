import os
import sys
import threading
import webbrowser
from pathlib import Path

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
        print("  [2] Share My Screen (Web Browser - Mobile Friendly)")
        print("  [3] View Someone's Screen (Desktop App)")
        print("  [4] Start Cloudflare Tunnel (Unlimited Bandwidth)")
        print("  [5] Start ngrok Tunnel (For Internet Access)")
        print("  [6] Check ngrok Status")
        print("  [7] Setup ngrok Authtoken")
        print("  [8] Exit")
        print()
        print("-" * 60)
        print(" " * 39, end="𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓭 𝓫𝔂 𝓑𝓲𝓫𝓮𝓴...")
        print()
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            return 'server'
        elif choice == '2':
            return 'web_server'
        elif choice == '3':
            return 'client'
        elif choice == '4':
            return 'cloudflare'
        elif choice == '5':
            return 'ngrok'
        elif choice == '6':
            return 'ngrok_status'
        elif choice == '7':
            return 'ngrok_authtoken'
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

def run_ngrok():
    """Run ngrok tunnel setup"""
    clear_screen()
    print_banner()
    print("🌐 START NGROK TUNNEL")
    print("=" * 60)
    print()
    
    try:
        # Import ngrok helper
        from ngrok_helper import start_ngrok_tunnel, stop_ngrok, NGROK_AVAILABLE
        
        if not NGROK_AVAILABLE:
            print("❌ pyngrok is not installed!")
            print("\nInstall it with:")
            print("   pip install pyngrok")
            print("\nThen restart this application.")
            input("\nPress Enter to return to main menu...")
            return
        
        print("This will create an ngrok tunnel for internet access.\n")
        print("Choose tunnel type:\n")
        print("  [1] HTTP Tunnel (Port 5000) - For Web Browser Mode")
        print("  [2] TCP Tunnel (Port 5555) - For Desktop App Mode")
        print("  [3] Custom Port")
        print("  [4] Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        print()
        
        if choice == '1':
            print("[*] Starting HTTP tunnel on port 5000...")
            print("[*] This tunnel is for Web Browser Mode (Option 2 in main menu)\n")
            url = start_ngrok_tunnel(port=5000, protocol='http')
            if url:
                print("\n✅ Tunnel started successfully!")
                print("\n📝 NEXT STEPS:")
                print("   1. Keep this window open")
                print("   2. Go back to main menu")
                print("   3. Choose option [2] - Web Browser Mode")
                print("   4. Share the ngrok URL with viewers")
                print("\n[*] Press Ctrl+C to stop the tunnel and return to menu")
                try:
                    import time
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n\n[*] Stopping ngrok tunnel...")
                    stop_ngrok()
                    print("[✓] Tunnel stopped")
                    input("\nPress Enter to return to main menu...")
            else:
                print("\n❌ Failed to start ngrok tunnel!")
                print("[*] Please check the error messages above for instructions.")
                input("\nPress Enter to return to main menu...")
        
        elif choice == '2':
            print("[*] Starting TCP tunnel on port 5555...")
            print("[*] This tunnel is for Desktop App Mode (Option 1 in main menu)\n")
            url = start_ngrok_tunnel(port=5555, protocol='tcp')
            if url:
                print("\n✅ Tunnel started successfully!")
                print("\n📝 NEXT STEPS:")
                print("   1. Keep this window open")
                print("   2. Go back to main menu")
                print("   3. Choose option [1] - Desktop App Mode")
                print("   4. Share the ngrok URL with viewers")
                print("\n[*] Press Ctrl+C to stop the tunnel and return to menu")
                try:
                    import time
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n\n[*] Stopping ngrok tunnel...")
                    stop_ngrok()
                    print("[✓] Tunnel stopped")
                    input("\nPress Enter to return to main menu...")
            else:
                print("\n❌ Failed to start ngrok tunnel!")
                print("[*] Please check the error messages above for instructions.")
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            port_input = input("Enter port number: ").strip()
            protocol_input = input("Enter protocol (http/tcp): ").strip().lower()
            
            try:
                port = int(port_input)
                if protocol_input not in ['http', 'tcp']:
                    print("\n❌ Invalid protocol! Use 'http' or 'tcp'")
                    input("\nPress Enter to return to main menu...")
                    return
                
                print(f"\n[*] Starting {protocol_input.upper()} tunnel on port {port}...\n")
                url = start_ngrok_tunnel(port=port, protocol=protocol_input)
                if url:
                    print("\n✅ Tunnel started successfully!")
                    print(f"\n📝 Make sure your application is running on port {port}")
                    print("\n[*] Press Ctrl+C to stop the tunnel and return to menu")
                    try:
                        import time
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n\n[*] Stopping ngrok tunnel...")
                        stop_ngrok()
                        print("[✓] Tunnel stopped")
                        input("\nPress Enter to return to main menu...")
                else:
                    print("\n❌ Failed to start ngrok tunnel!")
                    print("[*] Please check the error messages above for instructions.")
                    input("\nPress Enter to return to main menu...")
                    
            except ValueError:
                print("\n❌ Invalid port number!")
                input("\nPress Enter to return to main menu...")
        
        elif choice == '4':
            return
        else:
            print("❌ Invalid choice!")
            input("\nPress Enter to return to main menu...")
            
    except KeyboardInterrupt:
        print("\n\n[*] Returning to main menu...")
        try:
            from ngrok_helper import stop_ngrok
            stop_ngrok()
        except:
            pass
        input("\nPress Enter to continue...")
    except ImportError as e:
        print(f"❌ Error: Could not import ngrok_helper - {e}")
        print("Make sure ngrok_helper.py exists in the same directory.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def run_ngrok_status():
    """Check ngrok tunnel status"""
    clear_screen()
    print_banner()
    print("📊 NGROK TUNNEL STATUS")
    print("=" * 60)
    print()
    
    try:
        # Import ngrok helper
        from ngrok_helper import print_ngrok_status, is_ngrok_running
        
        # Check if ngrok process is running first
        if not is_ngrok_running():
            print("ℹ️  No ngrok process is currently running")
            print("\n💡 TIP: Use option [4] from main menu to start a tunnel")
            print("\n📝 STEPS:")
            print("   1. Choose [4] from main menu")
            print("   2. Select tunnel type (HTTP or TCP)")
            print("   3. Keep that terminal open")
            print("   4. Then check status from another terminal")
        else:
            # Print detailed status
            has_tunnels = print_ngrok_status()
            
            if not has_tunnels:
                print("\n💡 If you just started a tunnel, wait a few seconds")
                print("   and try checking status again.")
        
        input("\nPress Enter to return to main menu...")
        
    except ImportError as e:
        print(f"❌ Error: Could not import ngrok_helper - {e}")
        print("Make sure ngrok_helper.py exists in the same directory.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to return to main menu...")

def run_ngrok_authtoken():
    """Setup ngrok authtoken"""
    clear_screen()
    print_banner()
    print("🔑 SETUP NGROK AUTHTOKEN")
    print("=" * 60)
    print()
    
    try:
        from ngrok_helper import setup_ngrok_authtoken
        
        print("📝 About ngrok Authtoken:")
        print("   • Free ngrok tunnels show a warning page to visitors")
        print("   • Authenticated tunnels have better reliability")
        print("   • Higher connection limits with authtoken")
        print("   • Required for advanced features")
        print()
        print("💡 How to get your authtoken:")
        print("   1. Go to: https://dashboard.ngrok.com/signup")
        print("   2. Sign up for free (or log in)")
        print("   3. Copy your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken")
        print()
        print("-" * 60)
        print()
        
        # Ask if user wants to continue
        proceed = input("Do you have your authtoken ready? (y/n): ").strip().lower()
        
        if proceed not in ['y', 'yes']:
            print("\n💡 No problem! Come back when you have your authtoken.")
            print("   You can get it from: https://dashboard.ngrok.com/get-started/your-authtoken")
            input("\nPress Enter to return to main menu...")
            return
        
        print()
        authtoken = input("Enter your ngrok authtoken: ").strip()
        
        if not authtoken:
            print("\n❌ Authtoken cannot be empty!")
            input("\nPress Enter to return to main menu...")
            return
        
        print()
        print("[*] Setting up authtoken...")
        
        # Call the setup function
        success = setup_ngrok_authtoken(authtoken)
        
        if success:
            print("\n✅ Authtoken configured successfully!")
            print("\n📝 WHAT'S NEXT:")
            print("   • Your authtoken is saved")
            print("   • Future ngrok tunnels will use this authtoken automatically")
            print("   • You can now use option [4] to start tunnels")
            print("   • No more warning pages for visitors!")
        else:
            print("\n❌ Failed to configure authtoken!")
            print("   Please check the error message above and try again.")
        
        input("\nPress Enter to return to main menu...")
        
    except ImportError as e:
        print(f"❌ Error: Could not import ngrok_helper - {e}")
        print("Make sure ngrok_helper.py exists in the same directory.")
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
            elif choice == 'client':
                run_client()
            elif choice == 'cloudflare':
                run_cloudflare()
            elif choice == 'ngrok':
                run_ngrok()
            elif choice == 'ngrok_status':
                run_ngrok_status()
            elif choice == 'ngrok_authtoken':
                run_ngrok_authtoken()
                
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        exit_app()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
