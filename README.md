# Capstone Project: Autonomous Multi-Agent Market Research and GTM Planner

An enterprise-grade, dual-implementation autonomous marketing intelligence pipeline built with **Streamlit**, **CrewAI**, and the **Model Context Protocol (MCP)**. This system orchestrates a 4-agent team to conduct deep competitive research, execute strategic synthesis matrices, and output production-ready Go-to-Market (GTM) blueprints.

## 🏗️ Multi-Agent Architecture
The workflow leverages four highly specialized agent roles executing in sequence:
1. **Head Planner & Orchestrator:** Analyzes the core product brief and breaks it down into 5 critical target research vectors.
2. **Primary Market Research Scientist:** Dispatches automated tool requests through a custom FastMCP server layer to aggregate organic Google search evidence and pricing snippets using SerpAPI.
3. **Senior Competitive Intelligence Analyst:** Consolidates raw JSON data blocks into structured comparison matrices, SWOT diagrams, and 4P/7P marketing frameworks.
4. **Principal Go-To-Market Strategist:** Translates qualitative and quantitative analysis grids into Ideal Customer Profiles (ICPs) and actionable 90-day launch milestones.

---

## 🚀 Local Installation & Environment Execution Steps

### 1. Project Initialization & Dependencies
This project is built and optimized natively inside the modern `uv` Python package ecosystem. Ensure you are pointing your terminal inside the root directory and synchronize the local virtual environment layer:
```bash
# Sync dependencies tracking file
uv lock

# Automatically build your localized isolated virtual environment matrix
uv sync
```

### 2. Private Credential Layer Configuration
Your secure API keys are maintained externally in a unified master configuration `.env` file located in the parent folder workspace hierarchy (`../.env`) to ensure absolute environment boundary security:
```env
AZURE_OPENAI_API_KEY=your_azure_api_key_here
AZURE_OPENAI_ENDPOINT=https://azure-api.net
AZURE_OPENAI_CHAT_DEPLOYMENT=vt-agi-chat
AZURE_OPENAI_API_VERSION=2024-02-15-preview
SERPAPI_API_KEY=your_serp_api_token_here
```

### 3. Run the FastMCP Network Tool Server
Open a dedicated terminal window panel and ignite your background web socket tool listening service on port `8000`:
```bash
uv run python mcp_research_server.py
```

### 4. Boot Up the Streamlit Interactive Frontend Application
Open a secondary independent terminal window prompt to spin up your graphical user dashboard UI. Pass your parent environment token flag directly down line to hydrate the engine variables smoothly:
```bash
uv run --env-file "../.env" streamlit run app.py
```
*Navigate your web browser tab to `http://localhost:8501` to view, test, and execute your agent clusters live!*

---

## 💾 Export Artifact Formats
* **Streamlit Interface View:** Renders rich text markdown reports interactively on completion.
* **Local Disk Export:** The final execution loop automatically compiles and writes a structured Markdown blueprint file named **`GTM_Strategy_Report.md`** straight to your project root folder directory, fully optimized for immediate editing or direct conversion into standard Microsoft Word (`.docx`) file structures.
