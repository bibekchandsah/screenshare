"""
Test script to verify server approval/rejection works correctly
"""
import socket
import time
import threading

def test_client_connection(host, port, security_code, test_name):
    """Test client connection to server"""
    print(f"\n{'='*50}")
    print(f"Testing: {test_name}")
    print(f"{'='*50}")
    
    try:
        # Create client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10.0)  # 10 second timeout
        
        print(f"[*] Connecting to {host}:{port}")
        client_socket.connect((host, port))
        
        # Send security code
        print(f"[*] Sending security code: {security_code}")
        client_socket.send((security_code + '\n').encode('utf-8'))
        
        # Wait for response
        print("[*] Waiting for server response...")
        response = client_socket.recv(1024).decode('utf-8').strip()
        print(f"[*] Server response: {response}")
        
        if response == "WAITING_APPROVAL":
            print("[*] Server is asking for approval...")
            print("[*] Check the server console for approval prompt")
            
            # Wait for approval response
            print("[*] Waiting for approval result...")
            approval_response = client_socket.recv(1024).decode('utf-8').strip()
            print(f"[*] Approval result: {approval_response}")
            
            if approval_response == "APPROVED":
                print("✅ Connection approved!")
                print("[*] Would start receiving frames here...")
            elif approval_response == "REJECTED":
                print("❌ Connection rejected!")
            else:
                print(f"❓ Unexpected approval response: {approval_response}")
                
        elif response == "UNAUTHORIZED":
            print("❌ Unauthorized - Wrong security code!")
        else:
            print(f"❓ Unexpected response: {response}")
            
    except socket.timeout:
        print("⏱️  Connection timeout!")
    except ConnectionRefusedError:
        print("❌ Connection refused - Is server running?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass
        print(f"[*] {test_name} completed")

def run_test():
    print("="*60)
    print("        SERVER APPROVAL SYSTEM TEST")
    print("="*60)
    print("\nThis script tests the server approval system.")
    print("Make sure the server is running before starting tests.")
    print("\nInstructions:")
    print("1. Start the server (python main.py → option 1)")
    print("2. Note the IP and security code")
    print("3. Enter them below to test")
    print("="*60)
    
    # Get connection details
    host = input("\nEnter server IP address: ").strip()
    if not host:
        host = 'localhost'
    
    port_input = input("Enter server port (default: 5555): ").strip()
    port = int(port_input) if port_input else 5555
    
    security_code = input("Enter the security code: ").strip().upper()
    
    if not security_code:
        print("❌ Security code is required!")
        return
    
    print(f"\n[*] Testing connection to {host}:{port} with code '{security_code}'")
    print("[*] The server should show an approval prompt")
    
    # Test with correct code
    test_client_connection(host, port, security_code, "Correct Security Code Test")
    
    # Ask if user wants to test wrong code
    print("\n" + "="*60)
    test_wrong = input("Test with wrong security code? (y/n): ").strip().lower()
    if test_wrong in ['y', 'yes']:
        wrong_code = "WRONGCODE"
        test_client_connection(host, port, wrong_code, "Wrong Security Code Test")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    run_test()