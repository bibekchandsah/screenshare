# 🚀 Quick Start Guide - Screen Share with ngrok

## Installation

1. **Clone or download this repository**

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the helper:**
   ```bash
   python ngrok_helper.py
   # Choose option 5 for Setup ngrok Authtoken 
   Follow instruction for setting up authtoken
   ```

## Two Terminal Setup


### Terminal 1: Start Screen Share
```bash
python main.py
```

**Choose:** `2` (Web Browser - Mobile Friendly)

**What you'll see:**
```
============================================================
SECURITY CODE: F5PN52
============================================================
Share this code with people who want to view your screen
Multiple viewers can connect simultaneously!
============================================================

[*] Access the screen share from your browser at:
    http://10.5.234.63:8080 <-- screenshare_url
    http://localhost:8080
```

📋 **Copy the 6-character code** (e.g., `F5PN52`)   
📋 **Copy the screenshare_url** (e.g., `http://10.5.234.63:8080`)

---
### Terminal 2: Start ngrok
```bash
ngrok http http://screenshare_url:8080
```

**What you'll see:**
```
Forwarding    https://xxxxx-xxxxx-xxxxx.ngrok-free.dev -> http://localhost:8080
```

📋 **Copy the HTTPS URL** (e.g., `https://xxxxx-xxxxx-xxxxx.ngrok-free.dev`)

---

## 📤 Share with Viewers

Send them this information:

```
🌐 URL: https://xxxxx-xxxxx-xxxxx.ngrok-free.dev
🔐 Code: F5PN52

Instructions:
1. Open the URL
2. Enter the code
3. Wait for approval
```

---

## ✅ Approve Viewers

When someone connects, you'll see in Terminal 2:

```
[!] New connection request from: 192.168.x.x
    Username: JohnDoe
    Approve? (yes/no):
```

Type `yes` and press Enter to approve.

---

## 🛑 Stop Sharing

**Terminal 1 (screen share):** Press `Ctrl+C`   
**Terminal 2 (ngrok):** Press `Ctrl+C`  

---

## 📝 Tips

✅ **Keep both terminals open** while sharing  
✅ **Same security code** works for multiple viewers  
✅ **URL changes** each time you restart ngrok  
✅ **No warning page** - automatic bypass is already configured  
✅ **Works across different WiFi networks**  

---

## 🔧 Troubleshooting

### Problem: "This site can't be reached"
**Solution:** Make sure ngrok (Terminal 2) is still running

### Problem: "Invalid security code"
**Solution:** Double-check the code from Terminal 1 (case-sensitive)

### Problem: "Waiting for approval..."
**Solution:** Check Terminal 1 and type `yes` to approve

### Problem: ngrok URL changes every time
**Solution:** This is normal for free tier. Share new URL each session.

---

## 🎯 One-Minute Checklist

- [ ] Terminal 1: `python main.py` → Choose 2 → Copy code & screenshare_url
- [ ] Terminal 2: `ngrok http screenshare_url` → Copy URL
- [ ] Share URL + Code with viewer
- [ ] Approve connection when prompted
- [ ] Start sharing! 🎉

---

## 📱 Viewer Experience

1. **Opens URL** → Login page appears
2. **Enters code** → "Waiting for approval..." message
3. **You approve** → Screen appears instantly
4. **Controls:**
   - Click to zoom in
   - Press `F` for fullscreen
   - Press `Esc` to exit fullscreen
   - Double-click bottom controls for fullscreen

---

## 🌐 Alternative: Local Network Only

If viewers are on the **same WiFi network**, they can use the local URL instead:

```
http://10.5.234.63:8080
```

*(No ngrok needed, but only works on same network)*

---

**Need more help?** Check `README.md` for detailed instructions.
