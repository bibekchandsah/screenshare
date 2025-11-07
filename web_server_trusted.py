"""
Trusted Screen Share Server - No Security Code Required
For sharing with trusted users only
Reuses optimized code from web_server.py
"""

from mss import mss
import cv2
import numpy as np
import socket
import threading
import json
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# Try to import cursor capture (cross-platform)
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
        self.connected_users_log = []  # Log of connected users
        
        # Quality settings (same as regular server)
        self.quality_settings = {
            'high': {'scale': 100, 'jpeg_quality': 95},
            'medium': {'scale': 85, 'jpeg_quality': 85},
            'low': {'scale': 70, 'jpeg_quality': 75}
        }
        self.current_quality = 'medium'  # Default quality
        
        # Multi-user performance optimizations (same as regular server)
        self.frame_cache = {}
        self.cache_lock = threading.Lock()
        self.last_capture_time = 0
        self.adaptive_fps = 20
        self.user_count_lock = threading.Lock()
        self.performance_stats = {
            'frames_captured': 0,
            'frames_served': 0,
            'active_viewers': 0,
            'avg_frame_time': 0
        }
    
    def log_connection(self, session_id, ip_address):
        """Log connection details"""
        connection_info = {
            'session_id': session_id,
            'ip_address': ip_address,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'time_unix': time.time()
        }
        self.connected_users_log.append(connection_info)
        print(f"\n{'='*60}")
        print(f"[✓] New connection established")
        print(f"[*] IP Address: {ip_address}")
        print(f"[*] Session ID: {session_id[:8]}...")
        print(f"[*] Time: {connection_info['timestamp']}")
        print(f"[*] Total connections: {len(self.connected_users_log)}")
        print(f"[*] Currently active: {len(self.authorized_sessions)}")
        print(f"{'='*60}\n")
    
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
                    
                    # Adaptive FPS: More users = lower FPS to maintain performance
                    if active_count == 0:
                        self.adaptive_fps = 20
                    elif active_count <= 2:
                        self.adaptive_fps = 20
                    elif active_count <= 5:
                        self.adaptive_fps = 15
                    elif active_count <= 10:
                        self.adaptive_fps = 12
                    else:
                        self.adaptive_fps = 8
                
                # Capture the primary monitor
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Convert to numpy array
                img = np.array(screenshot)
                
                # Convert BGRA to BGR (remove alpha channel)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Draw cursor on the image
                if CURSOR_AVAILABLE:
                    try:
                        cursor_x, cursor_y = pyautogui.position()
                        cursor_x -= monitor['left']
                        cursor_y -= monitor['top']
                        
                        cursor_size = 12
                        cursor_thickness = 2
                        
                        cv2.circle(img, (cursor_x, cursor_y), cursor_size, (255, 255, 255), cursor_thickness + 2)
                        cv2.circle(img, (cursor_x, cursor_y), cursor_size, (0, 0, 0), cursor_thickness)
                        cv2.circle(img, (cursor_x, cursor_y), 3, (0, 0, 255), -1)
                    except Exception:
                        pass
                
                # Generate frames for all quality levels
                with self.cache_lock:
                    self.frame_cache.clear()
                    
                    for quality_name, quality_config in self.quality_settings.items():
                        scale_percent = quality_config['scale']
                        jpeg_quality = quality_config['jpeg_quality']
                        
                        if scale_percent == 100:
                            quality_img = img
                        else:
                            width = int(img.shape[1] * scale_percent / 100)
                            height = int(img.shape[0] * scale_percent / 100)
                            quality_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LANCZOS4)
                        
                        encode_param = [
                            int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality,
                            int(cv2.IMWRITE_JPEG_OPTIMIZE), 1
                        ]
                        result, encoded_img = cv2.imencode('.jpg', quality_img, encode_param)
                        self.frame_cache[quality_name] = encoded_img.tobytes()
                
                # Update current frame
                with self.frame_lock:
                    self.current_frame = self.frame_cache.get(self.current_quality)
                
                # Performance tracking
                capture_time = time.time() - capture_start
                frame_count += 1
                
                if frame_count % 100 == 0:
                    self.performance_stats['frames_captured'] = frame_count
                    self.performance_stats['active_viewers'] = len(self.active_streams)
                    self.performance_stats['avg_frame_time'] = capture_time
                    
                    if len(self.active_streams) > 0:
                        print(f"[📊] Performance: {len(self.active_streams)} viewers, "
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
    
    def get_current_frame(self, quality=None):
        """Get the current frame as JPEG bytes with optional quality specification"""
        if quality and quality in self.quality_settings:
            with self.cache_lock:
                frame = self.frame_cache.get(quality)
                if frame:
                    self.performance_stats['frames_served'] += 1
                    return frame
        
        with self.frame_lock:
            if self.current_frame:
                self.performance_stats['frames_served'] += 1
            return self.current_frame
    
    def create_request_handler(self):
        """Create HTTP request handler class with access to server instance"""
        server_instance = self
        
        class TrustedScreenShareHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                """Suppress default logging"""
                pass
            
            def do_GET(self):
                """Handle GET requests"""
                if self.path == '/':
                    # Serve the trusted HTML page
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    html_path = os.path.join(os.path.dirname(__file__), 'web_client_trusted.html')
                    try:
                        with open(html_path, 'r', encoding='utf-8') as f:
                            self.wfile.write(f.read().encode())
                    except FileNotFoundError:
                        self.wfile.write(b"Error: web_client_trusted.html not found")
                
                elif self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    active_count = len(server_instance.active_streams)
                    stats = server_instance.performance_stats.copy()
                    stats['active_viewers'] = active_count
                    stats['adaptive_fps'] = server_instance.adaptive_fps
                    
                    response = json.dumps({
                        'status': 'ok', 
                        'sharing': server_instance.sharing,
                        'current_quality': server_instance.current_quality,
                        'available_qualities': list(server_instance.quality_settings.keys()),
                        'performance': stats,
                        'trusted_mode': True
                    })
                    self.wfile.write(response.encode())
                
                elif self.path.startswith('/stream'):
                    # Stream MJPEG
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(self.path)
                    params = parse_qs(parsed.query)
                    session_id = params.get('session', [None])[0]
                    
                    if not session_id or session_id not in server_instance.authorized_sessions:
                        self.send_response(403)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b"Unauthorized - Invalid or missing session")
                        return
                    
                    # Track this stream
                    client_ip = self.client_address[0]
                    
                    with server_instance.user_count_lock:
                        server_instance.active_streams[session_id] = {
                            'ip': client_ip,
                            'start_time': time.time(),
                            'frames_sent': 0,
                            'quality': server_instance.current_quality
                        }
                    
                    active_count = len(server_instance.active_streams)
                    print(f"[*] Stream started for session {session_id[:8]}... from {client_ip}")
                    print(f"[*] Active viewers: {active_count}")
                    
                    # Send MJPEG stream headers
                    self.send_response(200)
                    self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.send_header('Connection', 'close')
                    self.send_header('X-Frame-Rate', str(server_instance.adaptive_fps))
                    self.send_header('X-Active-Viewers', str(active_count))
                    self.end_headers()
                    
                    try:
                        frames_sent = 0
                        while server_instance.sharing and session_id in server_instance.authorized_sessions:
                            # Get quality preference for this session
                            quality = server_instance.active_streams.get(session_id, {}).get('quality', server_instance.current_quality)
                            
                            frame = server_instance.get_current_frame(quality)
                            if frame:
                                try:
                                    self.wfile.write(b'--frame\r\n')
                                    self.wfile.write(b'Content-Type: image/jpeg\r\n')
                                    self.wfile.write(f'Content-Length: {len(frame)}\r\n'.encode())
                                    self.wfile.write(b'\r\n')
                                    self.wfile.write(frame)
                                    self.wfile.write(b'\r\n')
                                    
                                    frames_sent += 1
                                    server_instance.active_streams[session_id]['frames_sent'] = frames_sent
                                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                                    break
                            
                            time.sleep(1.0 / server_instance.adaptive_fps)
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        pass
                    except Exception as e:
                        print(f"[-] Stream error for {session_id[:8]}...: {e}")
                    finally:
                        with server_instance.user_count_lock:
                            if session_id in server_instance.active_streams:
                                del server_instance.active_streams[session_id]
                        print(f"[*] Stream ended for session {session_id[:8]}... ({frames_sent} frames sent)")
                
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                """Handle POST requests"""
                try:
                    if self.path == '/verify':
                        # Auto-verify in trusted mode (no security code needed)
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        
                        session_id = data.get('session')
                        client_ip = self.client_address[0]
                        
                        if not session_id:
                            self.send_response(400)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response = json.dumps({'status': 'error', 'message': 'Missing session ID'})
                            self.wfile.write(response.encode())
                            return
                        
                        # Automatically authorize in trusted mode
                        server_instance.authorized_sessions.add(session_id)
                        server_instance.log_connection(session_id, client_ip)
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = json.dumps({
                            'status': 'authorized',
                            'message': 'Connected in trusted mode',
                            'session': session_id
                        })
                        self.wfile.write(response.encode())
                    
                    elif self.path == '/set_quality':
                        # Handle quality change requests
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        
                        session_id = data.get('session')
                        quality = data.get('quality', 'medium')
                        
                        if session_id not in server_instance.authorized_sessions:
                            self.send_response(403)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response = json.dumps({'status': 'error', 'message': 'Unauthorized'})
                            self.wfile.write(response.encode())
                            return
                        
                        if quality not in server_instance.quality_settings:
                            self.send_response(400)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response = json.dumps({'status': 'error', 'message': 'Invalid quality setting'})
                            self.wfile.write(response.encode())
                            return
                        
                        # Update quality for this specific session
                        if session_id in server_instance.active_streams:
                            server_instance.active_streams[session_id]['quality'] = quality
                        
                        print(f"[*] Quality changed to '{quality}' for session {session_id[:8]}...")
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = json.dumps({
                            'status': 'success',
                            'quality': quality,
                            'message': f'Quality set to {quality}'
                        })
                        self.wfile.write(response.encode())
                    
                    else:
                        self.send_response(404)
                        self.end_headers()
                
                except Exception as e:
                    print(f"[-] Error handling POST request: {e}")
                    try:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = json.dumps({'status': 'error', 'message': str(e)})
                        self.wfile.write(response.encode())
                    except:
                        pass
        
        return TrustedScreenShareHandler
    
    def start_sharing(self):
        """Start the trusted web-based screen sharing server"""
        print("\n" + "="*60)
        print("TRUSTED MODE - NO SECURITY CODE REQUIRED")
        print("="*60)
        print("⚠️  All connections will be automatically accepted")
        print("📝 Connection details will be logged for your reference")
        print("="*60)
        
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
        print(f"[*] Default quality: {self.current_quality.title()} (clients can change this)")
        print("[*] Press Ctrl+C to stop sharing\n")
        
        self.sharing = True
        
        # Start screen capture thread
        capture_thread = threading.Thread(target=self.capture_screen_loop, daemon=True)
        capture_thread.start()
        
        # Create threaded HTTP server
        class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
            daemon_threads = True
        
        # Start HTTP server
        try:
            handler_class = self.create_request_handler()
            httpd = ThreadedHTTPServer((self.host, self.port), handler_class)
            print("[*] Threaded HTTP server initialized - multiple connections supported")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server stopped by user")
        except Exception as e:
            print(f"[-] Server error: {e}")
        finally:
            self.stop_sharing()
    
    def stop_sharing(self):
        """Stop the screen sharing server"""
        print("\n[*] Stopping server...")
        self.sharing = False
        self.authorized_sessions.clear()
        self.active_streams.clear()
        
        # Print connection summary
        if self.connected_users_log:
            print(f"\n[*] Connection Summary:")
            print(f"    Total connections: {len(self.connected_users_log)}")
            for conn in self.connected_users_log:
                print(f"    - {conn['ip_address']} at {conn['timestamp']}")
        
        print("[*] Server stopped")

def main():
    print("="*60)
    print("TRUSTED SCREEN SHARING WEB SERVER")
    print("="*60)
    
    server = TrustedScreenShareWebServer()
    
    try:
        server.start_sharing()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        server.stop_sharing()

if __name__ == "__main__":
    main()
