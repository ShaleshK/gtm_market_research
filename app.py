import os
import sys
import subprocess
import time
import pathlib
from pathlib import Path
from dotenv import load_dotenv

# Core Orchestration Components
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter
import streamlit as st
import pypdf

# Web Ingestion Utilities
import requests
from bs4 import BeautifulSoup

# 🎨 1. UI Layout Configuration
st.set_page_config(
    page_title="CrewAI Universal & Classic GTM Synthesizer",
    page_icon="🔮",
    layout="wide"
)

# 📂 Traversal Path Mappings & Keys Fetching
root_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=root_dir / ".env")

# 🛠️ 2. Core Text Extraction Utilities
def extract_file_content(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    name = uploaded_file.name.lower()
    if name.endswith('.pdf'):
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            return "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
        except Exception as e:
            return f"Error parsing PDF metadata: {str(e)}"
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")

def extract_url_content(url: str) -> str:
    """Scrapes raw web addresses and returns clean literal paragraph text string markers."""
    if not url:
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Decompose background boilerplate components
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            clean_text = soup.get_text(separator="\n", strip=True)
            return clean_text
    except Exception as e:
        return f"Failed to ingest URL track targets: {str(e)}"
    return ""

# 📊 3. Sidebar Layout Panel
with st.sidebar:
    st.markdown("### 🛠️ System Tool Status")
    st.success("🟢 FastMCP Server: Active")
    st.success("🔎 Web Scraping: Available")
    st.markdown("")
    st.markdown("### 🔌 MCP Network Connection")
    st.success("🔗 Connected: 2 Research Tools")
    
    st.markdown("---")
    st.subheader("🎯 Target Output Blueprint (The Shape)")
    st.caption("Leave empty for Classic GTM Market Research Mode")
    
    # Dual Ingestion Layout Options for the Template Target
    template_file = st.file_uploader(
        "Upload a reference template file (.pdf, .txt, .md):", 
        type=["txt", "md", "pdf"]
    )
    template_url = st.text_input(
        "OR paste a Blueprint URL (Google Sheet 'Publish to Web' link or layout page):",
        placeholder="https://google.com..."
    )
    
    st.markdown("---")
    st.subheader("📁 Source Knowledge Context (The Facts)")
    
    # Dual Ingestion Layout Options for the Data Inputs
    context_files = st.file_uploader(
        "Upload raw source input files:", 
        type=["txt", "md", "pdf"], 
        accept_multiple_files=True
    )
    context_url = st.text_input(
        "OR paste a reference Web URL for targeted research:",
        placeholder="https://yahoo.com..."
    )

# 📥 4. Main UI Application Content Dashboard Panel
st.title("🔮 Dual-Mode Universal Multi-Agent Orchestrator")
st.caption("Using Local Llama 3.1 Model via Port :11434")

st.info(
    "💡 **Dynamic Mode Engine Active**: If you fill out template or context items in the sidebar, this app acts as a **Universal Template Synthesizer**. "
    "If you leave the sidebar options completely blank, it runs as your **Classic Multi-Agent Market Research and GTM Generator** natively!"
)

# Request Input Field
user_prompt = st.text_input(
    "Define Research Focus / Prompts Guidance Parameters:",
    placeholder="e.g., 'Caterpillar competitors' or 'DeepSeek market segment trends'"
)

# 🚀 5. Execution Submission Button Handler
if st.button("Execute Multi-Agent Workflow", type="primary"):
    if not user_prompt:
        st.warning("Please enter a research topic refinement parameter before running.")
    else:
        st.markdown("### 🔄 Starting Multi-Agent Pipeline...")
        
        # Initialize progress tracking indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        st.toast("Parameters accepted successfully!", icon="🔮")
        status_text.markdown("🔮 Initializing background infrastructures...")
        progress_bar.progress(10)
        
        # 🎯 FALLBACK DETECTOR: Determine which track we are running based on sidebar inputs
        is_template_mode = (template_file is not None) or (len(template_url.strip()) > 0)
        
        # Extract template and file data in-memory if available
        with st.spinner("Analyzing uploaded documentation and network web streams..."):
            # A. Extract Target Structural Template Content
            if template_file:
                target_template_text = extract_file_content(template_file)[:6000]
            elif template_url:
                target_template_text = extract_url_content(template_url)[:6000]
            else:
                target_template_text = ""
                
            # B. Extract Source Data Knowledge Content
            compiled_context_text = ""
            if context_files:
                for f in context_files:
                    compiled_context_text += f"\n\n--- Source File: {f.name} ---\n" + extract_file_content(f)
            if context_url:
                compiled_context_text += f"\n\n--- Ingested Source URL Context ({context_url}) ---\n" + extract_url_content(context_url)
                
            compiled_context_text = compiled_context_text[:12000] # Safe scaling boundary cache limit

        try:
            # Bind your local Llama model via CrewAI wrapper
            local_llm = LLM(
                model="ollama/llama3.1",
                base_url="http://localhost:11434"
            )
            
            # FastMCP Client Connection Configuration Dictionary
            server_config = {"url": "http://localhost:8000/sse"}
            status_text.markdown("🔌 Establishing secure network handshake with your FastMCP server pool...")
            progress_bar.progress(40)
            
            with MCPServerAdapter(server_config) as mcp_tools:
                status_text.markdown("🤖 Orchestrating specialized agent memory matrices...")
                progress_bar.progress(55)

                # Initialize the 4 Core Roles
                structural_architect = Agent(
                    role="Head GTM Framework Architect",
                    goal="Coordinate the research workflow streams and synthesize structural findings.",
                    backstory="An expert operator who structures clean brief skeletons matching project metrics perfectly.",
                    llm=local_llm,
                    verbose=True
                )

                research_scientist = Agent(
                    role="Primary Market Research Scientist",
                    goal="Gather empirical evidence and retrieve competitor data structures using search tools.",
                    backstory="A data-mining specialist capable of compiling multi-source research strings via FastMCP.",
                    tools=mcp_tools,
                    llm=local_llm,
                    verbose=True
                )

                data_analyst = Agent(
                    role="Senior Competitive Intelligence Analyst",
                    goal="Convert raw text strings into structured data arrays, SWOT matrices, and 4P tables.",
                    backstory="A strategic modeling engineer focused on data synthesis and market pattern alignments.",
                    llm=local_llm,
                    verbose=True
                )

                executive_strategist = Agent(
                    role="Principal Go-To-Market Strategist",
                    goal="Formulate high-differentiation GTM playbooks, customer profiles, and 90-day launch maps.",
                    backstory="A growth architect who translates complex tables into publication-ready tactical reports.",
                    llm=local_llm,
                    verbose=True
                )

                # 🎯 CONFIGURING DYNAMIC TASK DESCRIPTIONS BASED ON THE RUNNING MODE
                if is_template_mode:
                    # Universal Mode Context Prompts
                    desc_structure = f"Analyze this target output template schema text carefully:\n\"\"\"\n{target_template_text}\n\"\"\"\nGenerate an empty Markdown framework matching its exact heading styles, layout bounds, and length caps."
                    desc_gather = f"Read this raw source data context text block:\n\"\"\"\n{compiled_context_text}\n\"\"\"\nUse your web search tools to gather any missing updates or facts based on the user's specific request: '{user_prompt}'."
                    desc_align = "Ingest the empty template framework blueprint and fill out every heading section completely using the raw factual data gathered by the Research Scientist."
                    desc_publish = "Polish the finalized synthesized document. Ensure headers are formatted correctly, remove empty text variables, and verify strict style alignment."
                else:
                    # Classic Hardcoded GTM Mode Context Prompts
                    desc_structure = f"Analyze context and outline 5 critical target research vectors for the market focus parameters: '{user_prompt}'."
                    desc_gather = f"Run your FastMCP research search tools across the scoped target nodes for the prompt focus: '{user_prompt}'. Gather clean competitor links and market snippet data variables."
                    desc_align = "Ingest the raw research data snippets string grid and generate a clean, formatted competitive landscape comparison table alongside a qualitative SWOT analysis matrix."
                    desc_publish = f"Compile the finalized publication-ready GTM strategy document for '{user_prompt}'. Detail segmented Ideal Customer Profiles (ICPs) and a comprehensive 90-day execution launch plan report."

                # Map text variable naming conventions for folder saving paths safely
                clean_filename_token = "".join(c for c in user_prompt if c.isalnum() or c.isspace()).strip().replace(" ", "_")
                if not clean_filename_token:
                    clean_filename_token = "GTM_Output"

                output_directory = root_dir / "output"
                output_directory.mkdir(exist_ok=True)
                final_report_path = str(output_directory / f"{clean_filename_token}_Strategy_Report.md")

                # Bind Task Classes
                task_1 = Task(description=desc_structure, expected_output="Markdown summary list containing structural headers or vector questions.", agent=structural_architect)
                task_2 = Task(description=desc_gather, expected_output="A clean text data contract containing verified data variables, quotes, and links.", agent=research_scientist)
                task_3 = Task(description=desc_align, expected_output="Formatted markdown layout containing competitive landscape criteria data tables.", agent=data_analyst)
                task_4 = Task(description=desc_publish, expected_output="Full length comprehensive strategy planning report document with markdown headers.", agent=executive_strategist, output_file=final_report_path)

                # Simulated progress tracking strings
                status_messages = [
                    "🔮 Agent 1: Outlining strategy vectors and reverse-engineering requirements...",
                    "🔎 Agent 2: Executing FastMCP network search queries and scraping internet data...",
                    "📊 Agent 3: Processing raw snippet data models and compiling structured matrices...",
                    "📝 Agent 4: Crafting Ideal Customer Profiles and structuring 90-day launch roadmap..."
                ]   

                # Initialize Crew Engine
                gtm_crew = Crew(
                    agents=[structural_architect, research_scientist, data_analyst, executive_strategist],
                    tasks=[task_1, task_2, task_3, task_4],
                    process=Process.sequential,
                    verbose=True
                )

                # Update progress bar smoothly across the execution window
                for i in range(40):
                    current_progress = 55 + i
                    progress_bar.progress(current_progress)
                    msg_index = i // 10
                    if msg_index < len(status_messages):
                        status_text.markdown(f"⏳ Status: {status_messages[msg_index]}")
                        time.sleep(0.4)

                status_text.markdown("⚙️ Status: Finalizing report files assembly and writing output text structures...")

                # Fire the background orchestration loops
                final_report = gtm_crew.kickoff()

                # Complete workflow paths
                progress_bar.progress(100)
                status_text.empty()

                st.success("🏆 Report Pipeline Completed and Compiled Successfully!")
                st.markdown("### 📋 Generated Production Output Preview:")
                st.markdown(final_report)
                st.info(f"💾 File Successfully Exported to: {final_report_path}")
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Execution Error: {str(e)}")  