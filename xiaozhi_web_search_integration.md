# XiaoZhi AI - Web Search Integration Guide
## Mengintegrasikan Kemampuan Pencarian Internet ke XiaoZhi AI

**Terakhir diupdate: June 2026**  
**Target Audience:** Developer IoT / AI Enthusiast  
**Bahasa:** Bahasa Indonesia + English Code Examples

---

## 📋 Daftar Isi

1. [Pendahuluan](#pendahuluan)
2. [Arsitektur Sistem](#arsitektur-sistem)
3. [Prerequisites](#prerequisites)
4. [Solusi 1: Cloud-Side MCP Web Search Tool](#solusi-1-cloud-side-mcp-web-search-tool)
5. [Solusi 2: Backend Integration dengan API eksternal](#solusi-2-backend-integration-dengan-api-eksternal)
6. [Solusi 3: Custom ESP32 HTTP Client](#solusi-3-custom-esp32-http-client)
7. [Implementasi Praktis](#implementasi-praktis)
8. [Testing & Troubleshooting](#testing--troubleshooting)

---

## Pendahuluan

XiaoZhi AI menggunakan **MCP (Model Context Protocol)** untuk menghubungkan LLM dengan tools eksternal. Untuk web search, ada 3 pendekatan:

| Pendekatan | Kompleksitas | Kecepatan | Skalabilitas | Rekomendasi |
|-----------|-------------|----------|-------------|------------|
| Cloud-Side MCP Tool | Menengah | Cepat | Tinggi | ⭐ Terbaik |
| Backend HTTP Integration | Tinggi | Sangat Cepat | Tinggi | Untuk production |
| ESP32 Direct HTTP | Rendah | Lambat | Rendah | POC/Testing |

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                    User Voice Input                      │
│                  "Cari informasi tentang..."             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
            ┌──────────────────────────┐
            │   XiaoZhi ESP32 Device   │
            │  (ASR + Voice Processing)│
            └──────────────┬───────────┘
                           │ (MCP Protocol via WebSocket/MQTT)
                           ▼
            ┌──────────────────────────────────┐
            │   XiaoZhi Backend Server         │
            │  (LLM + MCP Tool Orchestration)  │
            └──────────────┬───────────────────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
        ┌──────────────────┐  ┌─────────────────────┐
        │  Device Control  │  │  Web Search Tools   │
        │  (Light, etc)    │  │  (Brave/Tavily API) │
        └──────────────────┘  └─────────────────────┘
                  │                   │
                  └────────┬──────────┘
                           ▼
            ┌──────────────────────────┐
            │   External APIs          │
            │ - Brave Search           │
            │ - Tavily Search          │
            │ - Google Custom Search   │
            └──────────────────────────┘
```

---

## Prerequisites

### Hardware
- ESP32-S3 Development Board (XiaoZhi compatible)
- Koneksi WiFi stabil
- Microphone + Speaker

### Software
- ESP-IDF v5.3+ (untuk custom development)
- Python 3.8+ (untuk backend MCP server)
- XiaoZhi firmware terbaru (v2.x)

### API Credentials
Pilih salah satu web search API:

**Option A: Brave Search (Recommended untuk gratis)**
```
- Endpoint: https://api.search.brave.com/res/v1/web/search
- Free tier: 2000 queries/bulan
- Signup: https://brave.com/search/api/
```

**Option B: Tavily AI Search**
```
- Endpoint: https://api.tavily.com/search
- Free tier: 1000 queries/bulan
- Signup: https://tavily.com
```

**Option C: Google Custom Search**
```
- Endpoint: https://www.googleapis.com/customsearch/v1
- Free tier: 100 queries/hari
- Setup: Google Cloud Console
```

---

## Solusi 1: Cloud-Side MCP Web Search Tool

### ⭐ **Pendekatan Terekomendasi**

**Kelebihan:**
- ✅ Tidak perlu modifikasi firmware ESP32
- ✅ Mudah di-update tanpa re-flash device
- ✅ Scalable untuk multiple devices
- ✅ LLM dapat orchestrate multiple tools

### 1.1 Setup Backend MCP Server

Buat file: `mcp_web_search.py`

```python
import json
import httpx
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, TextContent, ToolResult
)

# Inisialisasi MCP Server
server = Server("xiaozhi-web-search")

# Konfigurasi API
BRAVE_API_KEY = "YOUR_BRAVE_API_KEY"  # Ganti dengan API key Anda
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

class WebSearchTool:
    """Tool untuk melakukan pencarian web menggunakan Brave Search API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()
    
    async def search(self, query: str, count: int = 5) -> dict:
        """
        Melakukan pencarian web
        
        Args:
            query: String pencarian
            count: Jumlah hasil (default: 5)
        
        Returns:
            Dictionary berisi hasil pencarian
        """
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": query,
            "count": count,
            "safesearch": "moderate",
            "freshness": "1m"  # Hasil dari 1 bulan terakhir
        }
        
        try:
            response = await self.client.get(
                BRAVE_ENDPOINT,
                headers=headers,
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Format hasil untuk konsumsi LLM
            results = []
            if "web" in data:
                for result in data["web"][:count]:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "description": result.get("description", ""),
                        "page_age": result.get("page_age", "")
                    })
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "total": len(results)
            }
            
        except httpx.HTTPError as e:
            return {
                "success": False,
                "error": f"API Error: {str(e)}",
                "query": query
            }

# Inisialisasi tool
search_tool = WebSearchTool(BRAVE_API_KEY)

# Register MCP Tool
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="web_search",
            description="Cari informasi di internet menggunakan Brave Search API. Tool ini memberikan hasil pencarian terbaru dengan source link.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Kalimat pencarian (e.g., 'cara merawat tanaman hias')"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Jumlah hasil yang dikembalikan (1-10, default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="web_search_detailed",
            description="Pencarian web dengan snippet lengkap dan metadata. Untuk query yang membutuhkan analisis mendalam.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Kalimat pencarian detail"
                    },
                    "language": {
                        "type": "string",
                        "description": "Bahasa hasil (en, id, zh, etc.)",
                        "default": "id"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Implementasi tools"""
    
    if name == "web_search":
        query = arguments.get("query", "")
        count = arguments.get("count", 5)
        
        result = await search_tool.search(query, count)
        
        if result["success"]:
            # Format output untuk XiaoZhi LLM
            response = f"Hasil pencarian untuk '{query}':\n\n"
            for i, item in enumerate(result["results"], 1):
                response += f"{i}. {item['title']}\n"
                response += f"   URL: {item['url']}\n"
                response += f"   Deskripsi: {item['description']}\n\n"
            
            return [TextContent(type="text", text=response)]
        else:
            return [TextContent(
                type="text",
                text=f"Gagal melakukan pencarian: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "web_search_detailed":
        query = arguments.get("query", "")
        language = arguments.get("language", "id")
        
        result = await search_tool.search(query, count=10)
        
        if result["success"]:
            response = json.dumps(result, ensure_ascii=False, indent=2)
            return [TextContent(type="text", text=response)]
        else:
            return [TextContent(type="text", text=f"Error: {result.get('error')}")]
    
    else:
        return [TextContent(type="text", text=f"Tool '{name}' not found")]

async def main():
    async with stdio_server(server) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 1.2 Install Dependencies

```bash
pip install mcp httpx
```

### 1.3 Konfigurasi Backend untuk XiaoZhi

Buat file: `xiaozhi_backend_config.yaml`

```yaml
# XiaoZhi Backend Configuration
backend:
  host: "0.0.0.0"
  port: 8080
  debug: false

# MCP Tools Configuration
mcp_tools:
  - name: "web_search"
    type: "stdio"
    command: "python"
    args: ["mcp_web_search.py"]
    enabled: true
    description: "Brave Search Integration"

# API Integrations
integrations:
  brave_search:
    api_key: "${BRAVE_API_KEY}"
    max_results: 10
    timeout: 10
    
  tavily_search:
    api_key: "${TAVILY_API_KEY}"
    search_depth: "basic"  # atau "advanced"

# Device Configuration
devices:
  esp32:
    connection_type: "websocket"  # atau "mqtt"
    endpoint: "ws://localhost:8080/device"
    mcp_enabled: true
    
# LLM Configuration  
llm:
  provider: "deepseek"  # atau "qwen"
  model: "deepseek-chat"
  temperature: 0.7
  max_tokens: 2048
  system_prompt: |
    Anda adalah assistant AI yang helpful dan cerdas.
    Anda dapat menggunakan tool web_search untuk mencari informasi terbaru.
    Selalu memberikan sumber URL ketika menggunakan informasi dari internet.
```

### 1.4 Deploy Backend Server

```bash
# Gunakan Docker untuk production deployment
# Buat Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "xiaozhi_backend_main.py"]
```

**Build & Run:**
```bash
docker build -t xiaozhi-backend .
docker run -p 8080:8080 -e BRAVE_API_KEY=your_key xiaozhi-backend
```

---

## Solusi 2: Backend Integration dengan API Eksternal

Ini adalah setup untuk backend yang lebih production-ready dengan error handling.

### 2.1 Backend dengan FastAPI + MCP

```python
# xiaozhi_backend_fastapi.py

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import httpx
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="XiaoZhi Web Search Backend")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BRAVE_API_KEY = "your_api_key_here"
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
TAVILY_API_KEY = "your_tavily_key"
TAVILY_ENDPOINT = "https://api.tavily.com/search"

# Connected devices
connected_devices = set()

class WebSearchService:
    """Service untuk web search dengan multiple providers"""
    
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    async def brave_search(self, query: str, count: int = 5) -> dict:
        """Search menggunakan Brave Search API"""
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        
        params = {
            "q": query,
            "count": min(count, 20),
            "safesearch": "moderate"
        }
        
        try:
            response = await self.client.get(
                BRAVE_ENDPOINT,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "provider": "brave",
                "success": True,
                "query": query,
                "results": self._format_results(data.get("web", []), count)
            }
        except Exception as e:
            logger.error(f"Brave search error: {e}")
            return {
                "provider": "brave",
                "success": False,
                "error": str(e)
            }
    
    async def tavily_search(self, query: str, depth: str = "basic") -> dict:
        """Search menggunakan Tavily API"""
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": depth,
            "include_answer": True,
            "max_results": 10
        }
        
        try:
            response = await self.client.post(
                TAVILY_ENDPOINT,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "provider": "tavily",
                "success": True,
                "query": query,
                "answer": data.get("answer", ""),
                "results": [
                    {
                        "title": r.get("title"),
                        "url": r.get("url"),
                        "description": r.get("content"),
                        "score": r.get("score")
                    }
                    for r in data.get("results", [])
                ]
            }
        except Exception as e:
            logger.error(f"Tavily search error: {e}")
            return {
                "provider": "tavily",
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def _format_results(results: list, count: int) -> list:
        """Format hasil pencarian"""
        formatted = []
        for result in results[:count]:
            formatted.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("description", ""),
                "page_age": result.get("page_age", "")
            })
        return formatted

web_search_service = WebSearchService()

# REST Endpoints
@app.post("/api/search")
async def search(query: str, provider: str = "brave", count: int = 5):
    """REST endpoint untuk web search"""
    
    if provider == "brave":
        result = await web_search_service.brave_search(query, count)
    elif provider == "tavily":
        result = await web_search_service.tavily_search(query)
    else:
        raise HTTPException(status_code=400, detail="Unknown provider")
    
    return result

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "connected_devices": len(connected_devices),
        "timestamp": asyncio.get_event_loop().time()
    }

# WebSocket untuk device communication (MCP)
@app.websocket("/ws/device")
async def websocket_device(websocket: WebSocket):
    """WebSocket endpoint untuk XiaoZhi device MCP communication"""
    await websocket.accept()
    device_id = None
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # MCP message handling
            if data.get("type") == "mcp":
                mcp_payload = data.get("payload", {})
                method = mcp_payload.get("method")
                
                # Handle web search tool call
                if method == "tools/call":
                    tool_name = mcp_payload.get("params", {}).get("name")
                    tool_args = mcp_payload.get("params", {}).get("arguments", {})
                    
                    if tool_name == "web_search":
                        query = tool_args.get("query", "")
                        count = tool_args.get("count", 5)
                        
                        result = await web_search_service.brave_search(query, count)
                        
                        response = {
                            "type": "mcp",
                            "payload": {
                                "jsonrpc": "2.0",
                                "id": mcp_payload.get("id"),
                                "result": {
                                    "content": json.dumps(result, ensure_ascii=False)
                                }
                            }
                        }
                        
                        await websocket.send_json(response)
                    
                    elif tool_name == "tavily_search":
                        query = tool_args.get("query", "")
                        depth = tool_args.get("depth", "basic")
                        
                        result = await web_search_service.tavily_search(query, depth)
                        
                        response = {
                            "type": "mcp",
                            "payload": {
                                "jsonrpc": "2.0",
                                "id": mcp_payload.get("id"),
                                "result": {
                                    "content": json.dumps(result, ensure_ascii=False)
                                }
                            }
                        }
                        
                        await websocket.send_json(response)
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if device_id:
            connected_devices.discard(device_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
```

**Requirements:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.0
pydantic==2.5.0
python-dotenv==1.0.0
```

**Run Backend:**
```bash
pip install -r requirements.txt
python xiaozhi_backend_fastapi.py
```

---

## Solusi 3: Custom ESP32 HTTP Client

Jika ingin langsung dari device tanpa backend.

```cpp
// components/web_search/web_search.c
// Implementasi HTTP client untuk ESP32

#include "esp_http_client.h"
#include "esp_log.h"
#include "cJSON.h"

static const char* TAG = "web_search";

typedef struct {
    char* api_key;
    char* endpoint;
} web_search_config_t;

esp_err_t web_search_init(web_search_config_t* config) {
    if (!config || !config->api_key || !config->endpoint) {
        ESP_LOGE(TAG, "Invalid config");
        return ESP_ERR_INVALID_ARG;
    }
    return ESP_OK;
}

esp_err_t web_search_query(
    web_search_config_t* config,
    const char* query,
    cJSON** results
) {
    if (!query || !results) {
        return ESP_ERR_INVALID_ARG;
    }
    
    // Build query URL
    char url[512];
    snprintf(url, sizeof(url), 
        "%s?q=%s&count=5",
        config->endpoint,
        query);
    
    // Create HTTP client
    esp_http_client_config_t http_config = {
        .url = url,
        .method = HTTP_METHOD_GET,
        .timeout_ms = 10000,
    };
    
    esp_http_client_handle_t client = esp_http_client_init(&http_config);
    
    // Add authorization header
    char auth_header[256];
    snprintf(auth_header, sizeof(auth_header),
        "X-Subscription-Token: %s",
        config->api_key);
    esp_http_client_set_header(client, "X-Subscription-Token", config->api_key);
    
    esp_err_t err = esp_http_client_perform(client);
    
    if (err == ESP_OK) {
        int status_code = esp_http_client_get_status_code(client);
        int content_length = esp_http_client_get_content_length(client);
        
        if (status_code == 200) {
            // Parse JSON response
            char* response_buffer = malloc(content_length + 1);
            int read_len = esp_http_client_read_response(client, response_buffer, content_length);
            response_buffer[read_len] = '\0';
            
            *results = cJSON_Parse(response_buffer);
            free(response_buffer);
            
            if (!*results) {
                ESP_LOGE(TAG, "Failed to parse JSON");
                err = ESP_FAIL;
            }
        } else {
            ESP_LOGE(TAG, "HTTP Status: %d", status_code);
            err = ESP_FAIL;
        }
    } else {
        ESP_LOGE(TAG, "HTTP request failed: %s", esp_err_to_name(err));
    }
    
    esp_http_client_cleanup(client);
    return err;
}
```

---

## Implementasi Praktis

### Step-by-Step untuk Production

#### 1. Setup Environment Variables

```bash
# .env
BRAVE_API_KEY=your_brave_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
BACKEND_URL=http://localhost:8080
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
```

#### 2. Configure XiaoZhi Device untuk connect ke backend

Via web console atau config file:
```json
{
  "backend": {
    "url": "ws://your_backend_ip:8080/ws/device",
    "mcp_enabled": true,
    "reconnect_interval": 5000
  },
  "features": {
    "web_search": true,
    "offline_mode": true
  }
}
```

#### 3. Test Integration

```bash
# Test REST endpoint
curl -X POST "http://localhost:8080/api/search?query=berita+hari+ini&provider=brave"

# Health check
curl http://localhost:8080/api/health
```

#### 4. Voice Command Examples

Setelah setup, Anda bisa menggunakan voice command:

```
"Xiaozhi, cari berita tentang AI terbaru"
"Xiaozhi, apa jadwal buka Rumah Sakit Cipto Mangunkusumo?"
"Xiaozhi, cari harga PS5 terbaru"
"Xiaozhi, siapa pemenang Piala Dunia terakhir?"
```

---

## Testing & Troubleshooting

### 1. Debug Log Level

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. Common Issues

| Issue | Solusi |
|-------|--------|
| API Key invalid | Verifikasi di dashboard provider (Brave/Tavily) |
| Connection timeout | Cek firewall, port forward untuk cloud deployment |
| JSON parsing error | Validate response format dari API |
| Rate limit exceeded | Implement caching atau upgrade API tier |

### 3. Monitoring Dashboard

```python
# Monitor.py
from prometheus_client import Counter, Histogram
import time

search_count = Counter('web_search_total', 'Total searches')
search_duration = Histogram('web_search_duration_seconds', 'Search duration')
search_errors = Counter('web_search_errors', 'Search errors')

@search_duration.time()
async def monitored_search(query: str):
    try:
        result = await web_search_service.brave_search(query)
        search_count.inc()
        return result
    except Exception as e:
        search_errors.inc()
        raise
```

---

## Kesimpulan & Next Steps

✅ **Selesai**: Anda sekarang punya 3 opsi untuk integrate web search ke XiaoZhi AI

🎯 **Rekomendasi untuk mulai:**
1. Daftar API key di Brave Search (gratis, mudah)
2. Deploy backend FastAPI (Solusi 2)
3. Connect ESP32 device ke backend
4. Test dengan voice commands

📚 **Resources Tambahan:**
- XiaoZhi GitHub: https://github.com/78/xiaozhi-esp32
- Brave Search API: https://brave.com/search/api/
- Tavily AI: https://tavily.com

---

**Pertanyaan atau issue?**  
Tanya di XiaoZhi GitHub discussions atau dokumentasi resmi.

Happy Coding! 🚀
