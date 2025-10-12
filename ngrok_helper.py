"""
ngrok Integration Helper for Screen Share Application

This script automatically starts ngrok tunnel when you start screen sharing,
making it easy to share your screen with users on different networks.

Installation:
    pip install pyngrok

Usage:
    python ngrok_helper.py

Or integrate with main application by importing this module.
"""

import sys
import time

try:
    from pyngrok import ngrok, conf
    NGROK_AVAILABLE = True
except ImportError:
    NGROK_AVAILABLE = False
    print("\n" + "="*60)
    print("[!] pyngrok is not installed!")
    print("[!] Install it with: pip install pyngrok")
    print("="*60 + "\n")

def start_ngrok_tunnel(port=8080, protocol='http', region='us'):
    """
    Start an ngrok tunnel for the given port
    
    Args:
        port (int): Local port to tunnel (default: 8080)
        protocol (str): Protocol type - 'http' or 'tcp' (default: 'http')
        region (str): ngrok region - 'us', 'eu', 'ap', 'au', 'sa', 'jp', 'in' (default: 'us')
    
    Returns:
        str: Public URL for the tunnel, or None if failed
    """
    if not NGROK_AVAILABLE:
        print("[!] Cannot start ngrok - pyngrok not installed")
        return None
    
    try:
        # Configure ngrok region for better performance
        conf.get_default().region = region
        
        # Start tunnel
        print(f"\n[*] Starting ngrok tunnel for {protocol}://localhost:{port}...")
        print(f"[*] Region: {region}")
        
        if protocol == 'http':
            tunnel = ngrok.connect(port, "http")
        elif protocol == 'tcp':
            tunnel = ngrok.connect(port, "tcp")
        else:
            print(f"[!] Unsupported protocol: {protocol}")
            return None
        
        public_url = tunnel.public_url
        
        print("\n" + "="*60)
        print("✅ ngrok TUNNEL ACTIVE!")
        print("="*60)
        print(f"📍 Public URL: {public_url}")
        print(f"🔗 Local URL:  {protocol}://localhost:{port}")
        print("="*60)
        print("\n👥 SHARE THIS WITH VIEWERS:")
        print(f"   URL: {public_url}")
        print("   (They'll need the security code from your screen share)")
        print("\n⚠️  IMPORTANT - First Time Users:")
        print("   1. ngrok shows a warning page first (anti-phishing protection)")
        print("   2. Click 'Visit Site' button to continue to screen share")
        print("   3. This is normal for ngrok's free tier")
        print("\n⚠️  OTHER NOTES:")
        print("   - Keep this terminal open while sharing")
        print("   - URL changes each time you restart")
        print("   - Free tier has connection limits")
        print("   - To skip warning page: Upgrade to ngrok paid plan")
        print("="*60 + "\n")
        
        return public_url
        
    except Exception as e:
        print(f"\n[!] Failed to start ngrok tunnel: {e}")
        print("\n💡 TIPS:")
        print("   1. Check if ngrok is installed: pip install pyngrok")
        print("   2. If you need auth token: ngrok config add-authtoken YOUR_TOKEN")
        print("   3. Get free token at: https://dashboard.ngrok.com/signup")
        print("   4. Check ngrok status at: https://status.ngrok.com/")
        return None

def stop_ngrok():
    """Stop all ngrok tunnels"""
    if NGROK_AVAILABLE:
        try:
            ngrok.kill()
            print("\n[*] ngrok tunnels stopped")
        except Exception as e:
            print(f"\n[!] Error stopping ngrok: {e}")

def get_ngrok_tunnels():
    """Get list of active ngrok tunnels"""
    if NGROK_AVAILABLE:
        try:
            tunnels = ngrok.get_tunnels()
            return tunnels
        except Exception as e:
            print(f"[!] Error getting tunnels: {e}")
            return []
    return []

