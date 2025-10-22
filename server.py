import socket
import threading
import pickle
import struct
import random
import string
import time
from mss import mss
import cv2
import numpy as np
from datetime import datetime

# Import for cursor capture
try:
    import pyautogui
    CURSOR_AVAILABLE = True
except ImportError:
    CURSOR_AVAILABLE = False
    print("[!] Warning: pyautogui not installed. Cursor won't be visible. Install with: pip install pyautogui")

class ScreenShareServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.security_code = None
        self.clients = []
        self.sharing = False
        
        # Multi-user performance optimizations
        self.frame_cache = {}  # Cache frames for different quality levels
        self.cache_lock = threading.Lock()
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.adaptive_fps = 20  # Dynamic FPS based on user count
        self.user_count_lock = threading.Lock()
        self.quality_settings = {
            'HIGH': {'scale': 100, 'jpeg_quality': 95},
            'MEDIUM': {'scale': 85, 'jpeg_quality': 85},
            'LOW': {'scale': 70, 'jpeg_quality': 75}
        }
        self.current_quality = 'MEDIUM'  # Default quality
        self.performance_stats = {
            'frames_captured': 0,
            'frames_served': 0,
            'active_clients': 0,
            'avg_frame_time': 0
        }
        self.capture_thread = None
    
    def get_local_ip(self):
        """Get the local IP address of this machine"""
        try:
            # Create a socket to find local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to a public DNS server (doesn't actually send data)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "Unable to detect"
        
    def generate_security_code(self, length=6):
        """Generate a random alphanumeric security code"""
        characters = string.ascii_uppercase + string.digits
        self.security_code = ''.join(random.choice(characters) for _ in range(length))
        return self.security_code
    
    def capture_screen_loop(self):
        """Optimized screen capture with multi-user performance enhancements"""
        sct = mss()
        frame_count = 0
        
        print("[*] Starting optimized capture loop for multi-user performance")
        
        while self.sharing:
            capture_start = time.time()
            
            try:
                # Dynamic FPS adjustment based on user count
                with self.user_count_lock:
                    active_count = len(self.clients)
                    
                    # Adaptive FPS: More users = lower FPS to maintain performance
                    if active_count == 0:
                        self.adaptive_fps = 20  # Full speed when no viewers
                    elif active_count <= 2:
                        self.adaptive_fps = 20  # Full speed for 1-2 users
                    elif active_count <= 5:
                        self.adaptive_fps = 15  # Slight reduction for 3-5 users
                    elif active_count <= 10:
                        self.adaptive_fps = 12  # Further reduction for 6-10 users
                    else:
                        self.adaptive_fps = 8   # Conservative for 10+ users
                
                # Capture the primary monitor
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Convert to numpy array
                img = np.array(screenshot)
                
                # Convert BGRA to BGR (remove alpha channel)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Draw cursor on the image (only once for all users)
                if CURSOR_AVAILABLE:
                    try:
                        # Get cursor position
                        cursor_x, cursor_y = pyautogui.position()
                        
                        # Adjust cursor position relative to monitor
                        cursor_x -= monitor['left']
                        cursor_y -= monitor['top']
                        
                        # Draw cursor (optimized for performance)
                        cursor_size = 12
                        cursor_thickness = 2
                        
                        # Draw outer circle (white outline for visibility on any background)
                        cv2.circle(img, (cursor_x, cursor_y), cursor_size, (255, 255, 255), cursor_thickness + 2)
                        # Draw inner circle (black for contrast)
                        cv2.circle(img, (cursor_x, cursor_y), cursor_size, (0, 0, 0), cursor_thickness)
                        # Draw center dot (red for visibility)
                        cv2.circle(img, (cursor_x, cursor_y), 3, (0, 0, 255), -1)
                        
                    except Exception:
                        # Cursor drawing failed, continue without cursor
                        pass
                
                # Generate frames for all quality levels (cache optimization)
                with self.cache_lock:
                    self.frame_cache.clear()  # Clear old cache
                    
                    for quality_name, quality_config in self.quality_settings.items():
                        # Create frame for each quality level
                        scale_percent = quality_config['scale']
                        jpeg_quality = quality_config['jpeg_quality']
                        
                        # Resize image for this quality
                        if scale_percent == 100:
                            quality_img = img.copy()
                        else:
                            width = int(img.shape[1] * scale_percent / 100)
                            height = int(img.shape[0] * scale_percent / 100)
                            quality_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)  # Faster for downscaling
                        
                        # Encode with quality-specific settings
                        encode_param = [
                            int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality,
                            int(cv2.IMWRITE_JPEG_OPTIMIZE), 1
                        ]
                        result, encoded_img = cv2.imencode('.jpg', quality_img, encode_param)
                        
                        # Cache the encoded frame
                        self.frame_cache[quality_name] = encoded_img
                
                # Update current frame (backward compatibility)
                with self.frame_lock:
                    self.current_frame = self.frame_cache.get(self.current_quality)
                
                # Performance tracking
                capture_time = time.time() - capture_start
                frame_count += 1
                
                # Update stats every 100 frames
                if frame_count % 100 == 0:
                    self.performance_stats['frames_captured'] = frame_count
                    self.performance_stats['active_clients'] = len(self.clients)
                    self.performance_stats['avg_frame_time'] = capture_time
                    
                    if len(self.clients) > 0:
                        print(f"[📊] Performance: {len(self.clients)} clients, "
                              f"{self.adaptive_fps} FPS, "
                              f"{capture_time*1000:.1f}ms/frame")
                
                # Dynamic sleep based on adaptive FPS
                sleep_time = max(0, (1.0 / self.adaptive_fps) - capture_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
            except Exception as e:
                print(f"[-] Error capturing screen: {e}")
                time.sleep(1)
        
        sct.close()
        print("[*] Screen capture loop ended")
    
    def get_cached_frame(self, quality='MEDIUM'):
        """Get cached frame for specific quality level"""
        with self.cache_lock:
            cached_frame = self.frame_cache.get(quality)
            if cached_frame is not None:
                self.performance_stats['frames_served'] += 1
                return cached_frame
        
        # Fallback to current frame
        with self.frame_lock:
            if self.current_frame is not None:
                self.performance_stats['frames_served'] += 1
                return self.current_frame
        return None
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection with multi-user optimization"""
        print(f"[*] Connection from {address}")
        client_quality = 'MEDIUM'  # Default quality for new clients
        
        try:
            # Receive security code from client
            received_code = client_socket.recv(1024).decode('utf-8').strip()
            
            print(f"[DEBUG] Expected code: '{self.security_code}' (length: {len(self.security_code)})")
            print(f"[DEBUG] Received code: '{received_code}' (length: {len(received_code)})")
            print(f"[DEBUG] Codes match: {received_code == self.security_code}")
            
            if received_code == self.security_code:
                # Code is correct, now ask for manual approval
                print(f"\n{'='*60}")
                print(f"[!] Connection request from {address}")
                print(f"{'='*60}")
                
                # Send waiting status to client
                client_socket.send(b"WAITING_APPROVAL\n")
                
                # Ask server operator for approval
                approval = input("Do you want to allow this connection? (y/n): ").strip().lower()
                
                if approval in ['y', 'yes']:
                    # Approved
                    client_socket.send(b"APPROVED\n")
                    
                    # Add client to active list (thread-safe)
                    with self.user_count_lock:
                        self.clients.append(client_socket)
                        active_count = len(self.clients)
                    
                    print(f"[+] Client {address} connection approved (Total clients: {active_count})")
                    print(f"[📺] Streaming with adaptive quality optimization")
                    print(f"[📊] Multi-user performance mode enabled")
                    
                    # Set socket timeout for quality change requests
                    client_socket.settimeout(0.1)
                    
                    # Performance tracking for this client
                    frame_count = 0
                    last_stats_time = time.time()
                    
                    # Stream optimized frames to this client
                    while self.sharing:
                        try:
                            # Check for quality change requests (non-blocking)
                            try:
                                data = client_socket.recv(64)
                                if data and data.startswith(b"QUALITY:"):
                                    new_quality = data.decode().replace("QUALITY:", "").strip()
                                    if new_quality in self.quality_settings:
                                        client_quality = new_quality
                                        print(f"[📺] Client {address} changed quality to {client_quality}")
                            except socket.timeout:
                                pass  # No quality change request
                            except (ConnectionResetError, BrokenPipeError):
                                break  # Client disconnected
                            
                            # Get cached frame for client's quality level
                            frame = self.get_cached_frame(client_quality)
                            
                            if frame is not None:
                                # Serialize and send frame (compatible with existing client)
                                data = pickle.dumps(frame)
                                message_size = struct.pack("L", len(data))
                                
                                try:
                                    client_socket.settimeout(1.0)  # Timeout for sending
                                    client_socket.sendall(message_size + data)
                                    frame_count += 1
                                except (BrokenPipeError, ConnectionResetError, socket.timeout):
                                    break
                            
                            # Adaptive frame rate based on user count
                            with self.user_count_lock:
                                current_user_count = len(self.clients)
                            
                            # Dynamic delay based on client count
                            if current_user_count <= 2:
                                client_delay = 0.033  # ~30 FPS for 1-2 users
                            elif current_user_count <= 5:
                                client_delay = 0.050  # ~20 FPS for 3-5 users
                            elif current_user_count <= 10:
                                client_delay = 0.067  # ~15 FPS for 6-10 users
                            else:
                                client_delay = 0.100  # ~10 FPS for 10+ users
                            
                            time.sleep(client_delay)
                            
                            # Log performance stats periodically
                            current_time = time.time()
                            if current_time - last_stats_time >= 30:  # Every 30 seconds
                                if last_stats_time > 0:
                                    fps = frame_count / (current_time - last_stats_time)
                                    print(f"[📊] Client {address}: Quality={client_quality}, "
                                          f"FPS={fps:.1f}, Total clients={current_user_count}")
                                frame_count = 0
                                last_stats_time = current_time
                            
                        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError) as e:
                            print(f"[*] Client {address} disconnected gracefully")
                            break
                        except OSError as e:
                            # Windows error 10053 and similar connection aborts
                            if e.winerror == 10053 or 'connection' in str(e).lower():
                                print(f"[*] Client {address} closed the connection")
                            else:
                                print(f"[-] Network error with {address}: {e}")
                            break
                        except Exception as e:
                            print(f"[-] Unexpected error sending to {address}: {e}")
                            break
                else:
                    # Rejected
                    client_socket.send(b"REJECTED\n")
                    print(f"[-] Client {address} connection rejected")
            else:
                client_socket.send(b"UNAUTHORIZED\n")
                print(f"[-] Client {address} provided wrong code: '{received_code}'")
                
        except Exception as e:
            print(f"[-] Error handling client {address}: {e}")
        finally:
            # Remove client from active list (thread-safe)
            with self.user_count_lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
                remaining_count = len(self.clients)
            
            try:
                client_socket.close()
            except:
                pass
            
            print(f"[-] Client {address} disconnected (Remaining clients: {remaining_count})")
    
    def start_sharing(self):
        """Start the screen sharing server"""
        # Generate security code
        code = self.generate_security_code()
        
        # Get local IP address
        local_ip = self.get_local_ip()
        
        print("\n" + "="*60)
        print(f"🔐 SECURITY CODE: {code}")
        print(f"📡 SERVER IP: {local_ip}")
        print(f"🔌 PORT: {self.port}")
        print("="*60)
        print("📤 Share this information with the viewer:")
        print(f"   IP Address: {local_ip}")
        print(f"   Security Code: {code}")
        print("="*60 + "\n")
        
        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.sharing = True
            
            print(f"[*] Server listening on {self.host}:{self.port}")
            print("[*] Starting optimized screen capture loop...")
            
            # Start the screen capture thread with multi-user optimization
            capture_thread = threading.Thread(target=self.capture_screen_loop, daemon=True)
            capture_thread.start()
            
            print("[*] Waiting for connections...")
            
            # Accept client connections
            while self.sharing:
                try:
                    self.server_socket.settimeout(1.0)
                    client_socket, address = self.server_socket.accept()
                    
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.sharing:
                        print(f"[-] Error accepting connection: {e}")
                    
        except Exception as e:
            print(f"[-] Server error: {e}")
        finally:
            self.stop_sharing()
    
    def stop_sharing(self):
        """Stop the screen sharing server"""
        print("\n[*] Stopping server...")
        self.sharing = False
        
        # Close all client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("[*] Server stopped")

def main():
    print("="*50)
    print("SCREEN SHARING SERVER")
    print("="*50)
    
    server = ScreenShareServer()
    
    try:
        server.start_sharing()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        server.stop_sharing()

if __name__ == "__main__":
    main()
