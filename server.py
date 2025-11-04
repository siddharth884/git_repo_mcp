# GIT_REPO_MCP/server.py

from mcp.server.fastmcp import FastMCP
import httpx
import base64

# Create an MCP server named "github_stats"
mcp = FastMCP("github_stats")

# --- Tool: GitHub Repository Query ---
@mcp.tool()
def get_repo_stats(owner: str, repo_name: str):
    """Fetch star count, fork count, and open issues for a GitHub repository."""
    try:
        # Construct the GitHub API Endpoint URL
        url = f"https://api.github.com/repos/{owner}/{repo_name}"
        
        response = httpx.get(url)
        response.raise_for_status() # Handle 4xx/5xx HTTP errors
        
        data = response.json()
        
        # Extract and structure the key statistics
        stats = {
            "name": data.get("full_name"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "open_issues": data.get("open_issues_count"),
            "description": data.get("description", "No description available")
        }
        
        return stats
    
    except httpx.HTTPStatusError as e:
        # Handle 404 Not Found error specifically
        if e.response.status_code == 404:
            return f"Error: Repository '{owner}/{repo_name}' not found on GitHub."
        return f"HTTP Error fetching stats: {e}"
        
    except Exception as e:
        return f"Error fetching stats: {str(e)}"

@mcp.tool()
def get_file_content(owner: str, repo_name: str, file_path: str):
    """Fetches the source code content of a specific file in a GitHub repository."""
    try:
        # GitHub API Endpoint to get file contents
        url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}"
        
        response = httpx.get(url)
        response.raise_for_status() 
        data = response.json()
        
        # Decode Base64 content to a readable string
        if data.get("encoding") == "base64" and data.get("content"):
            content_encoded = data["content"]
            source_code = base64.b64decode(content_encoded).decode('utf-8')
            
            # Return a useful snippet (first 500 characters)
            return f"File: {file_path}\n---\n{source_code[:500]}..." 
        
        return f"Error: Could not decode file content or file is a directory."
    
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: File '{file_path}' not found in '{owner}/{repo_name}'."
        return f"HTTP Error: {e}"
        
    except Exception as e:
        return f"Error fetching file content: {str(e)}"



if __name__ == "__main__":
    mcp.run(transport="stdio")