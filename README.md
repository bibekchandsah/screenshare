# Real-Time Screen Sharing Application

A Python-based screen sharing application with security code authentication and advanced web viewing features. Share your screen securely with others in real-time with professional quality!

## Features

### Core Features
- 🔒 **Secure Connection**: Random security code generation + manual approval system
- 📺 **Real-time Streaming**: Live screen capture and streaming at high quality
- 🚀 **Easy to Use**: Simple menu-driven interface
- 🔌 **Network Support**: Works over LAN, localhost, and **internet** (with ngrok)
- 🌐 **Remote Access**: Share screen across different networks/locations
- 👥 **Multiple Viewers**: Support for unlimited simultaneous viewers
- 🎯 **Unified Launcher**: Single entry point with menu options
- 🖱️ **Cursor Visibility**: See the presenter's mouse cursor in real-time

### Advanced Web Features (NEW! ✨)
- 📱 **Mobile Friendly**: Responsive design works on phones, tablets, and desktops
- 🖼️ **High Quality**: 100% resolution at 95% JPEG quality for crystal-clear viewing
- 🔍 **Interactive Zoom**: Click to zoom into any section, drag to pan around
- 🎬 **Fullscreen Mode**: Immersive viewing with draggable controls
- ⌨️ **Keyboard Shortcuts**: F key for fullscreen, Esc to exit
- 🎨 **Modern UI**: Clean, professional interface with individual digit input boxes
- 📢 **Toast Notifications**: Real-time status updates for all events
- 🔌 **Connection Monitoring**: Automatic disconnection detection
- ⚡ **Smooth Performance**: 20 FPS streaming with optimized JPEG encoding
- 🎮 **Touch Support**: Full touch gesture support for mobile devices

### Security Features
- 🔐 **Two-Factor Security**: Security code + manual server approval
- 🛡️ **Session Management**: Unique session IDs for each connection
- 📋 **Queue System**: Sequential approval processing for multiple requests
- 🚫 **Thread-Safe**: Race condition prevention with proper locking

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
   - Enter the security code in individual digit boxes (auto-focus, paste support)
   - Wait for server approval
   - View the screen in real-time with high quality!

5. Press `Ctrl+C` on the server to stop sharing

**Web Browser Features:**
- ✅ **Responsive Design**: Works perfectly on any screen size
- ✅ **Touch-Friendly Interface**: Optimized for mobile gestures
- ✅ **No App Installation**: Just open a browser
- ✅ **High Quality**: 100% resolution at 95% JPEG quality
- ✅ **Interactive Zoom**: 
  - Click anywhere to zoom into that section
  - Drag to pan when zoomed in
  - Click again to zoom out
- ✅ **Fullscreen Mode**: 
  - Double-click the F button to enter fullscreen
  - Drag the F button anywhere on screen
  - Press F key or Esc key to exit
  - Double-click F button again to exit
- ✅ **Keyboard Shortcuts**:
  - `F` key → Toggle fullscreen mode
  - `Esc` key → Exit fullscreen mode
- ✅ **Individual Digit Boxes**: Easy code entry with paste support
- ✅ **Toast Notifications**: Real-time status updates
- ✅ **Connection Monitoring**: Auto-detects server disconnection
- ✅ **Smooth Streaming**: 20 FPS for fluid motion
- ✅ **Multi-User Support**: Unlimited simultaneous viewers
- ✅ **Cross-Platform**: Works on iOS, Android, Windows, macOS, Linux

