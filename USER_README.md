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

  [1] Share My Screen (Desktop App)
  [2] Share My Screen (Web Browser - Mobile Friendly)
  [3] View Someone's Screen (Desktop App)
  [4] Start ngrok Tunnel (For Internet Access)
  [5] Check ngrok Status
  [6] Exit
------------------------------------------------------------

Enter your choice (1-6):
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

### 1. Share My Screen (Desktop App)

Share your screen with high quality using a desktop viewer.

**How to use:**
1. Choose option **[1]**
2. Note the security code shown
3. Share your IP address and security code with viewer
4. They connect using option **[3]**

**Benefits:**
- ✅ High quality
- ✅ Low latency
- ✅ Secure (code-protected)

### 2. Share My Screen (Web Browser)

Share your screen via web browser - perfect for mobile!

**How to use:**
1. Choose option **[2]**
2. Note the URLs shown (e.g., `http://192.168.1.100:5000`)
3. Share URL and security code with viewer
4. They open URL in any browser
5. They enter security code

**Benefits:**
- ✅ Mobile-friendly
- ✅ No app needed for viewer
- ✅ Works on any device (phone, tablet, PC)
- ✅ Beautiful web interface

### 3. View Someone's Screen

Connect to someone who is sharing their screen.

**How to use:**
1. Choose option **[3]**
2. Enter their IP address (e.g., `192.168.1.100` or `localhost`)
3. Enter port (default: `5555` for desktop)
4. Enter security code

**Tips:**
- Use `localhost` if on same PC
- Use LAN IP (e.g., `192.168.1.100`) if on same network
- Use ngrok URL for internet sharing

### 4. Start ngrok Tunnel

Share your screen over the **internet** (not just local network).

**How to use:**
1. Choose option **[4]**
2. Choose tunnel type:
   - **[1]** HTTP (for web browser mode - port 5000)
   - **[2]** TCP (for desktop app mode - port 5555)
   - **[3]** Custom port
3. Note the ngrok URL (e.g., `https://abc123.ngrok.io`)
4. Share this URL with anyone worldwide!

**Benefits:**
- ✅ Share over internet (not just LAN)
- ✅ No port forwarding needed
- ✅ Works from anywhere
- ✅ Free to use

### 5. Check ngrok Status

See if ngrok tunnels are running.

**How to use:**
1. Choose option **[5]**
2. View active tunnels and URLs

---

## 🚀 Usage Examples

### Example 1: Share Screen on Same Network

**Sharer (Person A):**
1. Run ScreenShare.exe
2. Choose **[2]** (Web Browser)
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

### Example 2: Share Screen Over Internet

**Sharer (Person A):**
1. Run ScreenShare.exe
2. Choose **[4]** (ngrok)
3. Choose **[1]** (HTTP tunnel)
4. Note URL: `https://abc123.ngrok.io`
5. Keep this window open!
6. Open **another terminal/command prompt**
7. Run ScreenShare.exe again
8. Choose **[2]** (Web Browser)
9. Note security code: `ABC123`
10. Tell Person B: "Go to `https://abc123.ngrok.io` and use code `ABC123`"

**Viewer (Person B - anywhere in the world!):**
1. Open browser
2. Go to `https://abc123.ngrok.io`
3. Enter code `ABC123`
4. Click "Connect"
5. See Person A's screen!

---

### Example 3: View Someone's Desktop Screen

**Viewer (You):**
1. Run ScreenShare.exe
2. Choose **[3]**
3. Enter IP: `192.168.1.100` (their LAN IP)
4. Enter port: `5555` (default)
5. Enter code: `ABC123` (they give you this)
6. View their screen in OpenCV window!

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

### 3. Internet (ngrok)

**Use when:** Different networks or worldwide

**Sharer:** 
1. Run option [4] (ngrok first!)
2. Run option [1] or [2] (sharing)

**Viewer:** Use ngrok URL (e.g., `https://abc123.ngrok.io`)

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
3. Try different port in ngrok (option [4] → [3] Custom)
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
1. Use ngrok (option [4])
2. Share ngrok URL (not local IP)
```

---

### Problem: "web_client.html not found"

**Solution:**
Make sure `web_client.html` is in the **same folder** as `ScreenShare.exe`!

```
Folder structure:
  ScreenShare.exe    ✅
  web_client.html    ✅
```

---

### Problem: Low Frame Rate

**Possible causes:**
- Slow network
- High resolution screen

**Solution:**
```
• Use Desktop mode (option [1]) for better performance
• Close unnecessary applications
• Use wired connection instead of WiFi
```

---

### Problem: ngrok Not Working

**Check:**
1. ✅ Internet connection
2. ✅ ngrok tunnel running (option [4])
3. ✅ Keep ngrok window open

**Solution:**
```
1. Check status: Option [5]
2. Restart ngrok: Close and choose option [4] again
3. Wait a few seconds for tunnel to establish
```

---

## 💡 Tips & Tricks

### Tip 1: Two Terminals for Internet Sharing

For best experience sharing over internet:

**Terminal 1:**
```
Run ScreenShare.exe
Choose [4] (ngrok)
Choose [1] (HTTP) or [2] (TCP)
KEEP THIS OPEN!
```

**Terminal 2:**
```
Run ScreenShare.exe again
Choose [2] (Web) or [1] (Desktop)
Share screen!
```

---

### Tip 2: Mobile Viewing

Use Web Browser mode (option [2]) for mobile viewers!

**Perfect for:**
- ✅ Phones
- ✅ Tablets
- ✅ Any device with browser

---

### Tip 3: Quick Same-PC Test

**Test everything works:**
1. Run ScreenShare.exe
2. Choose [2] (Web Browser)
3. Open browser
4. Go to `http://localhost:5000`
5. Enter security code
6. Should see your screen!

---

### Tip 4: Share Multiple Screens

Want to share to multiple viewers?

**Web mode (option [2]):**
- ✅ Multiple viewers can connect
- ✅ Each enters same security code
- ✅ All see your screen

**Desktop mode (option [1]):**
- ❌ One viewer at a time

**Recommendation:** Use Web mode for multiple viewers!

---

## ❓ FAQ

### Q: Do viewers need to install anything?

**A:** 
- **Web mode:** No! Just a browser.
- **Desktop mode:** Yes, they need the EXE too.

**Recommendation:** Use Web mode for easy sharing!

---

### Q: Is this free?

**A:** Yes! Completely free to use.

**ngrok:** Free tier allows:
- ✅ 1 online session at a time
- ✅ Random URL (changes each session)
- ✅ Unlimited bandwidth

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

**Web mode:** Many viewers (limited by your bandwidth)
**Desktop mode:** One viewer at a time

---

### Q: Is my data encrypted?

**For ngrok (internet):** Yes, HTTPS encrypted
**For local network:** Unencrypted (LAN only)

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

**Version:** 1.0
**Built:** October 13, 2025
**Size:** 86 MB
**Platform:** Windows 10/11 (64-bit)

---

*No installation required • Portable • Secure • Easy to use*
