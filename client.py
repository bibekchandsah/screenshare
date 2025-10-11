import socket
import pickle
import struct
import cv2
import numpy as np

class ScreenShareClient:
    def __init__(self):
        self.client_socket = None
        self.connected = False
        
    def connect_to_server(self, host, port, security_code):
        """Connect to the screen sharing server with security code"""
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            
            print(f"[DEBUG] Sending security code: '{security_code}'")
            print(f"[DEBUG] Code length: {len(security_code)}")
            
            # Send security code with newline
            self.client_socket.send((security_code + '\n').encode('utf-8'))
            
            # Wait for authorization response
            response = self.client_socket.recv(1024).decode('utf-8').strip()
            print(f"[DEBUG] Server response: '{response}'")
            
            if response == "AUTHORIZED":
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
    
    def receive_frames(self):
        """Receive and display screen frames from server"""
        data = b""
        payload_size = struct.calcsize("L")
        
        print("[*] Receiving screen feed...")
        print("[*] Press 'q' to quit\n")
        
        try:
            while self.connected:
                # Retrieve message size
                while len(data) < payload_size:
                    packet = self.client_socket.recv(4096)
                    if not packet:
                        return
                    data += packet
                
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]
                
                # Retrieve the full frame data
                while len(data) < msg_size:
                    data += self.client_socket.recv(4096)
                
                frame_data = data[:msg_size]
                data = data[msg_size:]
                
                # Deserialize frame
                frame = pickle.loads(frame_data)
                
                # Decode image
                img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                
                # Display the frame
                cv2.imshow('Screen Share - Press Q to quit', img)
                
                # Break on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except Exception as e:
            print(f"[-] Error receiving frames: {e}")
        finally:
            self.disconnect()
    
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
