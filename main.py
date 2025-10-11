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
        print("  [1] Share My Screen (Server)")
        print("  [2] View Someone's Screen (Client)")
        print("  [3] Exit")
        print()
        print("-" * 60)
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == '1':
            return 'server'
        elif choice == '2':
            return 'client'
        elif choice == '3':
            print("\nGoodbye! 👋")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, or 3.")
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
        server.start_sharing()
        
    except KeyboardInterrupt:
        print("\n\n[!] Sharing stopped by user")
    except ImportError as e:
        print(f"❌ Error: Could not import server module - {e}")
        print("Make sure server.py exists in the same directory.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("\nReturning to main menu...")
        input("Press Enter to continue...")

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
            
    except KeyboardInterrupt:
        print("\n\n[!] Viewing stopped by user")
    except ValueError:
        print("❌ Error: Invalid port number")
    except ImportError as e:
        print(f"❌ Error: Could not import client module - {e}")
        print("Make sure client.py exists in the same directory.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("\nReturning to main menu...")
        input("Press Enter to continue...")

def main():
    """Main application entry point"""
    try:
        while True:
            choice = main_menu()
            
            if choice == 'server':
                run_server()
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
