# 📋 XiaoZhi Setup - Commands Reference & Checklist

## 🎯 QUICK COMMANDS REFERENCE

Copy-paste commands di bawah saat di-step. Ini akan membuat setup lebih cepat!

---

## STEP 1: API Key Setup ✓

### Brave Search API
```
1. Buka: https://brave.com/search/api/
2. Click "Sign Up"
3. Isi email & password
4. Verify email
5. Copy API key dari dashboard
```

**Expected Output:**
```
API Key: sk_live_XXXXXXXXXXXXXXXXXXXXXX...
Status: Active
Queries: 0 / 2000
```

---

## STEP 2: Python Installation ✓

### Windows
```bash
# 1. Download dari: https://www.python.org/downloads/
# 2. Double-click installer
# 3. CENTANG: "Add Python to PATH"
# 4. Click "Install Now"
# 5. Verify:
python --version
# Output: Python 3.11.x
```

### Mac
```bash
# Download dari: https://www.python.org/downloads/
# Double-click .pkg file
# Ikuti installer
# Verify:
python3 --version
# Output: Python 3.11.x
```

### Linux
```bash
sudo apt-get update
sudo apt-get install python3.11 python3-pip
python3 --version
# Output: Python 3.11.x
```

---

## STEP 3: Project Setup ✓

### Windows
```bash
# 1. Buka File Explorer
# 2. Navigasi ke: C:\Users\YourUsername\Documents
# 3. Right-click → New → Folder
# 4. Rename ke: xiaozhi-web-search
# 5. Buka folder
# 6. Copy files ke sini:
#    - xiaozhi_backend_main.py
#    - requirements.txt
#    - .env
```

### Mac/Linux
```bash
# Buat folder
mkdir -p ~/xiaozhi-web-search
cd ~/xiaozhi-web-search

# Verify
ls -la
# Should show:
# xiaozhi_backend_main.py
# requirements.txt
# .env
```

---

## STEP 4: Configure .env ✓

```bash
# Edit .env file dengan text editor
# Ganti XXX dengan API key Anda:

BRAVE_API_KEY=sk_live_XXXXXXXXXXXXXXXXXXXXX
TAVILY_API_KEY=tvly_XXXXXXXXXXXXXXXXXXXXX
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8080
LOG_LEVEL=info
DEBUG=false

# Save file (Ctrl+S)
```

---

## STEP 5: Install Dependencies ✓

### Windows
```bash
# Buka Command Prompt
# Pastikan sudah di folder xiaozhi-web-search
cd Documents\xiaozhi-web-search

# Install dependencies
pip install -r requirements.txt

# Expected output:
# Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

### Mac/Linux
```bash
cd ~/xiaozhi-web-search
pip3 install -r requirements.txt

# Expected output:
# Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

---

## STEP 6: Run Backend ✓

### Windows
```bash
# Di Command Prompt yang sama:
python xiaozhi_backend_main.py

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8080
# INFO:     Application startup complete

# ⚠️ JANGAN CLOSE WINDOW INI!
```

### Mac/Linux
```bash
cd ~/xiaozhi-web-search
python3 xiaozhi_backend_main.py

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8080
# INFO:     Application startup complete

# ⚠️ JANGAN CLOSE TERMINAL INI!
```

---

## STEP 7: Test Backend ✓

### Buka Terminal/Command Prompt BARU!

### Windows
```bash
# Health check
curl http://localhost:8080/api/health

# Expected output:
# {"status":"healthy","timestamp":"2024-...","connected_devices":0,...}

# Test search
curl "http://localhost:8080/api/search?query=python&provider=brave&count=5"

# Expected output:
# {"success":true,"query":"python","provider":"brave","results":[...],...}
```

### Mac/Linux
```bash
# Health check
curl http://localhost:8080/api/health

# Expected output:
# {"status":"healthy","timestamp":"2024-...","connected_devices":0,...}

# Test search
curl "http://localhost:8080/api/search?query=python&provider=brave&count=5"

# Expected output:
# {"success":true,"query":"python","provider":"brave","results":[...],...}
```

### Alternatif: Test dengan Browser
```
1. Buka browser
2. Ketik di address bar: http://localhost:8080/docs
3. Seharusnya muncul: Swagger UI Documentation
4. Click: "GET /api/health"
5. Click: "Try it out"
6. Click: "Execute"
7. Seharusnya muncul response JSON
```

---

## STEP 8: Get Your IP Address ✓

