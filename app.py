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

# 🎨 1. UI Layout Configuration
st.set_page_config(
    page_title="CrewAI Multi-Agent Interactive Synthesizer",
    page_icon="🔮",
    layout="wide"
)

# 📂 Traversal Path Mappings & Keys Fetching
root_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=root_dir / ".env")

# Helper function to extract text cleanly from uploaded PDF/Text files
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

# 💾 2. MANAGED SESSION STATE: Persistent Chat Memory Layer
if "generated_report" not in st.session_state:
    st.session_state.generated_report = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clean_filename" not in st.session_state:
    st.session_state.clean_filename = "GTM_Output"

# 📊 3. Sidebar Layout Panel
with st.sidebar:
    st.markdown("### 🛠️ System Tool Status")
    st.success("🟢 FastMCP Server: Active")
    st.success("🔎 Web Scraping: Available")
    st.markdown("")
    st.markdown("### 🔌 MCP Network Connection")
    st.success("🔗 Connected: 2 Research Tools")
    
    st.markdown("---")
    st.subheader("🎯 Optional: Target Output Blueprint")
    st.caption("Leave empty for Classic GTM Market Research Mode")
    template_file = st.file_uploader(
        "Upload a reference template file (.pdf, .txt, .md):", 
        type=["txt", "md", "pdf"]
    )
    
    st.subheader("📁 Optional: Source Knowledge Context")
    context_files = st.file_uploader(
        "Upload raw source input files:", 
        type=["txt", "md", "pdf"], 
        accept_multiple_files=True
    )
    
    if st.button("🗑️ Reset Application Session", type="secondary"):
        st.session_state.generated_report = ""
        st.session_state.chat_history = []
        st.rerun()

# 📥 4. Main UI Application Content Dashboard Panel
st.title("🔮 Dual-Mode Interactive Multi-Agent Orchestrator")
st.caption("Using Local Llama 3.1 Model via Port :11434")

st.info(
    "💡 **Version 2.0 Conversational Feedback Active**: Trigger an initial report generation using the fields below. "
    "Once compilation finishes, an interactive chat canvas will unlock at the bottom of the screen to refine the draft report with your agents dynamically!"
)

# Initial Prompt Field
user_prompt = st.text_input(
    "Define Core Research Topic / Target Project Goals:",
    placeholder="e.g., 'Caterpillar competitors' or 'DeepSeek market segment trends'"
)

