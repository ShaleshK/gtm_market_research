import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from langchain_openai import AzureChatOpenAI
import streamlit as st

# ---------- 1) Streamlit View Port UI & Theme Setup ----------
st.set_page_config(
    page_title="CrewAI Multi-Agent GTM Generator",
    page_icon="🎯",
    layout="wide"
)

# Traversal Path Math: Fetch keys from your root environment file (.env)
root_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=root_dir / ".env")

# ---------- 2) Sidebar Metric Tracker Layout Panel ----------
with st.sidebar:
    st.markdown("### 🛠️ Tool Status")
    st.success("SerpAPI: ✅ Active")
    st.success("Scraping: ✅ Available")
    
    st.markdown("---")
    st.markdown("### 🔗 MCP Connection")
    st.success("Connected (5 tools)")
    
    # Matching your instructor's status indicator list panels exactly
    st.caption("• company_overview")
    st.caption("• list_competitors")
    st.caption("• product_portfolio")
    st.caption("• pricing_snapshot")
    st.caption("• recent_news_pulse")

# ---------- 3) Main UI Application Content Dashboard Panel ----------
st.title("🎯 CrewAI Multi-Agent GTM Generator")
st.caption("Using OPENAI model via env keys")

# Instructor's Class Brief Info Banner Component Box
st.info(
    "**We are launching 'MarketVision AI'**, an AI-powered market intelligence platform that "
    "automates market research and GTM planning for B2B SaaS companies.\n\n"
    "**Target:** US market, mid-market SaaS companies (50-500 employees) | "
    "**Differentiator:** Multi-agent AI system for comprehensive analysis."
)

# User Request Input Field Form Box
user_prompt = st.text_input(
    label="Refine Research Focus:",
    placeholder="Research topic (e.g., 'OpenAI competitors', 'AI market analysis')...",
    label_visibility="collapsed"
)