**Example Output:**
```
🌐 WEB BROWSER SCREEN SHARE MODE
============================================================

============================================================
SECURITY CODE: XK9M2P
============================================================
Share this code with the person who wants to view your screen
Multiple viewers can connect simultaneously!
============================================================

[*] Access the screen share from your browser at:
    http://192.168.1.100:8080
    http://localhost:8080

[*] Server starting on 0.0.0.0:8080
[*] Multi-user support enabled
[*] Approval processor started - requests will be handled sequentially
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
- ✅ Double-click F button or use F key for fullscreen
- ✅ Click on any area to zoom in, drag to pan
- ✅ Stable connection = smoother streaming
- ✅ Close unnecessary apps on phone for better performance
- ✅ Use paste functionality for quick code entry (long-press in code box)

### **Web Interface Controls:**

**Zoom Features:**
- **Click to Zoom**: Click anywhere on the screen to zoom into that exact section
- **Drag to Pan**: When zoomed, drag with mouse/finger to move around
- **Click to Zoom Out**: Click again to return to fit-to-screen view

**Fullscreen Features:**
- **Enter Fullscreen**: 
  - Double-click the F button in header
  - OR press F key on keyboard
- **Exit Fullscreen**: 
  - Press Esc key
  - OR press F key again
  - OR double-click the draggable F button
- **Move F Button**: Drag the F button to any position when in fullscreen

**Keyboard Shortcuts:**
- `F` → Toggle fullscreen mode (when viewing screen)
- `Esc` → Exit fullscreen mode (when in fullscreen)

---

## 🌐 Sharing Across Different Networks (Internet Access)

### Problem: Same WiFi Limitation
By default, screen sharing only works when both users are on the **same WiFi/local network**. But what if you want to share with someone in a different location?

### Solution: Remote Access Options

#### **Option 1: ngrok (Easiest, Recommended) ⭐**

**Quick Setup:**

1. **Install ngrok helper:**
   ```bash
   pip install pyngrok
   ```
2. **Run the helper:**
   ```bash
   python ngrok_helper.py
   # Choose option 5 for Setup ngrok Authtoken 
   Follow instruction for setting up authtoken
   ```
3. **use standalone ngrok:**
   ```bash
   # Start your screen share first
   python main.py
   
   # choose option [2] Share My Screen (Web Browser - Mobile Friendly)
   # you will see the 
   ```
```
============================================================
SECURITY CODE: 9TV0KX
============================================================
Share this code with people who want to view your screen
Multiple viewers can connect simultaneously!
============================================================

[*] Access the screen share from your browser at:
    http://10.5.234.63:8080 <------ screehshare_url
    http://localhost:8080
```
   ```
   # Then in another terminal:
   ngrok http http://YOUR_PC_IP:8080 or screenshare_url
   ```

4. **Share the public URL:**
   - ngrok gives you: `https://abc123.ngrok.io`
   - Share this URL + security code with anyone, anywhere!

**Benefits:**
- ✅ Works from anywhere in the world
- ✅ No router configuration needed
- ✅ Secure HTTPS tunnel
- ✅ Free tier available
- ✅ Setup in 2 minutes

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
- **Image Quality**: 
  - Adjust `scale_percent` (currently 100% for maximum quality) in `capture_screen_loop()`
  - Adjust JPEG quality (currently 95 for excellent quality)
  - Line 62-65: JPEG encoding parameters
- **Frame Rate**: Adjust `time.sleep(0.05)` for different FPS (currently 20 FPS)
- **Interpolation**: Uses `cv2.INTER_LANCZOS4` for best quality when scaling
- **Progressive JPEG**: Enabled for better streaming performance

**Quality Settings Explained:**
- `scale_percent = 100`: Full resolution (100% of original)
- `JPEG_QUALITY = 95`: Near-lossless compression
- `JPEG_OPTIMIZE = 1`: Optimize file size
- `JPEG_PROGRESSIVE = 1`: Progressive rendering for web
- `INTER_LANCZOS4`: Highest quality interpolation algorithm

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
- Lower quality in `web_server.py` (reduce `scale_percent` from 100 to 75 or 50)
- Use 5GHz WiFi instead of 2.4GHz if available
- Try reducing frame rate (increase `time.sleep(0.05)` to `0.1` for 10 FPS)

### Zoom Not Working Properly
- Make sure you're clicking on the screen image area, not the background
- Try clicking and waiting a moment for the zoom to process
- If zoomed, try dragging to see if pan works
- Refresh the page if zoom gets stuck

### Fullscreen Issues
- **F key not working**: Make sure you're viewing the screen (not on login page)
- **Can't exit fullscreen**: Press Esc key or double-click the draggable F button
- **White screen in fullscreen**: This has been fixed - refresh if you see it
- **F button disappeared**: It might be dragged off-screen - exit and re-enter fullscreen

