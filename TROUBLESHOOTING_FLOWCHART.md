# 🔍 XiaoZhi Setup - Troubleshooting Flowchart
## Visual Guide untuk Problem-Solving

---

## DECISION TREE: Apa yang tidak bekerja?

```
START
  │
  ├─→ Backend tidak jalan?
  │     └─→ Go to: SECTION A
  │
  ├─→ Backend jalan tapi error?
  │     └─→ Go to: SECTION B
  │
  ├─→ Device tidak connect?
  │     └─→ Go to: SECTION C
  │
  ├─→ Search tidak return hasil?
  │     └─→ Go to: SECTION D
  │
  ├─→ Suara tidak terdengar?
  │     └─→ Go to: SECTION E
  │
  └─→ Lainnya?
        └─→ Go to: SECTION F (Advanced)
```

---

# SECTION A: Backend Tidak Jalan

## A1: Error: "command not found: python"

```
┌─────────────────────────────────────┐
│ Problem: python command not found   │
├─────────────────────────────────────┤
│ Kemungkinan penyebab:                │
│ 1. Python belum diinstall            │
│ 2. Python tidak di-add ke PATH       │
│ 3. Terminal tidak di-restart         │
└─────────────────────────────────────┘

FIX:
┌──────────────────────────────┐
│ STEP 1: Pastikan Python Ada  │
├──────────────────────────────┤
│ Windows:                      │
│ → Start Menu → Search         │
│   "Python"                    │
│ → Jika tidak ada, install     │
│   dari python.org             │
│                              │
│ Mac/Linux:                    │
│ → Terminal: which python3     │
│ → Jika tidak ada, install     │
│   dengan homebrew/apt-get     │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Restart Terminal      │
├──────────────────────────────┤
│ Windows:                      │
│ → Close CMD                   │
│ → Open CMD baru               │
│                              │
│ Mac/Linux:                    │
│ → Close Terminal              │
│ → Open Terminal baru          │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Test                  │
├──────────────────────────────┤
│ Windows:                      │
│ → python --version            │
│                              │
│ Mac/Linux:                    │
│ → python3 --version           │
│                              │
│ Expected: Python 3.11.x       │
└──────────────────────────────┘

✓ FIXED: Lanjut ke run backend
✗ MASIH ERROR: Go to A2
```

---

## A2: Error: "ModuleNotFoundError: No module named 'fastapi'"

```
┌──────────────────────────────────────┐
│ Problem: fastapi module tidak ada     │
├──────────────────────────────────────┤
│ Penyebab:                             │
│ 1. pip install -r requirements.txt    │
│    belum dijalankan                   │
│ 2. Install gagal / incomplete         │
│ 3. Virtual environment berbeda        │
└──────────────────────────────────────┘

FIX:
┌──────────────────────────────┐
│ STEP 1: Cek requirements.txt  │
├──────────────────────────────┤
│ Windows:                      │
│ → dir requirements.txt        │
│                              │
│ Mac/Linux:                    │
│ → ls requirements.txt         │
│                              │
│ Expected: File ada            │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Install Dependencies  │
├──────────────────────────────┤
│ Windows:                      │
│ → pip install -r requirements.txt
│ → Tunggu sampai selesai       │
│                              │
│ Mac/Linux:                    │
│ → pip3 install -r requirements.txt
│ → Tunggu sampai selesai       │
│                              │
│ Expected: "Successfully       │
│ installed..." message         │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Verify Installation   │
├──────────────────────────────┤
│ Windows:                      │
│ → pip list | findstr fastapi  │
│                              │
│ Mac/Linux:                    │
│ → pip3 list | grep fastapi    │
│                              │
│ Expected: fastapi 0.104.1     │
└──────────────────────────────┘

✓ FIXED: Try run backend again
✗ MASIH ERROR: Go to A3
```

---

## A3: Error: "Address already in use" (port 8080)

