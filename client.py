import socket
import pickle
import struct
import cv2
import numpy as np
import time

class ScreenShareClient:
    def __init__(self):
        self.client_socket = None
        self.connected = False
        self.host = None
        self.port = None
        self.security_code = None
        self.auto_reconnect = True
        self.max_reconnect_attempts = 3
        
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
            response = self.client_socket.recv(1024).decode('utf-8').strip()
            if show_debug:
                print(f"[DEBUG] Server response: '{response}'")
            
            if response == "AUTHORIZED":
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
        except Exception as e:
            print(f"[-] Connection error: {e}")
            return False
    
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
    
    def receive_frames(self):
        """Receive and display screen frames from server"""
        data = b""
        payload_size = struct.calcsize("L")
        
        print("[*] Receiving screen feed...")
        print("[*] Press 'q' to quit or ESC to quit with confirmation\n")
        
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
                    
                    # Display the frame
                    cv2.imshow('Screen Share - Press Q to quit', img)
                    
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
