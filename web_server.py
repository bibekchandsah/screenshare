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
    def __init__(self, host='0.0.0.0', port=8080):
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
        
    def generate_security_code(self, length=6):
        """Generate a random alphanumeric security code"""
        characters = string.ascii_uppercase + string.digits
        self.security_code = ''.join(random.choice(characters) for _ in range(length))
        return self.security_code
    
    def capture_screen_loop(self):
        """Continuously capture screen and update current frame"""
        sct = mss()
        
        while self.sharing:
            try:
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
                        
                    except Exception as cursor_error:
                        # Cursor drawing failed, continue without cursor
                        pass
                
                # High-quality capture with minimal downscaling for zoom clarity
                scale_percent = 100  # Full resolution for maximum detail when zooming
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                
                # Only resize if scaling is needed, use best quality interpolation
                if scale_percent != 100:
                    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LANCZOS4)
                
                # Encode image to JPEG format with maximum quality
                encode_param = [
                    int(cv2.IMWRITE_JPEG_QUALITY), 95,  # Maximum practical quality
                    int(cv2.IMWRITE_JPEG_OPTIMIZE), 1,   # Optimize encoding
                    int(cv2.IMWRITE_JPEG_PROGRESSIVE), 1  # Progressive JPEG for better streaming
                ]
                result, encoded_img = cv2.imencode('.jpg', img, encode_param)
                
                # Update current frame
                with self.frame_lock:
                    self.current_frame = encoded_img.tobytes()
                
                # Control frame rate (20 FPS for smooth high-quality experience)
                time.sleep(0.05)  # 20 FPS
                
            except Exception as e:
                print(f"[-] Error capturing screen: {e}")
                time.sleep(1)
        
        sct.close()
    
    def get_current_frame(self):
        """Get the current frame as JPEG bytes"""
        with self.frame_lock:
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
                    # Simple health check endpoint
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'status': 'ok', 'sharing': server_instance.sharing})
                    self.wfile.write(response.encode())
                
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
                    
                    # Track this stream
                    client_ip = self.client_address[0]
                    server_instance.active_streams[session_id] = client_ip
                    print(f"[*] Stream started for session {session_id} from {client_ip}")
                    print(f"[*] Active viewers: {len(server_instance.active_streams)}")
                    
                    # Send MJPEG stream headers
                    self.send_response(200)
                    self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    
                    try:
                        while server_instance.sharing and session_id in server_instance.authorized_sessions:
                            frame = server_instance.get_current_frame()
                            
                            if frame:
                                # Send frame in MJPEG format
                                self.wfile.write(b'--frame\r\n')
                                self.wfile.write(b'Content-Type: image/jpeg\r\n')
                                self.wfile.write(f'Content-Length: {len(frame)}\r\n'.encode())
                                self.wfile.write(b'\r\n')
                                self.wfile.write(frame)
                                self.wfile.write(b'\r\n')
                                self.wfile.flush()
                            
                            time.sleep(0.1)  # 10 FPS
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        # Client disconnected gracefully
                        print(f"[*] Client {client_ip} (session {session_id}) disconnected")
                    except Exception as e:
                        print(f"[-] Stream error for session {session_id}: {e}")
                    finally:
                        # Remove from active streams
                        if session_id in server_instance.active_streams:
                            del server_instance.active_streams[session_id]
                        print(f"[*] Stream ended for {client_ip}")
                        print(f"[*] Active viewers: {len(server_instance.active_streams)}")
                
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
        print("[*] Multi-user support enabled")
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