### Multiple Connection Requests Overlapping
- **FIXED**: Requests are now queued and processed one at a time
- You'll see "Pending requests in queue: X" to know how many are waiting
- Server won't crash if sessions timeout during approval

### Server Crashes on Timeout
- **FIXED**: Added comprehensive exception handling
- Server continues running even if connections timeout
- All resources are properly cleaned up

---

## 🆘 Troubleshooting Remote Access

### ngrok Issues:

**Problem: "Warning page" or "License agreement" shown instead of app**
- **Solution:** This is ngrok's anti-phishing warning (normal for free tier)
- Click **"Visit Site"** button to continue
- Tell viewers to click through the warning
- To skip: Upgrade to ngrok paid plan ($10/month)

**Problem: "Tunnel not found"**
- Solution: Check if ngrok is running
- Verify port number matches

**Problem: "Too many connections" (Free tier)**
- Solution: Upgrade to paid plan or wait

**Problem: Slow performance**
- Solution: ngrok free servers may be far away
- Try different region: `ngrok http 8080 --region eu`

**Problem: Page shows "Oracle Database" or random content**
- **Cause:** You're seeing ngrok's interstitial warning page
- **Solution:** Scroll down and click "Visit Site" button
- This is NOT your application - it's ngrok's security check
- The warning page HTML sometimes shows random cached content

### Port Forwarding Issues:

**Problem: Cannot connect from outside**
- Check router port forwarding rules
- Verify Windows Firewall allows port
- Test if ISP blocks port (some block 80, 8080)
- Try different port (e.g., 8081, 9000)

**Problem: IP address changes**
- Setup Dynamic DNS service
- Check ISP if they provide static IP

### General Issues:

**Problem: Connection very slow**
- Reduce image quality in settings
- Check internet upload speed
- Consider local server closer to viewers

**Problem: Connection drops frequently**
- Check internet stability
- Increase timeout values
- Use wired connection instead of WiFi

---

## 📊 Performance Tips for Remote Access

### Optimize for Internet Streaming:

1. **Reduce Resolution** (in `web_server.py`):
   ```python
   scale_percent = 75  # Instead of 100
   ```

2. **Lower Quality** (for slower connections):
   ```python
   int(cv2.IMWRITE_JPEG_QUALITY), 80  # Instead of 95
   ```

3. **Reduce Frame Rate**:
   ```python
   time.sleep(0.1)  # 10 FPS instead of 20
   ```

