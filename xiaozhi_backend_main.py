#!/usr/bin/env python3
# xiaozhi_backend_main.py
# Production-ready XiaoZhi Backend dengan Web Search Integration

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
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

# ===================== PYDANTIC MODELS =====================

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query string")
    provider: str = Field(default="brave", description="Search provider (brave/tavily)")
    count: int = Field(default=5, le=20, description="Number of results")
    language: str = Field(default="id", description="Language code")

class WebSearchResult(BaseModel):
    title: str
    url: str
    description: str
    page_age: Optional[str] = None
    score: Optional[float] = None

class SearchResponse(BaseModel):
    success: bool
    query: str
    provider: str
    results: list[WebSearchResult] = []
    total: int = 0
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None

# ===================== WEB SEARCH SERVICE =====================

class WebSearchService:
    """
    Service untuk melakukan pencarian web dengan multiple providers
    """
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)
        self.cache: Dict[str, Any] = {}  # Simple cache
        logger.info("WebSearchService initialized")
    
    async def brave_search(self, query: str, count: int = 5) -> SearchResponse:
        """
        Search menggunakan Brave Search API
        
        Args:
            query: Search query
            count: Jumlah hasil (max 20)
        
        Returns:
            SearchResponse dengan hasil
        """
        try:
            if not BRAVE_API_KEY:
                return SearchResponse(
                    success=False,
                    query=query,
                    provider="brave",
                    error="BRAVE_API_KEY not configured"
                )
            
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": BRAVE_API_KEY
            }
            
            params = {
                "q": query,
                "count": min(count, 20),
                "safesearch": "moderate"
            }
            
            logger.info(f"Brave search: {query} (count={count})")
            response = await self.client.get(
                BRAVE_ENDPOINT,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if "web" in data:
                for item in data.get("web", [])[:count]:
                    results.append(WebSearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        description=item.get("description", ""),
                        page_age=item.get("page_age")
                    ))
            
            return SearchResponse(
                success=True,
                query=query,
                provider="brave",
                results=results,
                total=len(results)
            )
            
        except httpx.HTTPError as e:
            logger.error(f"Brave API error: {e}")
            return SearchResponse(
                success=False,
                query=query,
                provider="brave",
                error=f"HTTP Error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in brave_search: {e}")
            return SearchResponse(
                success=False,
                query=query,
                provider="brave",
                error=f"Error: {str(e)}"
            )
    
    async def tavily_search(self, query: str, depth: str = "basic") -> SearchResponse:
        """
        Search menggunakan Tavily AI API
        
        Args:
            query: Search query
            depth: Search depth (basic/advanced)
        
        Returns:
            SearchResponse dengan hasil
        """
        try:
            if not TAVILY_API_KEY:
                return SearchResponse(
                    success=False,
                    query=query,
                    provider="tavily",
                    error="TAVILY_API_KEY not configured"
                )
            
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": depth,
                "include_answer": True,
                "max_results": 10
            }
            
            logger.info(f"Tavily search: {query} (depth={depth})")
            response = await self.client.post(TAVILY_ENDPOINT, json=payload)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("results", []):
                results.append(WebSearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    description=item.get("content", ""),
                    score=item.get("score")
                ))
            
            return SearchResponse(
                success=True,
                query=query,
                provider="tavily",
                results=results,
                total=len(results)
            )
            
        except httpx.HTTPError as e:
            logger.error(f"Tavily API error: {e}")
            return SearchResponse(
                success=False,
                query=query,
                provider="tavily",
                error=f"HTTP Error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in tavily_search: {e}")
            return SearchResponse(
                success=False,
                query=query,
                provider="tavily",
                error=f"Error: {str(e)}"
            )

# ===================== FASTAPI APP =====================

# Global state
web_search_service = None
connected_devices = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global web_search_service
    web_search_service = WebSearchService()
    logger.info("Application startup complete")
    yield
    # Shutdown
    logger.info("Application shutdown")

app = FastAPI(
    title="XiaoZhi Web Search Backend",
    description="Backend server untuk XiaoZhi AI dengan web search capability",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== REST ENDPOINTS =====================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "service": "XiaoZhi Web Search Backend",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connected_devices": len(connected_devices),
        "brave_configured": bool(BRAVE_API_KEY),
        "tavily_configured": bool(TAVILY_API_KEY)
    }

