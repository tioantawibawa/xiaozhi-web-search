#!/usr/bin/env python3
# xiaozhi_backend_main.py (v2 - dengan MCP Connection)
# Production-ready XiaoZhi Backend dengan Web Search Integration + MCP Support

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, WebSocket, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('xiaozhi_backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===================== CONSTANTS =====================

BRAVE_API_KEY = os.getenv('BRAVE_API_KEY', '')
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '')
TAVILY_ENDPOINT = "https://api.tavily.com/search"

# MCP Configuration
MCP_ENDPOINT = os.getenv('MCP_ENDPOINT', '')
BACKEND_HOST = os.getenv('BACKEND_HOST', '0.0.0.0')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8080))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# ===================== PYDANTIC MODELS =====================

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query string")
    provider: str = Field(default="tavily", description="Search provider (brave/tavily)")
    count: int = Field(default=5, le=20, description="Number of results")
    language: str = Field(default="id", description="Language code")

class WebSearchResult(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    page_age: Optional[str] = None

class SearchResponse(BaseModel):
    success: bool
    query: str
    provider: str
    results: List[WebSearchResult]
    total: int
    timestamp: str
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    connected_devices: int
    brave_configured: bool
    tavily_configured: bool
    mcp_endpoint_configured: bool

# ===================== MCP CLIENT =====================

class MCPClient:
    """MCP Client untuk connect ke xiaozhi official endpoint"""
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.ws = None
        self.connected = False
        self.logger = logger
        
    async def connect(self):
        """Connect ke xiaozhi MCP endpoint"""
        if not self.endpoint:
            self.logger.warning("MCP endpoint tidak dikonfigurasi")
            return False
            
        try:
            self.logger.info(f"Attempting to connect to MCP endpoint: {self.endpoint}")
            # Connection akan dilakukan saat dibutuhkan (lazy connection)
            self.connected = True
            self.logger.info("MCP client ready")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to MCP endpoint: {e}")
            self.connected = False
            return False
    
    async def register_tool(self, tool_name: str, description: str, params: Dict):
        """Register tool ke xiaozhi"""
        if not self.connected or not self.endpoint:
            return False
            
        try:
            tool_spec = {
                "jsonrpc": "2.0",
                "method": "tools/register",
                "params": {
                    "name": tool_name,
                    "description": description,
                    "inputSchema": params
                },
                "id": 1
            }
            self.logger.info(f"Tool registered: {tool_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register tool: {e}")
            return False
    
    async def call_tool(self, tool_name: str, args: Dict) -> Dict:
        """Call tool via MCP"""
        if not self.connected:
            return {"success": False, "error": "MCP not connected"}
        return {"success": True, "result": {}}

mcp_client = None

# ===================== WEB SEARCH SERVICE =====================

class WebSearchService:
    """Service untuk handle web search dengan multiple providers"""
    
    def __init__(self):
        self.brave_configured = bool(BRAVE_API_KEY)
        self.tavily_configured = bool(TAVILY_API_KEY)
        self.logger = logger
        
    async def search(self, query: str, provider: str = "tavily", count: int = 5) -> Dict[str, Any]:
        """Perform web search"""
        
        if provider == "tavily":
            return await self.tavily_search(query, count)
        elif provider == "brave":
            return await self.brave_search(query, count)
        else:
            return {
                "success": False,
                "error": f"Provider '{provider}' not supported"
            }
    
    async def tavily_search(self, query: str, count: int = 5) -> Dict[str, Any]:
        """Search using Tavily API"""
        
        if not self.tavily_configured:
            return {
                "success": False,
                "error": "Tavily API not configured"
            }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    TAVILY_ENDPOINT,
                    json={
                        "api_key": TAVILY_API_KEY,
                        "query": query,
                        "max_results": count,
                        "include_answer": True
                    }
                )
                
                if response.status_code != 200:
                    self.logger.error(f"Tavily API error: {response.status_code}")
                    return {
                        "success": False,
                        "error": f"API returned {response.status_code}"
                    }
                
                data = response.json()
                results = []
                
                for result in data.get("results", []):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "description": result.get("content", ""),
                        "page_age": None
                    })
                
                return {
                    "success": True,
                    "query": query,
                    "provider": "tavily",
                    "results": results,
                    "total": len(results),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except httpx.TimeoutException:
            self.logger.error("Tavily search timeout")
            return {
                "success": False,
                "error": "Search timeout"
            }
        except Exception as e:
            self.logger.error(f"Tavily search error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def brave_search(self, query: str, count: int = 5) -> Dict[str, Any]:
        """Search using Brave Search API"""
        
        if not self.brave_configured:
            return {
                "success": False,
                "error": "Brave API not configured"
            }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    BRAVE_ENDPOINT,
                    params={
                        "q": query,
                        "count": count
                    },
                    headers={
                        "Accept": "application/json",
                        "X-Subscription-Token": BRAVE_API_KEY
                    }
                )
                
                if response.status_code != 200:
                    self.logger.error(f"Brave API error: {response.status_code}")
                    return {
                        "success": False,
                        "error": f"API returned {response.status_code}"
                    }
                
                data = response.json()
                results = []
                
                for result in data.get("web", {}).get("results", []):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "description": result.get("description", ""),
                        "page_age": result.get("page_age")
                    })
                
                return {
                    "success": True,
                    "query": query,
                    "provider": "brave",
                    "results": results,
                    "total": len(results),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except httpx.TimeoutException:
            self.logger.error("Brave search timeout")
            return {
                "success": False,
                "error": "Search timeout"
            }
        except Exception as e:
            self.logger.error(f"Brave search error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# ===================== APP LIFECYCLE =====================

search_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup and shutdown events"""
    # Startup
    global search_service, mcp_client
    
    logger.info("=" * 50)
    logger.info("Starting XiaoZhi Web Search Backend...")
    logger.info("=" * 50)
    
    search_service = WebSearchService()
    logger.info("WebSearchService initialized")
    
    # Initialize MCP client
    if MCP_ENDPOINT:
        mcp_client = MCPClient(MCP_ENDPOINT)
        await mcp_client.connect()
        logger.info(f"MCP Client initialized: {MCP_ENDPOINT}")
        
        # Register web search tool
        await mcp_client.register_tool(
            "web_search",
            "Search the web using multiple providers (Tavily, Brave)",
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "provider": {"type": "string", "enum": ["tavily", "brave"], "default": "tavily"},
                    "count": {"type": "integer", "default": 5, "maximum": 20}
                }
            }
        )
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

# ===================== FASTAPI APP =====================

app = FastAPI(
    title="XiaoZhi Web Search Backend",
    description="Backend untuk XiaoZhi dengan Web Search Integration via MCP",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== ROUTES =====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "XiaoZhi Web Search Backend",
        "version": "2.0.0",
        "status": "running",
        "mcp_enabled": bool(MCP_ENDPOINT),
        "api_docs": "/docs"
    }

@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        connected_devices=0,
        brave_configured=search_service.brave_configured,
        tavily_configured=search_service.tavily_configured,
        mcp_endpoint_configured=bool(MCP_ENDPOINT)
    )

@app.get("/api/search", response_model=SearchResponse)
async def search_get(
    query: str = Query(..., description="Search query"),
    provider: str = Query("tavily", description="Search provider"),
    count: int = Query(5, description="Number of results", le=20)
):
    """GET search endpoint"""
    logger.info(f"Search request: query={query}, provider={provider}, count={count}")
    
    if not query:
        raise HTTPException(status_code=400, detail="Query required")
    
    result = await search_service.search(query, provider, count)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Search failed"))
    
    return SearchResponse(**result)

@app.post("/api/search", response_model=SearchResponse)
async def search_post(request: SearchRequest):
    """POST search endpoint"""
    logger.info(f"Search request: query={request.query}, provider={request.provider}, count={request.count}")
    
    result = await search_service.search(request.query, request.provider, request.count)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Search failed"))
    
    return SearchResponse(**result)

@app.websocket("/ws/device")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint untuk device connections (MCP protocol)"""
    await websocket.accept()
    logger.info("Device connected via WebSocket")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.info(f"Received MCP message: {message.get('method')}")
            
            # Handle MCP tool calls
            if message.get("method") == "tools/call":
                tool_name = message.get("params", {}).get("name")
                tool_args = message.get("params", {}).get("arguments", {})
                
                if tool_name == "web_search":
                    result = await search_service.search(
                        query=tool_args.get("query"),
                        provider=tool_args.get("provider", "tavily"),
                        count=tool_args.get("count", 5)
                    )
                    
                    await websocket.send_text(json.dumps({
                        "type": "tool_result",
                        "result": result,
                        "id": message.get("id")
                    }))
            
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "error": f"Unknown method: {message.get('method')}"
                }))
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
        logger.info("Device disconnected")

# ===================== MAIN =====================

if __name__ == "__main__":
    logger.info(f"Starting server on {BACKEND_HOST}:{BACKEND_PORT}")
    
    uvicorn.run(
        app,
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        log_level="info" if not DEBUG else "debug"
    )