```
┌──────────────────────────────────┐
│ Problem: Port 8080 sedang        │
│ digunakan aplikasi lain          │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. Backend sudah running         │
│ 2. Aplikasi lain pakai port 8080 │
│ 3. Port belum fully released     │
└──────────────────────────────────┘

FIX - OPTION A: Kill existing process

┌──────────────────────────────┐
│ Windows:                      │
├──────────────────────────────┤
│ 1. Command Prompt:            │
│    netstat -ano | findstr     │
│    8080                       │
│                              │
│    Output:                    │
│    TCP ... LISTENING 4892     │
│    (catat number: 4892)       │
│                              │
│ 2. Kill process:              │
│    taskkill /PID 4892 /F      │
│                              │
│ 3. Verify:                    │
│    netstat -ano | findstr 8080│
│    (seharusnya tidak ada)     │
└──────────────────────────────┘

┌──────────────────────────────┐
│ Mac/Linux:                    │
├──────────────────────────────┤
│ 1. Terminal:                  │
│    lsof -i :8080              │
│                              │
│    Output:                    │
│    python 4892 user TCP ...   │
│    (catat: 4892)              │
│                              │
│ 2. Kill process:              │
│    kill -9 4892               │
│                              │
│ 3. Verify:                    │
│    lsof -i :8080              │
│    (seharusnya tidak ada)     │
└──────────────────────────────┘

FIX - OPTION B: Ganti port

┌──────────────────────────────┐
│ 1. Edit .env file:            │
│    BACKEND_PORT=8080 →        │
│    BACKEND_PORT=8081          │
│                              │
│ 2. Save file                  │
│                              │
│ 3. Restart backend            │
│                              │
│ 4. Test dengan port baru:     │
│    curl http://localhost:8081 │
│    /api/health                │
└──────────────────────────────┘

✓ FIXED: Backend seharusnya jalan
✗ MASIH ERROR: Go to A4
```

---

## A4: Backend jalan tapi tidak respond

```
┌──────────────────────────────────┐
│ Problem: Backend jalan tapi       │
│ tidak bisa diakses (timeout)      │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. Firewall block port           │
│ 2. Backend hang/crash            │
│ 3. Wrong IP/port                 │
│ 4. Network issue                 │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Check terminal output │
├──────────────────────────────┤
│ Lihat di terminal backend:    │
│                              │
│ ✓ GOOD:                       │
│ "Uvicorn running on          │
│  http://0.0.0.0:8080"        │
│                              │
│ ✗ BAD:                        │
│ Error messages atau crash     │
│                              │
│ Action: Restart backend       │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Test locally           │
├──────────────────────────────┤
│ Windows/Mac/Linux:            │
│                              │
│ 1. Di terminal baru:          │
│    curl http://localhost:     │
│    8080/api/health            │
│                              │
│ 2. Expected output:           │
│    {"status":"healthy"...}    │
│                              │
│ ✓ Success: Firewall issue     │
│ ✗ Error: Backend problem      │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Check firewall         │
├──────────────────────────────┤
│ Windows:                      │
│ Settings → Firewall           │
│ → Allow app → Find Python     │
│ → Check port 8080             │
│                              │
│ Mac:                          │
│ System Prefs → Security       │
│ → Firewall → Options          │
│ → Allow port 8080             │
│                              │
│ Linux:                        │
│ sudo ufw allow 8080           │
│ sudo ufw status               │
└──────────────────────────────┘

✓ FIXED: Backend should work
✗ MASIH ERROR: Go to F (Advanced)
```

---

# SECTION B: Backend Error Messages

## B1: Error: "BRAVE_API_KEY not configured"

