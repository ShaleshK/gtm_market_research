# Capstone Project: Dual-Mode Universal Template Synthesizer & GTM Planner

An enterprise-grade, highly adaptive multi-agent orchestration engine built with **Streamlit**, **CrewAI**, and the **Model Context Protocol (MCP)**. This system runs an automated 4-agent team utilizing local **Ollama `llama3.1` model** intelligence over port `:11434` to handle both direct, out-of-the-box competitive market research and few-shot template document synthesis completely offline.

## 🏗️ Multi-Agent Architecture
The workflow coordinates four highly specialized agent roles executing sequentially via deep session memory tracking:
1. **Head GTM Framework Architect:** Reverse-engineers target blueprint files or schemas to design empty structural markdown skeletons matching target layouts, headings, length bounds, and tone rules perfectly.
2. **Primary Market Research Scientist:** Dispatches automated data mining tool requests via a custom FastMCP server layer to aggregate live Google search evidence using SerpAPI while reading source context document records natively.
3. **Senior Competitive Intelligence Analyst:** Ingests raw data contracts, search snippets, and text variables to map contextual metrics straight into the empty template skeleton frames.
4. **Lead Executive Publisher:** Reviews final layouts, formats strict markdown margins, resolves parsing anomalies, and injects interactive conversational user feedback refinements dynamically to produce a publication-ready master artifact document.

---

## 🔮 Dual Dynamic Operational Modes

*   **Mode A: Classic GTM Market Research & Generator**  
    Leave all sidebar file uploading fields completely blank, type an explicit market focus target prompt (e.g., `Caterpillar competitors`) straight into the input row, and hit execute. The crew will run an end-to-end automated live corporate competitive threat profiling loop.
*   **Mode B: Universal Few-Shot Template Synthesizer**  
    Upload an exemplar formatting template (Course cheat sheets, Wall Street research briefs, specific corporate layouts) along with a folder of raw source knowledge files. The agents will instantly extract the layout guidelines, analyze your context documents, and synthesize a pristine new report matching your design specification.

---

## 🚀 Local Installation & Environment Execution Steps

### 1. Project Initialization & Dependencies
This project is fully managed and optimized inside the modern `uv` Python package ecosystem. Ensure your terminal prompt path is pointed inside the root directory and synchronize your local virtual environment layer:
```bash
# Sync dependencies tracking file
uv lock

# Automatically build your localized isolated virtual environment matrix
uv sync

# Ensure advanced text parsing modules are added to your environment library
uv pip install pypdf
```

### 2. Run the FastMCP Network Tool Server
Open a dedicated terminal window panel and ignite your background web socket tool listening service on port `8000`:
```bash
uv run python mcp_research_server.py
```

### 3. Boot Up the Streamlit Interactive Frontend Application
Open a secondary independent terminal window prompt inside Cursor to spin up your graphical user dashboard UI. Use a declarative package flag wrapper to bypass any system path conflicts smoothly:
```bash
uv run --with pypdf python -m streamlit run app.py
```
*Navigate your web browser tab to `http://localhost:8501` to execute your agent clusters and engage with the chat refinement console live!*

---

## 💾 Export Artifact Formats
* **Streamlit Interface Chat Canvas:** Displays rich text markdown blocks interactively and allows for iterative real-time chat revisions with the model crew.
* **Automated Hard-Drive Save:** Every single execution loop (both initial generations and subsequent conversational feedback updates) automatically compiles, formats, and exports a clean Markdown document (`.md`) straight to your local `output/` directory on disk for immediate production deployment.

