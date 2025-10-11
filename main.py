import os
import sys

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print(" " * 15 + "SCREEN SHARING APPLICATION")
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
        print("  [4] Exit")
        print()
        print("-" * 60)
        
        choice = input("\nEnter your choice (1/2/3/4): ").strip()
        
        if choice == '1':
            return 'server'
        elif choice == '2':
            return 'web_server'
        elif choice == '3':
            return 'client'
        elif choice == '4':
            # Confirm before exiting
            print()
            confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                print("\nGoodbye! 👋")
                sys.exit(0)
            # If 'no', loop continues and menu is shown again
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, 3, or 4.")
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

def main():
    """Main application entry point"""
    try:
        while True:
            choice = main_menu()
            
            if choice == 'server':
                run_server()
            elif choice == 'web_server':
                run_web_server()
            elif choice == 'client':
                run_client()
                
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
