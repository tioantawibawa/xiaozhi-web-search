# XiaoZhi AI Web Search Integration - Quick Start Guide

## 🚀 Mulai Dalam 5 Menit

### Prasyarat
- Python 3.8+ atau Docker installed
- API Key dari Brave Search atau Tavily (gratis)
- XiaoZhi device (ESP32-S3) yang sudah di-setup

---

## Option A: Lokal dengan Python

### 1. Clone/Download Files
```bash
# Download semua file ke folder
mkdir xiaozhi-web-search
cd xiaozhi-web-search

# Copy:
# - xiaozhi_backend_main.py
# - requirements.txt
# - .env.example
```

### 2. Setup Environment
```bash
# Copy dan edit .env
cp .env.example .env

# Edit .env, masukkan API keys Anda:
# BRAVE_API_KEY=sk_xxxxx
# TAVILY_API_KEY=tvly_xxxxx
```

### 3. Install Dependencies
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 4. Run Backend
```bash
python xiaozhi_backend_main.py
```

Output should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8080
```

### 5. Test API
```bash
# Terminal baru, test search endpoint
curl "http://localhost:8080/api/search?query=python+programming&provider=brave&count=5"

# Atau gunakan browser
http://localhost:8080/docs
```

---

## Option B: Docker (Recommended untuk Production)

### 1. Setup
```bash
mkdir xiaozhi-web-search
cd xiaozhi-web-search

# Copy files:
# - Dockerfile
# - docker-compose.yml
# - xiaozhi_backend_main.py
# - requirements.txt
# - .env.example
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env dengan API keys Anda
```

### 3. Run
```bash
docker-compose up -d
```

### 4. Check Status
```bash
docker-compose logs -f xiaozhi-backend
docker ps  # Lihat container running
```

### 5. Test
```bash
curl http://localhost:8080/api/health
curl "http://localhost:8080/api/search?query=hello&provider=brave"
```

---

## 📝 Konfigurasi XiaoZhi Device

Setelah backend running, configure device untuk connect:

### Via Web Console (xiaozhi.me)
1. Login ke console
2. Pilih device
3. Settings → Backend Configuration
4. Set:
   - Backend URL: `ws://your_ip:8080/ws/device` (atau HTTPS jika cloud)
   - MCP Enabled: true
   - Feature: web_search enabled

### Via Config File
Edit device config JSON:
```json
{
  "backend": {
    "url": "ws://192.168.1.100:8080/ws/device",
    "mcp_enabled": true,
    "reconnect_interval": 5000
  },
  "features": {
    "web_search": true,
    "offline_mode": true
  },
  "search_provider": "brave"
}
```

---

## 🗣️ Voice Commands Examples

Setelah setup, coba commands ini:

### Perintah Dasar
```
"小智，搜索 Python 编程"
"Xiaozhi, cari berita teknologi hari ini"
"Xiaozhi, search cara membuat website"
"小智，查一下 AI 最新发展"
```

### Perintah dengan Parameter
```
"搜索 AI 最新新闻，给我 10 个结果"
"Find latest quantum computing research"
"搜索 React.js 教程，用英文"
```

---

## 🔍 Testing & Debugging

### API Documentation
Browser ke: `http://localhost:8080/docs`

### Test Manual dengan cURL
```bash
# Simple search
curl "http://localhost:8080/api/search?query=AI&provider=brave"

# With more parameters
curl "http://localhost:8080/api/search?query=machine learning&provider=tavily&count=10"

# POST request
curl -X POST http://localhost:8080/api/search/smart \
  -H "Content-Type: application/json" \
  -d '{"query":"python tips","provider":"brave","count":5}'

# Health check
curl http://localhost:8080/api/health
```

### Check Logs
```bash
# Local Python
cat xiaozhi_backend.log

# Docker
docker-compose logs xiaozhi-backend
docker-compose logs -f xiaozhi-backend  # Follow logs
```

### Debug Mode
```bash
# Enable debug logging di .env
LOG_LEVEL=debug

# Or run dengan reload
python xiaozhi_backend_main.py  # dengan DEBUG=True di .env
```

---

## 🐛 Troubleshooting

### Issue 1: "API Key not configured"
```
Solusi: 
1. Check .env file ada BRAVE_API_KEY atau TAVILY_API_KEY
2. Restart backend setelah edit .env
3. Test: curl http://localhost:8080/api/health
```

### Issue 2: "Connection refused"
```
Solusi:
1. Check backend running: netstat -an | grep 8080 (Linux/Mac)
2. Check firewall tidak block port 8080
3. Check IP address correct di device config
```

### Issue 3: "JSON parse error"
```
Solusi:
1. Check API response format valid
2. Update pip packages: pip install -r requirements.txt --upgrade
3. Check API endpoint correct
```

### Issue 4: Device tidak connect
```
Solusi:
1. Check WebSocket URL correct
2. Test: curl -i http://localhost:8080/api/health
3. Check device logs: xiaozhi device console
4. Restart device dan backend
```

---

## 📊 Performance Tips

### 1. Caching
Backend sudah implementasi simple cache. Untuk production:
```python
# Tambah Redis:
pip install redis
# Edit backend untuk gunakan Redis cache
```

### 2. Rate Limiting
Brave: 2000 queries/month (gratis)
Tavily: 1000 queries/month (gratis)

Upgrade bila perlu lebih.

### 3. Scaling
```bash
# Jalankan multiple backend instances
# Load balance dengan nginx
# Containerize untuk Kubernetes
```

---

## 📚 Resources

### API Documentation
- **Brave Search**: https://api.search.brave.com/res/v1/web/search
  - Docs: https://brave.com/search/api/
  - Dashboard: https://api.search.brave.com/
  
- **Tavily AI**: https://tavily.com
  - Docs: https://docs.tavily.com/

### XiaoZhi Resources
- GitHub: https://github.com/78/xiaozhi-esp32
- Docs: https://xiaozhi.dev/docs
- Console: https://xiaozhi.me

### Related Tech
- FastAPI: https://fastapi.tiangolo.com/
- MCP Protocol: https://modelcontextprotocol.io/
- ESP-IDF: https://docs.espressif.com/

---

## ❓ FAQ

**Q: Bisa pakai provider lain?**
A: Ya, edit backend code, tambah provider baru (Google, Bing, dll)

**Q: Berapa cost untuk production?**
A: 
- Brave free tier: $0 untuk 2000/month
- Tavily free tier: $0 untuk 1000/month
- Upgrade plans tersedia

**Q: Bisa offline?**
A: Backend harus online, tapi XiaoZhi device support offline mode untuk non-search features

**Q: Bahasa apa yang support?**
A: Search API mendukung semua bahasa. Device support Mandarin, English, Japanese, Korean

**Q: Multi-device support?**
A: Ya, backend dapat handle multiple devices via WebSocket

---

## 🤝 Support

Pertanyaan atau issue?
1. Check logs: `xiaozhi_backend.log`
2. Test API directly: `http://localhost:8080/docs`
3. GitHub Issues: https://github.com/78/xiaozhi-esp32/issues
4. XiaoZhi Community: https://xiaozhi.dev

---

## ✅ Checklist Deployment

- [ ] API Keys obtained (Brave/Tavily)
- [ ] .env file configured
- [ ] Backend running successfully
- [ ] Health check passing
- [ ] Device connected to backend
- [ ] Test voice commands working
- [ ] Logs monitoring setup
- [ ] Rate limits understood
- [ ] Backup/logging configured
- [ ] Monitoring dashboard (optional)

---

**Happy Searching! 🚀**

Updated: June 2026
