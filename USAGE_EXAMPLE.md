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