```
┌──────────────────────────────────┐
│ Problem: API key tidak ada/       │
│ tidak terbaca                    │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. .env file tidak ada           │
│ 2. BRAVE_API_KEY tidak diisi     │
│ 3. .env tidak di-load            │
│ 4. Typo di .env                  │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Verifikasi .env ada   │
├──────────────────────────────┤
│ Windows:                      │
│ dir .env                      │
│                              │
│ Mac/Linux:                    │
│ ls .env                       │
│                              │
│ Expected: File ada            │
│ ✗ Not found: File tidak ada   │
│   → Copy .env.example ke .env │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Check .env content    │
├──────────────────────────────┤
│ Windows:                      │
│ type .env                     │
│                              │
│ Mac/Linux:                    │
│ cat .env                      │
│                              │
│ Expected:                     │
│ BRAVE_API_KEY=sk_live_...     │
│                              │
│ ✗ Empty or wrong:             │
│ → Edit .env, isi API key      │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Check for typo         │
├──────────────────────────────┤
│ WRONG:                        │
│ BRAVE_API_KEY =sk_live_...    │
│ (space sebelum =)             │
│                              │
│ WRONG:                        │
│ BRAVE_API_KEY= sk_live_...    │
│ (space setelah =)             │
│                              │
│ WRONG:                        │
│ BRAVE_APIKEY=sk_live_...      │
│ (typo nama variable)          │
│                              │
│ CORRECT:                      │
│ BRAVE_API_KEY=sk_live_...     │
│ (no spaces)                   │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 4: Restart backend        │
├──────────────────────────────┤
│ 1. Terminal backend:          │
│    Ctrl+C (stop backend)      │
│                              │
│ 2. Run again:                 │
│    python xiaozhi_backend     │
│    _main.py                   │
│                              │
│ 3. Check output:              │
│    Should not show            │
│    "API_KEY not configured"   │
└──────────────────────────────┘

✓ FIXED: Backend should work
✗ MASIH ERROR: Check API key format
```

---

## B2: Error: "HTTP 401 Unauthorized" dari API

```
┌──────────────────────────────────┐
│ Problem: API key rejected         │
│                                  │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. API key salah/invalid         │
│ 2. API key expired               │
│ 3. Account suspended             │
│ 4. API key revoked               │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Verify API key        │
├──────────────────────────────┤
│ 1. Buka: https://brave.com/   │
│    search/api/                │
│ 2. Login ke account           │
│ 3. Cek API key di dashboard   │
│ 4. Copy fresh key             │
│ 5. Paste ke .env              │
│ 6. Save .env                  │
│ 7. Restart backend            │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Check quota           │
├──────────────────────────────┤
│ Di dashboard Brave:           │
│ Queries: 1500 / 2000          │
│ Status: Active                │
│                              │
│ ✓ OK: Ada quota tinggal       │
│ ✗ PROBLEM:                    │
│   - Quota habis (upgrade)     │
│   - Status inactive (renew)   │
│   - Account suspended (fix)   │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Switch to Tavily      │
├──────────────────────────────┤
│ (Alternative provider)        │
│                              │
│ 1. Daftar: https://tavily.com │
│ 2. Copy API key               │
│ 3. Edit .env:                 │
│    TAVILY_API_KEY=tvly_...    │
│ 4. Test:                      │
│    curl "http://localhost:    │
│    8080/api/search?provider=  │
│    tavily&query=test"         │
└──────────────────────────────┘

✓ FIXED: API key valid again
✗ MASIH ERROR: Contact API support
```

---

# SECTION C: Device Connection Issues

## C1: Device tidak terlihat di console

```
┌──────────────────────────────────┐
│ Problem: Device tidak muncul      │
│ di xiaozhi.me console            │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. Device off atau belum boot    │
│ 2. Device tidak terhubung WiFi   │
│ 3. Device IP salah               │
│ 4. Akun belum verified           │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Physical checks       │
├──────────────────────────────┤
│ 1. Power: Apakah device on?   │
│    → Check LED indicator      │
│                              │
│ 2. WiFi: Check LED/UI         │
│    → Device terhubung ke      │
│      WiFi?                    │
│                              │
│ 3. Wait: Device butuh waktu   │
│    → Tunggu 30-60 detik       │
│    → Baru muncul di console   │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Check account        │
├──────────────────────────────┤
│ 1. Buka: xiaozhi.me          │
│ 2. Login successful?          │
│    → Email verified?          │
│    → Account active?          │
│                              │
│ 3. If not:                    │
│    → Verify email             │
│    → Contact support          │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Reset device          │
├──────────────────────────────┤
│ 1. Power off device           │
│ 2. Wait 10 seconds            │
│ 3. Power on device            │
│ 4. Wait 30-60 seconds         │
│ 5. Check console again        │
│ 6. Should appear now          │
└──────────────────────────────┘

✓ FIXED: Device visible
✗ MASIH ERROR: Go to C2
```