### Windows
```bash
# Di Command Prompt:
ipconfig

# Cari baris:
# IPv4 Address . . . . . . . . . . . : 192.168.1.100
# (Ingat nilai ini, pakai untuk Step 9)
```

### Mac/Linux
```bash
# Di Terminal:
ifconfig | grep "inet "

# Atau:
hostname -I

# Output contoh:
# inet 192.168.1.100
# (Ingat nilai ini untuk Step 9)
```

---

## STEP 9: Configure XiaoZhi Device ✓

### Via Web Console
```
1. Buka browser: https://xiaozhi.me
2. Login dengan akun Anda
3. Pilih device Anda
4. Click: Settings atau Backend Configuration
5. Isi:
   Backend URL: ws://192.168.1.100:8080/ws/device
   (Ganti 192.168.1.100 dengan IP Anda dari Step 8)
6. Toggle ON:
   - MCP Enabled
   - Web Search
7. Click: Save
8. Device akan restart
```

### Via Device Console (Alternative)
```
1. Connect ke device via serial/SSH
2. Edit config file:
   /config/xiaozhi.json
3. Update:
   {
     "backend": {
       "url": "ws://192.168.1.100:8080/ws/device",
       "mcp_enabled": true
     }
   }
4. Save & restart device
```

---

## STEP 10: Test Voice Commands ✓

### Activate Device
```
1. Katakan: "小智" atau "Xiaozhi"
2. Device akan respond: "Listening..."
3. Tunggu prompt/beep
```

### Simple Search Commands
```
"搜索 Python 编程"
"Search for AI news"
"Cari machine learning tutorial"
"Find latest tech news"
```

### Monitor Backend Logs
```
Di terminal backend (Step 6), Anda akan lihat:

INFO: Search request: query=python, provider=brave
INFO: Brave search: python (count=5)
INFO: Tool call: web_search
INFO: Device received response
```

---

# ✅ CHECKLIST LENGKAP

```
STEP 1: API Keys
  ☐ Brave Search API key diperoleh
  ☐ API key di-copy ke notepad
  ☐ Tavily API (optional)

STEP 2: Python Installation
  ☐ Python downloaded
  ☐ Python installed
  ☐ "Add to PATH" di-check saat install
  ☐ Verify: python --version works

STEP 3: Project Folder
  ☐ Folder xiaozhi-web-search dibuat
  ☐ xiaozhi_backend_main.py di-copy
  ☐ requirements.txt di-copy
  ☐ .env di-copy

STEP 4: Configuration
  ☐ .env file di-edit
  ☐ BRAVE_API_KEY diisi dengan benar
  ☐ TAVILY_API_KEY diisi (atau kosong)
  ☐ .env file di-save

STEP 5: Dependencies
  ☐ cd ke folder xiaozhi-web-search
  ☐ pip install -r requirements.txt sukses
  ☐ Tidak ada error saat install

STEP 6: Backend Start
  ☐ python xiaozhi_backend_main.py dijalankan
  ☐ "Uvicorn running on http://0.0.0.0:8080" muncul
  ☐ Terminal tetap terbuka

STEP 7: Backend Test
  ☐ curl health check returns 200
  ☐ curl search returns results
  ☐ Browser http://localhost:8080/docs accessible

STEP 8: IP Address
  ☐ IP address komputer di-find
  ☐ IP address di-catat (192.168.1.xxx)
  ☐ Device dapat ping ke IP ini

STEP 9: Device Configuration
  ☐ Login ke xiaozhi.me
  ☐ Backend URL di-set: ws://IP:8080/ws/device
  ☐ MCP Enabled toggle ON
  ☐ Web Search toggle ON
  ☐ Settings di-save
  ☐ Device restart selesai

STEP 10: Voice Test
  ☐ Device "listening" setelah wake word
  ☐ Search command di-katakan
  ☐ Backend logs menunjukkan request diterima
  ☐ Audio response terdengar dari speaker
  ☐ Search results akurat

OVERALL
  ☐ Semua steps selesai
  ☐ Sistem berfungsi end-to-end
  ☐ Voice commands working
  ☐ Siap untuk production use
```

---

# 🆘 TROUBLESHOOTING QUICK REFERENCE

## Problem: "command not found: python"
```
Windows: Restart CMD setelah Python install
Mac: Gunakan python3 bukan python
Linux: Gunakan python3 bukan python
```

## Problem: "ModuleNotFoundError: No module named 'fastapi'"
```
Jalankan: pip install -r requirements.txt
Verifikasi: pip list | grep fastapi
```

