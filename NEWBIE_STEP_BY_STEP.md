# 🎓 XiaoZhi AI Web Search - Panduan Lengkap untuk NEWBIE
## Step-by-Step Implementation Guide

**Durasi total: 30-45 menit**  
**Level: Beginner-friendly**  
**Bahasa: Bahasa Indonesia**

---

## 📚 Daftar Isi

1. [Apa itu XiaoZhi AI?](#apa-itu-xiaozhi-ai)
2. [Yang Perlu Disiapkan](#yang-perlu-disiapkan)
3. [Step 1: Daftar API Key (10 menit)](#step-1-daftar-api-key)
4. [Step 2: Setup Komputer (5 menit)](#step-2-setup-komputer)
5. [Step 3: Download & Setup Project (5 menit)](#step-3-download--setup-project)
6. [Step 4: Konfigurasi File (5 menit)](#step-4-konfigurasi-file)
7. [Step 5: Jalankan Backend (5 menit)](#step-5-jalankan-backend)
8. [Step 6: Test Backend (5 menit)](#step-6-test-backend)
9. [Step 7: Setup Device XiaoZhi (5 menit)](#step-7-setup-device-xiaozhi)
10. [Step 8: Test Voice Commands (5 menit)](#step-8-test-voice-commands)
11. [Troubleshooting](#troubleshooting)

---

## Apa itu XiaoZhi AI?

**XiaoZhi AI** adalah robot AI yang:
- Bisa mendengarkan suara Anda (speech recognition)
- Bisa berbicara balik (text-to-speech)
- Bisa melakukan pencarian internet
- Bisa mengontrol perangkat smart home
- Berjalan di ESP32 (chip kecil seperti Arduino)

**Apa yang kita buat:**
- Backend server untuk handle pencarian internet
- Koneksi antara device XiaoZhi dengan search API
- Voice commands untuk mencari informasi

---

## Yang Perlu Disiapkan

### Hardware 🖥️
- [ ] **1 x Komputer/Laptop** (Windows, Mac, atau Linux)
- [ ] **1 x XiaoZhi Device** (sudah ter-setup dan terhubung WiFi)
- [ ] **Internet connection** (untuk download dan testing)

### Software 📦
Akan kita install dalam tutorial ini:
- Python 3.8+
- FastAPI
- Uvicorn

### Akun Online 🔑
- [ ] **Brave Search API key** (gratis, dapat 2000 queries/bulan)
- [ ] **Tavily API key** (optional, gratis, dapat 1000 queries/bulan)
- [ ] **Akun XiaoZhi Console** (di xiaozhi.me)

### Pengetahuan 📖
- Dasar Command Line (terminal/CMD)
- Memahami IP address lokal
- Tidak perlu bisa programming!

---

# STEP 1: Daftar API Key
## ⏱️ Durasi: 10 menit

Kita butuh API key untuk bisa melakukan pencarian web.

### Opsi A: Brave Search API (RECOMMENDED untuk pemula)

**Langkah 1a: Buka website Brave Search**
```
Buka browser → Ketik di address bar:
https://brave.com/search/api/
```

Seharusnya muncul halaman seperti ini:
```
┌─────────────────────────────────────┐
│ Brave Search API                    │
│                                     │
│ [Sign Up Button]                    │
│ Get 2000 free queries a month       │
└─────────────────────────────────────┘
```

**Langkah 1b: Click "Sign Up"**
- Klik tombol "Sign Up"
- Isi email Anda
- Buat password
- Centang "I agree to terms"
- Click "Create Account"

**Langkah 1c: Verifikasi Email**
- Cek email inbox Anda
- Klik link verifikasi dari Brave
- Klik "Verify Email"

**Langkah 1d: Dapatkan API Key**
Setelah login, Anda akan melihat:
```
┌───────────────────────────────────────┐
│ Dashboard                             │
│                                       │
│ Subscription: Free                    │
│ Queries: 0 / 2000                     │
│                                       │
│ API Key:                              │
│ ┌─────────────────────────────┐       │
│ │ sk_live_XXXXXXXXXXXX... │ [Copy]   │
│ └─────────────────────────────┘       │
└───────────────────────────────────────┘
```

**🎯 ACTION: Copy API key ini dan simpan di notepad atau text editor**

Contoh API key (JANGAN gunakan ini, ini contoh):
```
sk_live_aB3dE4fG5hI6jK7lM8nO9pQ0rS1tU2v
```

---

### Opsi B: Tavily AI API (Optional)

Jika ingin backup atau mencoba provider lain:

**Langkah 1e: Buka Tavily**
```
https://tavily.com
```

**Langkah 1f: Sign Up**
- Click "Sign Up"
- Isi email
- Verify email
- Login

**Langkah 1g: Get API Key**
- Di dashboard, cari "API Key"
- Copy dan simpan

---

## ✅ Setelah Step 1, Anda punya:
- ✓ Brave API Key (wajib)
- ✓ Tavily API Key (optional)

**LANJUT KE STEP 2**

---

# STEP 2: Setup Komputer
## ⏱️ Durasi: 5 menit

Kita perlu install Python di komputer.

### Untuk Windows 🪟

**Langkah 2a: Download Python**
```
Buka browser → https://www.python.org/downloads/
```

Halaman akan terlihat seperti:
```
┌──────────────────────────────┐
│ Python.org                   │
│                              │
│ [Download Python 3.11]       │
│ (atau versi terbaru)         │
└──────────────────────────────┘
```

**Langkah 2b: Click tombol download**
- Klik "Download Python 3.11" (atau versi terbaru)
- File akan download ke folder "Downloads"

**Langkah 2c: Install Python**
- Cari file yang baru download di folder Downloads
- Nama file: `python-3.11.x-amd64.exe`
- Double-click untuk buka installer

**PENTING: Centang ini saat install:**
```
┌─────────────────────────────────┐
│ Python 3.11 Installer           │
│                                 │
│ ☑ Add Python to PATH            │ ← JANGAN LUPA!!!
│ ☑ Install pip                   │ ← JANGAN LUPA!!!
│ [ ] Install for all users       │
│                                 │
│ [Next] [Install]                │
└─────────────────────────────────┘
```

Klik "Install Now" dan tunggu sampai selesai.

**Langkah 2d: Verifikasi Install**
- Buka Command Prompt (CMD):
  - Click tombol Windows
  - Ketik: `cmd`
  - Press Enter
  
- Ketik di CMD:
```bash
python --version
```

Harusnya muncul:
```
Python 3.11.x
```

Jika muncul, berarti Python terinstall dengan benar! ✓

---

### Untuk Mac 🍎

**Langkah 2e: Download Python**
```
Safari → https://www.python.org/downloads/
```

**Langkah 2f: Click tombol "Download Python"**
- Download file `.pkg`

**Langkah 2g: Install**
- Double-click file `.pkg`
- Ikuti installer prompts
- Klik "Continue", "Agree", "Install"

**Langkah 2h: Verifikasi**
- Buka Terminal:
  - Cmd + Space
  - Ketik: `terminal`
  - Press Enter

- Ketik:
```bash
python3 --version
```

---

### Untuk Linux 🐧

```bash
# Buka Terminal dan jalankan:
sudo apt-get update
sudo apt-get install python3.11 python3-pip
python3 --version
```

---

## ✅ Setelah Step 2, Anda punya:
- ✓ Python terinstall
- ✓ Python bisa dijalankan dari Command Line

**LANJUT KE STEP 3**

---

# STEP 3: Download & Setup Project
## ⏱️ Durasi: 5 menit

Sekarang kita download semua file yang kita butuhkan.

### Langkah 3a: Buat Folder Project

**Windows:**
```
1. Buka File Explorer (atau klik folder icon di taskbar)
2. Navigasi ke folder Documents
3. Right-click → New → Folder
4. Beri nama: xiaozhi-web-search
```

**Mac/Linux:**
```bash
# Buka Terminal dan ketik:
mkdir ~/xiaozhi-web-search
cd ~/xiaozhi-web-search
```

### Langkah 3b: Download Files

Ada dua cara untuk mendapatkan files:

#### **Cara A: Copy Paste Manual (Untuk Pemula)**

1. **Buat file: `xiaozhi_backend_main.py`**
   - Buka Notepad (Windows) atau TextEdit (Mac)
   - Copy seluruh isi kode dari file `xiaozhi_backend_main.py`
   - Paste ke editor
   - Save dengan nama: `xiaozhi_backend_main.py`
   - Letakkan di folder `xiaozhi-web-search`

2. **Buat file: `requirements.txt`**
   - Buka Notepad
   - Copy:
   ```
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   httpx==0.25.0
   pydantic==2.5.0
   python-dotenv==1.0.0
   ```
   - Save dengan nama: `requirements.txt`
   - Letakkan di folder `xiaozhi-web-search`

3. **Buat file: `.env`**
   - Buka Notepad
   - Copy:
   ```
   BRAVE_API_KEY=your_brave_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   BACKEND_HOST=0.0.0.0
   BACKEND_PORT=8080
   LOG_LEVEL=info
   DEBUG=false
   ```
   - Save dengan nama: `.env`
   - Letakkan di folder `xiaozhi-web-search`

#### **Cara B: Download dari GitHub**
(Jika sudah familiar dengan Git)
```bash
cd ~
git clone <repo-url>
cd xiaozhi-web-search
```

### Langkah 3c: Verifikasi Files

Setelah selesai, folder `xiaozhi-web-search` seharusnya berisi:
```
xiaozhi-web-search/
├── xiaozhi_backend_main.py
├── requirements.txt
└── .env
```

**Untuk verifikasi:**
- Windows: Buka File Explorer, masuk ke folder xiaozhi-web-search
- Mac/Linux: 
  ```bash
  ls -la ~/xiaozhi-web-search
  ```

---

## ✅ Setelah Step 3, Anda punya:
- ✓ Folder project dengan semua files
- ✓ Siap untuk konfigurasi

**LANJUT KE STEP 4**

---

# STEP 4: Konfigurasi File
## ⏱️ Durasi: 5 menit

Sekarang kita masukkan API key ke file `.env`.

### Langkah 4a: Buka file `.env`

**Windows:**
1. Buka File Explorer
2. Navigasi ke folder `xiaozhi-web-search`
3. Cari file `.env`
4. Right-click → Open with → Notepad

**Mac/Linux:**
```bash
nano ~/.xiaozhi-web-search/.env
# atau
vi ~/.xiaozhi-web-search/.env
```

### Langkah 4b: Edit file `.env`

File asli terlihat seperti:
```
BRAVE_API_KEY=your_brave_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8080
LOG_LEVEL=info
DEBUG=false
```

**Ganti dengan API key Anda:**

Contoh (JANGAN copy ini, gunakan key Anda sendiri):
```
BRAVE_API_KEY=sk_live_aB3dE4fG5hI6jK7lM8nO9pQ0rS1tU2v
TAVILY_API_KEY=tvly_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8080
LOG_LEVEL=info
DEBUG=false
```

### Langkah 4c: Save file

**Windows Notepad:**
- Tekan `Ctrl + S`
- Atau File → Save

**Mac/Linux:**
- Nano: Tekan `Ctrl + X`, lalu `Y`, lalu `Enter`
- Vi: Tekan `Esc`, ketik `:wq`, tekan `Enter`

### Langkah 4d: Verifikasi

Buka file lagi dengan text editor untuk memastikan sudah tersave:
```
BRAVE_API_KEY=sk_live_xxxx... ✓
TAVILY_API_KEY=tvly_xxxx... ✓
```

---

## ⚠️ PENTING: API Key Security

**JANGAN pernah:**
- ❌ Share API key ke orang lain
- ❌ Upload `.env` ke GitHub
- ❌ Screenshot dengan API key terlihat
- ❌ Jangan commit `.env` ke version control

**Selalu:**
- ✓ Simpan di tempat aman
- ✓ Gunakan `.env` untuk dev, secret management untuk production
- ✓ Rotate key secara berkala jika exposed

---

## ✅ Setelah Step 4, Anda punya:
- ✓ File `.env` dengan API key yang benar
- ✓ Siap untuk jalankan backend

**LANJUT KE STEP 5**

---

# STEP 5: Jalankan Backend
## ⏱️ Durasi: 5 menit

Ini adalah momen krusial! Kita akan menjalankan backend server.

### Langkah 5a: Buka Terminal/Command Prompt

**Windows:**
1. Tekan tombol Windows + R
2. Ketik: `cmd`
3. Tekan Enter

Atau:
1. Buka folder `xiaozhi-web-search` di File Explorer
2. Di address bar, ketik: `cmd`
3. Tekan Enter

**Mac/Linux:**
1. Buka Terminal (Cmd+Space → Terminal)
2. Atau: Applications → Utilities → Terminal

### Langkah 5b: Navigasi ke folder project

**Windows CMD:**
```bash
cd Documents\xiaozhi-web-search
# Atau dimana Anda simpan foldernya
```

**Mac/Linux Terminal:**
```bash
cd ~/xiaozhi-web-search
```

### Langkah 5c: Install Python Dependencies

Ketik command ini di terminal:

```bash
pip install -r requirements.txt
```

Terminal akan menampilkan:
```
Collecting fastapi==0.104.1
  Downloading fastapi-0.104.1-py3-none-any.whl (92 kB)
     |████████████████████████████████| 92 kB ...
Installing collected packages: fastapi, uvicorn, httpx, pydantic, python-dotenv
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

**⏳ Tunggu sampai semua selesai install (1-2 menit)**

### Langkah 5d: Jalankan Backend

Ketik:
```bash
python xiaozhi_backend_main.py
```

**Jika sukses, terminal akan menampilkan:**
```
INFO:     Uvicorn running on http://0.0.0.0:8080
INFO:     Application startup complete
```

Artnya:
- ✅ Backend sudah jalan
- ✅ Listen di port 8080
- ✅ Siap untuk menerima request

**🎉 BACKEND SUDAH RUNNING!**

**JANGAN tutup terminal ini!** Biarkan backend terus jalan.

---

## Apa yang terjadi di background?

```
Backend Server (Port 8080)
├── FastAPI Framework
├── Web Search Service
│   ├── Brave Search API connector
│   └── Tavily Search API connector
├── WebSocket Handler (untuk XiaoZhi device)
└── REST API Endpoints
    ├── /api/search
    ├── /api/health
    └── /docs (Swagger UI)
```

---

## ✅ Setelah Step 5, Anda punya:
- ✓ Backend server berjalan
- ✓ Listen di http://localhost:8080
- ✓ Ready untuk test dan connect device

**LANJUT KE STEP 6 (TERMINAL BARU!)**

---

# STEP 6: Test Backend
## ⏱️ Durasi: 5 menit

Sekarang kita test apakah backend bekerja dengan benar.

### Langkah 6a: Buka Terminal/Command Prompt BARU

**PENTING: Jangan tutup terminal yang menjalankan backend!**

Buka terminal baru:

**Windows:**
1. Tekan tombol Windows + R
2. Ketik: `cmd`
3. Tekan Enter

**Mac/Linux:**
- Buka Terminal baru (Cmd+T atau File → New Tab)

### Langkah 6b: Test Health Check

Ketik command ini:

**Windows:**
```bash
curl http://localhost:8080/api/health
```

**Mac/Linux:**
```bash
curl http://localhost:8080/api/health
```

Seharusnya muncul response:
```json
{
  "status":"healthy",
  "timestamp":"2024-06-21T10:30:45.123456",
  "connected_devices":0,
  "brave_configured":true,
  "tavily_configured":true
}
```

✓ **Jika muncul JSON response, berarti backend berfungsi!**

---

### Langkah 6c: Test Search Functionality

Ketik command untuk search:

```bash
curl "http://localhost:8080/api/search?query=python+programming&provider=brave&count=5"
```

Seharusnya muncul:
```json
{
  "success": true,
  "query": "python programming",
  "provider": "brave",
  "results": [
    {
      "title": "Welcome to Python.org",
      "url": "https://www.python.org",
      "description": "The official home of the Python Programming Language",
      "page_age": null
    },
    ...
  ],
  "total": 5,
  "timestamp": "2024-06-21T10:31:15.234567"
}
```

✓ **Jika muncul hasil search, berarti API connection bekerja!**

---

### Langkah 6d: Test dengan Web Browser (Alternative)

Jika tidak familiar dengan curl, bisa gunakan browser:

1. Buka browser (Chrome, Firefox, Safari)
2. Ketik di address bar:
```
http://localhost:8080/docs
```

3. Seharusnya muncul halaman Swagger UI:
```
┌─────────────────────────────────────┐
│ XiaoZhi Web Search Backend           │
│ API Documentation                    │
│                                     │
│ GET /api/health                      │
│ POST /api/search                     │
│ GET /api/search                      │
│                                     │
│ [Try it out]                         │
└─────────────────────────────────────┘
```

4. Click "GET /api/health"
5. Click "Try it out"
6. Click "Execute"

Harusnya muncul response di bawah.

---

## Jika ada error:

**Error 1: "Connection refused"**
```
Solusi:
1. Pastikan terminal backend masih jalan (lihat Step 5)
2. Port 8080 tidak digunakan aplikasi lain
3. Coba ganti port di .env (misal 8081)
```

**Error 2: "API Key invalid"**
```
Solusi:
1. Check .env file sudah isi BRAVE_API_KEY
2. API key tidak ada typo
3. Restart backend (Ctrl+C, lalu jalankan lagi)
```

---

## ✅ Setelah Step 6, Anda punya:
- ✓ Backend berjalan dengan benar
- ✓ API endpoints berfungsi
- ✓ Koneksi ke search API sukses
- ✓ Siap untuk connect device XiaoZhi

**LANJUT KE STEP 7**

---

# STEP 7: Setup Device XiaoZhi
## ⏱️ Durasi: 5 menit

Sekarang kita connect device XiaoZhi ke backend server.

### Prasyarat:
- [ ] Device XiaoZhi sudah on
- [ ] Device terhubung ke WiFi yang sama dengan komputer
- [ ] Punya akun xiaozhi.me
- [ ] Backend server masih jalan

### Langkah 7a: Login ke XiaoZhi Console

1. Buka browser
2. Ketik: `https://xiaozhi.me`
3. Login dengan akun Anda

Seharusnya muncul halaman:
```
┌──────────────────────────────┐
│ XiaoZhi Console              │
│                              │
│ My Devices:                  │
│ ├── XiaoZhi Speaker #1234    │
│ └── [Edit] [Settings]        │
└──────────────────────────────┘
```

### Langkah 7b: Pilih Device Anda

1. Click pada device name atau icon
2. Akan muncul halaman detail device

### Langkah 7c: Cari Settings/Backend Configuration

Cari tab atau menu yang namanya:
- "Settings"
- "Backend Configuration"
- "Advanced Settings"
- "Network Settings"

Halaman seharusnya terlihat seperti:
```
┌────────────────────────────────────┐
│ Device Settings                    │
│                                   │
│ Backend Configuration:             │
│ ┌────────────────────────────────┐ │
│ │ Backend URL:                   │ │
│ │ [_________________________]    │ │
│ │ Contoh:                        │ │
│ │ ws://192.168.1.100:8080/ws/... │ │
│ └────────────────────────────────┘ │
│                                   │
│ MCP Enabled: [Toggle]              │
│ Web Search: [Toggle]               │
│                                   │
│ [Save] [Cancel]                    │
└────────────────────────────────────┘
```

### Langkah 7d: Dapatkan IP Address Komputer Anda

**Windows:**
Buka Command Prompt dan ketik:
```bash
ipconfig
```

Cari baris "IPv4 Address", contoh:
```
IPv4 Address . . . . . . . . . . . : 192.168.1.100
```

**Mac/Linux:**
Buka Terminal dan ketik:
```bash
ifconfig | grep inet
# Atau:
hostname -I
```

Cari IP yang dimulai dengan 192.168.x.x atau 10.0.x.x

### Langkah 7e: Input Backend URL

Di field "Backend URL", ketik:
```
ws://192.168.1.100:8080/ws/device
```

**Catatan:**
- Ganti `192.168.1.100` dengan IP address komputer Anda
- Gunakan `ws://` (bukan `http://`)
- Port harus `8080` (sesuai di .env)
- Path harus `/ws/device`

### Langkah 7f: Enable Features

Pastikan toggle ini ON:
- [✓] MCP Enabled
- [✓] Web Search

### Langkah 7g: Save Configuration

1. Click tombol "Save"
2. Tunggu notification "Settings saved successfully"
3. Device akan restart secara otomatis

Terminal backend seharusnya menampilkan:
```
INFO: New device connected via WebSocket
INFO: Device registered successfully
```

✅ **Device berhasil connect ke backend!**

---

## Alternatif: Via Config File (Advanced)

Jika console tidak ada opsi backend configuration:

1. Download config file dari device
2. Edit dengan text editor
3. Ubah:
```json
{
  "backend": {
    "url": "ws://192.168.1.100:8080/ws/device",
    "mcp_enabled": true
  },
  "features": {
    "web_search": true
  }
}
```
4. Upload kembali ke device

---

## ✅ Setelah Step 7, Anda punya:
- ✓ Device terhubung ke backend
- ✓ MCP protocol active
- ✓ Web search feature enabled
- ✓ Siap untuk test voice commands

**LANJUT KE STEP 8**

---

# STEP 8: Test Voice Commands
## ⏱️ Durasi: 5 menit

Ini adalah moment terakhir sebelum semuanya working! Mari test dengan suara.

### Langkah 8a: Pastikan Setup Lengkap

Checklist sebelum mulai:
- [ ] Backend server still running (terminal Step 5)
- [ ] Device XiaoZhi on dan connected
- [ ] Internet stabil
- [ ] Speaker/audio output aktif
- [ ] Microphone berfungsi

### Langkah 8b: Activate Voice

Ada dua cara untuk activate device:

**Cara A: Wake Word (Default)**
Katakan:
```
"小智" (Xiaozhi)
# Atau dalam bahasa lokal Anda
"Xiaozhi"
"Hey Xiaozhi"
```

Device akan merespons dengan beep atau prompt "Listening..."

**Cara B: Press Button**
Tekan tombol di device (jika ada physical button)

Seharusnya akan terdengar suara dari speaker:
```
"listening..." atau suara prompt
```

### Langkah 8c: Berikan Voice Command untuk Search

Setelah device "listening", katakan perintah search:

#### **Contoh Command 1 (Simple)**
```
"搜索 Python 编程"
"Cari Python programming"
"Search for machine learning"
```

Device akan:
1. Menangkap suara → ASR (speech recognition)
2. Mengirim ke backend
3. Backend melakukan search
4. Mengkonversi hasil ke suara → TTS
5. Play audio response

Seharusnya Anda dengar:
```
"搜索结果:... 第一个结果是 ..."
"Search results: ... First result is ..."
```

#### **Contoh Command 2 (Dengan jumlah hasil)**
```
"搜索 AI 最新新闻，给我 10 个结果"
"Cari berita AI terbaru, berikan 10 hasil"
"Search latest AI news, show me 5 results"
```

#### **Contoh Command 3 (Specific Question)**
```
"小智，Python 是什么？"
"Xiaozhi, apa itu machine learning?"
"Tell me about quantum computing"
```

### Langkah 8d: Monitor Terminal Backend

Di terminal backend (dari Step 5), Anda seharusnya lihat logs:

```
INFO: Search request: query=python programming, provider=brave
INFO: Brave search: python programming (count=5)
INFO: Tool call: web_search with args {'query': 'python programming', 'count': 5}
```

Ini menunjukkan bahwa:
- ✓ Device mengirim request
- ✓ Backend menerima request
- ✓ Search API dipanggil
- ✓ Hasil dikembalikan

---

## Test Cases:

| Command | Expected Result | Status |
|---------|-----------------|--------|
| "Search Python" | Menerima 5 hasil | ✓/✗ |
| "Search AI news" | Menerima hasil berita | ✓/✗ |
| "Cari COVID-19" | Hasil terkini | ✓/✗ |
| "搜索 天气" | Weather related | ✓/✗ |

---

## Jika Ada Issues:

### Issue 1: Device tidak "listening"
```
Solusi:
1. Pastikan device on dan terhubung WiFi
2. Check console xiaozhi.me apakah device online
3. Coba tekan physical button (jika ada)
4. Restart device
```

### Issue 2: Backend tidak menerima request
```
Solusi:
1. Check backend URL di device config benar
2. Ping device dari komputer:
   Windows: ping 192.168.1.xxx
   Mac/Linux: ping -c 4 192.168.1.xxx
3. Lihat logs backend, ada error?
4. Check firewall port 8080 open
```

### Issue 3: Search tidak return hasil
```
Solusi:
1. Cek di terminal backend, ada error?
2. Pastikan API key di .env sudah benar
3. Test manual search:
   curl "http://localhost:8080/api/search?query=test"
4. Check API quota (Brave max 2000/month)
```

### Issue 4: Audio response tidak terdengar
```
Solusi:
1. Check speaker volume di device
2. Cek audio output connected
3. Lihat di device logs apakah TTS berhasil
4. Try dengan browser speaker dulu (play test audio)
```

---

## ✅ Setelah Step 8, Anda punya:
- ✓ Seluruh sistem working end-to-end
- ✓ Voice commands dapat dijalankan
- ✓ Search results dikembalikan
- ✓ Audio response terdengar
- ✓ **SIAP UNTUK PRODUCTION!**

---

# CONGRATULATIONS! 🎉

Anda berhasil setup XiaoZhi AI dengan Web Search Integration!

## Apa yang sudah Anda capai:

✅ Backend server berjalan  
✅ API endpoints aktif  
✅ Device XiaoZhi terhubung  
✅ Voice commands working  
✅ Search functionality operational  

---

# TROUBLESHOOTING GUIDE
## Jika Masih Ada Problem

### A. Terminal/Installation Issues

**Problem: "Python command not found"**
```
Windows: 
- Pastikan python di-add ke PATH saat install
- Restart CMD setelah install
- Coba: py --version

Mac/Linux:
- Gunakan python3 bukan python
- python3 --version
```

**Problem: "pip is not recognized"**
```
Windows:
- Restart komputer setelah install Python
- Atau jalankan: python -m pip install -r requirements.txt

Mac/Linux:
- Gunakan pip3 bukan pip
- pip3 install -r requirements.txt
```

---

### B. Backend Issues

**Problem: "ModuleNotFoundError: No module named 'fastapi'"**
```
Solusi:
1. Pastikan sudah run: pip install -r requirements.txt
2. Pastikan di folder yang benar: cd xiaozhi-web-search
3. Verifikasi install sukses:
   pip list | grep fastapi
```

**Problem: "Address already in use" di port 8080**
```
Windows:
netstat -ano | findstr :8080
taskkill /PID [PID_NUMBER] /F

Mac/Linux:
lsof -i :8080
kill -9 [PID_NUMBER]

Atau ganti port di .env ke 8081
```

**Problem: "BRAVE_API_KEY not configured"**
```
Solusi:
1. Check .env file ada BRAVE_API_KEY
2. Tidak ada typo di key
3. Pastikan sudah save .env
4. Restart backend dengan Ctrl+C dan jalankan lagi
```

---

### C. Device Connection Issues

**Problem: Device tidak terlihat di console xiaozhi.me**
```
Solusi:
1. Check device on dan punya power
2. Device terhubung WiFi (lihat LED indicator)
3. Restart device
4. Factory reset jika sudah coba semua
```

**Problem: "Backend URL tidak valid"**
```
Solusi:
1. Test IP address benar:
   Windows CMD: ipconfig
   Mac/Linux: ifconfig | grep inet
   
2. Test koneksi:
   ping 192.168.1.100 (ganti dengan IP Anda)
   
3. Test backend:
   curl http://192.168.1.100:8080/api/health
```

**Problem: Device connect tapi timeout**
```
Solusi:
1. Check firewall jangan block port 8080
2. Device dan komputer di WiFi yang sama
3. Tidak ada password WiFi yang minta re-auth
4. Coba hardwire with ethernet (jika bisa)
```

---

### D. Search Issues

**Problem: "Search returns empty results"**
```
Solusi:
1. Check API key valid di dashboard Brave/Tavily
2. Check quota tidak exceeded (2000/month)
3. Test query sederhana dulu: "python"
4. Cek internet connection stabil
```

**Problem: "Special characters tidak support"**
```
Solusi:
1. Backend support Unicode, pastikan terminal punya UTF-8
2. Coba dengan query English dulu
3. Check device keyboard input benar
```

---

### E. Voice/Audio Issues

**Problem: "Device tidak menangkap suara"**
```
Solusi:
1. Check microphone terhubung
2. Microphone tidak muted
3. Volume input tidak minimal
4. Test dengan aplikasi recording lain dulu
```

**Problem: "Audio output tidak kerja"**
```
Solusi:
1. Speaker/headphone terhubung
2. Audio tidak muted
3. Volume output tidak 0
4. Test dengan music player dulu
```

**Problem: "Suara hasil tidak terdengar jelas"**
```
Solusi:
1. Reduce background noise
2. Increase speaker volume
3. Try different microphone/speaker
4. Check device temperature (jangan panas)
```

---

### F. Network Issues

**Problem: "Cannot reach backend from device"**
```
Solusi:
1. Ping test:
   From device side, ping komputer
   ping 192.168.1.100
   
2. Check firewall:
   Windows: Settings → Firewall → Allow port 8080
   Mac: System Preferences → Security → Firewall
   Linux: sudo ufw allow 8080

3. Check WiFi SSID same:
   Device dan komputer harus di WiFi yang sama
   Bukan guest network yang isolated
```

**Problem: "DNS resolution failed"**
```
Solusi:
1. Gunakan IP address langsung bukan hostname
   ✓ ws://192.168.1.100:8080
   ✗ ws://mycomputer.local:8080
   
2. Check DNS di router settings
3. Try dengan hardwire Ethernet
```

---

## Getting Help

Jika masih bermasalah:

1. **Check logs:**
   - Terminal backend: lihat error message
   - Device logs: di console xiaozhi.me
   - Browser console: F12 → Console tab

2. **Provide information:**
   - Exact error message
   - OS (Windows/Mac/Linux)
   - Device model
   - Network setup (WiFi/Ethernet)

3. **Resources:**
   - XiaoZhi Discord/Community
   - GitHub Issues: https://github.com/78/xiaozhi-esp32
   - Official Docs: https://xiaozhi.dev

---

# NEXT STEPS

Sekarang backend sudah berjalan, Anda bisa:

## 1. Customization

- Ganti search provider (Google, Bing, dll)
- Tambah custom tools (weather, email, dll)
- Ubah response format
- Add caching dengan Redis

## 2. Deployment

- Deploy ke cloud (Railway, Render, AWS)
- Use Docker untuk containerization
- Setup reverse proxy (nginx)
- Add SSL/HTTPS certificate

## 3. Monitoring

- Setup logging sistem
- Add metrics collection
- Create monitoring dashboard
- Setup alerts

## 4. Production Hardening

- Add rate limiting
- Implement authentication
- Add request validation
- Setup backup & recovery

## 5. Features Extension

- Add email integration
- Weather API integration
- Smart home control
- Database integration

---

# SUMMARY

```
┌─────────────────────────────────────────────────────────┐
│                  XiaoZhi AI Web Search                  │
│                  Implementation Complete!                │
├─────────────────────────────────────────────────────────┤
│ ✓ Backend Server Running (Port 8080)                    │
│ ✓ API Endpoints Functional                              │
│ ✓ Web Search Integration Working                        │
│ ✓ Device Connected & Configured                         │
│ ✓ Voice Commands Operational                            │
│ ✓ End-to-End System Tested                              │
├─────────────────────────────────────────────────────────┤
│ You are now ready to:                                   │
│ • Use voice commands for web search                     │
│ • Deploy to production                                  │
│ • Extend with custom features                           │
│ • Scale to multiple devices                             │
└─────────────────────────────────────────────────────────┘
```

---

## Total Time Investment:
- Setup: 30-45 minutes ⏱️
- Learning: Invaluable 📚
- Results: Amazing! 🎉

---

**Selamat! Anda sudah menjadi XiaoZhi AI Developer!** 🚀

Jika ada pertanyaan atau butuh bantuan lebih lanjut, jangan ragu untuk bertanya!

---

**Last Updated: June 2026**
**Version: 1.0**
**Difficulty: Beginner**
**Estimated Completion: 30-45 minutes**