@app.post("/api/search", response_model=SearchResponse, tags=["Search"])
async def search(
    query: str = Query(..., description="Search query"),
    provider: str = Query(default="brave", description="Search provider"),
    count: int = Query(default=5, le=20),
    language: str = Query(default="id")
):
    """
    Endpoint untuk melakukan web search
    
    ### Query Parameters:
    - **query**: Kalimat pencarian (required)
    - **provider**: Pilihan provider (brave/tavily), default: brave
    - **count**: Jumlah hasil (1-20), default: 5
    - **language**: Bahasa hasil (id/en/zh/etc), default: id
    
    ### Example:
    ```
    GET /api/search?query=python+programming&provider=brave&count=5
    ```
    """
    logger.info(f"Search request: query={query}, provider={provider}")
    
    if provider == "brave":
        result = await web_search_service.brave_search(query, count)
    elif provider == "tavily":
        result = await web_search_service.tavily_search(query)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown provider: {provider}. Use 'brave' or 'tavily'"
        )
    
    return result

@app.post("/api/search/smart", response_model=SearchResponse, tags=["Search"])
async def smart_search(request: SearchRequest):
    """
    Smart search endpoint dengan request body
    
    ### Request Body:
    ```json
    {
        "query": "python programming tips",
        "provider": "brave",
        "count": 5,
        "language": "en"
    }
    ```
    """
    logger.info(f"Smart search: {request.query}")
    
    if request.provider == "brave":
        return await web_search_service.brave_search(request.query, request.count)
    elif request.provider == "tavily":
        return await web_search_service.tavily_search(request.query)
    else:
        raise HTTPException(status_code=400, detail="Unknown provider")

# ===================== WEBSOCKET ENDPOINTS =====================

@app.websocket("/ws/device")
async def websocket_device(websocket: WebSocket):
    """
    WebSocket endpoint untuk XiaoZhi device MCP communication
    
    Format pesan MCP:
    ```json
    {
        "type": "mcp",
        "payload": {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "web_search",
                "arguments": {
                    "query": "python",
                    "count": 5
                }
            },
            "id": 1
        }
    }
    ```
    """
    await websocket.accept()
    device_id = None
    
    try:
        logger.info("New device connected via WebSocket")
        
        while True:
            data = await websocket.receive_json()
            logger.debug(f"Received message: {data}")
            
            if data.get("type") == "mcp":
                mcp_payload = data.get("payload", {})
                method = mcp_payload.get("method")
                msg_id = mcp_payload.get("id")
                
                # Handle tools/call method
                if method == "tools/call":
                    tool_name = mcp_payload.get("params", {}).get("name")
                    tool_args = mcp_payload.get("params", {}).get("arguments", {})
                    
                    logger.info(f"Tool call: {tool_name} with args {tool_args}")
                    
                    if tool_name == "web_search":
                        query = tool_args.get("query", "")
                        count = tool_args.get("count", 5)
                        
                        result = await web_search_service.brave_search(query, count)
                        
                        # Format response untuk MCP
                        response = {
                            "type": "mcp",
                            "payload": {
                                "jsonrpc": "2.0",
                                "id": msg_id,
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": json.dumps(
                                                result.dict(),
                                                ensure_ascii=False,
                                                indent=2
                                            )
                                        }
                                    ]
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
                                "id": msg_id,
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": json.dumps(
                                                result.dict(),
                                                ensure_ascii=False,
                                                indent=2
                                            )
                                        }
                                    ]
                                }
                            }
                        }
                        
                        await websocket.send_json(response)
                    
                    else:
                        error_response = {
                            "type": "mcp",
                            "payload": {
                                "jsonrpc": "2.0",
                                "id": msg_id,
                                "error": {
                                    "code": -32601,
                                    "message": f"Tool '{tool_name}' not found"
                                }
                            }
                        }
                        await websocket.send_json(error_response)
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
    finally:
        logger.info(f"Device disconnected: {device_id}")

# ===================== ERROR HANDLERS =====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

# ===================== MAIN =====================

if __name__ == "__main__":
    logger.info("Starting XiaoZhi Web Search Backend...")
    
    uvicorn.run(
        app,
        host=os.getenv('BACKEND_HOST', '0.0.0.0'),
        port=int(os.getenv('BACKEND_PORT', 8080)),
        log_level=os.getenv('LOG_LEVEL', 'info'),
        reload=os.getenv('DEBUG', 'False').lower() == 'true'
    )
