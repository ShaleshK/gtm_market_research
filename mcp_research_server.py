import os
import sys
from pathlib import Path

# Force-insert the active virtual environment site-packages path to prevent missing module errors
venv_site_packages = str(Path(__file__).resolve().parents[1] / ".venv" / "Lib" / "site-packages")
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

try:
    from mcp.server.fastmcp import FastMCP
    import requests
    from dotenv import load_dotenv, find_dotenv
except ImportError as e:
    # Explicitly write crashes to a local diagnostic error file since standard output is hijacked by stdio
    with open("mcp_crash_log.txt", "w") as f:
        f.write(f"Import Initialization Failure: {str(e)}\n")
    sys.exit(1)

# Dynamically locate your parent folder .env file registry
load_dotenv(find_dotenv())

# Initialize FastMCP Server Object
mcp = FastMCP("Market-Research-Core")

@mcp.tool()
def desk_research_search(query: str) -> dict:
    """
    Executes deep desk research using SerpAPI. Returns structured organic search results, 
    metadata snippets, and primary citations for GTM validation mapping.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return {"error": "Missing SERPAPI_API_KEY inside your environment variables."}
        
    url = "https://serpapi.com"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        results = []
        for item in data.get("organic_results", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
            
        return {"sources_extracted": results}
    except Exception as e:
        return {"error": f"Handshake network failure: {str(e)}"}

if __name__ == "__main__":
    # 🎯 PERMANENT WINDOWS FIX: Switch from standard I/O pipes to a dedicated web network socket
    import uvicorn
    # Boots up as a persistent local network API listening service on port 8000
    mcp.run(transport="sse")