---

## C2: "Backend URL invalid" error

```
┌──────────────────────────────────┐
│ Problem: Device reject URL        │
│                                  │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. URL format salah             │
│ 2. IP address salah             │
│ 3. Port salah                   │
│ 4. Device dan PC beda network   │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Verify URL format      │
├──────────────────────────────┤
│ CORRECT FORMAT:               │
│ ws://192.168.1.100:8080/      │
│ ws/device                     │
│                              │
│ ✗ WRONG:                      │
│ http://192.168.1.100:8080/... │
│ (use ws:// not http://)       │
│                              │
│ ✗ WRONG:                      │
│ ws://192.168.1.100:9000/...   │
│ (port salah, should be 8080)  │
│                              │
│ ✗ WRONG:                      │
│ ws://192.168.1.100/ws/device  │
│ (no port, missing :8080)      │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Get correct IP        │
├──────────────────────────────┤
│ Windows:                      │
│ ipconfig                      │
│ → Find "IPv4 Address"         │
│                              │
│ Mac:                          │
│ ifconfig | grep inet          │
│ → Find inet 192.168.x.x       │
│                              │
│ Linux:                        │
│ hostname -I                   │
│ → Get first IP                │
│                              │
│ Copy dan catat IP address     │
│ Contoh: 192.168.1.100         │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Verify connectivity   │
├──────────────────────────────┤
│ From device, ping PC:         │
│ ping 192.168.1.100            │
│                              │
│ Expected: Reply from ...      │
│                              │
│ ✗ Timeout: Network issue      │
│   → Device & PC beda WiFi?    │
│   → Need same WiFi network    │
│   → Check WiFi password       │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 4: Test backend from PC  │
├──────────────────────────────┤
│ Terminal PC:                  │
│ curl http://192.168.1.100:    │
│ 8080/api/health               │
│                              │
│ Expected: JSON response       │
│                              │
│ ✓ Works: URL correct          │
│ ✗ Error: Check firewall       │
└──────────────────────────────┘

✓ FIXED: URL valid
✗ MASIH ERROR: Go to C3
```

---

## C3: Device connect tapi timeout

```
┌──────────────────────────────────┐
│ Problem: Device connect tapi      │
│ sering timeout/disconnect         │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. Network unstable             │
│ 2. Backend crashes              │
│ 3. Firewall aggressive          │
│ 4. WiFi signal weak             │
│ 5. IP address changes           │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Check network quality  │
├──────────────────────────────┤
│ 1. Device signal strength:    │
│    → Move closer to router    │
│                              │
│ 2. Internet speed:            │
│    → Open speedtest.net       │
│    → Check download/upload    │
│    → Min 5 Mbps OK            │
│                              │
│ 3. Other devices:             │
│    → Disconnect WiFi hogs     │
│    → Reduce congestion        │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Monitor backend logs  │
├──────────────────────────────┤
│ Terminal backend:             │
│ python xiaozhi_backend_main.py│
│                              │
│ Watch for:                    │
│ ✓ "Device connected"          │
│ ✓ "Request received"          │
│ ✗ "Timeout"                   │
│ ✗ "Connection lost"           │
│ ✗ Errors                      │
│                              │
│ If errors: Note them down     │
│ for debugging                 │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Use static IP         │
├──────────────────────────────┤
│ Instead of relying on DHCP:   │
│ 1. Assign static IP to PC     │
│ 2. Configure device with      │
│    that fixed IP              │
│ 3. Prevents IP change         │
│ 4. More stable connection     │
│                              │
│ How to set static IP:         │
│ Windows: Settings → Network   │
│         → IP settings         │
│ Mac: System Prefs → Network   │
│ Linux: Edit /etc/network/     │
│        interfaces             │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 4: Increase timeout      │
├──────────────────────────────┤
│ Edit .env:                    │
│ BACKEND_PORT=8080             │
│ LOG_LEVEL=info                │
│ (add:)                        │
│ CONNECTION_TIMEOUT=30         │
│ HEARTBEAT_INTERVAL=10         │
│                              │
│ Restart backend              │
└──────────────────────────────┘

✓ MORE STABLE: Timeout reduced
✗ MASIH ISSUE: Go to F (Advanced)
```

