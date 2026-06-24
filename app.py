import os
import re
import streamlit as st

# 1. First-Step Fix: st.set_page_config MUST be the very first Streamlit command!
st.set_page_config(
    page_title="InterviewPilot AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports
from tools.pdf_reader import extract_pdf_text
from tools.resume_parser import parse_resume
from agents.orchestrator import run_agents
from agents.adk_orchestrator import run_adk_agents, get_agent_names
from database.db import create_tables, save_report, get_user_reports
from security.login import register_user, login_user
from reports.pdf_exporter import generate_pdf
from mcp_servers.course_mcp import CourseMCP

# Initialize Database Tables
create_tables()

# 2. Score Extractor Helper
def extract_score_from_text(text):
    """
    Dynamically extracts the resume score (out of 100) from the agent's markdown output.
    """
    if not text:
        return 75
        
    # Search for "Score: XX" or "Score out of 100: XX" or "Score - XX"
    matches = re.findall(r'(?:score|rating|points|result)\s*[:\-]*\s*(\d{1,3})', text, re.IGNORECASE)
    if matches:
        val = int(matches[0])
        if 0 <= val <= 100:
            return val
            
    # Search for "XX/100"
    matches2 = re.findall(r'(\d{1,3})\s*/\s*100', text)
    if matches2:
        val = int(matches2[0])
        if 0 <= val <= 100:
            return val
            
    # Default fallback
    return 75

# 3. Premium CSS Styling for Rich Aesthetics
st.markdown("""
<style>
    /* Import modern Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Apply Fonts globally */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #f8fafc;
    }

    /* Main App Background (sleek dark mode) */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f0b29 50%, #050414 100%);
        color: #e2e8f0;
    }
    
    /* Styled Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 8, 28, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Glassmorphic Cards & Bordered Containers */
    .glass-card, div[data-testid="stVerticalBlockBorder"] {
        background: rgba(17, 12, 46, 0.45) !important;
        backdrop-filter: blur(12px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(12px) saturate(160%) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        transition: transform 0.25s ease, border-color 0.25s ease !important;
    }
    .glass-card:hover, div[data-testid="stVerticalBlockBorder"]:hover {
        transform: translateY(-2px);
        border-color: rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Primary buttons (glass/gradient) */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(168, 85, 247, 0.5) !important;
    }
    
    /* Title text styling */
    .glowing-title {
        font-size: 3rem;
        background: linear-gradient(to right, #818cf8, #c084fc, #e879f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(129, 140, 248, 0.2);
        margin-bottom: 5px;
        font-weight: 800;
        letter-spacing: -0.025em;
    }
    
    .glowing-subtitle {
        color: #94a3b8;
        font-size: 1.15rem;
        margin-bottom: 30px;
        font-weight: 400;
    }
    
    /* Metrics display */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #c084fc !important;
    }
    
    /* Table styling for dark theme */
    div[data-testid="stTable"] table {
        background-color: rgba(17, 12, 46, 0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Styled expander headers */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    /* Custom colored alerts */
    .success-alert {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        color: #a7f3d0;
        margin-bottom: 20px;
    }
    .error-alert {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        color: #fca5a5;
        margin-bottom: 20px;
    }
    
    /* Timeline styling for Roadmap */
    .roadmap-week {
        border-left: 3px solid #8b5cf6;
        padding-left: 20px;
        margin-left: 10px;
        position: relative;
        margin-bottom: 25px;
    }
    .roadmap-week::before {
        content: '';
        position: absolute;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #a855f7;
        left: -8px;
        top: 4px;
        box-shadow: 0 0 10px #a855f7;
    }
</style>
""", unsafe_allow_html=True)

# 4. Sidebar Authentication Flow
st.sidebar.markdown("<div style='text-align: center; padding: 10px;'><h2 style='margin:0; background: linear-gradient(135deg, #a78bfa, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>✈️ InterviewPilot</h2></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Authentication menu
st.sidebar.subheader("👤 User Authentication")
menu = st.sidebar.selectbox("Select Action", ["Login", "Signup"])

if menu == "Signup":
    st.markdown("<h1 class='glowing-title'>Create Account</h1>", unsafe_allow_html=True)
    st.markdown("<p class='glowing-subtitle'>Sign up to start analyzing your resumes and preparing for interviews</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email Address", placeholder="john@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Create Account"):
            if not name or not email or not password:
                st.markdown("<div class='error-alert'>Please fill in all fields.</div>", unsafe_allow_html=True)
            elif register_user(name, email, password):
                st.markdown("<div class='success-alert'>Account successfully created! Please switch to 'Login' in the sidebar.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='error-alert'>Email already registered. Try logging in.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if menu == "Login":
    if not st.session_state.get("logged_in"):
        st.markdown("<h1 class='glowing-title'>Welcome to InterviewPilot AI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>The AI-powered multi-agent interview preparation platform</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            email = st.text_input("Email Address", placeholder="john@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In"):
                if login_user(email, password):
                    st.session_state["logged_in"] = True
                    st.session_state["email"] = email
                    st.rerun()
                else:
                    st.markdown("<div class='error-alert'>Invalid email or password. Please try again.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Add educational card about the stack on the home screen
        st.markdown("<div class='glass-card'><h3>💡 Powered by Advanced Agentic Tech</h3><p>InterviewPilot AI integrates the brand-new <b>Google Agent Development Kit (ADK)</b> and <b>Model Context Protocol (MCP)</b> to deliver specialized multi-agent assessments. Log in to try both our Standard and Google ADK engines!</p></div>", unsafe_allow_html=True)
        st.stop()

# 5. Main Logged-In Interface
if st.session_state.get("logged_in"):
    
    # Sidebar logout
    st.sidebar.success(f"Logged in as: {st.session_state['email']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["email"] = None
        st.rerun()
        
    # Navigation Radio
    st.sidebar.markdown("---")
    st.sidebar.subheader("🗺️ Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Report History", "ADK & MCP Guide 🧠"])
    
    # Sidebar: Display active ADK Agents & Recommended Courses
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 Active ADK Agents")
    try:
        agent_names = get_agent_names()
        for name in agent_names:
            st.sidebar.markdown(f"• `{name}`")
    except Exception as e:
        st.sidebar.error(f"Error loading agents: {e}")
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("📚 Quick Course Recommendations")
    try:
        course_server = CourseMCP()
        courses = course_server.recommend_courses()
        for course in courses:
            st.sidebar.markdown(f"🎓 **{course}**")
    except Exception as e:
        st.sidebar.error(f"Error loading courses: {e}")

    # PAGE 1: ADK & MCP Guide
    if page == "ADK & MCP Guide 🧠":
        st.markdown("<h1 class='glowing-title'>Understanding ADK & MCP</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Learn about the powerful technologies powering this application</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='glass-card'>
                <h3 style='color: #818cf8;'>🤖 Google Agent Development Kit (ADK)</h3>
                <p>The <b>Agent Development Kit (ADK)</b> is Google's open-source, code-first framework designed to build, test, and deploy AI agents at scale.</p>
                <ul>
                    <li><b>Model Agnostic:</b> Programmed to orchestrate and manage agents natively.</li>
                    <li><b>Asynchronous Execution:</b> Run multiple specialized agents concurrently (we run all 5 agents in parallel!).</li>
                    <li><b>Sessions & History:</b> Natively maintains conversation context using <code>InMemorySessionService</code>.</li>
                    <li><b>Runner System:</b> An orchestration loop that routes messages, runs tools, and handles state.</li>
                </ul>
                <h4 style='color: #a78bfa; margin-top: 15px;'>How it's used in this app:</h4>
                <p>When you choose the <b>Google ADK Orchestrator</b>, we initialize 5 individual agents: <code>ResumeAgent</code>, <code>SkillGapAgent</code>, <code>HRAgent</code>, <code>TechnicalAgent</code>, and <code>RoadmapAgent</code>. They run concurrently inside a managed ADK session to analyze your resume.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='glass-card'>
                <h3 style='color: #f472b6;'>🔌 Model Context Protocol (MCP)</h3>
                <p>The <b>Model Context Protocol (MCP)</b> is an open standard that allows LLMs to securely connect to external tools, databases, APIs, and local resources.</p>
                <ul>
                    <li><b>Universal Adapter:</b> Eliminates writing custom code for every API; instead, servers declare tools and the model calls them directly.</li>
                    <li><b>Secure & Governed:</b> Keeps data access sandboxed and traceable.</li>
                    <li><b>Resource Sharing:</b> Exposes documents, logs, and files safely to the AI model.</li>
                </ul>
                <h4 style='color: #f472b6; margin-top: 15px;'>How it's used in this app:</h4>
                <p>We have built a mock <code>CourseMCP</code> server. In our ADK engine, this server's <code>recommend_courses</code> tool is <b>actively registered</b> with the ADK <code>SkillGapAgent</code>. When the agent detects a skill gap, it dynamically invokes this MCP tool to fetch course recommendations!</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Architecture Diagram
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🖥️ Agentic Architecture Diagram")
        st.markdown("""
        ```mermaid
        graph TD
            User[User Resume Upload] --> |Triggers Analysis| Orchestrator[Orchestrator System]
            
            subgraph Google ADK Engine
                Orchestrator --> |Concurrently Runs| Runner[ADK Runner & Sessions]
                Runner --> Agent1[Resume Agent]
                Runner --> Agent2[Skill Gap Agent]
                Runner --> Agent3[HR Agent]
                Runner --> Agent4[Technical Agent]
                Runner --> Agent5[Roadmap Agent]
            end
            
            subgraph Model Context Protocol (MCP) Tools
                Agent2 --> |Calls Tool| CourseMCP[Course MCP Server]
                CourseMCP --> |Returns| CourseList[Recommended Courses]
            end
            
            Agent1 --> |MD Output| Final[Unified Evaluation & PDF Export]
            Agent2 --> |MD Output| Final
            Agent3 --> |MD Output| Final
            Agent4 --> |MD Output| Final
            Agent5 --> |MD Output| Final
        ```
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # PAGE 2: Report History
    if page == "Report History":
        st.markdown("<h1 class='glowing-title'>Your Evaluation History</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Access your past resume assessments and interview roadmaps</p>", unsafe_allow_html=True)
        
        reports = get_user_reports(st.session_state["email"])
        
        if not reports:
            st.markdown("<div class='glass-card'><h3 style='text-align: center; color: #94a3b8;'>No reports found. Upload a resume on the Dashboard to get started!</h3></div>", unsafe_allow_html=True)
        else:
            # Format history table
            import pandas as pd
            formatted_data = []
            for row in reports:
                # row structure: (id, email, score, created_at)
                formatted_data.append({
                    "Report ID": f"📄 #{row[0]}",
                    "Score": f"🎯 {row[2]}/100",
                    "Generated At": row[3]
                })
            df = pd.DataFrame(formatted_data)
            
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.table(df)
            st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # PAGE 3: Dashboard (Main Interface)
    if page == "Dashboard":
        st.markdown("<h1 class='glowing-title'>InterviewPilot AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Upload your resume and prepare for your dream tech job with multi-agent intelligence</p>", unsafe_allow_html=True)
        
        # Load user stats
        reports = get_user_reports(st.session_state["email"])
        total_reports = len(reports)
        
        scores = []
        for row in reports:
            try:
                scores.append(float(row[2]))
            except:
                pass
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        
        # Metrics Display
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 15px;'>
                <span style='color: #94a3b8; font-size: 0.95rem; font-weight: 500;'>📁 TOTAL REPORTS</span>
                <h1 style='color: #818cf8; margin: 5px 0; font-size: 2.8rem;'>{total_reports}</h1>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 15px;'>
                <span style='color: #94a3b8; font-size: 0.95rem; font-weight: 500;'>🎯 AVERAGE RESUME SCORE</span>
                <h1 style='color: #c084fc; margin: 5px 0; font-size: 2.8rem;'>{avg_score if avg_score > 0 else 'N/A'}<span style='font-size: 1.2rem; color: #64748b;'>/100</span></h1>
            </div>
            """, unsafe_allow_html=True)
            
        # File Upload & Orchestrator Configuration
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("⚙️ Analysis Configuration & File Upload")
        
        # Check for test mode query parameter
        is_test_mode = st.query_params.get("test") == "true"
        
        col_c1, col_c2 = st.columns([2, 3])
        with col_c1:
            orchestrator_type = st.radio(
                "Select Multi-Agent Orchestrator Engine",
                [
                    "🤖 Google ADK (Agent Development Kit) Engine",
                    "⚙️ Standard Multi-Agent Engine"
                ],
                help="Google ADK uses the official asynchronous runner, session services, and integrates the Course MCP Server directly as a tool! Standard engine uses concurrent standard LLM calls."
            )
        with col_c2:
            uploaded_file = st.file_uploader("Drag and drop your Resume PDF here", type=["pdf"])
            if is_test_mode and not uploaded_file:
                st.info("🧪 Test Mode Active: Automatically loading mock resume (test_resume.pdf)")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        has_resume = False
        pdf_path = None
        
        if uploaded_file:
            has_resume = True
            os.makedirs("uploads", exist_ok=True)
            pdf_path = f"uploads/{uploaded_file.name}"
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        elif is_test_mode:
            has_resume = True
            pdf_path = "d:\\InterviewPilotAI\\test_resume.pdf"
            
        if has_resume:
            if not uploaded_file and is_test_mode:
                st.markdown("<div class='success-alert'>✓ Test Mode: Automatically loaded mock resume 'test_resume.pdf'.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='success-alert'>✓ Resume '{uploaded_file.name}' uploaded successfully! Cleaned text extracted.</div>", unsafe_allow_html=True)
            
            # Action Button
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            trigger_analysis = st.button("🚀 Analyze Resume & Generate Prep Kit")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if trigger_analysis:
                # Execution
                with st.spinner("🧠 Orchestrating Agents and Running Analysis... Please wait..."):
                    try:
                        # Extract and parse only after clicking the button
                        text = extract_pdf_text(pdf_path)
                        
                        try:
                            parsed_resume = parse_resume(text)
                        except Exception as parse_err:
                            print(f"[WARNING] Resume parsing failed: {parse_err}. Using raw extracted text.")
                            parsed_resume = text
                            
                        if "Google ADK" in orchestrator_type:
                            results = run_adk_agents(parsed_resume)
                            engine_used = "Google ADK"
                        else:
                            results = run_agents(parsed_resume)
                            engine_used = "Standard Engine"
                            
                        # Extract dynamic score and save
                        score = extract_score_from_text(results["resume_analysis"])
                        save_report(st.session_state["email"], str(score))
                        
                        # Generate PDF Report
                        pdf_report_path = "reports/interview_report.pdf"
                        generate_pdf(pdf_report_path, results)
                        
                        # Store in session state to persist after render
                        st.session_state["results"] = results
                        st.session_state["score"] = score
                        st.session_state["pdf_path"] = pdf_report_path
                        st.session_state["engine_used"] = engine_used
                        
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error executing agent orchestration: {e}")
                        import traceback
                        st.code(traceback.format_exc())
            
            # Render Results if they exist in session state
            if st.session_state.get("results"):
                results = st.session_state["results"]
                score = st.session_state["score"]
                pdf_path = st.session_state["pdf_path"]
                engine_used = st.session_state["engine_used"]
                
                st.markdown("<br><hr><br>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: #c084fc;'>✨ Evaluation Results ({engine_used})</h2>", unsafe_allow_html=True)
                
                # Display Score Card
                col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
                with col_s2:
                    st.markdown(f"""
                    <div class='glass-card' style='text-align: center; border: 2px solid rgba(139, 92, 246, 0.5); background: linear-gradient(135deg, rgba(30, 27, 75, 0.8), rgba(88, 28, 135, 0.4));'>
                        <h2 style='margin:0; font-size: 2.2rem;'>🎯 RESUME SCORE</h2>
                        <h1 style='font-size: 4.5rem; color: #a855f7; margin: 10px 0; text-shadow: 0 0 20px rgba(168, 85, 247, 0.5);'>{score}<span style='font-size: 1.5rem; color: #94a3b8;'>/100</span></h1>
                        <p style='color: #cbd5e1; font-size: 1rem;'>Based on industry standards for Software Developers and AI Engineers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Tabbed display of report sections
                tab1, tab2, tab3, tab4, tab5 = st.columns(5)
                
                # We can use button-like tabs or Streamlit tabs. Streamlit tabs are very clean!
                st_tabs = st.tabs([
                    "📋 Resume Assessment", 
                    "⚠️ Skill Gap Analysis", 
                    "💬 HR Interview Prep", 
                    "💻 Tech Interview Prep", 
                    "📅 30-Day Roadmap"
                ])
                
                with st_tabs[0]:
                    with st.container(border=True):
                        st.markdown("### Detailed Resume Assessment")
                        st.markdown(results["resume_analysis"])
                    
                with st_tabs[1]:
                    with st.container(border=True):
                        st.markdown("### Skill Gaps & Course Recommendations")
                        st.markdown(results["skill_gap"])
                    
                with st_tabs[2]:
                    with st.container(border=True):
                        st.markdown("### Tailored HR & Behavioral Questions")
                        st.markdown(results["hr_questions"])
                    
                with st_tabs[3]:
                    with st.container(border=True):
                        st.markdown("### Custom Technical Interview Questions")
                        st.markdown(results["technical_questions"])
                    
                with st_tabs[4]:
                    with st.container(border=True):
                        st.markdown("### Personalized 30-Day Preparation Timeline")
                        
                        # Style roadmap weeks uniquely
                        roadmap_text = results["roadmap"]
                        # Highlight weeks by placing them in nice blocks
                        roadmap_weeks = roadmap_text.split("Week ")
                        if len(roadmap_weeks) > 1:
                            for i, week_content in enumerate(roadmap_weeks[1:]):
                                st.markdown(f"""
                                <div class='roadmap-week'>
                                    <h4 style='color: #a855f7; margin-bottom: 5px;'>Week {i+1}</h4>
                                    <div style='color: #cbd5e1;'>
                                """, unsafe_allow_html=True)
                                st.markdown("Week " + week_content)
                                st.markdown("""
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown(roadmap_text)
                
                # Download Report Button
                st.markdown("<br>", unsafe_allow_html=True)
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Comprehensive PDF Evaluation Report",
                        data=file,
                        file_name=f"InterviewPilot_Report_{st.session_state['email'].split('@')[0]}.pdf",
                        mime="application/pdf"
                    )