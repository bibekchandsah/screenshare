# 📝 README - ScreenShare.exe

## Welcome to Screen Sharing Application! 👋

A simple, powerful, and portable screen sharing tool for Windows.

---

## ⚡ Quick Start

### 1. Download & Extract

Extract the zip file to any folder.

### 2. Run the Application

Double-click **ScreenShare.exe**

### 3. Choose Your Option

```
============================================================
              SCREEN SHARING APPLICATION
============================================================

Choose an option:

  [1] Share My Screen
  [2] View Someone's Screen
  [3] Cloudflare Tunnel (HTTP) - Web Browser Access
  [4] Cloudflare Tunnel (TCP) - Direct Connection
  [5] Trusted Mode - No Security Code Required
  [6] Cloudflare + Trusted - Easy Internet Sharing
  [7] Help - Show Usage Instructions
  [8] Exit
------------------------------------------------------------

Enter your choice (1-8):
```

---

## 📋 System Requirements

- ✅ **OS:** Windows 10/11 (64-bit)
- ✅ **RAM:** 4 GB minimum
- ✅ **Disk:** 100 MB free space
- ✅ **Network:** Local network or internet connection
- ✅ **Python:** **NOT REQUIRED!** (Built-in)

**That's it!** No installation needed!

---

## 🎯 Features

### 1. Share My Screen

Share your screen with high quality using web browser access.

**How to use:**
1. Choose option **[1]**
2. Note the security code shown
3. Note the URL (e.g., `http://192.168.1.100:5000`)
4. Share URL and security code with viewer
5. They open URL in any browser and enter the code

**Benefits:**
- ✅ High quality streaming
- ✅ Mobile-friendly web interface
- ✅ Secure (code-protected)
- ✅ Works on any device with a browser

### 2. View Someone's Screen

Connect to someone who is sharing their screen.

**How to use:**
1. Choose option **[2]**
2. Enter their IP address (e.g., `192.168.1.100` or `localhost`)
3. Enter port (default: `5555`)
4. Enter security code

**Tips:**
- Use `localhost` if on same PC
- Use LAN IP (e.g., `192.168.1.100`) if on same network
- Use Cloudflare URL for internet sharing

### 3. Cloudflare Tunnel (HTTP) - Web Browser Access

Share your screen over the **internet** using Cloudflare tunnels for web browser access.

**How to use:**
1. Choose option **[3]**
2. Note the Cloudflare URL (e.g., `https://abc-def-123.trycloudflare.com`)
3. Share this URL with anyone worldwide!
4. They can access your screen through their web browser

**Benefits:**
- ✅ Share over internet (not just LAN)
- ✅ No port forwarding needed
- ✅ Unlimited bandwidth
- ✅ Works from anywhere
- ✅ Mobile-friendly

### 4. Cloudflare Tunnel (TCP) - Direct Connection

Create a direct TCP tunnel for desktop-to-desktop connections over the internet.

**How to use:**
1. Choose option **[4]**
2. Note the tunnel details shown
3. Share connection info with viewer
4. They use option **[2]** to connect

**Benefits:**
- ✅ Direct TCP connection
- ✅ Lower latency than HTTP
- ✅ Internet access via Cloudflare
- ✅ No bandwidth limits

### 5. Trusted Mode - No Security Code Required

Share your screen without requiring security codes - perfect for trusted environments.

**How to use:**
1. Choose option **[5]**
2. Note the URL shown
3. Share URL with trusted viewers
4. They can connect immediately without entering codes

**Benefits:**
- ✅ No security code hassle
- ✅ Instant access for trusted users
- ✅ Perfect for family/team sharing
- ✅ Same high-quality streaming

**⚠️ Security Note:** Only use in trusted environments!

### 6. Cloudflare + Trusted - Easy Internet Sharing

Combines Cloudflare internet access with trusted mode for the easiest possible sharing.

**How to use:**
1. Choose option **[6]**
2. Note the Cloudflare URL
3. Share URL with anyone worldwide
4. They connect instantly without codes

**Benefits:**
- ✅ Internet access via Cloudflare
- ✅ No security codes needed
- ✅ Easiest sharing method
- ✅ Perfect for demonstrations

**⚠️ Security Note:** URL access grants immediate screen viewing!

### 7. Help - Show Usage Instructions

Get detailed help and usage instructions.

**How to use:**
1. Choose option **[7]**
2. View comprehensive usage guide
3. Learn about all features and options

### 8. Exit

Safely close the application.

---

## 🚀 Usage Examples

### Example 1: Share Screen on Same Network