---

# SECTION D: Search Issues

## D1: Search returns empty results

```
┌──────────────────────────────────┐
│ Problem: Search query submitted   │
│ tapi tidak return hasil           │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. API quota exceeded            │
│ 2. Query terlalu spesifik        │
│ 3. API key invalid               │
│ 4. Internet down                 │
│ 5. API rate limited              │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Test dengan simple    │
│ query                         │
├──────────────────────────────┤
│ Terminal (new):               │
│ curl "http://localhost:       │
│ 8080/api/search?query=        │
│ python&provider=brave"        │
│                              │
│ Expected:                     │
│ {"success":true,              │
│  "results":[...]}             │
│                              │
│ ✓ Works: Complex query issue  │
│ ✗ Empty: API problem          │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Check API quota       │
├──────────────────────────────┤
│ Brave:                        │
│ https://brave.com/search/api/ │
│ → Dashboard → Check usage     │
│ → Queries: X / 2000           │
│                              │
│ Tavily:                       │
│ https://tavily.com            │
│ → Dashboard → Check usage     │
│                              │
│ Action if exceeded:           │
│ → Upgrade plan                │
│ → Wait for reset (daily)      │
│ → Switch to another provider  │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Try different query   │
├──────────────────────────────┤
│ Instead of:                   │
│ "小智怎样学习Python同步编程" │
│ (too specific)                │
│                              │
│ Try:                          │
│ "Python"                      │
│ "AI"                          │
│ "News"                        │
│ (simple keywords)             │
│                              │
│ If simple works:              │
│ → Long queries work after     │
│ → API probably OK             │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 4: Check internet        │
├──────────────────────────────┤
│ Test:                         │
│ ping 8.8.8.8                  │
│ (Google DNS)                  │
│                              │
│ Expected: Reply from ...      │
│                              │
│ ✗ Timeout:                    │
│ → Internet down               │
│ → Need to fix connection      │
│ → Check WiFi/Ethernet         │
└──────────────────────────────┘

✓ WORKING: Search OK
✗ MASIH ISSUE: Go to D2
```

---

# SECTION E: Voice/Audio Issues

## E1: Device tidak menangkap suara

```
┌──────────────────────────────────┐
│ Problem: Microphone tidak        │
│ capture suara                    │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. Microphone off/muted          │
│ 2. Microphone not connected      │
│ 3. Microphone broken             │
│ 4. Wrong microphone selected     │
│ 5. Volume input = 0              │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Physical check         │
├──────────────────────────────┤
│ 1. Is mic plugged in?         │
│    ✓ Check cable connection   │
│    ✓ Check no loose wires     │
│                              │
│ 2. Is mic muted?              │
│    ✓ Check device volume      │
│    ✓ Check OS volume control  │
│    ✓ Check mic mute button    │
│                              │
│ 3. Test mic elsewhere:        │
│    ✓ Try on different device  │
│    ✓ Works? → Device problem  │
│    ✓ Not work? → Mic broken   │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Check OS audio        │
│ settings                      │
├──────────────────────────────┤
│ Windows:                      │
│ Settings → Sound              │
│ → Input devices               │
│ → Select correct microphone   │
│ → Volume not 0                │
│                              │
│ Mac:                          │
│ System Prefs → Sound          │
│ → Input tab                   │
│ → Select correct mic          │
│                              │
│ Linux:                        │
│ alsamixer / pavucontrol       │
│ → Check mic volume            │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Test microphone       │
├──────────────────────────────┤
│ Windows:                      │
│ Settings → Sound              │
│ → Microphone properties       │
│ → Talk dan check level bar    │
│                              │
│ Mac:                          │
│ System Prefs → Sound          │
│ → Input → Talk & watch       │
│                              │
│ Expected: Level bar bergerak  │
│ saat Anda bicara              │
└──────────────────────────────┘

✓ FIXED: Mic working
✗ MASIH ISSUE: Try different mic
```

