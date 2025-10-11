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

You'll see a menu with three options:

```
============================================================
               SCREEN SHARING APPLICATION
============================================================

Choose an option:

  [1] Share My Screen (Server)
  [2] View Someone's Screen (Client)
  [3] Exit

------------------------------------------------------------

Enter your choice (1/2/3):
```

#### Option 1: Share My Screen

1. Select option **1** from the menu
2. A **security code** will be generated and displayed (e.g., `XGFRDW`)
3. Share this code with the person who wants to view your screen
4. The server will start listening for connections
5. When someone connects with the correct code, their screen will show your desktop
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
[+] Client ('127.0.0.1', 58210) authorized successfully
```

#### Option 2: View Someone's Screen

1. Select option **2** from the menu
2. Enter the required information when prompted:
   - **Server IP address**: 
     - Use `localhost` or `127.0.0.1` if viewing on the same PC
     - Use the actual IP address if connecting from another PC (e.g., `192.168.1.100`)
   - **Port**: Press Enter for default (5555) or enter custom port
   - **Security code**: Enter the 6-character code provided by the person sharing
3. If the code is correct, you'll see the shared screen in a new window
4. Press `Q` key to quit viewing and return to the menu

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

#### Option 3: Exit

Closes the application.

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
   - Allow incoming connections on port 5555
   - **Windows Firewall**: 
     - Open Windows Defender Firewall
     - Click "Advanced settings"
     - Create new Inbound Rule for port 5555

3. **Connect:**
   - On the client PC, enter the server's IP address when prompted

## Configuration

You can customize the following settings by editing the source code:

### Main Menu (`main.py`)
- Main entry point for the application
- Handles user interface and navigation
- Imports and runs server or client based on user choice

### Server (`server.py`)
- **Port**: Change `port=5555` in the `ScreenShareServer` initialization
- **Code Length**: Change `length=6` in `generate_security_code()` method
- **Image Quality**: Adjust `scale_percent` (around line 58) and JPEG quality (around line 64)
  - Lower values = better performance, lower quality
  - Higher values = worse performance, better quality

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

## Security Notes

⚠️ **Important:**
- This is a basic implementation for educational purposes
- The security code provides minimal security
- For production use, consider:
  - SSL/TLS encryption
  - Stronger authentication mechanisms
  - Password protection
  - Connection logging

## How It Works

1. **Server** captures the screen using `mss` library in real-time
2. Each frame is converted to a numpy array and compressed using OpenCV with JPEG encoding
3. Compressed images are serialized with `pickle` and sent over TCP socket
4. **Client** connects and sends the security code for authentication
5. Upon successful authentication, client receives, deserializes, and displays frames continuously
6. Security code ensures only authorized viewers can connect
7. **Main Menu** (`main.py`) provides a unified interface to launch either server or client mode

## Project Structure

```
screen share/
│
├── main.py              # Main launcher with menu interface (RECOMMENDED)
├── server.py            # Server application (screen sharing)
├── client.py            # Client application (screen viewing)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Files Description

- **`main.py`**: Unified launcher - start here! Provides a menu to choose between sharing or viewing.
- **`server.py`**: Captures and streams the screen. Generates security codes and handles client connections.
- **`client.py`**: Connects to server and displays the shared screen in real-time.
- **`requirements.txt`**: Lists all required Python packages for easy installation.

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork, modify, and improve this project!

## Support

If you encounter any issues, please check the troubleshooting section or create an issue in the repository.

---

**Enjoy secure screen sharing! 🎉**
