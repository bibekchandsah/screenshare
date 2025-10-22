import socket
import pickle
import struct
import cv2
import numpy as np
import time
import os
import sys

class ScreenShareClient:
    def __init__(self):
        self.client_socket = None
        self.connected = False
        self.host = None
        self.port = None
        self.security_code = None
        self.auto_reconnect = True
        self.max_reconnect_attempts = 3
        self.window_name = 'Screen Share - Multi-User Optimized (Press q to Quit)'
        self.window_created = False
        
        # Multi-user optimized quality system
        self.quality = "MEDIUM"  # Default quality
        self.quality_scales = {
            'LOW': 0.6,      # 60% scale for bandwidth conservation
            'MEDIUM': 0.8,   # 80% scale for balanced performance
            'HIGH': 1.0      # Full quality for best visual experience
        }
        self.server_quality = "MEDIUM"  # Quality requested from server
        self.show_quality_menu = False
        self.quality_menu_rect = None
        
        # Performance monitoring
        self.frame_count = 0
        self.fps_counter = 0
        self.last_fps_time = time.time()
        self.performance_stats = {
            'frames_received': 0,
            'avg_fps': 0,
            'last_frame_time': 0,
            'connection_quality': 'Good'
        }
        
        # Zoom feature
        self.is_zoomed = False
        self.zoom_center = None
        self.zoom_level = 2.0  # 2x zoom
        self.original_frame = None
        self.current_frame_size = None  # Store current frame dimensions
        # Drag feature for zoom
        self.is_dragging = False
        self.drag_start = None
        
        # Multi-user awareness
        self.adaptive_quality = True  # Automatically adjust quality based on performance
        self.connection_timeout = 5.0  # Timeout for server communication
        
    def connect_to_server(self, host, port, security_code, show_debug=True):
        """Connect to the screen sharing server with security code"""
        # Store connection details for reconnection
        self.host = host
        self.port = port
        self.security_code = security_code
        
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            
            if show_debug:
                print(f"[DEBUG] Sending security code: '{security_code}'")
                print(f"[DEBUG] Code length: {len(security_code)}")
            
            # Send security code with newline
            self.client_socket.send((security_code + '\n').encode('utf-8'))
            
            # Wait for authorization response
            try:
                response = self.client_socket.recv(1024).decode('utf-8').strip()
                if show_debug:
                    print(f"[DEBUG] Server response: '{response}'")
            except UnicodeDecodeError:
                print("[-] Connection error: Invalid server response")
                self.client_socket.close()
                return False
            
            if response == "WAITING_APPROVAL":
                # Server is waiting for manual approval
                print("[*] Waiting for server to approve connection...")
                print("[*] Please wait while the server operator reviews your request.\n")
                
                # Set a timeout for waiting approval (60 seconds)
                self.client_socket.settimeout(60.0)
                
                try:
                    approval_response = self.client_socket.recv(1024).decode('utf-8').strip()
                    
                    if approval_response == "APPROVED":
                        if show_debug:
                            print("[+] Successfully connected to server!")
                            print("[*] Server streaming in HIGH quality")
                            print("[*] You can adjust quality from the window if needed")
                        
                        self.connected = True
                        self.client_socket.settimeout(None)  # Remove timeout
                        return True
                    elif approval_response == "REJECTED":
                        print("[-] Server connection rejected!")
                        print("[-] Try again in a few moments!")
                        self.client_socket.close()
                        return False
                    else:
                        print(f"[-] Unexpected response: {approval_response}")
                        self.client_socket.close()
                        return False
                        
                except socket.timeout:
                    print("[-] Connection approval timeout!")
                    print("[-] Server did not respond in time. Try again later.")
                    self.client_socket.close()
                    return False
                except UnicodeDecodeError:
                    print("[-] Server connection rejected!")
                    print("[-] Try again in a few moments!")
                    self.client_socket.close()
                    return False
                except (ConnectionResetError, ConnectionAbortedError, OSError):
                    print("[-] Server connection rejected!")
                    print("[-] Try again in a few moments!")
                    self.client_socket.close()
                    return False
                    
            elif response == "AUTHORIZED":
                # Old behavior for backward compatibility
                if show_debug:
                    print("[+] Successfully connected to server!")
                self.connected = True
                return True
            else:
                print("[-] Unauthorized - Wrong security code!")
                self.client_socket.close()
                return False
                
        except ConnectionRefusedError:
            print("[-] Connection refused. Make sure the server is running.")
            return False
        except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
            if "connection" in str(e).lower() or "reset" in str(e).lower():
                print("[-] Server closed the connection unexpectedly")
                print("[-] The connection may have been rejected")
            else:
                print(f"[-] Connection error: {e}")
            return False
        except UnicodeDecodeError:
            print("[-] Connection error: Invalid server response")
            print("[-] The connection may have been rejected")
            return False
        except Exception as e:
            print(f"[-] Connection error: {e}")
            return False
    
    def send_quality_change(self, new_quality):
        """Send quality change request to server (multi-user optimized)"""
        if not self.connected or not self.client_socket:
            return False
        
        try:
            quality_msg = f"QUALITY:{new_quality}"
            self.client_socket.send(quality_msg.encode())
            self.server_quality = new_quality
            print(f"[📺] Requested quality change to {new_quality} from server")
            return True
        except Exception as e:
            print(f"[-] Failed to send quality change: {e}")
            return False
    
    def update_performance_stats(self):
        """Update performance statistics for multi-user optimization"""
        current_time = time.time()
        self.fps_counter += 1
        
        # Calculate FPS every second
        if current_time - self.last_fps_time >= 1.0:
            self.performance_stats['avg_fps'] = self.fps_counter / (current_time - self.last_fps_time)
            self.performance_stats['frames_received'] = self.frame_count
            
            # Determine connection quality based on FPS
            fps = self.performance_stats['avg_fps']
            if fps >= 20:
                self.performance_stats['connection_quality'] = 'Excellent'
            elif fps >= 15:
                self.performance_stats['connection_quality'] = 'Good'
            elif fps >= 10:
                self.performance_stats['connection_quality'] = 'Fair'
            else:
                self.performance_stats['connection_quality'] = 'Poor'
            
            # Adaptive quality adjustment based on performance
            if self.adaptive_quality:
                if fps < 10 and self.server_quality != 'LOW':
                    print(f"[⚡] Low FPS ({fps:.1f}), automatically switching to LOW quality")
                    self.quality = 'LOW'
                    self.server_quality = 'LOW'
                    self.send_quality_change('LOW')
                elif fps > 25 and self.server_quality != 'HIGH':
                    print(f"[⚡] High FPS ({fps:.1f}), automatically switching to HIGH quality")
                    self.quality = 'HIGH'
                    self.server_quality = 'HIGH'
                    self.send_quality_change('HIGH')
            
            # Reset counters
            self.fps_counter = 0
            self.last_fps_time = current_time
            
            # Log performance occasionally
            if self.frame_count % 1000 == 0 and self.frame_count > 0:  # Every ~33 seconds at 30 FPS
                print(f"[📊] Performance: {fps:.1f} FPS, "
                      f"Quality: {self.server_quality}, "
                      f"Connection: {self.performance_stats['connection_quality']}")
        
        self.performance_stats['last_frame_time'] = current_time
        self.frame_count += 1
    
    def attempt_reconnection(self):
        """Try to reconnect to the server"""
        for attempt in range(1, self.max_reconnect_attempts + 1):
            print(f"\n[*] Reconnection attempt {attempt}/{self.max_reconnect_attempts}...")
            time.sleep(2)  # Wait before reconnecting
            
            if self.connect_to_server(self.host, self.port, self.security_code, show_debug=False):
                print("[+] Reconnected successfully!")
                return True
        
        print(f"\n[-] Failed to reconnect after {self.max_reconnect_attempts} attempts")
        return False
    
    def draw_quality_selector(self, frame):
        """Draw quality selector button and dropdown menu on frame"""
        height, width = frame.shape[:2]
        
        # Scale button size proportionally to frame dimensions
        # Use clamped scale ratio to prevent UI from becoming too large or too small
        base_width = 1500
        scale_ratio = width / base_width
        
        # Clamp scale ratio between 0.15 and 1.5 to keep UI reasonable
        scale_ratio = max(0.15, min(scale_ratio, 1.5))
        
        # Button dimensions scaled to frame size with minimum sizes
        button_width = max(int(150 * scale_ratio), 120)   # Min 120px, max ~225px
        button_height = max(int(35 * scale_ratio), 28)    # Min 28px
        margin = max(int(10 * scale_ratio), 8)            # Min 8px
        
        # Position from top-right corner
        button_x = width - button_width - margin
        button_y = margin
        
        # Ensure button fits within frame
        if button_x < 5:
            button_x = 5
        if button_y < 5:
            button_y = 5
        
        # Button background
        cv2.rectangle(frame, (button_x, button_y), 
                     (button_x + button_width, button_y + button_height),
                     (50, 50, 50), -1)
        
        # Button border
        border_color = (0, 255, 0) if self.show_quality_menu else (100, 100, 100)
        border_thickness = max(int(2 * scale_ratio), 1)
        cv2.rectangle(frame, (button_x, button_y), 
                     (button_x + button_width, button_y + button_height),
                     border_color, border_thickness)
        
        # Button text - scaled font size with limits
        text = f"Quality: {self.quality}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = max(min(0.4 * scale_ratio, 0.5), 0.32)  # Between 0.32 and 0.5
        font_thickness = max(int(1 * scale_ratio), 1)
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = button_x + (button_width - text_size[0]) // 2
        text_y = button_y + (button_height + text_size[1]) // 2
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
        
        # Store button rectangle for click detection
        self.quality_menu_rect = (button_x, button_y, button_width, button_height)
        
        # Draw dropdown menu if active
        if self.show_quality_menu:
            menu_gap = max(int(5 * scale_ratio), 4)
            menu_y = button_y + button_height + menu_gap
            menu_height = max(int(105 * scale_ratio), 90)  # Min 90px for 3 options
            
            # Ensure menu fits within frame
            if menu_y + menu_height > height:
                menu_y = max(button_y - menu_height - menu_gap, 5)
            
            # Menu background
            cv2.rectangle(frame, (button_x, menu_y), 
                         (button_x + button_width, menu_y + menu_height),
                         (40, 40, 40), -1)
            
            # Menu border
            cv2.rectangle(frame, (button_x, menu_y), 
                         (button_x + button_width, menu_y + menu_height),
                         (100, 100, 100), border_thickness)
            
            # Menu options
            options = ['HIGH', 'MEDIUM', 'LOW']
            option_height = max(int(30 * scale_ratio), 26)  # Min 26px per option
            padding = max(int(5 * scale_ratio), 4)
            
            for i, option in enumerate(options):
                opt_y = menu_y + padding + (i * option_height)
                
                # Highlight selected option
                if option == self.quality:
                    cv2.rectangle(frame, (button_x + padding, opt_y), 
                                 (button_x + button_width - padding, opt_y + option_height - padding),
                                 (0, 120, 0), -1)
                
                # Option text with description
                if option == 'HIGH':
                    opt_text = "HIGH (Best)"
                    opt_color = (0, 255, 0)
                elif option == 'MEDIUM':
                    opt_text = "MEDIUM (Balanced)"
                    opt_color = (0, 200, 255)
                else:
                    opt_text = "LOW (Fast)"
                    opt_color = (0, 150, 255)
                
                text_y_offset = max(int(18 * scale_ratio), 16)
                text_x_offset = max(int(10 * scale_ratio), 8)
                menu_font_scale = max(min(0.35 * scale_ratio, 0.42), 0.28)
                cv2.putText(frame, opt_text, (button_x + text_x_offset, opt_y + text_y_offset), 
                           font, menu_font_scale, opt_color, font_thickness)
            
            # Store menu rectangles for click detection
            self.menu_options_rects = {
                'HIGH': (button_x, menu_y + padding, button_width, option_height),
                'MEDIUM': (button_x, menu_y + padding + option_height, button_width, option_height),
                'LOW': (button_x, menu_y + padding + (2 * option_height), button_width, option_height)
            }
        
        return frame
    
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse clicks on quality selector, zoom, and drag"""
        # Handle left button down
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if clicked on quality button
            if self.quality_menu_rect:
                bx, by, bw, bh = self.quality_menu_rect
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    self.show_quality_menu = not self.show_quality_menu
                    return
            
            # Check if clicked on menu options
            if self.show_quality_menu and hasattr(self, 'menu_options_rects'):
                for quality, (mx, my, mw, mh) in self.menu_options_rects.items():
                    if mx <= x <= mx + mw and my <= y <= my + mh:
                        old_quality = self.quality
                        self.quality = quality
                        self.show_quality_menu = False
                        
                        # Send quality change to server for multi-user optimization
                        success = self.send_quality_change(quality)
                        
                        if success:
                            print(f"\n[📺] Quality changed: {old_quality} → {self.quality}")
                            print(f"[⚡] Server notified for optimized streaming")
                        else:
                            print(f"\n[*] Quality changed locally: {old_quality} → {self.quality}")
                            print(f"[!] Server communication failed - using client-side scaling")
                        
                        # Disable adaptive quality temporarily after manual change
                        self.adaptive_quality = False
                        
                        # Re-enable adaptive quality after 2 minutes
                        import threading
                        def re_enable_adaptive():
                            time.sleep(120)  # 2 minutes
                            self.adaptive_quality = True
                            print("[⚡] Adaptive quality re-enabled")
                        
                        threading.Thread(target=re_enable_adaptive, daemon=True).start()
                        return
            
            # Handle zoom toggle and drag start (only if not clicking on UI elements)
            if not self.show_quality_menu:
                if self.is_zoomed:
                    # Start dragging when already zoomed
                    self.is_dragging = True
                    self.drag_start = (x, y)
                else:
                    # Zoom in at clicked position
                    # Convert window coordinates to frame coordinates
                    frame_coords = self.window_to_frame_coords(x, y)
                    if frame_coords:
                        self.is_zoomed = True
                        self.zoom_center = frame_coords
                        print(f"\n[*] Zoom: ON at window ({x}, {y}) -> frame {frame_coords}")
                        print("[*] Hold and drag to pan around")
                return
        
        # Handle mouse movement while dragging
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.is_zoomed and self.is_dragging and self.drag_start and self.current_frame_size:
                # Calculate drag offset in window coordinates
                dx = x - self.drag_start[0]
                dy = y - self.drag_start[1]
                
                # Convert drag offset to frame coordinates based on current scaling
                # Get window size
                try:
                    window_rect = cv2.getWindowImageRect(self.window_name)
                    window_width = window_rect[2]
                    window_height = window_rect[3]
                    
                    if window_width > 0 and window_height > 0 and self.current_frame_size:
                        frame_width, frame_height = self.current_frame_size
                        
                        # Calculate scale factor between window and frame
                        scale_x = frame_width / window_width
                        scale_y = frame_height / window_height
                        
                        # Convert drag offset to frame space
                        frame_dx = int(dx * scale_x)
                        frame_dy = int(dy * scale_y)
                        
                        # Update zoom center (move in opposite direction for natural feel)
                        if self.zoom_center:
                            new_x = self.zoom_center[0] - frame_dx
                            new_y = self.zoom_center[1] - frame_dy
                            self.zoom_center = (new_x, new_y)
                except:
                    pass
                
                # Update drag start position for next movement
                self.drag_start = (x, y)
        
        # Handle left button up
        elif event == cv2.EVENT_LBUTTONUP:
            if self.is_dragging:
                self.is_dragging = False
                self.drag_start = None
        
        # Handle right button click to zoom out
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.is_zoomed:
                self.is_zoomed = False
                self.zoom_center = None
                self.is_dragging = False
                self.drag_start = None
                print("\n[*] Zoom: OFF")
    
    def window_to_frame_coords(self, window_x, window_y):
        """Convert window coordinates to frame coordinates"""
        try:
            # Get window size
            window_rect = cv2.getWindowImageRect(self.window_name)
            window_width = window_rect[2]
            window_height = window_rect[3]
            
            if window_width <= 0 or window_height <= 0 or not self.current_frame_size:
                return None
            
            frame_width, frame_height = self.current_frame_size
            
            # Calculate the aspect ratio scaling that was applied
            img_aspect = frame_width / frame_height
            window_aspect = window_width / window_height
            
            if img_aspect > window_aspect:
                # Image is wider - fit to width
                displayed_width = window_width
                displayed_height = int(window_width / img_aspect)
                x_offset = 0
                y_offset = (window_height - displayed_height) // 2
            else:
                # Image is taller - fit to height
                displayed_height = window_height
                displayed_width = int(window_height * img_aspect)
                y_offset = 0
                x_offset = (window_width - displayed_width) // 2
            
            # Check if click is within the displayed frame area
            if (window_x < x_offset or window_x > x_offset + displayed_width or
                window_y < y_offset or window_y > y_offset + displayed_height):
                return None
            
            # Convert to frame coordinates
            frame_x = int((window_x - x_offset) * frame_width / displayed_width)
            frame_y = int((window_y - y_offset) * frame_height / displayed_height)
            
            # Clamp to frame bounds
            frame_x = max(0, min(frame_x, frame_width - 1))
            frame_y = max(0, min(frame_y, frame_height - 1))
            
            return (frame_x, frame_y)
        except:
            return None
    
    def apply_zoom(self, img, click_x, click_y):
        """Apply zoom effect centered at the clicked position"""
        img_height, img_width = img.shape[:2]
        
        # Calculate the region to extract (smaller region = more zoom)
        extract_width = int(img_width / self.zoom_level)
        extract_height = int(img_height / self.zoom_level)
        
        # Calculate extraction boundaries centered on click position
        x1 = max(0, click_x - extract_width // 2)
        y1 = max(0, click_y - extract_height // 2)
        x2 = min(img_width, x1 + extract_width)
        y2 = min(img_height, y1 + extract_height)
        
        # Adjust if we hit boundaries
        if x2 - x1 < extract_width:
            x1 = max(0, x2 - extract_width)
        if y2 - y1 < extract_height:
            y1 = max(0, y2 - extract_height)
        
        # Extract the region
        zoomed_region = img[y1:y2, x1:x2]
        
        # Scale up to original image size
        zoomed_img = cv2.resize(zoomed_region, (img_width, img_height), interpolation=cv2.INTER_LINEAR)
        
        # Add a visual indicator (border) to show zoom is active
        border_color = (0, 255, 255)  # Yellow border
        border_thickness = 3
        cv2.rectangle(zoomed_img, (0, 0), (img_width - 1, img_height - 1), border_color, border_thickness)
        
        # Add zoom indicator text
        zoom_text = f"ZOOM {self.zoom_level}x"
        drag_text = "Drag to Pan | Right-click to Exit"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 2
        
        # Main zoom text
        text_size = cv2.getTextSize(zoom_text, font, font_scale, font_thickness)[0]
        text_x = 10
        text_y = 30
        
        # Text background
        cv2.rectangle(zoomed_img, (text_x - 5, text_y - text_size[1] - 5),
                     (text_x + text_size[0] + 5, text_y + 5), (0, 0, 0), -1)
        # Text
        cv2.putText(zoomed_img, zoom_text, (text_x, text_y), font, font_scale, 
                   border_color, font_thickness)
        
        # Drag instruction text (smaller)
        drag_font_scale = 0.4
        drag_font_thickness = 1
        drag_text_size = cv2.getTextSize(drag_text, font, drag_font_scale, drag_font_thickness)[0]
        drag_text_x = 10
        drag_text_y = text_y + 25
        
        # Drag text background
        cv2.rectangle(zoomed_img, (drag_text_x - 5, drag_text_y - drag_text_size[1] - 5),
                     (drag_text_x + drag_text_size[0] + 5, drag_text_y + 5), (0, 0, 0), -1)
        # Drag text
        cv2.putText(zoomed_img, drag_text, (drag_text_x, drag_text_y), font, drag_font_scale, 
                   (200, 200, 200), drag_font_thickness)
        
        return zoomed_img
    
    def resize_with_aspect_ratio(self, img, window_width, window_height):
        """Resize image to fit window while maintaining aspect ratio"""
        img_height, img_width = img.shape[:2]
        
        # Calculate aspect ratios
        img_aspect = img_width / img_height
        window_aspect = window_width / window_height
        
        # Determine scaling to fit within window while maintaining aspect ratio
        if img_aspect > window_aspect:
            # Image is wider - fit to width
            new_width = window_width
            new_height = int(window_width / img_aspect)
        else:
            # Image is taller - fit to height
            new_height = window_height
            new_width = int(window_height * img_aspect)
        
        # Resize image
        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        
        # Create black canvas with window size
        canvas = np.zeros((window_height, window_width, 3), dtype=np.uint8)
        
        # Center the resized image on canvas
        y_offset = (window_height - new_height) // 2
        x_offset = (window_width - new_width) // 2
        canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized
        
        return canvas
    
    def receive_frames(self):
        """Receive and display screen frames from server"""
        data = b""
        payload_size = struct.calcsize("L")
        
        print("[*] Receiving screen feed...")
        print("[*] Press 'q' to quit or ESC to quit with confirmation")
        print("[*] Click 'Quality' button in top-right to adjust quality")
        print("[*] Left-click anywhere to ZOOM IN (2x)")
        print("[*] While zoomed: Hold and DRAG to pan around")
        print("[*] Right-click to ZOOM OUT")
        print("[*] Window is resizable - maximize or resize as needed")
        print("[*] Aspect ratio is maintained when resizing\n")
        
        # Create a named window with normal flag (resizable) and keep aspect ratio
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        
        # Set initial window size (1280x720 is a good default)
        cv2.resizeWindow(self.window_name, 1280, 720)
        
        # Set window icon (Windows only) - Must be done after window is created and sized
        if os.name == 'nt':  # Windows
            try:
                # Get the directory where the script is located
                script_dir = os.path.dirname(os.path.abspath(__file__))
                icon_path = os.path.join(script_dir, 'icon.ico')
                
                # Check if icon exists
                if os.path.exists(icon_path):
                    import ctypes
                    
                    # Small delay to ensure window is fully created
                    time.sleep(0.1)
                    
                    # Get window handle - try multiple times as window may not be ready immediately
                    hwnd = None
                    for attempt in range(5):
                        hwnd = ctypes.windll.user32.FindWindowW(None, self.window_name)
                        if hwnd:
                            break
                        time.sleep(0.05)
                    
                    if hwnd:
                        # Load icon using LoadImage for better compatibility
                        IMAGE_ICON = 1
                        LR_LOADFROMFILE = 0x0010
                        LR_DEFAULTSIZE = 0x0040
                        
                        # Load small icon (16x16) for title bar
                        hicon_small = ctypes.windll.user32.LoadImageW(
                            0, icon_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE
                        )
                        
                        # Load large icon (32x32) for taskbar and Alt+Tab
                        hicon_large = ctypes.windll.user32.LoadImageW(
                            0, icon_path, IMAGE_ICON, 32, 32, LR_LOADFROMFILE
                        )
                        
                        # Set both icons
                        WM_SETICON = 0x0080
                        ICON_SMALL = 0  # Small icon (title bar)
                        ICON_BIG = 1    # Large icon (taskbar, Alt+Tab)
                        
                        if hicon_small:
                            ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
                        if hicon_large:
                            ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_large)
                        
                        # Force taskbar to update
                        ctypes.windll.user32.UpdateWindow(hwnd)
            except Exception as e:
                # Icon setting failed, continue without icon
                pass
        
        # Set mouse callback
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        self.window_created = True
        
        try:
            while self.connected:
                try:
                    # Retrieve message size
                    while len(data) < payload_size:
                        packet = self.client_socket.recv(4096)
                        if not packet:
                            # Connection lost
                            print("\n[!] Connection lost to server")
                            if self.auto_reconnect:
                                if self.attempt_reconnection():
                                    data = b""  # Reset data buffer
                                    continue
                            return
                        data += packet
                    
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0]
                    
                    # Retrieve the full frame data
                    while len(data) < msg_size:
                        packet = self.client_socket.recv(4096)
                        if not packet:
                            print("\n[!] Connection lost to server")
                            if self.auto_reconnect:
                                if self.attempt_reconnection():
                                    data = b""
                                    continue
                            return
                        data += packet
                    
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    
                    # Deserialize frame
                    frame = pickle.loads(frame_data)
                    
                    # Decode image
                    img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    
                    # Store original frame for zoom
                    self.original_frame = img.copy()
                    
                    # Apply client-side quality scaling
                    scale_factor = self.quality_scales.get(self.quality, 0.75)
                    if scale_factor < 1.0:
                        new_width = int(img.shape[1] * scale_factor)
                        new_height = int(img.shape[0] * scale_factor)
                        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
                    
                    # Store current frame size for coordinate conversion
                    self.current_frame_size = (img.shape[1], img.shape[0])
                    
                    # Apply zoom if active
                    if self.is_zoomed and self.zoom_center:
                        img = self.apply_zoom(img, self.zoom_center[0], self.zoom_center[1])
                    
                    # Get current window size
                    window_rect = cv2.getWindowImageRect(self.window_name)
                    window_width = window_rect[2]
                    window_height = window_rect[3]
                    
                    # Resize image to fit window while maintaining aspect ratio
                    if window_width > 0 and window_height > 0:
                        img = self.resize_with_aspect_ratio(img, window_width, window_height)
                    
                    # Draw quality selector overlay
                    img = self.draw_quality_selector(img)
                    
                    # Display the frame
                    cv2.imshow(self.window_name, img)
                    
                    # Update performance statistics for multi-user optimization
                    self.update_performance_stats()
                    
                    # Check for key press
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        # Quit with confirmation
                        if self.confirm_quit():
                            break
                    elif key == 27:  # ESC key
                        if self.confirm_quit():
                            break
                
                except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                    print("\n[!] Connection interrupted")
                    if self.auto_reconnect:
                        if self.attempt_reconnection():
                            data = b""
                            continue
                    break
                except Exception as e:
                    print(f"\n[-] Error receiving frame: {e}")
                    if self.auto_reconnect and "connection" in str(e).lower():
                        if self.attempt_reconnection():
                            data = b""
                            continue
                    break
                    
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
        finally:
            self.disconnect()
    
    def confirm_quit(self):
        """Ask user to confirm before quitting"""
        print("\n" + "="*50)
        confirm = input("Are you sure you want to quit? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            return True
        else:
            print("[*] Continuing screen share...")
            return False
    
    def disconnect(self):
        """Disconnect from the server"""
        print("\n[*] Disconnecting...")
        self.connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        
        cv2.destroyAllWindows()
        print("[*] Disconnected")

def main():
    print("="*50)
    print("SCREEN SHARING CLIENT")
    print("="*50)
    
    # Get connection details from user
    host = input("\nEnter server IP address (or 'localhost' for same PC): ").strip()
    if not host:
        host = 'localhost'
    
    port_input = input("Enter server port (default: 5555): ").strip()
    port = int(port_input) if port_input else 5555
    
    security_code = input("Enter the security code: ").strip().upper()
    
    if not security_code:
        print("[-] Security code is required!")
        return
    
    print("\n[*] Quality can be adjusted from the viewer window")
    print("[*] Look for the 'Quality' button in the top-right corner\n")
    
    # Create client and connect
    client = ScreenShareClient()
    
    if client.connect_to_server(host, port, security_code):
        try:
            client.receive_frames()
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
            client.disconnect()
    else:
        print("[-] Failed to connect to server")

if __name__ == "__main__":
    main()
