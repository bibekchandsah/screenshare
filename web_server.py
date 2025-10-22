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

# Import for cursor capture (cross-platform)
try:
    import pyautogui
    CURSOR_AVAILABLE = True
except ImportError:
    CURSOR_AVAILABLE = False
    print("[!] Warning: pyautogui not installed. Cursor won't be visible. Install with: pip install pyautogui")

class ScreenShareWebServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.security_code = None
        self.sharing = False
        self.authorized_sessions = set()
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.active_streams = {}  # Track active streaming connections
        self.pending_approvals = {}  # session_id -> {'ip': ip, 'approved': None}
        self.approval_lock = threading.Lock()  # Lock for approval process
        self.approval_queue = queue.Queue()  # Queue for approval requests
        self.approval_processor_thread = None  # Thread to process approvals sequentially
        
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
                    active_count = len(self.active_streams)
                    
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
                        self.frame_cache[quality_name] = encoded_img.tobytes()
                
                # Update current frame (backward compatibility)
                with self.frame_lock:
                    self.current_frame = self.frame_cache.get(self.current_quality)
                
                # Performance tracking
                capture_time = time.time() - capture_start
                frame_count += 1
                
                # Update stats every 100 frames
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
            # Return cached frame for specific quality
            with self.cache_lock:
                frame = self.frame_cache.get(quality)
                if frame:
                    self.performance_stats['frames_served'] += 1
                    return frame
        
        # Fallback to current frame (backward compatibility)
        with self.frame_lock:
            if self.current_frame:
                self.performance_stats['frames_served'] += 1
            return self.current_frame
    
    def verify_security_code(self, code):
        """Verify if the provided security code is correct"""
        return code == self.security_code
    
    def process_approval_queue(self):
        """Process approval requests sequentially from the queue"""
        while self.sharing:
            try:
                # Get approval request from queue (blocking with timeout)
                approval_request = self.approval_queue.get(timeout=1)
                if approval_request is None:  # Poison pill to stop thread
                    break
                
                session_id = approval_request['session_id']
                ip_address = approval_request['ip_address']
                
                # Add to pending approvals with lock
                with self.approval_lock:
                    if session_id not in self.pending_approvals:
                        continue  # Skip if already timed out
                    
                print(f"\n{'='*60}")
                print(f"[!] Web connection request from {ip_address}")
                print(f"[!] Session: {session_id[:8]}...")
                print(f"[!] Currently {len(self.authorized_sessions)} user(s) connected")
                print(f"[!] Pending requests in queue: {self.approval_queue.qsize()}")
                print(f"{'='*60}")
                
                approval = input("Do you want to allow this connection? (y/n): ").strip().lower()
                
                # Update approval status with lock and check if session still exists
                with self.approval_lock:
                    if session_id in self.pending_approvals:
                        if approval in ['y', 'yes']:
                            self.authorized_sessions.add(session_id)
                            self.pending_approvals[session_id]['approved'] = True
                            print(f"[+] Web client {ip_address} connection approved")
                            print(f"[+] Total connected users: {len(self.authorized_sessions)}")
                        else:
                            self.pending_approvals[session_id]['approved'] = False
                            print(f"[-] Web client {ip_address} connection rejected")
                    else:
                        # Session was already cleaned up (timeout)
                        print(f"[-] Session {session_id[:8]}... timed out before approval")
                
                self.approval_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[-] Error processing approval: {e}")
                continue
    
    def request_approval(self, session_id, ip_address):
        """Queue an approval request (non-blocking)"""
        # Add to pending approvals with lock
        with self.approval_lock:
            self.pending_approvals[session_id] = {'ip': ip_address, 'approved': None}
        
        # Add to approval queue
        self.approval_queue.put({
            'session_id': session_id,
            'ip_address': ip_address
        })
    
    def wait_for_approval(self, session_id, timeout=60):
        """Wait for approval decision (with timeout)"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.approval_lock:
                if session_id in self.pending_approvals:
                    approval_status = self.pending_approvals[session_id]['approved']
                    if approval_status is not None:
                        # Clean up
                        del self.pending_approvals[session_id]
                        return approval_status
            time.sleep(0.1)
        
        # Timeout - clean up with lock
        with self.approval_lock:
            if session_id in self.pending_approvals:
                del self.pending_approvals[session_id]
        return False
    
    def force_frame_update(self):
        """Force an immediate frame capture with current quality settings"""
        if not self.sharing:
            return
            
        try:
            sct = mss()
            
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
                    # Get cursor position
                    cursor_x, cursor_y = pyautogui.position()
                    
                    # Adjust cursor position relative to monitor
                    cursor_x -= monitor['left']
                    cursor_y -= monitor['top']
                    
                    # Draw cursor (simple circle with outline for visibility)
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
            
            # Apply current quality settings
            quality_config = self.quality_settings[self.current_quality]
            scale_percent = quality_config['scale']
            jpeg_quality = quality_config['jpeg_quality']
            
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            
            # Only resize if scaling is needed, use best quality interpolation
            if scale_percent != 100:
                img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LANCZOS4)
            
            # Encode image to JPEG format with current quality setting
            encode_param = [
                int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality,
                int(cv2.IMWRITE_JPEG_OPTIMIZE), 1,   # Optimize encoding
                int(cv2.IMWRITE_JPEG_PROGRESSIVE), 1  # Progressive JPEG for better streaming
            ]
            result, encoded_img = cv2.imencode('.jpg', img, encode_param)
            
            # Update current frame immediately
            with self.frame_lock:
                self.current_frame = encoded_img.tobytes()
                
            print(f"[*] Frame updated immediately with {self.current_quality} quality")
            
        except Exception as e:
            print(f"[-] Error forcing frame update: {e}")
    
    def create_request_handler(self):
        """Create HTTP request handler class with access to server instance"""
        server_instance = self
        
        class ScreenShareHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                """Suppress default logging"""
                pass
            
            def do_GET(self):
                """Handle GET requests"""
                if self.path == '/':
                    # Serve the main HTML page
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    html_path = os.path.join(os.path.dirname(__file__), 'web_client.html')
                    try:
                        with open(html_path, 'r', encoding='utf-8') as f:
                            self.wfile.write(f.read().encode())
                    except FileNotFoundError:
                        self.wfile.write(b"Error: web_client.html not found")
                
                elif self.path == '/health':
                    # Enhanced health check with performance metrics
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    # Gather performance stats
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
                        'optimizations': {
                            'multi_user_cache': True,
                            'adaptive_fps': True,
                            'quality_specific_frames': True,
                            'performance_monitoring': True
                        }
                    })
                    self.wfile.write(response.encode())
                    
                elif self.path == '/stats':
                    # Detailed performance statistics endpoint
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    detailed_stats = {
                        'server': {
                            'adaptive_fps': server_instance.adaptive_fps,
                            'current_quality': server_instance.current_quality,
                            'sharing_active': server_instance.sharing
                        },
                        'performance': server_instance.performance_stats,
                        'active_streams': {
                            session_id: {
                                'ip': info['ip'],
                                'duration': time.time() - info['start_time'],
                                'frames_sent': info['frames_sent'],
                                'quality': info['quality']
                            }
                            for session_id, info in server_instance.active_streams.items()
                        },
                        'optimization_status': {
                            'frame_caching': len(server_instance.frame_cache),
                            'total_active_viewers': len(server_instance.active_streams)
                        }
                    }
                    
                    self.wfile.write(json.dumps(detailed_stats, indent=2).encode())
                
                elif self.path.startswith('/stream'):
                    # Stream MJPEG
                    # Parse session ID from query parameter
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
                    
                    # Track this stream with performance monitoring
                    client_ip = self.client_address[0]
                    
                    with server_instance.user_count_lock:
                        server_instance.active_streams[session_id] = {
                            'ip': client_ip,
                            'start_time': time.time(),
                            'frames_sent': 0,
                            'quality': server_instance.current_quality
                        }
                    
                    active_count = len(server_instance.active_streams)
                    print(f"[*] Stream started for session {session_id} from {client_ip}")
                    print(f"[*] Active viewers: {active_count}")
                    
                    if active_count > 5:
                        print(f"[⚠️] High user load detected ({active_count} viewers) - adaptive performance active")
                    
                    # Send MJPEG stream headers with optimizations
                    self.send_response(200)
                    self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.send_header('Connection', 'close')
                    # Add performance headers
                    self.send_header('X-Frame-Rate', str(server_instance.adaptive_fps))
                    self.send_header('X-Active-Viewers', str(active_count))
                    self.end_headers()
                    
                    try:
                        frames_sent = 0
                        last_frame_time = time.time()
                        
                        while server_instance.sharing and session_id in server_instance.authorized_sessions:
                            # Get user's preferred quality or fallback to server default
                            user_quality = server_instance.active_streams.get(session_id, {}).get('quality', server_instance.current_quality)
                            frame = server_instance.get_current_frame(user_quality)
                            
                            if frame:
                                # Send frame in MJPEG format
                                self.wfile.write(b'--frame\r\n')
                                self.wfile.write(b'Content-Type: image/jpeg\r\n')
                                self.wfile.write(f'Content-Length: {len(frame)}\r\n'.encode())
                                self.wfile.write(b'\r\n')
                                self.wfile.write(frame)
                                self.wfile.write(b'\r\n')
                                self.wfile.flush()
                                
                                frames_sent += 1
                                
                                # Update stream stats
                                if session_id in server_instance.active_streams:
                                    server_instance.active_streams[session_id]['frames_sent'] = frames_sent
                            
                            # Adaptive sleep based on current FPS and user count
                            current_time = time.time()
                            frame_interval = 1.0 / server_instance.adaptive_fps
                            elapsed = current_time - last_frame_time
                            sleep_time = max(0, frame_interval - elapsed)
                            
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                            last_frame_time = time.time()
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        # Client disconnected gracefully
                        print(f"[*] Client {client_ip} (session {session_id}) disconnected")
                    except Exception as e:
                        print(f"[-] Stream error for session {session_id}: {e}")
                    finally:
                        # Remove from active streams with performance stats
                        with server_instance.user_count_lock:
                            if session_id in server_instance.active_streams:
                                stream_info = server_instance.active_streams[session_id]
                                session_duration = time.time() - stream_info['start_time']
                                frames_sent = stream_info['frames_sent']
                                
                                print(f"[*] Stream ended for {client_ip}")
                                print(f"    Duration: {session_duration:.1f}s, Frames sent: {frames_sent}")
                                
                                del server_instance.active_streams[session_id]
                        
                        remaining_viewers = len(server_instance.active_streams)
                        print(f"[*] Active viewers: {remaining_viewers}")
                        
                        if remaining_viewers == 0:
                            print(f"[*] All viewers disconnected - full performance restored")
                
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                """Handle POST requests"""
                try:
                    if self.path == '/verify':
                        # Verify security code
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        data = json.loads(post_data.decode('utf-8'))
                        
                        code = data.get('code', '').strip().upper()
                        
                        if server_instance.verify_security_code(code):
                            # Generate session ID
                            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                            
                            # Queue the approval request (will be processed sequentially)
                            server_instance.request_approval(
                                session_id, 
                                self.client_address[0]
                            )
                            
                            # Wait for approval with timeout (this is in HTTP handler thread, so it won't block other requests)
                            approved = server_instance.wait_for_approval(session_id, timeout=60)
                            
                            if approved:
                                self.send_response(200)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                response = {
                                    'status': 'approved',
                                    'session_id': session_id,
                                    'message': 'Connection approved'
                                }
                                self.wfile.write(json.dumps(response).encode())
                            else:
                                self.send_response(403)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                response = {
                                    'status': 'rejected',
                                    'message': 'Connection rejected by server or timeout'
                                }
                                self.wfile.write(json.dumps(response).encode())
                        else:
                            self.send_response(401)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response = {
                                'status': 'unauthorized',
                                'message': 'Invalid security code'
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
                            self.send_response(403)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response = {
                                'status': 'unauthorized',
                                'message': 'Invalid session'
                            }
                            self.wfile.write(json.dumps(response).encode())
                            return
                        
                        # Validate quality setting
                        if quality not in server_instance.quality_settings:
                            self.send_response(400)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            response = {
                                'status': 'error',
                                'message': 'Invalid quality setting. Valid options: high, medium, low'
                            }
                            self.wfile.write(json.dumps(response).encode())
                            return
                        
                        # Update quality
                        old_quality = server_instance.current_quality
                        server_instance.current_quality = quality
                        
                        quality_config = server_instance.quality_settings[quality]
                        print(f"[*] Quality changed from {old_quality} to {quality}")
                        print(f"    Scale: {quality_config['scale']}%, JPEG Quality: {quality_config['jpeg_quality']}%")
                        
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
        """Start the web-based screen sharing server"""
        # Generate security code
        code = self.generate_security_code()
        print("\n" + "="*60)
        print(f"SECURITY CODE: {code}")
        print("="*60)
        print("Share this code with people who want to view your screen")
        print("Multiple viewers can connect simultaneously!")
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
        print(f"[*] Default quality: {self.current_quality.title()} (clients can change this)")
        print("[*] Performance endpoints: /health, /stats")
        print("[*] Press Ctrl+C to stop sharing\n")
        
        self.sharing = True
        
        # Start screen capture thread
        capture_thread = threading.Thread(target=self.capture_screen_loop, daemon=True)
        capture_thread.start()
        
        # Start approval processor thread
        self.approval_processor_thread = threading.Thread(target=self.process_approval_queue, daemon=True)
        self.approval_processor_thread.start()
        print("[*] Approval processor started - requests will be handled sequentially")
        
        # Create a threaded HTTP server
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
        
        # Stop approval processor thread
        if self.approval_processor_thread and self.approval_processor_thread.is_alive():
            self.approval_queue.put(None)  # Poison pill to stop the thread
            self.approval_processor_thread.join(timeout=2)
        
        self.authorized_sessions.clear()
        self.active_streams.clear()
        self.pending_approvals.clear()
        
        # Clear the queue
        while not self.approval_queue.empty():
            try:
                self.approval_queue.get_nowait()
                self.approval_queue.task_done()
            except queue.Empty:
                break
        
        print("[*] Server stopped")

def main():
    print("="*60)
    print("SCREEN SHARING WEB SERVER")
    print("="*60)
    
    server = ScreenShareWebServer()
    
    try:
        server.start_sharing()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        server.stop_sharing()

if __name__ == "__main__":
    main()
