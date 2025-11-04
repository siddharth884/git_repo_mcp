# GIT_REPO_MCP/client.py

import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# MCP server configuration
SERVERS = {
    "github_server": {
        "command": "python",
        "args": ["server.py"], # server.py in the same directory
        "transport": "stdio"
    }
}

async def main():
    # nitialize MCP client
    client = MultiServerMCPClient(SERVERS)

    # Note: LLM initialization is included for production readiness
    llm = ChatGroq(
        model="llama3-8b-8192",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Connect to the GitHub server session
    async with client.session("github_server") as session:
        print("\n✅ Connected to GitHub Stats Server!")

        # List and display the tool
        tools = await session.list_tools()
        print("\n Tool available:")
        if tools.tools:
            print(f"- {tools.tools[0].name}")
        
        # Test calling the get_repo_stats tool
        if tools.tools and tools.tools[0].name == 'get_repo_stats':
            print("\n--- TESTING get_repo_stats ---")
            
            try:
                # Testing with Meta's Llama repository (highly visible data)
                owner_name = "siddharth884"
                repo_name_val = "Portfolio"
                
                print(f"Querying Repo: {owner_name}/{repo_name_val}")
                
                # Call the tool with required inputs
                result = await session.call_tool(
                    'get_repo_stats', 
                    {"owner": owner_name, "repo_name": repo_name_val}
                )
                
                print("\n Tool Result:", result)
                print("\n--- Test complete. ---")
            except Exception as e:
                print(f" Error while invoking tool: {e}")
        else:
            print(" 'get_repo_stats' tool not found on server.")

        if len(tools.tools) > 1 and tools.tools[1].name == 'get_file_content':
            print("\n--- TESTING get_file_content (Source Code Fetch) ---")
            
            try:
                owner_name = "siddharth884"
                repo_name_val = "Portfolio"
                file_path_val = "README.md"
                
                print(f"Fetching file content for: {owner_name}/{repo_name_val}/{file_path_val}")
                
                result = await session.call_tool(
                    'get_file_content', 
                    {"owner": owner_name, "repo_name": repo_name_val, "file_path": file_path_val}
                )
                
                
                print("\n Source Code Result (First 500 chars):\n", result.content[0].text)
                print("\n--- Source Code Fetch Test complete. ---")
            except Exception as e:
                print(f" Error while invoking get_file_content: {e}")
        else:
            print(" 'get_file_content' tool not found on server (Check server.py).")

if __name__ == "__main__":
    asyncio.run(main())