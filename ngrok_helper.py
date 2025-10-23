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
import subprocess
import os

try:
    from pyngrok import ngrok, conf
    NGROK_AVAILABLE = True
except ImportError:
    NGROK_AVAILABLE = False
    print("\n" + "="*60)
    print("[!] pyngrok is not installed!")
    print("[!] Install it with: pip install pyngrok")
    print("="*60 + "\n")

def kill_existing_ngrok():
    """Kill any existing ngrok processes"""
    try:
        print("[*] Checking for existing ngrok processes...")
        if sys.platform == 'win32':
            # Windows
            result = subprocess.run(
                ['taskkill', '/F', '/IM', 'ngrok.exe'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("[✓] Stopped existing ngrok process")
            else:
                print("[✓] No existing ngrok process found")
        else:
            # Linux/Mac
            result = subprocess.run(
                ['pkill', 'ngrok'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("[✓] Stopped existing ngrok process")
            else:
                print("[✓] No existing ngrok process found")
        
        # Wait for process to fully terminate
        time.sleep(1)
        
    except Exception as e:
        print(f"[!] Could not check for existing ngrok: {e}")
        print("[*] Continuing anyway...")

def start_ngrok_tunnel(port=5000, protocol='http', region='us'):
    """
    Start an ngrok tunnel for the given port
    
    Args:
        port (int): Local port to tunnel (default: 5000)
        protocol (str): Protocol type - 'http' or 'tcp' (default: 'http')
        region (str): ngrok region - 'us', 'eu', 'ap', 'au', 'sa', 'jp', 'in' (default: 'us')
    
    Returns:
        str: Public URL for the tunnel, or None if failed
    """
    if not NGROK_AVAILABLE:
        print("[!] Cannot start ngrok - pyngrok not installed")
        return None
    
    try:
        # Kill any existing ngrok processes first
        kill_existing_ngrok()
        
        # Also disconnect any existing tunnels through pyngrok
        try:
            ngrok.kill()
            time.sleep(0.5)
        except:
            pass
        
        # Configure pyngrok to use system's ngrok if available, or download without SSL verification
        try:
            pyngrok_config = conf.get_default()
            pyngrok_config.region = region
            
            # Set download timeout and disable SSL verification for download
            pyngrok_config.ngrok_download_timeout = 60
            
            # Try to use system ngrok first if available
            system_ngrok = None
            if sys.platform == 'win32':
                # Check PyInstaller bundled location first, then common Windows paths
                possible_paths = []
                
                # Add current directory (where main exe is located)
                possible_paths.append(os.path.join(os.getcwd(), 'ngrok.exe'))
                
                # Add PyInstaller temp directory if available
                if hasattr(sys, '_MEIPASS'):
                    print(f"[DEBUG] PyInstaller temp dir: {sys._MEIPASS}")
                    possible_paths.append(os.path.join(sys._MEIPASS, 'ngrok.exe'))
                
                # Add script directory
                script_dir = os.path.dirname(os.path.abspath(__file__))
                possible_paths.append(os.path.join(script_dir, 'ngrok.exe'))
                
                # Add traditional system paths
                possible_paths.extend([
                    os.path.expanduser('~\\ngrok.exe'),
                    'C:\\ngrok\\ngrok.exe',
                    'C:\\Program Files\\ngrok\\ngrok.exe',
                ])
                
                print(f"[DEBUG] Searching for ngrok in directories: {[os.path.dirname(p) for p in possible_paths[:3]]}")
                
                for path in possible_paths:
                    if os.path.exists(path):
                        system_ngrok = path
                        print(f"[✓] ngrok found at: {system_ngrok}")
                        break
            
            if system_ngrok:
                print(f"[✓] Using system ngrok at: {system_ngrok}")
                pyngrok_config.ngrok_path = system_ngrok
        except Exception as e:
            print(f"[!] Warning during config: {e}")
            print("[*] Continuing with default configuration...")
        
        # Start tunnel
        print(f"\n[*] Starting ngrok tunnel for {protocol}://localhost:{port}...")
        print(f"[*] Region: {region}")
        print("[*] Downloading ngrok...")
        
        if protocol == 'http':
            tunnel = ngrok.connect(port, "http")
        elif protocol == 'tcp':
            tunnel = ngrok.connect(port, "tcp")
        else:
            print(f"[!] Unsupported protocol: {protocol}")
            return None
        
        public_url = tunnel.public_url
        
        # Get local IP address
        import socket
        try:
            # Get the local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "your-local-ip"
        
        print("\n" + "="*60)
        print("✅ ngrok TUNNEL ACTIVE!")
        print("="*60)
        print(f"📍 Public URL: {public_url}")
        print(f"🔗 Local URLs:")
        print(f"   - http://localhost:{port} (this machine)")
        print(f"   - http://{local_ip}:{port} (LAN access)")
        print(f"\n💡 NOTE: ngrok tunnels to port {port} on ALL network interfaces")
        print(f"   Both localhost and {local_ip} are tunneled")
        print("="*60)
        print("\n👥 SHARE THIS WITH VIEWERS:")
        print(f"   Public URL: {public_url}")
        print("   (They'll need the security code from your screen share)")
        print("\n📱 FOR LOCAL NETWORK (Same WiFi):")
        print(f"   LAN URL: http://{local_ip}:{port}")
        print("   (No ngrok needed for same network)")
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
        error_msg = str(e)
        print(f"\n[!] Failed to start ngrok tunnel: {error_msg}")
        
        # Check for SSL certificate error
        if "CERTIFICATE_VERIFY_FAILED" in error_msg or "SSL" in error_msg:
            print("\n⚠️  SSL CERTIFICATE ERROR DETECTED!")
            print("   This happens when downloading ngrok for the first time.")
            print("\n💡 SOLUTION - Download ngrok manually:")
            print("\n   STEP 1: Download ngrok")
            print("   -------")
            print("   1. Go to: https://ngrok.com/download")
            print("   2. Download Windows version (64-bit)")
            print("   3. Extract ngrok.exe from the zip file")
            print("\n   STEP 2: Install ngrok")
            print("   -------")
            print("   Option A (Easy):")
            print("   • Place ngrok.exe in your user folder:")
            print(f"     {os.path.expanduser('~')}\\ngrok.exe")
            print("\n   Option B (System-wide):")
            print("   • Create folder: C:\\ngrok")
            print("   • Place ngrok.exe there: C:\\ngrok\\ngrok.exe")
            print("   • Add to PATH: C:\\ngrok")
            print("\n   STEP 3: Setup ngrok (Optional but recommended)")
            print("   -------")
            print("   1. Sign up at: https://dashboard.ngrok.com/signup")
            print("   2. Get your authtoken")
            print("   3. Run in PowerShell:")
            print("      ngrok config add-authtoken YOUR_TOKEN_HERE")
            print("\n   STEP 4: Try again")
            print("   -------")
            print("   • After installing ngrok.exe, run this program again")
            print("   • The tunnel should start without downloading")
            print("\n⚠️  QUICK FIX (Temporary):")
            print("   You can also try:")
            print("   1. Update Python certificates:")
            print("      pip install --upgrade certifi")
            print("   2. Reinstall pyngrok:")
            print("      pip uninstall pyngrok")
            print("      pip install pyngrok")
            print("="*60)
            
            # Wait for user to read the instructions
            input("\n⏸️  Press Enter after reading these instructions...")
            
        # Check if it's the "already online" error
        elif "already online" in error_msg or "ERR_NGROK_334" in error_msg:
            print("\n⚠️  ENDPOINT CONFLICT DETECTED!")
            print("   An ngrok tunnel with this endpoint is already running.")
            print("\n💡 SOLUTIONS:")
            print("   1. Wait a moment and try again (automatic cleanup may need more time)")
            print("   2. Manually kill ngrok:")
            if sys.platform == 'win32':
                print("      Windows: taskkill /F /IM ngrok.exe")
            else:
                print("      Linux/Mac: pkill ngrok")
            print("   3. Or run this script again (it will auto-cleanup)")
            
            # Wait for user to read the instructions
            input("\n⏸️  Press Enter after reading these instructions...")
            
        else:
            print("\n💡 TIPS:")
            print("   1. Check if ngrok is installed: pip install pyngrok")
            print("   2. If you need auth token: ngrok config add-authtoken YOUR_TOKEN")
            print("   3. Get free token at: https://dashboard.ngrok.com/signup")
            print("   4. Check ngrok status at: https://status.ngrok.com/")
            
            # Wait for user to read the tips
            input("\n⏸️  Press Enter to return to menu...")
            
        return None

def stop_ngrok():
    """Stop all ngrok tunnels"""
    print("[*] Stopping all ngrok tunnels...")
    
    # Stop via pyngrok
    if NGROK_AVAILABLE:
        try:
            ngrok.kill()
            print("[✓] Stopped pyngrok tunnels")
        except Exception as e:
            print(f"[!] Error stopping pyngrok: {e}")
    
    # Also kill any ngrok processes
    kill_existing_ngrok()
    
    print("[✓] All ngrok processes stopped")

def get_ngrok_tunnels():
    """Get list of active ngrok tunnels from web API (works across processes)"""
    try:
        import requests
        import json
        
        # Try different ngrok web interface ports
        ports = [4040, 4041, 4042, 4043]
        
        for port in ports:
            try:
                response = requests.get(f'http://127.0.0.1:{port}/api/tunnels', timeout=1)
                if response.status_code == 200:
                    data = response.json()
                    tunnels = data.get('tunnels', [])
                    if tunnels:
                        return tunnels, port
            except:
                continue
        
        return [], None
        
    except ImportError:
        # Fallback to pyngrok method (only works for same process)
        if NGROK_AVAILABLE:
            try:
                tunnels = ngrok.get_tunnels()
                return tunnels, None
            except Exception as e:
                return [], None
        return [], None
    except Exception as e:
        return [], None

def is_ngrok_running():
    """Check if ngrok process is running"""
    try:
        if sys.platform == 'win32':
            # Windows
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq ngrok.exe'],
                capture_output=True,
                text=True
            )
            return 'ngrok.exe' in result.stdout
        else:
            # Linux/Mac
            result = subprocess.run(
                ['pgrep', 'ngrok'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
    except:
        return False

def print_ngrok_status():
    """Print status of all active ngrok tunnels (works across processes)"""
    
    # First check if ngrok process is running
    if not is_ngrok_running():
        print("\n[*] No ngrok process found")
        print("\n💡 TIP: Start a tunnel with option [4] from main menu")
        return False
    
    # Get tunnels from web API
    tunnels, port = get_ngrok_tunnels()
    
    if not tunnels:
        print("\n[*] ngrok is running but no tunnels are active")
        print("    This might mean:")
        print("    - Tunnel is starting up (wait a moment)")
        print("    - ngrok process is stuck (restart recommended)")
        return False
    
    print("\n" + "="*60)
    print("✅ ACTIVE NGROK TUNNELS")
    print("="*60)
    
    for tunnel in tunnels:
        # Handle both API response format and pyngrok object format
        if isinstance(tunnel, dict):
            # API response format
            name = tunnel.get('name', 'N/A')
            public_url = tunnel.get('public_url', 'N/A')
            config = tunnel.get('config', {})
            local_addr = config.get('addr', 'N/A')
            proto = tunnel.get('proto', 'N/A')
            
            print(f"Name:     {name}")
            print(f"Protocol: {proto}")
            print(f"Public:   {public_url}")
            print(f"Local:    {local_addr}")
        else:
            # pyngrok object format
            print(f"Name:     {tunnel.name}")
            print(f"Public:   {tunnel.public_url}")
            print(f"Local:    {tunnel.config['addr']}")
        
        print("-" * 60)
    
    if port:
        print(f"\n💡 Web Interface: http://127.0.0.1:{port}")
    print("="*60 + "\n")
    return True

def setup_ngrok_authtoken(authtoken=None):
    """
    Interactive setup for ngrok authtoken
    
    Args:
        authtoken (str, optional): The authtoken to configure. If None, will prompt user.
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not NGROK_AVAILABLE:
        print("[!] pyngrok is not installed!")
        print("    Install it with: pip install pyngrok")
        return False
    
    # If no authtoken provided, prompt user
    if authtoken is None:
        print("\n" + "="*60)
        print("NGROK AUTHENTICATION SETUP")
        print("="*60)
        print("\n1. Go to: https://dashboard.ngrok.com/signup")
        print("2. Sign up for free account")
        print("3. Copy your authtoken from the dashboard")
        print("4. Paste it below\n")
        
        authtoken = input("Enter your ngrok authtoken (or press Enter to skip): ").strip()
    
    if not authtoken:
        print("\n[*] Skipped authtoken setup")
        print("   You may need to configure it later for full access\n")
        return False
    
    # Basic validation: Check authtoken format
    # ngrok authtokens are typically long alphanumeric strings with underscores
    if len(authtoken) < 20:
        print("\n❌ Invalid authtoken format!")
        print("   Authtokens are usually long strings (40+ characters)")
        print("   Example format: 2abc...XYZ_123...789")
        print("\n💡 Get your real authtoken from:")
        print("   https://dashboard.ngrok.com/get-started/your-authtoken")
        return False
    
    try:
        # Method 1: Try using ngrok CLI directly (most reliable)
        ngrok_exe = None
        try:
            # Find ngrok executable
            ngrok_paths = []
            
            if sys.platform == 'win32':
                # Check PyInstaller bundled location first, then common paths
                # Add current directory (where main exe is located)
                ngrok_paths.append(os.path.join(os.getcwd(), 'ngrok.exe'))
                
                # Add PyInstaller temp directory if available
                if hasattr(sys, '_MEIPASS'):
                    ngrok_paths.append(os.path.join(sys._MEIPASS, 'ngrok.exe'))
                
                # Add script directory
                script_dir = os.path.dirname(os.path.abspath(__file__))
                ngrok_paths.append(os.path.join(script_dir, 'ngrok.exe'))
                
                # Add traditional system paths
                ngrok_paths.extend([
                    os.path.join(os.path.expanduser('~'), 'ngrok.exe'),
                    'C:\\ngrok\\ngrok.exe',
                ])
            else:
                ngrok_paths = [
                    '/usr/local/bin/ngrok',
                    '/usr/bin/ngrok',
                    os.path.join(os.path.expanduser('~'), 'ngrok'),
                ]
            
            # Also check pyngrok's ngrok path
            try:
                pyngrok_config = conf.get_default()
                if pyngrok_config.ngrok_path and os.path.exists(pyngrok_config.ngrok_path):
                    ngrok_paths.insert(0, pyngrok_config.ngrok_path)
            except:
                pass
            
            ngrok_exe = None
            for path in ngrok_paths:
                if os.path.exists(path):
                    ngrok_exe = path
                    break
            
            if ngrok_exe:
                # Use ngrok CLI to set authtoken
                result = subprocess.run(
                    [ngrok_exe, 'config', 'add-authtoken', authtoken],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"[✓] Authtoken saved to configuration")
                    
                    # REAL VALIDATION: Test the authtoken by starting ngrok
                    print("[*] Validating authtoken with ngrok servers...")
                    print("    (This will take a few seconds...)")
                    
                    try:
                        # Start ngrok with a test tunnel to verify authtoken
                        # Use ngrok start with --none to just test authentication without creating tunnels
                        validation_process = subprocess.Popen(
                            [ngrok_exe, 'http', '0', '--log=stdout', '--log-level=info'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        
                        # Wait up to 10 seconds for ngrok to authenticate
                        validation_output = ""
                        validation_error = ""
                        authenticated = False
                        auth_failed = False
                        
                        import threading
                        
                        def read_output():
                            nonlocal validation_output, authenticated, auth_failed
                            try:
                                for line in validation_process.stdout:
                                    validation_output += line
                                    # Look for success indicators
                                    if any(keyword in line.lower() for keyword in ['established', 'tunnel established', 'session established']):
                                        authenticated = True
                                        break
                                    # Look for authentication errors
                                    if any(keyword in line.lower() for keyword in ['authentication failed', 'invalid authtoken', 'err_ngrok_105', 'unauthorized']):
                                        auth_failed = True
                                        break
                            except:
                                pass
                        
                        # Start reading output in background
                        output_thread = threading.Thread(target=read_output, daemon=True)
                        output_thread.start()
                        
                        # Wait up to 10 seconds
                        output_thread.join(timeout=10)
                        
                        # Kill the validation process
                        try:
                            validation_process.terminate()
                            validation_process.wait(timeout=2)
                        except:
                            validation_process.kill()
                        
                        # Check results
                        if auth_failed:
                            print("\n❌ Authtoken validation FAILED!")
                            print("   ngrok servers rejected this authtoken.")
                            print("\n💡 This means:")
                            print("   • The authtoken is incorrect or invalid")
                            print("   • You may have copied it incorrectly")
                            print("   • The token might be expired (rare)")
                            print("\n🔗 Get your REAL authtoken from:")
                            print("   https://dashboard.ngrok.com/get-started/your-authtoken")
                            print("\n📝 Make sure to:")
                            print("   1. Copy the ENTIRE token (it's very long)")
                            print("   2. Don't add any extra spaces")
                            print("   3. Paste it exactly as shown")
                            return False
                        
                        elif authenticated:
                            print("[✓] Authtoken validated with ngrok servers!")
                            print("    ✅ Authentication successful!")
                            return True
                        
                        else:
                            # Timeout or unclear result - be cautious
                            print("\n⚠️  Could not validate authtoken (timeout/network issue)")
                            print("   The authtoken was saved, but validation timed out.")
                            print("\n💡 Possible reasons:")
                            print("   • Network connectivity issues")
                            print("   • Firewall blocking ngrok")
                            print("   • ngrok service temporarily unavailable")
                            print("\n🔄 Next steps:")
                            print("   1. Try using option [4] to start a tunnel")
                            print("   2. If tunnel fails, the authtoken might be invalid")
                            print("   3. Come back to option [6] to re-configure")
                            return False  # Return False to be safe
                            
                    except Exception as validation_error:
                        print(f"\n⚠️  Validation error: {validation_error}")
                        print("   Authtoken saved but couldn't validate.")
                        return False
                
                else:
                    error_msg = result.stderr.strip()
                    if "invalid" in error_msg.lower() or "authentication" in error_msg.lower():
                        print(f"\n❌ Invalid authtoken!")
                        print(f"   Error: {error_msg}")
                        print("\n💡 Please check:")
                        print("   1. Did you copy the FULL authtoken from the dashboard?")
                        print("   2. Get your real authtoken from:")
                        print("      https://dashboard.ngrok.com/get-started/your-authtoken")
                        return False
                    else:
                        print(f"[!] ngrok CLI returned error: {error_msg}")
                        # Fall through to try pyngrok method
            else:
                print("[!] ngrok executable not found, trying pyngrok method...")
                # Fall through to try pyngrok method
        
        except Exception as e:
            print(f"[!] Error using ngrok CLI: {e}")
            print("[*] Trying alternative method...")
        
        # Method 2: Use pyngrok's set_auth_token (fallback)
        try:
            print("[*] Configuring authtoken via pyngrok...")
            ngrok.set_auth_token(authtoken)
            pyngrok_config = conf.get_default()
            pyngrok_config.auth_token = authtoken
            print("[✓] Authtoken saved to pyngrok configuration")
            
            # REAL VALIDATION: Test the authtoken with ngrok API
            print("[*] Validating authtoken with ngrok servers...")
            print("    (This will take a few seconds...)")
            
            try:
                # Kill any existing ngrok processes first
                try:
                    ngrok.kill()
                    time.sleep(0.5)
                except:
                    pass
                
                # Try to create a quick tunnel to test the authtoken
                # This makes a real API call to ngrok servers
                test_tunnel = ngrok.connect(0, bind_tls=True)  # Port 0 = random available port
                
                # If we got here without exception, authtoken is valid!
                print("[✓] Authtoken validated with ngrok servers!")
                print("    ✅ Authentication successful!")
                
                # Immediately disconnect the test tunnel
                try:
                    ngrok.disconnect(test_tunnel.public_url)
                    time.sleep(0.5)
                    ngrok.kill()
                except:
                    pass
                
                return True
                
            except Exception as validation_error:
                error_msg = str(validation_error).lower()
                
                # Check for authentication/authorization errors
                if any(keyword in error_msg for keyword in [
                    'authentication failed',
                    'invalid authtoken', 
                    'authtoken',
                    'unauthorized',
                    'forbidden',
                    'err_ngrok_105',
                    'does not look like a proper',
                    'authentication'
                ]):
                    print("\n❌ Authtoken validation FAILED!")
                    print("   ngrok servers rejected this authtoken.")
                    print(f"\n   Error details: {validation_error}")
                    print("\n💡 This means:")
                    print("   • The authtoken is incorrect or invalid")
                    print("   • You may have copied it incorrectly")
                    print("   • The token might be expired or revoked")
                    print("\n🔗 Get your REAL authtoken from:")
                    print("   https://dashboard.ngrok.com/get-started/your-authtoken")
                    print("\n📝 Make sure to:")
                    print("   1. Copy the ENTIRE token (it's very long)")
                    print("   2. Don't add any extra spaces")
                    print("   3. Paste it exactly as shown")
                    
                    # Clean up
                    try:
                        ngrok.kill()
                    except:
                        pass
                    
                    return False
                else:
                    # Other error - might be network or ngrok service issue
                    print(f"\n⚠️  Validation error: {validation_error}")
                    print("\n💡 Possible reasons:")
                    print("   • Network connectivity issues")
                    print("   • Firewall blocking ngrok")
                    print("   • ngrok service temporarily unavailable")
                    print("\n🔄 The authtoken was saved, but we couldn't verify it.")
                    print("   Try using option [4] to test if tunnels work.")
                    
                    # Clean up
                    try:
                        ngrok.kill()
                    except:
                        pass
                    
                    return False  # Return False to be safe
            
        except Exception as e:
            error_msg = str(e).lower()
            if any(keyword in error_msg for keyword in ['invalid', 'authenticate', 'authorization', 'authtoken']):
                print(f"\n❌ Invalid authtoken: {e}")
                print("\n� Get your real authtoken from:")
                print("   https://dashboard.ngrok.com/get-started/your-authtoken")
                return False
            else:
                print(f"[!] pyngrok method failed: {e}")
                return False
            
    except Exception as e:
        print(f"\n❌ Failed to configure authtoken: {e}\n")
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
    print("  [1] Web Browser Mode (HTTP, Port 5000) - Recommended")
    print("  [2] Desktop Mode (TCP, Port 5555)")
    print("  [3] Custom Port")
    print("  [4] Check ngrok Status")
    print("  [5] Setup ngrok Authtoken")
    print("  [6] Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == '1':
        print("\n[*] Selected: Web Browser Mode (Port 5000)")
        print("[*] Starting ngrok HTTP tunnel...")
        url = start_ngrok_tunnel(port=5000, protocol='http')
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
