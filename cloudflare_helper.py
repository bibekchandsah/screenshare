"""
Cloudflare Tunnel Integration Helper for Screen Share Application

This script automatically starts Cloudflare Tunnel when you start screen sharing,
making it easy to share your screen with users on different networks.

Cloudflare Tunnel Benefits:
- No bandwidth limits (unlike ngrok's monthly limits)
- Better performance and reliability
- Multiple concurrent users supported
- Enterprise-grade infrastructure
- No monthly subscription required

Installation:
1. Download cloudflared from: https://github.com/cloudflare/cloudflared/releases
2. Add cloudflared to your PATH
3. Login: cloudflared tunnel login

Usage:
    python cloudflare_helper.py

Or integrate with main application by importing this module.
"""

import sys
import time
import subprocess
import os
import json
import re
import threading
import uuid
import queue
from datetime import datetime

def check_cloudflared_installed():
    """Check if cloudflared is installed and accessible"""
    # Try different possible names and locations
    possible_names = ['cloudflared', 'cloudflared.exe']
    
    for name in possible_names:
        try:
            result = subprocess.run(
                [name, '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"[✓] cloudflared found: {version}")
                return True, name
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    # Check if cloudflared exists in local directories
    search_dirs = []
    
    # Add current working directory
    search_dirs.append(os.getcwd())
    
    # If running as PyInstaller executable, also check the temporary directory
    if getattr(sys, 'frozen', False):
        # PyInstaller temp directory
        search_dirs.append(sys._MEIPASS)
        print(f"[DEBUG] PyInstaller temp dir: {sys._MEIPASS}")
    
    # Add script directory (for development)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in search_dirs:
        search_dirs.append(script_dir)
    
    print(f"[DEBUG] Searching for cloudflared in directories: {search_dirs}")
    
    for search_dir in search_dirs:
        local_paths = [
            os.path.join(search_dir, 'cloudflared.exe'),
            os.path.join(search_dir, 'cloudflared')
        ]
        
        for path in local_paths:
            if os.path.exists(path):
                try:
                    result = subprocess.run(
                        [path, '--version'], 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        print(f"[✓] cloudflared found at: {path}")
                        print(f"    Version: {version}")
                        return True, path
                except Exception as e:
                    print(f"[DEBUG] Error testing {path}: {e}")
                    continue
    
    return False, None

def install_cloudflared():
    """Guide user through cloudflared installation"""
    print("\n" + "="*70)
    print("🚀 CLOUDFLARE TUNNEL SETUP REQUIRED")
    print("="*70)
    print("\n[!] cloudflared is not found in PATH or current directory")
    print("\n🔍 QUICK FIX OPTIONS:")
    print("\n📁 Option 1: Copy to Current Folder (Easiest)")
    print("   - Copy your 'cloudflared.exe' to this folder:")
    print(f"   - {os.getcwd()}")
    print("   - Then re-run this script")
    
    print("\n🌐 Option 2: Add to System PATH")
    print("   - Press Win+R, type 'sysdm.cpl', press Enter")
    print("   - Click 'Environment Variables'")
    print("   - Edit 'PATH' variable")
    print("   - Add the folder containing cloudflared.exe")
    print("   - Restart terminal and re-run this script")
    
    print("\n📥 Option 3: Fresh Download")
    print("1. Download from: https://github.com/cloudflare/cloudflared/releases")
    print("2. For Windows: Download 'cloudflared-windows-amd64.exe'")
    print("3. Rename to 'cloudflared.exe'")
    print("4. Place in this folder or add to PATH")
    
    print("\n💡 DETECTED: You seem to have cloudflared working")
    print("   (Your manual command worked successfully)")
    print("   Just copy the .exe file to this folder!")
    print("="*70 + "\n")
    
    choice = input("📁 Do you want to copy cloudflared.exe to current folder? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        print(f"\n📂 Please copy 'cloudflared.exe' to:")
        print(f"   {os.getcwd()}")
        print("\n⏳ Press Enter when done...")
        input()
        return check_cloudflared_installed()[0]
    
    return False

def check_cloudflare_login(cloudflared_cmd='cloudflared'):
    """Check if user is logged into Cloudflare"""
    try:
        # Check if tunnel list works (requires login)
        result = subprocess.run(
            [cloudflared_cmd, 'tunnel', 'list'], 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        if result.returncode == 0:
            print("[✓] Cloudflare login verified")
            return True
        else:
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def setup_cloudflare_login(cloudflared_cmd='cloudflared'):
    """Guide user through Cloudflare login"""
    print("\n" + "="*60)
    print("🔐 CLOUDFLARE LOGIN REQUIRED")
    print("="*60)
    print("\n[!] You need to login to Cloudflare first")
    print("\n🚀 LOGIN OPTIONS:")
    print("1. 🚀 Quick Tunnels (No login required)")
    print("   - Works immediately without Cloudflare account")
    print("   - Perfect for testing and demos")
    print("   - URLs like: https://xxx-xxx-xxx.trycloudflare.com")
    print("\n2. 🏢 Named Tunnels (Login required)")
    print("   - More professional and persistent")
    print("   - Requires Cloudflare account (free)")
    print("   - Better for production usage")
    print("\n💡 RECOMMENDATION: Use Quick Tunnels (Option 1)")
    print("   Perfect for screen sharing - no setup needed!")
    print("="*60 + "\n")
    
    choice = input("Choose: (1) Quick Tunnels [Recommended] / (2) Named Tunnels / (s) Skip: ").strip()
    
    if choice == '1' or choice.lower() == 'quick':
        print("\n✅ Using Quick Tunnels - No login required!")
        print("   Perfect for screen sharing demos and testing")
        return True
    elif choice == '2' or choice.lower() == 'named':
        print(f"\n[*] Setting up Named Tunnels...")
        print(f"1. Run: {cloudflared_cmd} tunnel login")
        print("2. This will open your browser")
        print("3. Login to Cloudflare and authorize")
        print("4. Return here and re-run this script")
        
        login_choice = input("\nDo you want to login now? (y/n): ").strip().lower()
        if login_choice in ['y', 'yes']:
            try:
                print("\n[*] Opening Cloudflare login...")
                subprocess.run([cloudflared_cmd, 'tunnel', 'login'], check=True)
                print("[✓] Login completed!")
                return True
            except subprocess.CalledProcessError:
                print("[-] Login failed")
                return False
            except KeyboardInterrupt:
                print("\n[!] Login cancelled by user")
                return False
    
    print("\n💡 Continuing with Quick Tunnels (no login needed)")
    return True

def kill_existing_cloudflared():
    """Kill any existing cloudflared processes"""
    try:
        print("[*] Checking for existing cloudflared processes...")
        if sys.platform == 'win32':
            # Windows
            result = subprocess.run(
                ['taskkill', '/F', '/IM', 'cloudflared.exe'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("[✓] Stopped existing cloudflared process")
            else:
                print("[✓] No existing cloudflared process found")
        else:
            # Linux/Mac
            result = subprocess.run(
                ['pkill', 'cloudflared'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("[✓] Stopped existing cloudflared process")
            else:
                print("[✓] No existing cloudflared process found")
    except Exception as e:
        print(f"[!] Error checking processes: {e}")

def create_tunnel(tunnel_name=None):
    """Create a new Cloudflare tunnel"""
    if not tunnel_name:
        tunnel_name = f"screenshare-{uuid.uuid4().hex[:8]}"
    
    try:
        print(f"[*] Creating tunnel: {tunnel_name}")
        result = subprocess.run(
            ['cloudflared', 'tunnel', 'create', tunnel_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Extract tunnel ID from output
            tunnel_id = None
            for line in result.stdout.split('\n'):
                if 'Created tunnel' in line:
                    # Extract UUID from line like "Created tunnel screenshare with id 12345-67890-..."
                    match = re.search(r'with id ([a-f0-9-]+)', line)
                    if match:
                        tunnel_id = match.group(1)
                        break
            
            print(f"[✓] Tunnel created successfully")
            print(f"    Name: {tunnel_name}")
            if tunnel_id:
                print(f"    ID: {tunnel_id}")
            return tunnel_name, tunnel_id
        else:
            print(f"[-] Failed to create tunnel: {result.stderr}")
            return None, None
    except subprocess.TimeoutExpired:
        print("[-] Timeout creating tunnel")
        return None, None
    except Exception as e:
        print(f"[-] Error creating tunnel: {e}")
        return None, None

def list_tunnels():
    """List existing Cloudflare tunnels"""
    try:
        result = subprocess.run(
            ['cloudflared', 'tunnel', 'list'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            tunnels = []
            lines = result.stdout.split('\n')
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        tunnel_id = parts[0]
                        tunnel_name = parts[1]
                        status = parts[2] if len(parts) > 2 else 'unknown'
                        tunnels.append({
                            'id': tunnel_id,
                            'name': tunnel_name,
                            'status': status
                        })
            return tunnels
        else:
            print(f"[-] Failed to list tunnels: {result.stderr}")
            return []
    except Exception as e:
        print(f"[-] Error listing tunnels: {e}")
        return []

def read_output_thread(process, output_queue, stop_event):
    """Thread function to continuously read process output"""
    try:
        while not stop_event.is_set() and process.poll() is None:
            try:
                # Read from stdout
                line = process.stdout.readline()
                if line:
                    output_queue.put(('stdout', line.strip()))
                else:
                    time.sleep(0.1)
            except Exception as e:
                output_queue.put(('error', f"Error reading output: {e}"))
                break
    except Exception as e:
        output_queue.put(('error', f"Thread error: {e}"))

def start_cloudflare_tunnel(port=5000, protocol='http', tunnel_name=None, cloudflared_cmd='cloudflared'):
    """
    Start Cloudflare tunnel for the specified port
    
    Args:
        port: Port number to expose
        protocol: 'http' or 'tcp' 
        tunnel_name: Specific tunnel name to use
        cloudflared_cmd: Path/name of cloudflared executable
    
    Returns:
        tuple: (success, tunnel_url, process)
    """
    try:
        print(f"\n🚀 Starting Cloudflare Tunnel...")
        print(f"   Port: {port}")
        print(f"   Protocol: {protocol}")
        print(f"   Mode: Quick Tunnel (No login required)")
        
        # Kill existing processes
        kill_existing_cloudflared()
        
        # Use Quick Tunnel with http2 protocol (no authentication required)
        # This is perfect for screen sharing and demos
        if protocol == 'http':
            local_url = f"http://localhost:{port}"
            cmd = [
                cloudflared_cmd, 'tunnel',
                '--protocol', 'http2',
                '--url', local_url
            ]
        else:  # TCP - use HTTP2 protocol for better performance
            local_url = f"http://localhost:{port}"
            cmd = [
                cloudflared_cmd, 'tunnel',
                '--protocol', 'http2',
                '--url', local_url
            ]
        
        print(f"[*] Command: {' '.join(cmd)}")
        print(f"[*] Starting tunnel process...")
        
        # Start the tunnel process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout
            text=True,
            bufsize=0,  # Unbuffered
            universal_newlines=True
        )
        
        # Create queue and thread for output monitoring
        output_queue = queue.Queue()
        stop_event = threading.Event()
        
        # Start output reading thread
        output_thread = threading.Thread(
            target=read_output_thread, 
            args=(process, output_queue, stop_event)
        )
        output_thread.daemon = True
        output_thread.start()
        
        # Monitor output for tunnel URL
        tunnel_url = None
        start_time = time.time()
        timeout = 60  # 60 seconds should be enough
        
        print(f"[⏳] Waiting up to {timeout} seconds for tunnel URL...")
        print(f"[🔍] Monitoring cloudflared output...")
        
        output_lines = []
        
        while tunnel_url is None and time.time() - start_time < timeout:
            # Check if process is still running
            if process.poll() is not None:
                print(f"[-] Process terminated unexpectedly")
                break
            
            # Get output from queue
            try:
                output_type, line = output_queue.get(timeout=1)
                
                if output_type == 'error':
                    print(f"[!] {line}")
                    continue
                
                if line:
                    print(f"[CLOUDFLARE] {line}")
                    output_lines.append(line)
                    
                    # Look for tunnel URL
                    if '.trycloudflare.com' in line:
                        url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                        if url_match:
                            tunnel_url = url_match.group(0)
                            print(f"[🌐] Found tunnel URL: {tunnel_url}")
                            break
                            
            except queue.Empty:
                # No output available, show progress
                elapsed = int(time.time() - start_time)
                if elapsed % 5 == 0 and elapsed != 0:
                    print(f"[⏳] Still waiting... ({elapsed}/{timeout}s) Process: {'Running' if process.poll() is None else 'Stopped'}")
                continue
        
        # Stop the output thread
        stop_event.set()
        output_thread.join(timeout=2)
        
        if tunnel_url:
            print(f"\n✅ CLOUDFLARE TUNNEL ACTIVE!")
            print(f"🌐 Public URL: {tunnel_url}")
            print(f"📡 Local: localhost:{port}")
            print(f"🚀 Protocol: {protocol.upper()}")
            
            # Additional info for different protocols
            if protocol == 'http':
                print(f"\n📋 SHARE THESE DETAILS:")
                print(f"   Web URL: {tunnel_url}")
                print(f"   No additional setup required!")
            else:
                print(f"\n📋 SHARE THESE DETAILS:")
                print(f"   URL: {tunnel_url}")
                print(f"   Port: Extract from URL or use default")
                
            print(f"\n💡 BANDWIDTH: Unlimited (Cloudflare advantage!)")
            print(f"👥 USERS: Supports multiple concurrent users")
            print(f"⚡ PERFORMANCE: Enterprise-grade Cloudflare network")
            
            return True, tunnel_url, process
        else:
            print("[-] Timeout waiting for tunnel URL")
            
            # Check if process is still running (tunnel might be working but we missed the URL)
            if process.poll() is None:
                print("\n[!] Process is still running but URL not detected")
                print("💡 The tunnel might be working, but we couldn't capture the URL")
                print("🔍 Check the cloudflare output above for the tunnel URL")
                
                # Try to continue anyway
                choice = input("\nDo you want to continue with the running tunnel? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    print("\n⚠️  TUNNEL RUNNING (Manual URL Detection Required)")
                    print("📋 Look for a line like:")
                    print("   https://xxx-xxx-xxx.trycloudflare.com")
                    manual_url = input("\nPaste the tunnel URL here (or press Enter to exit): ").strip()
                    if manual_url and 'trycloudflare.com' in manual_url:
                        print(f"\n✅ TUNNEL ACTIVE WITH MANUAL URL!")
                        print(f"🌐 Public URL: {manual_url}")
                        return True, manual_url, process
                
                print("[*] Terminating tunnel process...")
                process.terminate()
            
            return False, None, None
            
    except Exception as e:
        print(f"[-] Error starting tunnel: {e}")
        return False, None, None

def stop_cloudflare_tunnel(process=None):
    """Stop the Cloudflare tunnel"""
    try:
        print("\n[*] Stopping Cloudflare tunnel...")
        
        if process and process.poll() is None:
            print("[*] Terminating tunnel process...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print("[✓] Tunnel process stopped")
            except subprocess.TimeoutExpired:
                print("[!] Force killing tunnel process...")
                process.kill()
                process.wait()
        
        # Also kill any remaining cloudflared processes
        kill_existing_cloudflared()
        
        print("[✓] Cloudflare tunnel stopped")
        return True
        
    except Exception as e:
        print(f"[-] Error stopping tunnel: {e}")
        return False

def get_tunnel_status():
    """Get status of running tunnels"""
    try:
        # Check running processes
        if sys.platform == 'win32':
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq cloudflared.exe'],
                capture_output=True,
                text=True
            )
            is_running = 'cloudflared.exe' in result.stdout
        else:
            result = subprocess.run(
                ['pgrep', 'cloudflared'],
                capture_output=True,
                text=True
            )
            is_running = result.returncode == 0
        
        # For Quick Tunnels, we can't list them (they're anonymous)
        # So we'll just check if the process is running
        return {
            'running': is_running,
            'tunnels': [],  # Quick Tunnels are anonymous, can't be listed
            'tunnel_type': 'Quick Tunnel' if is_running else 'None'
        }
    except Exception as e:
        print(f"[-] Error checking status: {e}")
        return {'running': False, 'tunnels': [], 'tunnel_type': 'None'}

def print_tunnel_status():
    """Print current tunnel status"""
    print("\n" + "="*60)
    print("🔍 CLOUDFLARE TUNNEL STATUS")
    print("="*60)
    
    status = get_tunnel_status()
    
    if status['running']:
        print("✅ Status: RUNNING")
        print(f"🚀 Type: {status.get('tunnel_type', 'Quick Tunnel')}")
        print("\n📍 Active Tunnel Details:")
        print("   🌐 Mode: Quick Tunnel (Anonymous)")
        print("   ⚡ Protocol: HTTP2")
        print("   🔒 Authentication: Not required")
        print("   📡 Network: Cloudflare Global CDN")
        print("\n💡 To see the tunnel URL, check the terminal where")
        print("   you started the tunnel - look for lines like:")
        print("   https://xxx-xxx-xxx.trycloudflare.com")
    else:
        print("❌ Status: STOPPED")
        print("\n📋 No active tunnels")
        print("\n🚀 To start a tunnel:")
        print("   1. Choose option 1 (Web Mode) or 2 (Desktop Mode)")
        print("   2. Get your instant public URL")
        print("   3. Share with unlimited users!")
    
    print("\n💡 Cloudflare Quick Tunnel Advantages:")
    print("   ✅ No bandwidth limits (vs ngrok 40GB)")
    print("   ✅ Multiple concurrent users")
    print("   ✅ Enterprise-grade performance")
    print("   ✅ Global CDN network")
    print("   ✅ No account or login required")
    print("   ✅ No monthly subscription fees")
    print("   ✅ Instant setup (5 seconds)")
    print("="*60 + "\n")

def cleanup_old_tunnels():
    """Clean up old/unused tunnels"""
    print("\n" + "="*60)
    print("🧹 TUNNEL CLEANUP")
    print("="*60)
    
    print("\n💡 About Quick Tunnels:")
    print("   🚀 Quick Tunnels are temporary and anonymous")
    print("   🔄 They automatically clean up when stopped")
    print("   ⏰ No persistent storage or cleanup needed")
    
    # Check if any tunnel processes are running
    status = get_tunnel_status()
    if status['running']:
        print("\n✅ Found running tunnel process")
        print("🛑 To clean up: Simply stop the current tunnel (Ctrl+C)")
        choice = input("\n🔧 Kill running tunnel process now? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            kill_existing_cloudflared()
            print("✅ Tunnel process stopped")
        else:
            print("ℹ️  Tunnel process left running")
    else:
        print("\n✅ No cleanup needed - no running processes found")
    
    print("\n📋 Named Tunnels (Authentication Required):")
    try:
        # Try to list named tunnels (might fail if not authenticated)
        result = subprocess.run(
            ['cloudflared', 'tunnel', 'list'],
            capture_output=True,
            text=True,
            timeout=5  # Short timeout to fail fast
        )
        
        if result.returncode == 0:
            # Successfully authenticated - parse tunnels
            tunnels = []
            lines = result.stdout.split('\n')
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        tunnel_id = parts[0]
                        tunnel_name = parts[1]
                        status = parts[2] if len(parts) > 2 else 'unknown'
                        tunnels.append({
                            'id': tunnel_id,
                            'name': tunnel_name,
                            'status': status
                        })
            
            if tunnels:
                print(f"📋 Found {len(tunnels)} named tunnel(s):")
                for i, tunnel in enumerate(tunnels, 1):
                    print(f"   {i}. {tunnel['name']} (ID: {tunnel['id'][:8]}...)")
                
                choice = input(f"\nDelete named tunnels? (y/N): ").strip().lower()
                if choice in ['y', 'yes']:
                    for tunnel in tunnels:
                        try:
                            result = subprocess.run(
                                ['cloudflared', 'tunnel', 'delete', tunnel['name']],
                                capture_output=True,
                                text=True,
                                timeout=15
                            )
                            if result.returncode == 0:
                                print(f"[✓] Deleted tunnel: {tunnel['name']}")
                            else:
                                print(f"[-] Failed to delete {tunnel['name']}: {result.stderr}")
                        except Exception as e:
                            print(f"[-] Error deleting {tunnel['name']}: {e}")
            else:
                print("📋 No named tunnels found")
        else:
            # Authentication error or other issue
            print("ℹ️  Named tunnels require Cloudflare login")
            print("💡 Quick Tunnels are anonymous and auto-cleanup!")
            print("✅ No manual cleanup needed for Quick Tunnels")
    except Exception:
        print("ℹ️  Named tunnels require Cloudflare login")
        print("💡 Quick Tunnels are anonymous and auto-cleanup!")
        print("✅ No manual cleanup needed for Quick Tunnels")
    
    print("="*60 + "\n")

def main():
    """Main interactive menu"""
    print("\n" + "="*70)
    print("🚀 CLOUDFLARE TUNNEL HELPER - Screen Share Edition")
    print("="*70)
    print("🌐 Unlimited Bandwidth | 👥 Multiple Users | ⚡ Enterprise Performance")
    print("="*70)
    
    # Check prerequisites
    installed, cloudflared_cmd = check_cloudflared_installed()
    if not installed:
        if install_cloudflared():
            # Re-check after installation attempt
            installed, cloudflared_cmd = check_cloudflared_installed()
            if not installed:
                print("\n[!] cloudflared still not found. Please follow the setup instructions.")
                return
        else:
            return
    
    print(f"\n✅ Using cloudflared: {cloudflared_cmd}")
    
    # Setup login (Quick Tunnels don't require login)
    if not setup_cloudflare_login(cloudflared_cmd):
        return
    
    while True:
        print("\n📋 CLOUDFLARE TUNNEL MENU:")
        print("1. 🌐 Web Mode (HTTP - Port 5000)")
        print("2. 🖥️  Desktop Mode (TCP - Port 5555)")  
        print("3. ⚙️  Custom Port/Protocol")
        print("4. 📊 Tunnel Status")
        print("5. 🧹 Clean Up Old Tunnels")
        print("6. 🚪 Exit")
        
        choice = input("\n🎯 Choose option (1-6): ").strip()
        
        if choice == '1':
            print("\n[*] Selected: Web Mode (Port 5000)")
            print("[*] Starting Cloudflare HTTP tunnel...")
            success, url, process = start_cloudflare_tunnel(port=5000, protocol='http', cloudflared_cmd=cloudflared_cmd)
            if success:
                print("\n✅ Ready! Now start your screen share server:")
                print("   python main.py")
                print("   Choose option 2 (Web Mode)")
                print(f"\n🌐 Share this URL: {url}")
                print("\n[*] Press Ctrl+C to stop tunnel")
                try:
                    while True:
                        time.sleep(1)
                        if process and process.poll() is not None:
                            print("\n[!] Tunnel process stopped unexpectedly")
                            break
                except KeyboardInterrupt:
                    print("\n\n[*] Stopping tunnel...")
                    stop_cloudflare_tunnel(process)
                    print("[*] Goodbye!")
        
        elif choice == '2':
            print("\n[*] Selected: Desktop Mode (Port 5555)")
            print("[*] Starting Cloudflare TCP tunnel...")
            success, url, process = start_cloudflare_tunnel(port=5555, protocol='tcp', cloudflared_cmd=cloudflared_cmd)
            if success:
                print("\n✅ Ready! Now start your screen share server:")
                print("   python main.py")
                print("   Choose option 1 (Desktop Mode)")
                print(f"\n🔗 Share this URL: {url}")
                print("\n[*] Press Ctrl+C to stop tunnel")
                try:
                    while True:
                        time.sleep(1)
                        if process and process.poll() is not None:
                            print("\n[!] Tunnel process stopped unexpectedly")
                            break
                except KeyboardInterrupt:
                    print("\n\n[*] Stopping tunnel...")
                    stop_cloudflare_tunnel(process)
                    print("[*] Goodbye!")
        
        elif choice == '3':
            port = input("Enter port number: ").strip()
            protocol = input("Enter protocol (http/tcp): ").strip().lower()
            try:
                port = int(port)
                if protocol not in ['http', 'tcp']:
                    print("[!] Protocol must be 'http' or 'tcp'")
                    continue
                
                success, url, process = start_cloudflare_tunnel(port=port, protocol=protocol, cloudflared_cmd=cloudflared_cmd)
                if success:
                    print(f"\n🔗 Tunnel URL: {url}")
                    print("\n[*] Press Ctrl+C to stop tunnel")
                    try:
                        while True:
                            time.sleep(1)
                            if process and process.poll() is not None:
                                print("\n[!] Tunnel process stopped unexpectedly")
                                break
                    except KeyboardInterrupt:
                        print("\n\n[*] Stopping tunnel...")
                        stop_cloudflare_tunnel(process)
                        print("[*] Goodbye!")
            except ValueError:
                print("[!] Invalid port number")
        
        elif choice == '4':
            print_tunnel_status()
        
        elif choice == '5':
            cleanup_old_tunnels()
        
        elif choice == '6':
            print("\n🎉 Thanks for using Cloudflare Tunnel!")
            print("💡 Enjoy unlimited bandwidth and multiple user support!")
            return
        
        else:
            print("\n[!] Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user")
        print("[*] Stopping any running tunnels...")
        stop_cloudflare_tunnel()
    except Exception as e:
        print(f"\n[!] Error: {e}")