def print_ngrok_status():
    """Print status of all active ngrok tunnels"""
    if not NGROK_AVAILABLE:
        print("[!] pyngrok not available")
        return
    
    tunnels = get_ngrok_tunnels()
    
    if not tunnels:
        print("\n[*] No active ngrok tunnels")
        return
    
    print("\n" + "="*60)
    print("ACTIVE NGROK TUNNELS")
    print("="*60)
    for tunnel in tunnels:
        print(f"Name:   {tunnel.name}")
        print(f"Public: {tunnel.public_url}")
        print(f"Local:  {tunnel.config['addr']}")
        print("-" * 60)
    print("="*60 + "\n")

def setup_ngrok_authtoken():
    """Interactive setup for ngrok authtoken"""
    print("\n" + "="*60)
    print("NGROK AUTHENTICATION SETUP")
    print("="*60)
    print("\n1. Go to: https://dashboard.ngrok.com/signup")
    print("2. Sign up for free account")
    print("3. Copy your authtoken from the dashboard")
    print("4. Paste it below\n")
    
    token = input("Enter your ngrok authtoken (or press Enter to skip): ").strip()
    
    if token:
        try:
            conf.get_default().auth_token = token
            ngrok.set_auth_token(token)
            print("\n✅ Authtoken configured successfully!")
            print("   You can now use ngrok tunnels\n")
            return True
        except Exception as e:
            print(f"\n❌ Failed to configure authtoken: {e}\n")
            return False
    else:
        print("\n[*] Skipped authtoken setup")
        print("   You may need to configure it later for full access\n")
        return False

def main():
    """Main function for standalone usage"""
    print("\n" + "="*60)
    print("        NGROK HELPER FOR SCREEN SHARE")
    print("="*60)
    
    if not NGROK_AVAILABLE:
        print("\n❌ pyngrok is not installed!")
        print("\nInstall it with:")
        print("   pip install pyngrok")
        print("\nThen run this script again.")
        return
    
    print("\nThis helper will create an ngrok tunnel for your screen share.")
    print("\nChoose your screen share mode:")
    print("  [1] Web Browser Mode (HTTP, Port 8080) - Recommended")
    print("  [2] Desktop Mode (TCP, Port 5555)")
    print("  [3] Custom Port")
    print("  [4] Check ngrok Status")
    print("  [5] Setup ngrok Authtoken")
    print("  [6] Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == '1':
        print("\n[*] Selected: Web Browser Mode (Port 8080)")
        print("[*] Starting ngrok HTTP tunnel...")
        url = start_ngrok_tunnel(port=8080, protocol='http')
        if url:
            print("\n✅ Ready! Now start your screen share server:")
            print("   python main.py")
            print("   Choose option 2 (Web Browser - Mobile Friendly)")
            print("\n[*] Press Ctrl+C to stop ngrok")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n[*] Stopping ngrok...")
                stop_ngrok()
                print("[*] Goodbye!")
    
    elif choice == '2':
        print("\n[*] Selected: Desktop Mode (Port 5555)")
        print("[*] Starting ngrok TCP tunnel...")
        url = start_ngrok_tunnel(port=5555, protocol='tcp')
        if url:
            print("\n✅ Ready! Now start your screen share server:")
            print("   python main.py")
            print("   Choose option 1 (Desktop Mode)")
            print("\n[*] Press Ctrl+C to stop ngrok")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n[*] Stopping ngrok...")
                stop_ngrok()
                print("[*] Goodbye!")
    
    elif choice == '3':
        port = input("Enter port number: ").strip()
        protocol = input("Enter protocol (http/tcp): ").strip().lower()
        try:
            port = int(port)
            url = start_ngrok_tunnel(port=port, protocol=protocol)
            if url:
                print("\n[*] Press Ctrl+C to stop ngrok")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n\n[*] Stopping ngrok...")
                    stop_ngrok()
                    print("[*] Goodbye!")
        except ValueError:
            print("[!] Invalid port number")
    
    elif choice == '4':
        print_ngrok_status()
    
    elif choice == '5':
        setup_ngrok_authtoken()
    
    elif choice == '6':
        print("\n[*] Goodbye!")
        return
    
    else:
        print("\n[!] Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user")
        stop_ngrok()
    except Exception as e:
        print(f"\n[!] Error: {e}")
