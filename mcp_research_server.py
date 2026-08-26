import os
from mcp.server.fastmcp import FastMCP
import requests
from dotenv import load_dotenv, find_dotenv

# Automatically searches the current folder, then climbs recursively up parent directories until it targets your true .env file!
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
        return {"error": "Missing SerpAPI Key configuration token inside .env file."}
        
    url = "https://serpapi.com"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 5
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        # Extract top-tier primary organic evidence streams
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
    # Boots the server container via Standard Input/Output channel vectors
    mcp.run()
