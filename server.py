import socket
import threading
import pickle
import struct
import random
import string
from mss import mss
import cv2
import numpy as np
from datetime import datetime

class ScreenShareServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.security_code = None
        self.clients = []
        self.sharing = False
        
    def generate_security_code(self, length=6):
        """Generate a random alphanumeric security code"""
        characters = string.ascii_uppercase + string.digits
        self.security_code = ''.join(random.choice(characters) for _ in range(length))
        return self.security_code
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        print(f"[*] Connection from {address}")
        
        # Create a separate mss instance for this thread
        sct = mss()
        
        try:
            # Receive security code from client
            received_code = client_socket.recv(1024).decode('utf-8').strip()
            
            print(f"[DEBUG] Expected code: '{self.security_code}' (length: {len(self.security_code)})")
            print(f"[DEBUG] Received code: '{received_code}' (length: {len(received_code)})")
            print(f"[DEBUG] Codes match: {received_code == self.security_code}")
            
            if received_code == self.security_code:
                client_socket.send(b"AUTHORIZED\n")
                print(f"[+] Client {address} authorized successfully")
                
                self.clients.append(client_socket)
                
                # Stream screen to this client
                while self.sharing:
                    try:
                        # Capture screen using thread-local mss instance
                        monitor = sct.monitors[1]
                        screenshot = sct.grab(monitor)
                        
                        # Convert to numpy array
                        img = np.array(screenshot)
                        
                        # Convert BGRA to BGR (remove alpha channel)
                        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                        
                        # Resize to reduce bandwidth
                        scale_percent = 60
                        width = int(img.shape[1] * scale_percent / 100)
                        height = int(img.shape[0] * scale_percent / 100)
                        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
                        
                        # Encode image to JPEG format
                        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                        result, encoded_img = cv2.imencode('.jpg', img, encode_param)
                        
                        # Serialize and send frame
                        data = pickle.dumps(encoded_img)
                        message_size = struct.pack("L", len(data))
                        
                        client_socket.sendall(message_size + data)
                        
                    except (ConnectionResetError, BrokenPipeError):
                        print(f"[-] Client {address} disconnected")
                        break
                    except Exception as e:
                        print(f"[-] Error sending to {address}: {e}")
                        break
            else:
                client_socket.send(b"UNAUTHORIZED\n")
                print(f"[-] Client {address} provided wrong code: '{received_code}'")
                
        except Exception as e:
            print(f"[-] Error handling client {address}: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            sct.close()  # Close the thread-local mss instance
    
    def start_sharing(self):
        """Start the screen sharing server"""
        # Generate security code
        code = self.generate_security_code()
        print("\n" + "="*50)
        print(f"SECURITY CODE: {code}")
        print("="*50)
        print("Share this code with the person who wants to view your screen")
        print("="*50 + "\n")
        
        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.sharing = True
            
            print(f"[*] Server listening on {self.host}:{self.port}")
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