4. **Monitor Bandwidth**:
   - Check your upload speed: [speedtest.net](https://speedtest.net)
   - Required: ~2-5 Mbps upload for good quality

---

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
7. Automatic reconnection if connection drops (3 attempts with 2-second delays)

### Web Browser Mode (Mobile-Friendly):
1. **Web Server** captures screen continuously at 100% resolution in a background thread
2. Frames are compressed using JPEG (95% quality) with progressive encoding and optimization
3. Uses LANCZOS4 interpolation for highest quality scaling
4. Compressed frames stored in memory with thread-safe locking
5. **HTTP Server** serves a responsive HTML/JavaScript interface with modern design
6. **ThreadingHTTPServer** handles multiple simultaneous connections
7. Browser connects, displays modern UI with individual digit input boxes
8. Client enters security code, sends via AJAX POST request
9. Server validates code and queues approval request
10. **Sequential Approval Processing**: Requests processed one at a time in order (FIFO)
11. Server asks for manual approval (shows queue status)
12. Upon approval, server sends session ID to browser
13. Browser receives frames via MJPEG streaming (multipart/x-mixed-replace boundary)
14. Client can:
    - **Zoom**: Click any area to zoom into that section (calculates relative position)
    - **Pan**: Drag with mouse/touch when zoomed to navigate
    - **Fullscreen**: Double-click F button or press F key
    - **Exit Fullscreen**: Press Esc key or double-click F button
    - **Move Controls**: Drag F button to any position
15. **Connection Monitoring**: Browser checks `/health` endpoint every 3 seconds
16. **Auto-disconnect Detection**: Shows notification if server disconnects
17. Optimized for mobile with touch gestures and responsive layout
18. 20 FPS streaming for smooth motion

### Security & Threading:
- **Two-Factor Security**: Security code + manual server approval
- **Thread-Safe Operations**: All shared data protected with locks
- **Approval Queue**: Sequential processing prevents overlapping prompts
- **Race Condition Prevention**: Proper locking on all pending approvals
- **Graceful Timeout Handling**: Sessions cleaned up properly without crashes
- **Exception Handling**: Comprehensive error handling prevents server crashes

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
  - Features: 100% resolution, 95% JPEG quality, 20 FPS streaming
  - Threading: ThreadingHTTPServer for multi-user support
  - Security: Sequential approval queue system
  - Thread-safe: Comprehensive locking mechanisms
- **`web_client.html`**: Responsive web interface with modern features. 🆕
  - **UI Components**: Individual digit input boxes with auto-focus and paste support
  - **Zoom System**: Click-to-zoom with intelligent section targeting
  - **Fullscreen**: Draggable controls with keyboard shortcuts (F, Esc)
  - **Notifications**: Toast notification system for all events
  - **Connection Monitoring**: Auto-detects disconnections via /health endpoint
  - **Touch Support**: Full mobile gesture support
  - **Responsive Design**: Works on all screen sizes
- **`client.py`**: Desktop client that connects to server and displays shared screen in OpenCV window.
- **`requirements.txt`**: Lists all required Python packages for easy installation.

## Recent Updates & Improvements

### Version 2.1 (Latest) 🆕
✨ **New Remote Access Features:**
- 🌐 **Internet Sharing**: Share screen across different networks/locations
- 🚀 **ngrok Integration**: Easy tunneling with `ngrok_helper.py`
- 📖 **Remote Access Guide**: Comprehensive guide for all remote access methods
- 🔌 **Port Forwarding Documentation**: Step-by-step router configuration
- 🛡️ **VPN Setup Guide**: ZeroTier/Tailscale integration instructions

🖱️ **Cursor Visibility:**
- 👆 **Real-time Cursor**: Viewers can now see your mouse cursor
- 🎨 **Smart Design**: Triple-layer cursor (white outline, black ring, red center)
- 📍 **Precise Tracking**: Cursor position updates at stream frame rate
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux via pyautogui

### Version 2.0
✨ **Major Feature Additions:**
- 🔍 **Intelligent Zoom**: Click anywhere to zoom into that exact section
- 🎬 **Advanced Fullscreen**: Draggable F button with keyboard shortcuts
- ⌨️ **Keyboard Controls**: F key for fullscreen, Esc to exit
- 📢 **Toast Notifications**: Real-time status updates for all events
- 📊 **Connection Monitoring**: Health check endpoint with auto-reconnect
- 🎨 **Modern UI**: Individual digit boxes with paste support

🛠️ **Performance Improvements:**
- 📈 **Maximum Quality**: Upgraded to 100% resolution at 95% JPEG quality
- 🚀 **Faster Streaming**: Increased to 20 FPS with progressive JPEG
- 🎯 **Smart Interpolation**: LANCZOS4 algorithm for best quality
- 🔧 **Optimized Encoding**: Progressive JPEG with optimization enabled

🔒 **Security & Stability Enhancements:**
- 🔐 **Approval Queue System**: Sequential processing of connection requests
- 🛡️ **Thread-Safe Operations**: Comprehensive locking prevents race conditions
- 🔄 **Graceful Timeout Handling**: No crashes on session timeouts
- 🚫 **Exception Handling**: Robust error handling throughout
- 📋 **Queue Status Display**: Shows pending requests count

🐛 **Bug Fixes:**
- ✅ Fixed: White screen in fullscreen mode (CSS display issue)
- ✅ Fixed: KeyError on session timeout (race condition)
- ✅ Fixed: Overlapping approval prompts (queue system)
- ✅ Fixed: Server crashes on timeout (exception handling)
- ✅ Fixed: Single-click fullscreen toggle (changed to double-click)
- ✅ Fixed: Zoom centers on click position (not image center)
- ✅ Fixed: **ngrok warning page** - automatically bypassed with header

🌐 **ngrok Integration:**
- 🎯 **Auto-Bypass Warning**: Sends `ngrok-skip-browser-warning` header automatically
- 📱 **Direct Access**: Viewers skip the "Visit Site" button completely
- 🚀 **Better UX**: One less step for viewers to access screen share

## Technical Architecture

### Threading Model:
```
Web Server Process
├── Main Thread (HTTP Server)
├── Screen Capture Thread (Background, continuous capture)
├── Approval Processor Thread (Sequential approval handling)
└── HTTP Handler Threads (One per client connection)
    ├── Handles /verify endpoint
    ├── Handles /stream endpoint (MJPEG)
    └── Handles /health endpoint
```

### Data Flow:
```
Screen → mss.grab() → NumPy Array → cv2.resize() → JPEG Encode → Memory Buffer
                                                                         ↓
Browser ← MJPEG Stream ← HTTP Response ← ThreadingHTTPServer ← Memory Buffer
```

### Synchronization:
- **frame_lock**: Protects current_frame buffer during read/write
- **approval_lock**: Protects pending_approvals dictionary
- **approval_queue**: Thread-safe queue for approval requests
- All dictionary operations on shared data are protected

### Web Client Architecture:
```javascript
Login View
    ↓ (Security Code Verification)
Session Established
    ↓
Viewer Screen (with controls)
    ├── MJPEG Stream Display
    ├── Health Check Interval (3s)
    ├── Zoom Event Handlers
    ├── Fullscreen Controls
    └── Toast Notification System
```

### Performance Optimizations:
1. **Screen Capture**: Single capture thread, shared buffer
2. **JPEG Encoding**: Progressive with optimization
3. **Streaming**: Direct memory-to-HTTP without file I/O
4. **Threading**: Daemon threads for clean shutdown
5. **Frame Rate Control**: Sleep-based limiting (0.05s = 20 FPS)
6. **Image Quality**: LANCZOS4 interpolation for scaling

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork, modify, and improve this project!

## Support

If you encounter any issues, please check the troubleshooting section or create an issue in the repository.

## Quick Reference Card

### For Server (PC Sharing Screen):
```bash
python main.py
Choose option 2 (Web Browser)
Share the security code and URL
Approve connections when prompted
Press Ctrl+C to stop
```

### For Viewer (Mobile/Browser):
```
1. Connect to same WiFi as server
2. Open browser: http://SERVER_IP:8080
3. Enter 6-digit security code
4. Wait for approval
5. Double-click F or press F key for fullscreen
6. Click screen to zoom, drag to pan
7. Press Esc to exit fullscreen
```

### Keyboard Shortcuts (Web Client):
| Key | Action |
|-----|--------|
| `F` | Toggle fullscreen mode |
| `Esc` | Exit fullscreen mode |

### Mouse/Touch Controls (Web Client):
| Action | Effect |
|--------|--------|
| **Single Click** | Zoom into clicked section |
| **Drag** | Pan when zoomed (move around) |
| **Click Again** | Zoom out to fit screen |
| **Double-Click F Button** | Toggle fullscreen |
| **Drag F Button** | Move button position (fullscreen) |

### Connection URLs:
- **Same PC**: `http://localhost:8080`
- **Other Device**: `http://YOUR_PC_IP:8080`
- **Find IP**: Run `ipconfig` (Windows) or `ifconfig` (Linux/Mac)

### Ports Used:
- **Desktop Mode**: Port 5555 (TCP)
- **Web Mode**: Port 8080 (HTTP)

### Default Settings:
- **Resolution**: 100% (full quality)
- **JPEG Quality**: 95% (near-lossless)
- **Frame Rate**: 20 FPS
- **Code Length**: 6 characters
- **Approval Timeout**: 60 seconds
- **Health Check**: Every 3 seconds

---

**Enjoy secure screen sharing! 🎉**