---

## E2: Audio response tidak terdengar

```
┌──────────────────────────────────┐
│ Problem: Speaker tidak            │
│ mengeluarkan suara                │
├──────────────────────────────────┤
│ Penyebab:                        │
│ 1. Speaker off/muted              │
│ 2. Speaker not connected          │
│ 3. Speaker broken                 │
│ 4. Wrong output device selected   │
│ 5. Volume output = 0              │
│ 6. TTS service down               │
└──────────────────────────────────┘

FIX:

┌──────────────────────────────┐
│ STEP 1: Physical check         │
├──────────────────────────────┤
│ 1. Is speaker plugged in?     │
│    ✓ Check cable connection   │
│    ✓ Check power indicator    │
│                              │
│ 2. Is speaker muted?          │
│    ✓ Check device volume      │
│    ✓ Check speaker power      │
│    ✓ Check mute button        │
│                              │
│ 3. Test speaker:              │
│    ✓ Play music/video         │
│    ✓ Works? → Device problem  │
│    ✗ Not work? → Speaker bad  │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 2: Check OS audio        │
│ output                        │
├──────────────────────────────┤
│ Windows:                      │
│ Settings → Sound              │
│ → Output devices              │
│ → Select correct speaker      │
│ → Volume not 0                │
│ → Test sound plays            │
│                              │
│ Mac:                          │
│ System Prefs → Sound          │
│ → Output tab                  │
│ → Select correct speaker      │
│ → Volume > 0                  │
└──────────────────────────────┘

┌──────────────────────────────┐
│ STEP 3: Check TTS service     │
├──────────────────────────────┤
│ Backend logs:                 │
│ python xiaozhi_backend_main.py│
│                              │
│ Look for TTS errors:          │
│ "TTS Error"                   │
│ "Audio service down"          │
│ "Network timeout"             │
│                              │
│ If errors:                    │
│ → Restart backend             │
│ → Check internet connection   │
└──────────────────────────────┘

✓ FIXED: Speaker working
✗ MASIH ISSUE: Try different speaker
```

---

# SECTION F: Advanced Debugging

Jika Anda sudah coba semua di atas tapi masih bermasalah:

## F1: Collect Debug Information

```
Kumpulkan data ini sebelum asking help:

1. Terminal output:
   - Copy semua output dari backend
   - Save ke file: backend_output.txt

2. Error messages:
   - Exact error message
   - Kapan muncul (Step berapa)
   - Screenshot jika bisa

3. System info:
   - OS: Windows/Mac/Linux
   - OS version
   - Python version (python --version)
   - Device model
   - Device firmware version

4. Configuration:
   - .env file content (hide API keys)
   - Backend URL
   - IP address

5. Network info:
   - Device IP address
   - PC IP address
   - WiFi network name (SSID)
   - Internet speed test result
```

## F2: Where to Ask for Help

```
1. GitHub Issues:
   https://github.com/78/xiaozhi-esp32/issues
   - Search existing issues first
   - Provide detailed information
   - Include debug logs

2. Official Forum:
   https://xiaozhi.dev/community
   - Check FAQ first
   - Post in relevant category
   - Include error message

3. Community Discord:
   - XiaoZhi community server
   - Active maintainers
   - Real-time help

4. This Guide:
   - Re-read TROUBLESHOOTING section
   - Try different approach
   - Verify each step carefully
```

---

# 🎯 SUMMARY

Gunakan flowchart di awal untuk identifikasi problem Anda.

Jika masih tidak ketemu:
1. ✓ Collect debug information
2. ✓ Search di GitHub/Forum
3. ✓ Ask community dengan detail
4. ✓ Be patient, helpful people akan assist!

---

**Remember:**
- ✓ Read error messages carefully
- ✓ Try solutions step-by-step
- ✓ Restart/retry after changes
- ✓ Document what you tried
- ✓ Don't give up! 💪

---

**Version: 1.0**
**Created: June 2026**
**For: All Skill Levels**
