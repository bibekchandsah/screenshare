"""
Trusted Screen Share Server - No Security Code Required
For sharing with trusted users only
"""

import socket
import threading
import random
import string
from mss import mss
import cv2
import numpy as np
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import base64
import time
import os
import queue

# Try to import clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# Import for cursor capture (cross-platform)
try:
    import pyautogui
    CURSOR_AVAILABLE = True
except ImportError:
    CURSOR_AVAILABLE = False
    print("[!] Warning: pyautogui not installed. Cursor won't be visible. Install with: pip install pyautogui")

class TrustedScreenShareWebServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.sharing = False
        self.authorized_sessions = set()
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.active_streams = {}  # Track active streaming connections
        self.connected_users_log = []  # Log of all connected users
        
        # Quality settings
        self.quality_settings = {
            'high': {'scale': 100, 'jpeg_quality': 95},
            'medium': {'scale': 85, 'jpeg_quality': 85},
            'low': {'scale': 70, 'jpeg_quality': 75}
        }
        self.current_quality = 'medium'  # Default quality
        
        # Multi-user performance optimizations
        self.frame_cache = {}  # Cache frames for different quality levels
        self.cache_lock = threading.Lock()
        self.last_capture_time = 0
        self.adaptive_fps = 20  # Dynamic FPS based on user count
        self.user_count_lock = threading.Lock()
        self.performance_stats = {
            'frames_captured': 0,
            'frames_served': 0,
            'active_viewers': 0,
            'avg_frame_time': 0
        }
        
    def copy_to_clipboard(self, text, description="text"):
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
                    active_count = len(self.active_streams)
                    
                    # Adaptive FPS: 20 FPS for 1-2 users, scale down for more users
                    if active_count <= 2:
                        self.adaptive_fps = 20
                    elif active_count <= 4:
                        self.adaptive_fps = 15
                    elif active_count <= 6:
                        self.adaptive_fps = 12
                    else:
                        self.adaptive_fps = 8
                
                # Capture screen
                screenshot = sct.grab(sct.monitors[0])
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Capture cursor if available
                if CURSOR_AVAILABLE:
                    try:
                        cursor_x, cursor_y = pyautogui.position()
                        # Draw cursor as a circle
                        cv2.circle(img, (cursor_x, cursor_y), 10, (0, 0, 255), -1)
                        cv2.circle(img, (cursor_x, cursor_y), 12, (255, 255, 255), 2)
                    except:
                        pass
                
                # Update frame with thread safety
                with self.frame_lock:
                    self.current_frame = img.copy()
                    # Clear cache when new frame captured
                    with self.cache_lock:
                        self.frame_cache.clear()
                
                frame_count += 1
                self.performance_stats['frames_captured'] += 1
                
                # Calculate and display performance metrics every 100 frames
                if frame_count % 100 == 0:
                    frame_time = (time.time() - capture_start) * 1000
                    self.performance_stats['avg_frame_time'] = frame_time
                    with self.user_count_lock:
                        viewers = len(self.active_streams)
                        self.performance_stats['active_viewers'] = viewers
                        print(f"[📊] Performance: {viewers} viewers, {self.adaptive_fps} FPS, {frame_time:.1f}ms/frame")
                
                # Dynamic sleep based on adaptive FPS
                time.sleep(1.0 / self.adaptive_fps)
                
            except Exception as e:
                print(f"[-] Error capturing screen: {e}")
                time.sleep(0.1)
        
        print("[*] Screen capture loop ended")
    
    def get_cached_frame(self, quality='medium'):
        """Get frame from cache or encode new one"""
        cache_key = quality
        
        with self.cache_lock:
            if cache_key in self.frame_cache:
                return self.frame_cache[cache_key]
        
        # Encode new frame
        with self.frame_lock:
            if self.current_frame is None:
                return None
            
            frame = self.current_frame.copy()
        
        # Apply quality settings
        settings = self.quality_settings.get(quality, self.quality_settings['medium'])
        scale_percent = settings['scale']
        jpeg_quality = settings['jpeg_quality']
        
        # Resize if needed
        if scale_percent != 100:
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        
        # Encode to JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        frame_data = base64.b64encode(buffer).decode('utf-8')
        
        # Cache the encoded frame
        with self.cache_lock:
            self.frame_cache[cache_key] = frame_data
        
        return frame_data
    
    def force_frame_update(self):
        """Force cache clear to update frame immediately"""
        with self.cache_lock:
            self.frame_cache.clear()
    
    def verify_security_code(self, code):
        """Always return True for trusted mode - no security check"""
        return True
    
    def log_connection(self, session_id, client_ip):
        """Log a new connection"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'session_id': session_id,
            'ip': client_ip
        }
        self.connected_users_log.append(log_entry)
        
        # Display connection log
        print("\n" + "="*60)
        print(f"[✓] NEW CONNECTION")
        print("="*60)
        print(f"📅 Time: {timestamp}")
        print(f"🌐 IP Address: {client_ip}")
        print(f"🔑 Session ID: {session_id}")
        print(f"👥 Total Connections: {len(self.connected_users_log)}")
        print(f"🟢 Active Viewers: {len(self.active_streams)}")
        print("="*60 + "\n")
    
    def create_handler(self):
        """Create HTTP request handler class"""
        server_instance = self
        
        class ScreenShareHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                """Suppress default logging"""
                pass
            
            def do_GET(self):
                """Handle GET requests"""
                try:
                    if self.path == '/':
                        # Serve the trusted HTML viewer (no security code)
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        # Read and serve the trusted HTML file
                        try:
                            with open('web_client_trusted.html', 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            self.wfile.write(html_content.encode('utf-8'))
                        except FileNotFoundError:
                            error_html = """
                            <!DOCTYPE html>
                            <html>
                            <head><title>Error</title></head>
                            <body>
                                <h1>Error: web_client_trusted.html not found</h1>
                                <p>Please make sure web_client_trusted.html is in the same directory as the server script.</p>
                            </body>
                            </html>
                            """
                            self.wfile.write(error_html.encode('utf-8'))
                    
                    elif self.path == '/health':
                        # Health check endpoint
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        health = {
                            'status': 'healthy',
                            'active_viewers': server_instance.performance_stats['active_viewers'],
                            'fps': server_instance.adaptive_fps
                        }
                        self.wfile.write(json.dumps(health).encode())
                    
                    elif self.path == '/stats':
                        # Performance stats endpoint
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(server_instance.performance_stats).encode())
                    
                    elif self.path.startswith('/stream'):
                        # Handle stream request - auto-approve in trusted mode
                        session_id = self.path.split('?')[1].split('=')[1] if '?' in self.path else str(random.randint(100000, 999999))
                        client_ip = self.client_address[0]
                        
                        # Automatically authorize in trusted mode
                        server_instance.authorized_sessions.add(session_id)
                        
                        # Log the connection
                        server_instance.log_connection(session_id, client_ip)
                        
                        # Add to active streams
                        with server_instance.user_count_lock:
                            server_instance.active_streams[session_id] = {
                                'ip': client_ip,
                                'start_time': time.time(),
                                'quality': 'medium'
                            }
                        
                        print(f"[*] Stream started for session {session_id} from {client_ip}")
                        print(f"[*] Active viewers: {len(server_instance.active_streams)}")
                        
                        # Send response headers for streaming
                        self.send_response(200)
                        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
                        self.send_header('Cache-Control', 'no-cache')
                        self.end_headers()
                        
                        try:
                            while server_instance.sharing and session_id in server_instance.authorized_sessions:
                                # Get current quality for this session
                                quality = 'medium'
                                with server_instance.user_count_lock:
                                    if session_id in server_instance.active_streams:
                                        quality = server_instance.active_streams[session_id].get('quality', 'medium')
                                
                                # Get frame (cached or new)
                                frame_data = server_instance.get_cached_frame(quality)
                                
                                if frame_data:
                                    try:
                                        self.wfile.write(b'--frame\r\n')
                                        self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n')
                                        self.wfile.write(base64.b64decode(frame_data))
                                        self.wfile.write(b'\r\n')
                                        server_instance.performance_stats['frames_served'] += 1
                                    except (BrokenPipeError, ConnectionResetError):
                                        break
                                
                                time.sleep(0.03)  # ~30 FPS max client-side
                        
                        except Exception as e:
                            print(f"[-] Streaming error for {client_ip}: {e}")
                        
                        finally:
                            # Clean up
                            with server_instance.user_count_lock:
                                server_instance.active_streams.pop(session_id, None)
                            
                            server_instance.authorized_sessions.discard(session_id)
                            
                            print(f"\n[−] DISCONNECTION")
                            print(f"[−] IP: {client_ip}")
                            print(f"[−] Session: {session_id}")
                            print(f"[*] Active viewers: {len(server_instance.active_streams)}\n")
                    
                    else:
                        self.send_response(404)
                        self.end_headers()
                        
                except Exception as e:
                    print(f"[-] Error handling GET request: {e}")
                    try:
                        self.send_response(500)
                        self.end_headers()
                    except:
                        pass
            
            def do_POST(self):
                """Handle POST requests"""
                try:
                    if self.path == '/verify':
                        # No verification needed in trusted mode - always accept
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        
                        session_id = data.get('session', str(random.randint(100000, 999999)))
                        
                        # Always authorize in trusted mode
                        server_instance.authorized_sessions.add(session_id)
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {
                            'status': 'authorized',
                            'session': session_id,
                            'message': 'Trusted mode - no security code required'
                        }
                        self.wfile.write(json.dumps(response).encode())
                    
                    elif self.path == '/set_quality':
                        # Set stream quality
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        
                        session_id = data.get('session', '')
                        quality = data.get('quality', '').lower()
                        
                        # Validate session
                        if not session_id or session_id not in server_instance.authorized_sessions:
                            self.send_response(401)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response = {
                                'status': 'unauthorized',
                                'message': 'Invalid session'
                            }
                            self.wfile.write(json.dumps(response).encode())
                            return
                        
                        # Validate quality
                        if quality not in server_instance.quality_settings:
                            quality = 'medium'
                        
                        # Update quality for this session
                        with server_instance.user_count_lock:
                            if session_id in server_instance.active_streams:
                                server_instance.active_streams[session_id]['quality'] = quality
                        
                        # Force an immediate frame update with new quality
                        server_instance.force_frame_update()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {
                            'status': 'success',
                            'quality': quality,
                            'message': f'Quality set to {quality}'
                        }
                        self.wfile.write(json.dumps(response).encode())
                    
                    else:
                        self.send_response(404)
                        self.end_headers()
                        
                except Exception as e:
                    print(f"[-] Error handling POST request: {e}")
                    try:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {
                            'status': 'error',
                            'message': 'Internal server error'
                        }
                        self.wfile.write(json.dumps(response).encode())
                    except:
                        pass  # If we can't send error response, just continue
        
        return ScreenShareHandler
    
    def start_sharing(self):
        """Start the trusted web-based screen sharing server"""
        print("\n" + "="*60)
        print("⚠️  TRUSTED MODE - NO SECURITY CODE OR APPROVAL")
        print("="*60)
        print("⚠️  WARNING: Connections are automatically accepted!")
        print("⚠️  Anyone with the URL can view your screen instantly!")
        print("⚠️  Only use with trusted users on secure networks!")
        print("⚠️  All connections will be logged below.")
        print("="*60 + "\n")
        
        # Get local IP addresses
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"[*] Access the screen share from your browser at:")
            print(f"    http://{local_ip}:{self.port}")
            print(f"    http://localhost:{self.port}")
        except:
            print(f"[*] Access the screen share from your browser at:")
            print(f"    http://localhost:{self.port}")
        
        print(f"\n[*] Server starting on {self.host}:{self.port}")
        print("[*] 🚀 Multi-user optimizations ENABLED")
        print("    ✅ Adaptive FPS scaling (20→8 FPS based on user count)")
        print("    ✅ Quality-specific frame caching")
        print("    ✅ Performance monitoring and statistics")
        print("    ✅ Optimized memory usage")
        print("    ✅ Auto-accept connections with logging")
        print("[*] Default quality: Medium (clients can change this)")
        print("[*] Performance endpoints: /health, /stats")
        print("[*] Press Ctrl+C to stop sharing\n")
        
        self.sharing = True
        
        # Start screen capture thread
        capture_thread = threading.Thread(target=self.capture_screen_loop, daemon=True)
        capture_thread.start()
        
        # Create HTTP server with threading support
        class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
            daemon_threads = True
            allow_reuse_address = True
        
        try:
            server = ThreadedHTTPServer((self.host, self.port), self.create_handler())
            print("[*] Threaded HTTP server initialized - multiple connections supported\n")
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n\n[*] Stopping server...")
            self.sharing = False
            server.shutdown()
            print("[*] Server stopped")
        except Exception as e:
            print(f"[-] Server error: {e}")
            self.sharing = False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  TRUSTED SCREEN SHARE SERVER - AUTO-ACCEPT MODE")
    print("="*60)
    print("\n⚠️  WARNING: This server auto-accepts ALL connections!")
    print("⚠️  No security code or approval required!")
    print("⚠️  Use only with trusted users on secure networks!")
    print("⚠️  All connections will be logged.\n")
    
    server = TrustedScreenShareWebServer()
    server.start_sharing()
