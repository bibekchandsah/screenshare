# Real-Time Screen Sharing Application

A Python-based screen sharing application with security code authentication. Share your screen securely with others in real-time!

## Features

- 🔒 **Secure Connection**: Random security code generation for each session
- 📺 **Real-time Streaming**: Live screen capture and streaming
- 🚀 **Easy to Use**: Simple menu-driven interface
- 🔌 **Network Support**: Works over LAN or localhost
- 👥 **Multiple Viewers**: Support for multiple simultaneous viewers
- 🎯 **Unified Launcher**: Single entry point with menu options

## Requirements

- Python 3.7 or higher
- Windows/Linux/macOS

## Installation

1. **Clone or download this repository**

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start (Recommended)

Simply run the main application and choose what you want to do:

```bash
python main.py
```

You'll see a menu with four options:

```
============================================================
               SCREEN SHARING APPLICATION
============================================================

Choose an option:

  [1] Share My Screen (Desktop App)
  [2] Share My Screen (Web Browser - Mobile Friendly)
  [3] View Someone's Screen (Desktop App)
  [4] Exit

------------------------------------------------------------

Enter your choice (1/2/3/4):
```

#### Option 1: Share My Screen (Desktop App)

1. Select option **1** from the menu
2. A **security code** will be generated and displayed (e.g., `XGFRDW`)
3. Share this code with the person who wants to view your screen
4. The server will start listening for connections
5. When someone connects with the correct code, you'll be asked to approve the connection
6. Press `Ctrl+C` to stop sharing and return to the menu

**Example Output:**
```
🖥️  SHARE MY SCREEN MODE
============================================================

==================================================
SECURITY CODE: XGFRDW
==================================================
Share this code with the person who wants to view your screen
==================================================

[*] Server listening on 0.0.0.0:5555
[*] Waiting for connections...
[*] Connection from ('127.0.0.1', 58210)
Do you want to allow this connection? (y/n): y
[+] Client ('127.0.0.1', 58210) connection approved
```

#### Option 2: Share My Screen (Web Browser - Mobile Friendly) 🆕

**Perfect for viewing on mobile phones, tablets, or any device with a browser!**

1. Select option **2** from the menu
2. A **security code** will be generated and displayed
3. The application will show URLs to access the screen share:
   ```
   Access the screen share from your browser at:
       http://192.168.1.100:8080
       http://localhost:8080
   ```
4. **On your mobile phone or any device:**
   - Make sure it's connected to the **same WiFi network** as your PC
   - Open a web browser (Chrome, Safari, Firefox, etc.)
   - Enter the URL shown (e.g., `http://192.168.1.100:8080`)
   - Enter the security code
   - Wait for server approval
   - View the screen in real-time!

5. Press `Ctrl+C` on the server to stop sharing

**Mobile Browser Features:**
- ✅ Responsive design - works on any screen size
- ✅ Touch-friendly interface
- ✅ No app installation required
- ✅ Works on iOS, Android, tablets, laptops
- ✅ Lower bandwidth usage optimized for mobile
- ✅ Smooth streaming at 10 FPS

**Example Output:**
```
🌐 WEB BROWSER SCREEN SHARE MODE
============================================================

==================================================
SECURITY CODE: XK9M2P
==================================================
Share this code with the person who wants to view your screen
==================================================

[*] Access the screen share from your browser at:
    http://192.168.1.100:8080
    http://localhost:8080

[*] Server starting on 0.0.0.0:8080
[*] Press Ctrl+C to stop sharing
```

#### Option 3: View Someone's Screen (Desktop App)

1. Select option **3** from the menu
2. Enter the required information when prompted:
   - **Server IP address**: 
     - Use `localhost` or `127.0.0.1` if viewing on the same PC
     - Use the actual IP address if connecting from another PC (e.g., `192.168.1.100`)
   - **Port**: Press Enter for default (5555) or enter custom port
   - **Security code**: Enter the 6-character code provided by the person sharing
3. Wait for server approval
4. If approved, you'll see the shared screen in a new window
5. Press `Q` key or `ESC` to quit viewing and return to the menu

**Example:**
```
👀 VIEW SOMEONE'S SCREEN MODE
============================================================

Enter server IP address (or 'localhost' for same PC): localhost
Enter server port (default: 5555): 
Enter the security code: XGFRDW

------------------------------------------------------------
[+] Successfully connected to server!
[*] Receiving screen feed...
[*] Press 'q' to quit
```