**Sharer (Person A):**
1. Run ScreenShare.exe
2. Choose **[1]** (Share My Screen)
3. Note URL: `http://192.168.1.100:5000`
4. Note security code: `ABC123`
5. Tell Person B: "Go to `192.168.1.100:5000` and use code `ABC123`"

**Viewer (Person B):**
1. Open browser
2. Go to `http://192.168.1.100:5000`
3. Enter code `ABC123`
4. Click "Connect"
5. See Person A's screen!

---

### Example 2: Share Screen Over Internet (with Security)

**Sharer (Person A):**
1. Run ScreenShare.exe
2. Choose **[3]** (Cloudflare HTTP)
3. Note URL: `https://abc-def-123.trycloudflare.com`
4. Note security code: `ABC123`
5. Tell Person B: "Go to `https://abc-def-123.trycloudflare.com` and use code `ABC123`"

**Viewer (Person B - anywhere in the world!):**
1. Open browser
2. Go to `https://abc-def-123.trycloudflare.com`
3. Enter code `ABC123`
4. Click "Connect"
5. See Person A's screen!

---

### Example 3: Easy Internet Sharing (Trusted Mode)

**Sharer (Person A):**
1. Run ScreenShare.exe
2. Choose **[6]** (Cloudflare + Trusted)
3. Note URL: `https://xyz-uvw-789.trycloudflare.com`
4. Tell Person B: "Just go to `https://xyz-uvw-789.trycloudflare.com`"

**Viewer (Person B - anywhere in the world!):**
1. Open browser
2. Go to `https://xyz-uvw-789.trycloudflare.com`
3. Instantly see Person A's screen! (No code needed)

---

### Example 4: View Someone's Screen

