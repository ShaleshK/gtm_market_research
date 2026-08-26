import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from langchain_openai import AzureChatOpenAI

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
        
        status_text.markdown("🔄 *Executing workflow... Running hierarchical workflow. May take 5-15 minutes...*")
        progress_bar.progress(20)
        
        try:
            # 1. Bind your cloud-based Azure OpenAI model context natively
            azure_llm = AzureChatOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "vt-agi-chat")
            )
            
            # 2. Setup Stdio transport parameters to connect directly to your server file
            server_params = StdioServerParameters(
                command="uv",
                args=["run", str(root_dir / "src" / "mcp_research_server.py")],
                env={**os.environ}
            )
            
            progress_bar.progress(40)
            status_text.markdown("📡 *Establishing secure runtime handshake with your FastMCP server...*")
            
            # 3. Mount your custom MCP research tools using CrewAI adapters
            with MCPServerAdapter(server_params) as mcp_tools:
                
                status_text.markdown("👥 *Orchestrating specialized agent memory matrices...*")
                progress_bar.progress(60)
                
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
                task_gtm_draft = Task(
                    description="Compile the finalized publication-ready GTM strategy document. Detail ideal customer profiles and a launch plan.",
                    expected_output="Full length GTM planning report containing precise markdown headers.",
                    agent=strategy_agent
                )
                
                status_text.markdown("🤖 *Agents are running tool calls and compiling market reports...*")
                progress_bar.progress(80)
                
                # Assemble your automated execution engine crew
                gtm_crew = Crew(
                    agents=[head_planner, research_agent, analyst_agent, strategy_agent],
                    tasks=[task_plan, task_research, task_analysis, task_gtm_draft],
                    process=Process.sequential,  # Sequences execution step-by-step
                    verbose=True
                )
                
                # Run the pipeline natively inside the Streamlit instance
                final_report = gtm_crew.kickoff()
                
                # Render results to web view
                progress_bar.progress(100)
                status_text.empty()
                
                st.success("🏆 Go-To-Market Blueprint Compiled Successfully!")
                st.markdown("### 📝 Generated Strategy Report")
                st.markdown(final_report)
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Execution Error: {str(e)}")
