🧠 Git MCP Client

A lightweight Multi-Client Protocol (MCP) implementation that connects with Git repositories and allows direct interaction through LangChain tools.
It enables AI agents to fetch repo statistics, read file contents, and perform other Git-related operations programmatically.

🚀 Features

🔗 Connects seamlessly to GitHub repositories

📊 Fetches repository metadata (stars, forks, watchers, etc.)

📂 Reads file contents directly from any repo path

🧩 Easily extensible — add custom tools for new operations

⚡ Built using LangChain + AsyncIO + MCP Framework

🧰 Tech Stack

Python 3.10+

LangChain (v1.x)

AsyncIO

MultiServerMCPClient

⚙️ How to Run
# 1️⃣ Create a virtual environment
python -m venv mcp_env
source mcp_env/Scripts/activate  # on Windows PowerShell

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run the client
python client.py

🧩 Example Output
✅ Connected to GitHub repository
📈 Repo Stats:
  Stars: 42 | Forks: 3 | Watchers: 6
📄 File Content:
  README.md loaded successfully!