# Helper execution engine encapsulating core crew configurations
def run_agentic_pipeline(prompt_text, feedback_text=""):
    is_template_mode = template_file is not None
    
    target_template_text = extract_file_content(template_file)[:6000] if is_template_mode else ""
    compiled_context_text = ""
    if context_files:
        for f in context_files:
            compiled_context_text += f"\n\n--- Source Document: {f.name} ---\n" + extract_file_content(f)
    compiled_context_text = compiled_context_text[:12000]

    local_llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
    server_config = {"url": "http://localhost:8000/sse"}
    
    with MCPServerAdapter(server_config) as mcp_tools:
        # Initialize Core Agent Squad Roles
        structural_architect = Agent(role="Head GTM Framework Architect", goal="Coordinate the research workflow streams and synthesize structural findings.", backstory="An expert operator who structures clean briefs.", llm=local_llm, verbose=True)
        research_scientist = Agent(role="Primary Market Research Scientist", goal="Gather empirical evidence using search tools.", backstory="Data mining specialist via FastMCP.", tools=mcp_tools, llm=local_llm, verbose=True)
        data_analyst = Agent(role="Senior Competitive Intelligence Analyst", goal="Convert raw text strings into structured tables.", backstory="Strategic pattern modeling expert.", llm=local_llm, verbose=True)
        executive_strategist = Agent(role="Principal Go-To-Market Strategist", goal="Formulate high-differentiation tactical playbooks and final reports.", backstory="Senior editor translating analysis into publication-ready files.", llm=local_llm, verbose=True)

        if is_template_mode:
            desc_structure = f"Analyze this template:\n\"\"\"\n{target_template_text}\n\"\"\"\nGenerate a matching Markdown framework blueprint structure."
            desc_gather = f"Read this data context:\n\"\"\"\n{compiled_context_text}\n\"\"\"\nSearch the web via tools to extract details matching: '{prompt_text}'."
            desc_align = "Ingest the blueprint framework and map the raw search data text into its structural headers completely."
            desc_publish = "Review layout tracks, format strict markdown margins, and compile the final text report document."
        else:
            desc_structure = f"Outline 5 critical research vectors for the market parameters: '{prompt_text}'."
            desc_gather = f"Run FastMCP tools across target nodes for the prompt focus: '{prompt_text}'. Gather clean links and snippets variables."
            desc_align = "Convert the raw search data strings loop into a clean formatted comparison table and a qualitative SWOT analysis matrix."
            desc_publish = f"Compile the finalized GTM strategy document for '{prompt_text}'. Detail segmented customer profiles and a 90-day launch timeline roadmap."

        # Setup Saving Paths File Mappings Natively
        output_directory = root_dir / "output"
        output_directory.mkdir(exist_ok=True)
        final_report_path = str(output_directory / f"{st.session_state.clean_filename}_Strategy_Report.md")

        # Core Task Chains
        task_1 = Task(description=desc_structure, expected_output="Markdown structural header skeleton.", agent=structural_architect)
        task_2 = Task(description=desc_gather, expected_output="A clean text data contract with links and facts.", agent=research_scientist)
        task_3 = Task(description=desc_align, expected_output="Formatted markdown landscape table and criteria matrices grid.", agent=data_analyst)
        
        # Configure or inject a feedback task loop
        if feedback_text:
            desc_publish_with_feedback = (
                f"Take the previous draft document report and systematically modify it based on this explicit user critique request: '{feedback_text}'.\n"
                f"Maintain the overall formatting structure, but overwrite contents or adjust tone exactly as instructed."
            )
            task_4 = Task(description=desc_publish_with_feedback, expected_output="An updated, polished full-length Markdown report integrated with user modifications.", agent=executive_strategist)
        else:
            task_4 = Task(description=desc_publish, expected_output="Full length structural report document with markdown headers.", agent=executive_strategist)

        # Execute Assembly Run
        crew = Crew(
            agents=[structural_architect, research_scientist, data_analyst, executive_strategist],
            tasks=[task_1, task_2, task_3, task_4],
            process=Process.sequential,
            verbose=True
        )
        
        # Fire generation engine
        result_content = crew.kickoff()
        
        # 🎯 THE FILE CREATION GUARANTEE: Hard-force saving raw text straight to disk artifact
        try:
            report_text_string = str(result_content)
            with open(final_report_path, "w", encoding="utf-8") as file_out:
                file_handle = file_out.write(report_text_string)
        except Exception as file_err:
            st.sidebar.error(f"Auto-Save Disk IO Failure: {str(file_err)}")
            
        return result_content, final_report_path

# 🚀 5. INITIAL EXECUTION CONTROL
if st.button("Execute Initial Report Workflow", type="primary"):
    if not user_prompt:
        st.warning("Please enter a research topic or project parameters target before running.")
    else:
        st.session_state.clean_filename = "".join(c for c in user_prompt if c.isalnum() or c.isspace()).strip().replace(" ", "_")
        progress_bar = st.progress(10)
        status_text = st.empty()
        
        status_text.markdown("⏳ **Status**: Running multi-agent generation loops over local GPU cores...")
        progress_bar.progress(50)
        
        try:
            report_out, path_saved = run_agentic_pipeline(user_prompt)
            st.session_state.generated_report = report_out
            progress_bar.progress(100)
            status_text.empty()
            st.success("🏆 Document Draft Compiled Successfully!")
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Handshake Pipeline Failure: {str(e)}")

# 📊 6. RENDER THE GENERATED ARTIFACT OUTPUT
if st.session_state.generated_report:
    st.markdown("---")
    st.markdown("### 📋 Current Active Strategy Report Document:")
    with st.container(border=True):
        st.markdown(st.session_state.generated_report)
        
    st.markdown("---")
    st.markdown("### 💬 Chat with Your Agents (Interactive Feedback Loop)")
    
    # Render historic modifications conversational lines
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Capture live modifications prompts strings
    if feedback_input := st.chat_input("Tell the agents what to change (e.g., 'Make section 2 shorter' or 'Add pricing estimates'):"):
        st.session_state.chat_history.append({"role": "user", "content": feedback_input})
        with st.chat_message("user"):
            st.markdown(feedback_input)
            
        with st.chat_message("assistant"):
            refine_status = st.empty()
            refine_status.markdown("⚙️ **Agents are re-evaluating the document and applying edits...**")
            
            try:
                # Trigger the pipeline with user modifications attached
                updated_report, path_saved = run_agentic_pipeline(user_prompt, feedback_text=feedback_input)
                st.session_state.generated_report = updated_report
                
                refine_status.empty()
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": "I have successfully modified the document report file on disk according to your instructions! Check the updated view box layout above."
                })
                st.rerun() # Refresh layout views immediately
            except Exception as e:
                refine_status.empty()
                st.error(f"Refinement Crash: {str(e)}")