## Problem: "Address already in use"
```
Windows: netstat -ano | findstr :8080
Mac/Linux: lsof -i :8080
Solusi: Kill process atau ganti port di .env
```

## Problem: "API Key invalid"
```
Check: API key di .env tidak ada typo
Check: API key sudah active di dashboard
Action: Restart backend
```

## Problem: "Connection refused"
```
Check: Backend masih running?
Check: Port 8080 correct?
Check: Firewall tidak block?
```

## Problem: "Device tidak connect"
```
Check: Device on dan WiFi connected?
Check: Backend URL correct di device?
Check: IP address benar?
Action: Restart device
```

## Problem: "Search returns empty"
```
Check: API quota (max 2000/month)?
Check: Internet connection?
Try: Simple query "python"
```

---

# 📱 VOICE COMMAND EXAMPLES

## English
```
"Search for python programming"
"Find latest AI news"
"What is machine learning?"
"Search quantum computing"
"Tell me about blockchain"
```

## Mandarin Chinese
```
"搜索 Python 编程"
"查找最新的 AI 新闻"
"什么是机器学习"
"搜索量子计算"
"告诉我关于区块链"
```

## Indonesian
```
"Cari Python programming"
"Cari berita AI terbaru"
"Apa itu machine learning"
"Cari tentang quantum computing"
"Beritahu saya tentang blockchain"
```

---

# 🔧 USEFUL PORTS & DEFAULTS

```
Backend Server Port: 8080
Backend Host: 0.0.0.0 (all interfaces)
WebSocket Endpoint: ws://localhost:8080/ws/device
REST API Docs: http://localhost:8080/docs
Health Check: http://localhost:8080/api/health
Search Endpoint: http://localhost:8080/api/search
```

---

# 📚 FILE STRUCTURE

```
xiaozhi-web-search/
├── xiaozhi_backend_main.py      # Main backend server
├── requirements.txt              # Python dependencies
├── .env                          # Configuration (API keys)
└── xiaozhi_backend.log          # Logs (created after run)
```

---

# 💾 SAVING FILES PROPERLY

## Windows Notepad
```
1. File → Save As
2. Choose folder: xiaozhi-web-search
3. Filename: xiaozhi_backend_main.py
4. Save type: All Files (*.*)
5. Click Save
```

## Mac TextEdit
```
1. Format → Make Plain Text
2. File → Save
3. Filename: xiaozhi_backend_main.py
4. File Format: UTF-8
5. Click Save
```

## Linux nano
```
nano xiaozhi_backend_main.py
(paste content)
Ctrl+X → Y → Enter
```

---

# 📞 STILL HAVING ISSUES?

## Debug Steps:

1. **Check logs:**
   ```bash
   # Terminal backend:
   cat xiaozhi_backend.log  # or tail -f
   
   # Device logs:
   # Login ke xiaozhi.me → Device → Logs
   ```

2. **Test connectivity:**
   ```bash
   # Windows:
   ping 192.168.1.100
   netstat -ano | findstr :8080
   
   # Mac/Linux:
   ping -c 4 192.168.1.100
   lsof -i :8080
   ```

3. **Test API manually:**
   ```bash
   curl -v http://localhost:8080/api/health
   curl -v "http://localhost:8080/api/search?query=test"
   ```

4. **Check firewall:**
   - Windows: Settings → Firewall → Allow port 8080
   - Mac: System Preferences → Security → Firewall
   - Linux: sudo ufw allow 8080

5. **Verify configuration:**
   ```bash
   # Check .env file content:
   cat .env
   
   # Should show BRAVE_API_KEY and TAVILY_API_KEY
   ```

---

# 🎓 LEARNING RESOURCES

- FastAPI Docs: https://fastapi.tiangolo.com/
- WebSocket Guide: https://fastapi.tiangolo.com/advanced/websockets/
- MCP Protocol: https://modelcontextprotocol.io/
- XiaoZhi Official: https://xiaozhi.dev
- ESP-IDF Guide: https://docs.espressif.com/

---

# ✨ YOU'RE READY!

Jika sudah selesai semua steps dan semuanya berfungsi:

```
✓ Anda adalah XiaoZhi AI Developer!
✓ Sistem berfungsi dengan baik
✓ Siap untuk eksplorasi lebih lanjut
✓ Bisa customize & extend
✓ Bisa deploy ke production
```

**Selamat! Enjoy your XiaoZhi AI setup! 🚀**

---

**Version: 1.0**
**Updated: June 2026**
**For: Complete Beginners**