#### Option 4: Exit

Closes the application with confirmation.

---

## 📱 **Viewing on Mobile Phone (Recommended Method)**

### **Step-by-Step Guide:**

1. **On Your PC:**
   ```bash
   python main.py
   ```
   - Choose option **2** (Web Browser - Mobile Friendly)
   - Note the security code and URL displayed

2. **Find Your PC's IP Address:**
   - The app will show it, or manually check:
     - Windows: `ipconfig` in PowerShell
     - Look for IPv4 Address (e.g., `192.168.1.100`)

3. **On Your Mobile Phone:**
   - Connect to the **same WiFi network** as your PC
   - Open any web browser (Chrome, Safari, Firefox, etc.)
   - Type the URL: `http://YOUR_PC_IP:8080`
     - Example: `http://192.168.1.100:8080`
   - Enter the 6-character security code
   - Wait for approval on PC
   - Enjoy viewing your PC screen on your phone! 📱

### **Firewall Configuration (Important for Mobile):**

If your phone can't connect, you may need to allow the port through Windows Firewall:

**Method 1 - Quick Test (Temporary):**
- Temporarily disable Windows Firewall
- Test if it works
- Re-enable firewall after testing

**Method 2 - Add Firewall Rule (Recommended):**
1. Open Windows Security → Firewall & network protection
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. TCP, Specific port: **8080** → Next
6. Allow the connection → Next
7. Check all profiles → Next
8. Name: "Screen Share Web Server" → Finish

### **Tips for Mobile Viewing:**
- ✅ Use the same WiFi network
- ✅ Use landscape mode for better viewing
- ✅ Enable full-screen in browser
- ✅ Stable connection = smoother streaming
- ✅ Close unnecessary apps on phone for better performance

---

### Alternative Usage (Advanced)

You can also run the server and client directly if you prefer:

#### Run Server Only:
```bash
python server.py
```

#### Run Client Only:
```bash
python client.py
```

## Network Setup

### For Same PC Testing
- Server IP: `localhost` or `127.0.0.1`
- No firewall configuration needed

### For Different PCs on the Same Network

1. **Find the server PC's IP address:**
   - **Windows**: Open Command Prompt and type `ipconfig`
   - **Linux/Mac**: Open Terminal and type `ifconfig` or `ip addr`
   - Look for the IPv4 address (e.g., `192.168.1.100`)

2. **Configure Firewall (if needed):**
   - Allow incoming connections on port 5555 (Desktop) or 8080 (Web)
   - **Windows Firewall**: 
     - Open Windows Defender Firewall
     - Click "Advanced settings"
     - Create new Inbound Rule for port 5555 and/or 8080

3. **Connect:**
   - Desktop Client: Enter the server's IP address when prompted
   - Web Browser: Navigate to `http://SERVER_IP:8080`

## Configuration

You can customize the following settings by editing the source code:

### Main Menu (`main.py`)
- Main entry point for the application
- Handles user interface and navigation
- Imports and runs server, web server, or client based on user choice

### Server (`server.py`)
- **Port**: Change `port=5555` in the `ScreenShareServer` initialization
- **Code Length**: Change `length=6` in `generate_security_code()` method
- **Image Quality**: Adjust `scale_percent` (around line 58) and JPEG quality (around line 64)
  - Lower values = better performance, lower quality
  - Higher values = worse performance, better quality

### Web Server (`web_server.py`) 🆕
- **Port**: Change `port=8080` in the `ScreenShareWebServer` initialization
- **Code Length**: Change `length=6` in `generate_security_code()` method
- **Image Quality**: Adjust `scale_percent` (50% for mobile) and JPEG quality (70)
- **Frame Rate**: Adjust `time.sleep(0.1)` for different FPS (currently 10 FPS)

### Client (`client.py`)
- Default port can be changed in the main() function

## Performance Tips

1. **Reduce Screen Resolution**: The server automatically scales to 60% of original size
2. **Adjust Quality**: Lower JPEG quality in `server.py` for faster streaming
3. **Close Unused Applications**: Free up system resources
4. **Use Wired Connection**: Better than WiFi for smoother streaming

## Troubleshooting

### Connection Refused
- Make sure the server is running before starting the client
- Check if the IP address is correct
- Verify firewall settings
- If using `main.py`, ensure you select option 1 (Share) on server PC first