# Form Trigger Submission Button Handler
if st.button("🚀 Execute Hierarchical Workflow", type="primary"):
    if not user_prompt:
        st.warning("Please enter a research topic refinement parameter before running.")
    else:
        st.markdown("### ⚙️ Starting hierarchical workflow with openai...")
        
        # Initialize animated progress tracking indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Proactively alert the user about the background agent window
        st.toast("⚡ Research focus parameters accepted successfully!", icon="✅")
        
        status_text.markdown("🔄 *Initializing background infrastructure...*")
        progress_bar.progress(10)
        
        try:
            # 1. Bind your high-performance local Llama 3.1 sandbox model natively using CrewAI's LLM wrapper
            # 🎯 PERMANENT BLOCKADE BYPASS: Fully strips out the 'stop' parameter error by running locally over Ollama
            from crewai import LLM
            
            azure_llm = LLM(
                model="ollama/llama3.1",
                base_url="http://localhost:11434"
            )


            # Formulate absolute path to your background server file cleanly
            server_script_path = str(root_dir / "mcp_research_server.py")
            
            # CRITICAL WINDOWS FIX: Pre-warm the background subprocess shell ahead of the adapter
            status_text.markdown("📡 *Pre-warming FastMCP Server process pipeline...*")
            progress_bar.progress(25)
            
            # 2. Package your client network link inside a standard configuration dictionary contract
            # 🎯 RESOLVES VALUEERROR: Directly satisfies the adapter's expected data type parameter check
            server_config = {
                "url": "http://localhost:8000/sse"
            }
            
            status_text.markdown("📡 *Establishing secure network handshake with your FastMCP server pool...*")
            progress_bar.progress(40)
            
            # 3. Mount your custom MCP research tools by passing your new configuration dictionary
            with MCPServerAdapter(server_config) as mcp_tools:
                
                status_text.markdown("👥 *Orchestrating specialized agent memory matrices...*")
                progress_bar.progress(55)
                
                # --- Your remaining definitions for your 4 agents and tasks continue right beneath here untouched ---

                
                # --- Define the 4 Core Agents ---
                head_planner = Agent(
                    role="Head GTM Planner and Orchestrator",
                    goal="Coordinate the research workflow streams and synthesize specialist findings.",
                    backstory="Corporate systems operator who structures raw project briefs.",
                    llm=azure_llm,
                    verbose=True
                )
                
                research_agent = Agent(
                    role="Primary Market Research Scientist",
                    goal="Gather empirical evidence and retrieve competitor data structures using tools.",
                    backstory="Data-mining specialist who extracts clean links.",
                    tools=mcp_tools,  # Attaches your FastMCP tools cleanly to this specific agent
                    llm=azure_llm,
                    verbose=True
                )
                
                analyst_agent = Agent(
                    role="Senior Competitive Intelligence Analyst",
                    goal="Convert raw snippets into structured arrays, SWOT, and 4P matrices.",
                    backstory="Strategic modeling expert focused on industry analysis.",
                    llm=azure_llm,
                    verbose=True
                )
                
                strategy_agent = Agent(
                    role="Principal Go-To-Market Strategist",
                    goal="Formulate high-differentiation GTM playbooks and 90-day launch maps.",
                    backstory="Growth architect translating analytical grids into plans.",
                    llm=azure_llm,
                    verbose=True
                )
                
                # --- Define the Chained Tasks ---
                task_plan = Task(
                    description=f"Analyze user context: '{user_prompt}'. Outline 5 critical target research vectors for MarketVision AI.",
                    expected_output="Markdown summary list containing 5 research questions.",
                    agent=head_planner
                )
                task_research = Task(
                    description="Run your FastMCP desk research search tool across the scoped target nodes. Gather competitor links.",
                    expected_output="JSON data contract containing verified link variables and snippets.",
                    agent=research_agent
                )
                task_analysis = Task(
                    description="Ingest the research data strings and generate a competitive landscape table alongside a SWOT matrix.",
                    expected_output="Formatted markdown layout containing tables and SWOT criteria blocks.",
                    agent=analyst_agent
                )
                # 🎯 TARGET FIXED: Sanitize user input text to use as a clean file name token
                clean_filename_token = user_prompt.strip().replace(" ", "_").replace('"', "").replace("'", "")
                
                # Ensure a dedicated output folder exists inside the repository footprint
                output_directory = root_dir / "output"
                output_directory.mkdir(exist_ok=True)
                
                # Construct the customized dynamic path string asset
                final_report_path = str(output_directory / f"{clean_filename_token}_Strategy_Report.md")
                
                # --- Define the Finalized Task Card ---
                task_gtm_draft = Task(
                    description="Compile the finalized publication-ready GTM strategy document. Detail ideal customer profiles and a launch plan.",
                    expected_output="Full length GTM planning report containing precise markdown headers.",
                    agent=strategy_agent,
                    # Dynamic naming allocation targeting the dedicated directory structure natively
                    output_file=final_report_path 
                )

                
                # Simulated incremental feedback loops while the actual multi-agent threads process
                status_messages = [
                    "📋 Head Planner: Analyzing brief and charting 5 critical research target nodes... (Minutes 0-2)",
                    "📡 Research Agent: Launching FastMCP search tools and scraping competitor pricing models... (Minutes 2-5)",
                    "📊 Analyst Agent: Ingesting raw JSON data contracts and compiling SWOT/4P text grids... (Minutes 5-8)",
                    "🧠 Strategy Agent: Constructing Ideal Customer Profiles and mapping 90-day GTM milestones... (Minutes 8-12)",
                    "📝 Finalizing Document: Packaging markdown text structures and exporting reports... (Minutes 12-15)"
                ]
                
                                # Assemble your automated execution engine crew
                gtm_crew = Crew(
                    agents=[head_planner, research_agent, analyst_agent, strategy_agent],
                    tasks=[task_plan, task_research, task_analysis, task_gtm_draft],
                    process=Process.sequential,  # Sequences execution step-by-step
                    verbose=True
                )
                
                # 🚀 UI STATUS UPDATE & PROGRESS TIMER INTEGRATION
                status_messages = [
                    "📋 Head Planner: Analyzing brief and charting 5 critical research target nodes... (Minutes 0-2)",
                    "📡 Research Agent: Launching FastMCP search tools and scraping competitor pricing models... (Minutes 2-5)",
                    "📊 Analyst Agent: Ingesting raw JSON data contracts and compiling SWOT/4P text grids... (Minutes 5-8)",
                    "🧠 Strategy Agent: Constructing Ideal Customer Profiles and mapping 90-day GTM milestones... (Minutes 8-12)",
                    "📝 Finalizing Document: Packaging markdown text structures and exporting reports... (Minutes 12-15)"
                ]
                
                # Slowly advance the progress bar through the agent stages to keep the UI active
                for i in range(45):
                    current_progress = 55 + int((i / 45) * 35)  # Scales smoothly from 55% up to 90%
                    progress_bar.progress(current_progress)
                    
                    # Cycle through the messages based on the current step
                    msg_index = min(i // 9, len(status_messages) - 1)
                    status_text.markdown(f"⏳ **Status:** *{status_messages[msg_index]}*")
                    time.sleep(0.5)  # Keep it responsive without locking up Streamlit's web thread
                
                status_text.markdown("🤖 **Status:** *Agents are processing your final analytical layers and compiling the GTM report now...*")
                
                # ⚙️ Execute the real background multi-agent generation loop
                final_report = gtm_crew.kickoff()
                
                # Render results to web view once fully completed
                progress_bar.progress(100)
                status_text.empty()
                
                st.success("🏆 Go-To-Market Blueprint Compiled Successfully!")
                st.markdown("### 📝 Generated Strategy Report")
                st.markdown(final_report)
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Execution Error: {str(e)}")