**Viewer (You):**
1. Run ScreenShare.exe
2. Choose **[2]** (View Someone's Screen)
3. Enter IP: `192.168.1.100` (their LAN IP) or Cloudflare URL
4. Enter port: `5555` (default)
5. Enter code: `ABC123` (they give you this)
6. View their screen in your browser!

---

## 🔒 Security

### Security Code

Every session generates a **unique security code**.

**Features:**
- ✅ 6-character random code
- ✅ Required for all connections
- ✅ Changes every session
- ✅ Cannot be bypassed

**Example codes:**
```
ABC123
XYZ789
QWE456
```

### Best Practices:

- ✅ Only share code with trusted people
- ✅ Use new session for each sharing
- ✅ Don't share code publicly
- ✅ Close sharing when done

---

## 🌐 Network Modes

### 1. Same PC (localhost)

**Use when:** Testing or demo on same computer

**Sharer:** Run option [1] or [2]
**Viewer:** Use `localhost` or `127.0.0.1`

### 2. Same Network (LAN)

**Use when:** Same WiFi or office network

**Sharer:** Run option [1] or [2]
**Viewer:** Use LAN IP (e.g., `192.168.1.100`)

**Find your IP:**
```
Windows: ipconfig
Look for "IPv4 Address"
```

### 3. Internet (Cloudflare)

**Use when:** Different networks or worldwide

**Sharer:** 
1. Run option [3] (Cloudflare HTTP) or [6] (Cloudflare + Trusted)
2. Note the Cloudflare URL

**Viewer:** Use Cloudflare URL (e.g., `https://abc-def-123.trycloudflare.com`)

---

## 🐛 Troubleshooting

### Problem: Windows Defender Blocks EXE

**Solution:**
1. Click "More info"
2. Click "Run anyway"

This is a false positive - the app is safe!

---

### Problem: "Cannot start screen share"

**Possible causes:**
- Port already in use
- Firewall blocking

**Solution:**
```
1. Close other screen sharing apps
2. Check Windows Firewall
3. Try different Cloudflare tunnel (restart option [3])
```

---

### Problem: Viewer Can't Connect

**Check these:**
1. ✅ Correct IP address?
2. ✅ Correct port?
3. ✅ Correct security code?
4. ✅ Sharer is running?
5. ✅ Same network (or using ngrok)?
6. ✅ Firewall not blocking?

**Solution:**
```
For internet sharing:
1. Use Cloudflare tunnels (option [3] or [6])
2. Share Cloudflare URL (not local IP)
```

---

### Problem: "web_client.html not found"

**Solution:**
Make sure both `web_client.html` and `web_client_trusted.html` are in the **same folder** as `ScreenShare.exe`!

```
Folder structure:
  ScreenShare.exe           ✅
  web_client.html          ✅
  web_client_trusted.html  ✅
```

---

### Problem: Low Frame Rate

**Possible causes:**
- Slow network
- High resolution screen

**Solution:**
```
• Use local network sharing for better performance
• Close unnecessary applications
• Use wired connection instead of WiFi
• Try trusted mode (option [5]) for fewer authentication delays
```

---

### Problem: Cloudflare Tunnel Not Working

**Check:**
1. ✅ Internet connection
2. ✅ Cloudflare tunnel running (option [3] or [4])
3. ✅ Keep tunnel window open

**Solution:**
```
1. Check if tunnel is active
2. Restart Cloudflare: Close and choose option [3] or [4] again
3. Wait a few seconds for tunnel to establish
4. Try option [7] for help
```

---

## 💡 Tips & Tricks

### Tip 1: Easy Internet Sharing

For the simplest internet sharing experience:

**Single Step:**
```
Run ScreenShare.exe
Choose [6] (Cloudflare + Trusted)
Share the URL - that's it!
```

### Tip 2: Secure Internet Sharing

For secure internet sharing with authentication:

**Two Steps:**
```
1. Run ScreenShare.exe
2. Choose [3] (Cloudflare HTTP)
3. Share URL and security code
```

---

### Tip 3: Mobile Viewing

All sharing modes work great on mobile!

**Perfect for:**
- ✅ Phones
- ✅ Tablets
- ✅ Any device with browser

**Best options for mobile:**
- Option [1] (regular mode)
- Option [5] (trusted mode - no code needed)
- Option [6] (Cloudflare + trusted for internet)

---

### Tip 4: Quick Same-PC Test

**Test everything works:**
1. Run ScreenShare.exe
2. Choose [1] (Share My Screen)
3. Open browser
4. Go to `http://localhost:5000`
5. Enter security code
6. Should see your screen!

**Test trusted mode:**
1. Run ScreenShare.exe
2. Choose [5] (Trusted Mode)
3. Open browser
4. Go to `http://localhost:5000`
5. No code needed - instant access!

---

### Tip 5: Share Multiple Screens

Want to share to multiple viewers?

**All modes support multiple viewers:**
- ✅ Multiple viewers can connect simultaneously
- ✅ Each enters same security code (except trusted mode)
- ✅ All see your screen

**Recommendation:** 
- Use trusted mode (option [5]) for easy multiple access
- Use Cloudflare + trusted (option [6]) for internet sharing to multiple people

---

## ❓ FAQ

### Q: Do viewers need to install anything?

**A:** No! All modes use web browsers.
- All screen sharing is browser-based
- Works on any device with a web browser
- No installation required for viewers

**Recommendation:** Share the URL and viewers just open their browser!

---

### Q: Is this free?

**A:** Yes! Completely free to use.

**Cloudflare tunnels:** Free and unlimited
- ✅ Unlimited bandwidth
- ✅ No session limits  
- ✅ Global edge network
- ✅ HTTPS encryption

---

### Q: Can I use this for work/commercial?

**A:** Yes! Free to use for personal and commercial projects.

---

### Q: How do I stop sharing?

**A:** Press `Ctrl+C` in the terminal, or close the window.

---

### Q: Can I customize the security code?

**A:** No, it's randomly generated for security.

---

### Q: Does this work on Mac/Linux?

**A:** This EXE is **Windows only**. 

For Mac/Linux, use the Python source code instead.

---

### Q: How many people can view at once?

**All modes:** Many viewers (limited by your bandwidth)
- Multiple people can connect simultaneously
- Each uses same URL (and security code if not in trusted mode)
- Great for presentations and demonstrations

---

### Q: Is my data encrypted?

**For Cloudflare (internet):** Yes, HTTPS encrypted
**For local network:** Unencrypted (LAN only)
**Trusted mode:** Same encryption as regular mode (just no authentication)

---

## 📞 Support

### Need Help?

1. **Read this README** (you're here!)
2. **Check Troubleshooting** section above
3. **Try console version** to see errors:
   - Build with: `python build_console_exe.py`

### Found a Bug?

Report issues with these details:
- Windows version
- What you were doing
- Error message (if any)
- Steps to reproduce

---

## 📄 License

Free to use for personal and commercial projects.

**Open source libraries used:**
- Python (PSF License)
- OpenCV (Apache 2.0)
- Flask (BSD)
- mss (MIT)
- Pillow (PIL License)
- PyInstaller (GPL)

---

## 🎉 Enjoy!

Thank you for using **Screen Sharing Application**!

**Happy screen sharing!** 🚀✨

---

**Version:** 2.0
**Built:** November 8, 2025
**Size:** ~85-100 MB
**Platform:** Windows 10/11 (64-bit)

---

*No installation required • Portable • Secure • Easy to use*
