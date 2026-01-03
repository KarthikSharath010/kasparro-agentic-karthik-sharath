import streamlit as st
import streamlit.components.v1 as components
import json
import os
import time
import html
import textwrap
from dotenv import load_dotenv

# Core Imports
from core.state import SharedState
from core.orchestrator import ApexSupervisor

# Agent Imports
from agents.data_agent import DataAgent
from agents.ideation_agent import IdeationAgent
from agents.content_agent import ContentAgent
from agents.validator_agent import ValidatorAgent

# --- Configuration ---
st.set_page_config(
    page_title="ApexAgent",
    page_icon="🤖",
    layout="wide",
)

load_dotenv()

# --- Custom CSS (Refined Geometric Dark) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0A0A0A;
        color: #E0E0E0;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #1A1A1A;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        color: #FFFFFF !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(90deg, #FFFFFF, #FF8800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #FF8800 0%, #FF6600 100%);
        color: #000000;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 136, 0, 0.3);
        color: #000000;
    }

    /* Inputs (Neat & Dark) */
    div[data-testid="stTextInput"] input {
        background-color: #111 !important;
        border: 1px solid #333 !important;
        color: #EEE !important;
        border-radius: 8px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #FF8800 !important;
        box-shadow: 0 0 0 1px #FF8800 !important;
    }
    label[data-testid="stWidgetLabel"] p {
        font-size: 0.85rem;
        color: #888;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* Logs Container */
    .log-container {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        background-color: #0F0F0F;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 10px;
        height: 300px;
        overflow-y: auto;
        display: flex;
        flex-direction: column; 
    }
    .log-entry {
        padding: 6px 8px;
        border-bottom: 1px solid #1A1A1A;
        display: flex;
        gap: 12px;
        align-items: baseline;
    }
    .log-entry:last-child {
        border-bottom: none;
    }
    .log-time { color: #666; min-width: 65px; font-size: 0.8rem; }
    .log-source { color: #FF8800; font-weight: bold; min-width: 110px; }
    .log-msg { color: #DDD; word-break: break-all; }

    /* Cards/Expanders */
    .stExpander {
        border: 1px solid #222;
        border-radius: 8px;
        background-color: #111;
    }
    
    /* JSON/Code */
    code {
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1>🤖 ApexAgent</h1>", unsafe_allow_html=True)
    st.caption("Autonomous System v2.1")
    
    st.markdown("---")
    
    # SIMULATION MODE TOGGLE
    sim_mode = st.toggle("Enable Simulation Mode", value=False, help="Run without API Key using pre-calculated data.")
    
    if not sim_mode:
        # Persistent API Key Input (GEMINI)
        api_key_input = st.text_input("Gemini API Key", type="password")
        
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
        elif "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
    else:
        st.info("⚡ Running in Simulation Mode. No API Key required.")
    
    st.markdown("### 🧠 Cortex State")
    if "shared_state" in st.session_state:
        state = st.session_state.shared_state
        ctx = state.get_all().get("context", {})
        if ctx:
            st.metric("Context Keys", len(ctx))
            with st.expander("View Keys", expanded=False):
                 st.code("\n".join(list(ctx.keys())), language="text")
        else:
            st.info("System Initialized")

# --- Main App ---
col_header, col_status = st.columns([3, 1])
with col_header:
    st.markdown("## 📡 Mission Control")
    st.caption("Monitoring Supervisor Reasoning & Agent Delegation")

# Initialize System in Session State
if "shared_state" not in st.session_state:
    st.session_state.shared_state = SharedState()

state = st.session_state.shared_state

# --- Execution Controls ---
# Small Button
col_btn, col_space = st.columns([1, 4])
with col_btn:
    if st.button("🚀 Start Mission", type="primary"):
        # Validation Logic
        if not sim_mode and not os.environ.get("GEMINI_API_KEY"):
            st.error("⚠️ Missing Gemini API Key.")
            st.toast("Please enter your Gemini API Key or Enable Simulation Mode.", icon="⚠️")
        else:
            # Re-initialize
            st.session_state.shared_state = SharedState()
            state = st.session_state.shared_state
            
            # Update Context with Sim Mode
            state.update_context("simulation_mode", sim_mode)
            
            # Re-init Supervisor/Agents
            supervisor = ApexSupervisor(state)
            supervisor.register_agent("DataAgent", DataAgent(state))
            supervisor.register_agent("IdeationAgent", IdeationAgent(state))
            supervisor.register_agent("ContentAgent", ContentAgent(state))
            supervisor.register_agent("ValidatorAgent", ValidatorAgent(state))
            
            st.session_state.is_running = True
            st.rerun()

if "is_running" not in st.session_state:
    st.session_state.is_running = False

# --- Live Log Display (Persistent) ---
with st.container():
    st.subheader("Agent Logs")
    
    log_messages = state._state["messages"]
    
    if log_messages:
        # Standard Chronological Order
        log_html = "<div class='log-container'>"
        for entry in log_messages:
            safe_msg = html.escape(entry['message'])
            safe_source = html.escape(entry['source'])
            
            # NO INDENTATION in the HTML string to prevent markdown code block
            log_html += f"<div class='log-entry'><span class='log-time'>{entry['timestamp']}</span><span class='log-source'>{safe_source}</span><span class='log-msg'>{safe_msg}</span></div>"
            
        log_html += "</div>"
        st.markdown(log_html, unsafe_allow_html=True)
    else:
        st.info("Waiting for mission start...")

# --- Execution Loop ---
if st.session_state.is_running:
    # RE-INITIALIZE Agents
    supervisor = ApexSupervisor(state)
    supervisor.register_agent("DataAgent", DataAgent(state))
    supervisor.register_agent("IdeationAgent", IdeationAgent(state))
    supervisor.register_agent("ContentAgent", ContentAgent(state))
    supervisor.register_agent("ValidatorAgent", ValidatorAgent(state)) 

    with st.spinner("Agents working..."):
        keep_going = supervisor.run_step()
    
    time.sleep(1.0) 
    
    if not keep_going:
        st.session_state.is_running = False
        st.success("Mission Cycle Ended.")
    
    st.rerun()

# --- Artifact Display ---
if state.get_context("validation_report"):
    st.markdown("---")
    st.subheader("📦 Generated Artifacts")

    if state.get_context("validation_report") == "PASS":
        artifacts = state.get_all()["artifacts"]
        
        tab1, tab2, tab3, tab4 = st.tabs(["👁️ Product Page Preview", "📄 Product JSON", "❓ FAQ JSON", "⚖️ Comparison JSON"])
        
        with tab1:
            pp = artifacts.get("product_page.json", {})
            if pp:
                # FIX: Access call_to_action correctly from nested hero_section
                cta = pp.get('hero_section', {}).get('call_to_action', 'Buy Now')
                
                preview_html = f"""
                    <html>
                    <head>
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
                        body {{
                            font-family: 'Outfit', sans-serif;
                            background-color: #151515;
                            color: #EEE;
                            padding: 2rem;
                            margin: 0;
                        }}
                        .container {{
                            max-width: 1000px;
                            margin: 0 auto;
                            border: 1px solid #333;
                            border-radius: 12px;
                            background: #151515;
                            padding: 3rem;
                            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                        }}
                        h1 {{ color: #FF8800; font-size: 3rem; margin: 0.5rem 0; letter-spacing: -1px; }}
                        h2 {{ color: #FFF; font-size: 3.5rem; margin: 1.5rem 0; line-height: 1.2; }}
                        h3 {{ color: #FF8800; margin-top: 0; }}
                        .btn {{
                            display: inline-block;
                            background: #FF8800;
                            color: #000;
                            padding: 15px 40px;
                            border-radius: 50px;
                            font-size: 1.2rem;
                            font-weight: 800;
                            cursor: pointer;
                            box-shadow: 0 0 20px rgba(255,136,0,0.4);
                            text-decoration: none;
                        }}
                        .grid {{
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            gap: 3rem;
                            margin-top: 2rem;
                        }}
                        .card {{
                            background: #202020;
                            padding: 2rem;
                            border-radius: 12px;
                            border: 1px solid #333;
                        }}
                        ul {{ line-height: 1.8; color: #DDD; padding-left: 1.2rem; }}
                        strong {{ color: #FFF; }}
                    </style>
                    </head>
                    <body>
                        <div class="container">
                            <div style="text-align: center; border-bottom: 1px solid #333; padding-bottom: 2rem; margin-bottom: 2rem;">
                                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; color: #888; margin-bottom: 1rem;">Official Store</div>
                                <h1>{pp.get('meta', {}).get('title')}</h1>
                                <p style="color: #AAA; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">{pp.get('meta', {}).get('description')}</p>
                            </div>
                            
                            <div style="text-align: center; margin-bottom: 4rem;">
                                <h2>{pp.get('hero_section', {}).get('headline')}</h2>
                                <a class="btn">
                                    {cta} — ${pp.get('specifications', {}).get('price')}
                                </a>
                            </div>
                            
                            <div class="grid">
                                <div class="card">
                                    <h3>✨ Key Benefits</h3>
                                    <ul>
                                        {"".join([f"<li>{item}</li>" for item in pp.get('hero_section', {}).get('key_benefits', [])])}
                                    </ul>
                                </div>
                                <div class="card">
                                    <h3>🔬 Specifications</h3>
                                    <p style="margin-bottom: 1rem;"><strong>Volume:</strong> <span style="color: #AAA;">{pp.get('specifications', {}).get('volume')}</span></p>
                                    <div>
                                        <strong>Ingredients:</strong>
                                        <div style="margin-top: 0.5rem; color: #AAA; font-size: 0.95rem; line-height: 1.6;">
                                            {", ".join(pp.get('specifications', {}).get('ingredients', []))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                """
                components.html(preview_html, height=1000, scrolling=True)
            else:
                st.warning("Product page artifact missing.")

        with tab2:
            st.download_button("⬇️ Download JSON", json.dumps(artifacts.get("product_page.json"), indent=2), "product_page.json", "application/json")
            st.json(artifacts.get("product_page.json"))
        
        with tab3:
            st.download_button("⬇️ Download JSON", json.dumps(artifacts.get("faq.json"), indent=2), "faq.json", "application/json")
            st.json(artifacts.get("faq.json"))

        with tab4:
            st.download_button("⬇️ Download JSON", json.dumps(artifacts.get("comparison_page.json"), indent=2), "comparison_page.json", "application/json")
            st.json(artifacts.get("comparison_page.json"))
            
    elif state.get_context("validation_report") == "FAIL":
        st.error("Trace Validation Failed. Check logs for critique.")