### Unauthorized Error
- Double-check the security code (it's case-sensitive, but automatically converted to uppercase)
- Make sure you're entering the current code from the active server session
- Verify you're copying the complete 6-character code
- Check debug output to see what codes are being compared

### Poor Performance / Lag
- Reduce the image quality in `server.py` (lower `scale_percent` and JPEG quality)
- Close bandwidth-heavy applications on both PCs
- Check network connection speed
- Use wired Ethernet instead of WiFi for better stability

### Black Screen or No Display
- Verify screen capture permissions (especially on macOS)
- Try running with administrator/sudo privileges
- Check if `mss` library is properly installed
- Ensure OpenCV (`cv2`) is correctly installed

### Application Crashes or Freezes
- Update all dependencies to latest compatible versions
- Check Python version (requires 3.7+)
- Verify all packages in `requirements.txt` are installed
- Try restarting both applications

### "Press Enter to continue" Not Working
- This is normal behavior - just press the Enter key to return to main menu
- If stuck, press `Ctrl+C` to force exit

### Mobile Browser Can't Connect
- Ensure both devices are on the **same WiFi network**
- Check Windows Firewall settings (allow port 8080)
- Try accessing with PC's IP instead of localhost
- Verify the URL format: `http://IP:8080` (not https)
- Check if another app is using port 8080

### Stream is Laggy on Mobile
- Move closer to WiFi router
- Close other apps using bandwidth
- Lower quality in `web_server.py` (reduce `scale_percent` or JPEG quality)
- Use 5GHz WiFi instead of 2.4GHz if available

## Security Notes

⚠️ **Important:**
- This is a basic implementation for educational purposes
- The security code provides minimal security
- **Two-factor security:** Security code + manual server approval
- For production use, consider:
  - SSL/TLS encryption (HTTPS)
  - Stronger authentication mechanisms
  - Password protection
  - Connection logging
  - End-to-end encryption

## How It Works

### Desktop Mode:
1. **Server** captures the screen using `mss` library in real-time
2. Each frame is converted to a numpy array and compressed using OpenCV with JPEG encoding
3. Compressed images are serialized with `pickle` and sent over TCP socket
4. **Client** connects and sends the security code for authentication
5. Server asks for manual approval before allowing connection
6. Upon approval, client receives, deserializes, and displays frames continuously
7. Automatic reconnection if connection drops

### Web Browser Mode (Mobile-Friendly):
1. **Web Server** captures screen continuously in a background thread
2. Frames are compressed and stored in memory
3. **HTTP Server** serves a responsive HTML/JavaScript interface
4. Browser connects, sends security code via AJAX POST request
5. Server validates code and asks for manual approval
6. Upon approval, server sends session ID to browser
7. Browser displays frames via MJPEG streaming (multipart/x-mixed-replace)
8. Optimized for mobile with lower resolution and frame rate
3. Compressed images are serialized with `pickle` and sent over TCP socket
4. **Client** connects and sends the security code for authentication
5. Upon successful authentication, client receives, deserializes, and displays frames continuously
6. Security code ensures only authorized viewers can connect
7. **Main Menu** (`main.py`) provides a unified interface to launch either server or client mode

## Project Structure

```
screen share/
│
├── main.py              # Main launcher with menu interface (START HERE!)
├── server.py            # Desktop server (screen sharing via socket)
├── web_server.py        # Web server (browser-based, mobile-friendly) 🆕
├── web_client.html      # HTML/JS client for web browser 🆕
├── client.py            # Desktop client (screen viewing)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Files Description

- **`main.py`**: Unified launcher - start here! Provides a menu to choose between desktop/web sharing or desktop viewing.
- **`server.py`**: Desktop server that captures and streams screen via TCP sockets. For PC-to-PC connections.
- **`web_server.py`**: HTTP server for browser-based viewing. Perfect for mobile phones and tablets! 🆕
- **`web_client.html`**: Responsive web interface with beautiful design. Works on any device with a browser. 🆕
- **`client.py`**: Desktop client that connects to server and displays shared screen in OpenCV window.
- **`requirements.txt`**: Lists all required Python packages for easy installation.

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork, modify, and improve this project!

## Support

If you encounter any issues, please check the troubleshooting section or create an issue in the repository.

---

**Enjoy secure screen sharing! 🎉**
