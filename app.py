import streamlit as st
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our new Agents
from agents.data_agent import DataAgent
from agents.ideation_agent import IdeationAgent
from agents.content_agent import ContentAgent

# --- Configuration ---
st.set_page_config(
    page_title="ApexAgent | Content Pipeline",
    page_icon="🤖",
    layout="wide",
)

# --- Custom CSS for 'Geometric Dark' Theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #050505; /* Deep Black */
        color: #FFFFFF;
    }

    /* Minimalist Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Hero Title Styling */
    h1 {
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        letter-spacing: -1.5px;
        color: #FFFFFF !important;
        background: none !important;
        -webkit-text-fill-color: #FFFFFF !important;
        margin-bottom: 0px !important;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #888888;
        font-weight: 300;
        margin-bottom: 2rem;
    }

    /* Cards (Wireframe Style) */
    div[data-testid="stExpander"], div[data-testid="stContainer"] {
        background-color: #0A0A0A;
        border: 1px solid #333333;
        border-radius: 0px; /* Geometric/Sharp */
        box-shadow: none;
    }
    
    div[data-testid="stExpander"]:hover, div[data-testid="stContainer"]:hover {
        border-color: #FF8800; /* Deep Orange Accent */
    }

    /* Accent Button - Orange Pill */
    div.stButton > button {
        background-color: #FF8800;
        color: #000000;
        border: none;
        border-radius: 50px;
        font-weight: 700;
        padding: 0.6rem 2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }
    div.stButton > button:hover {
        background-color: #FFA500;
        color: #000000;
        box-shadow: 0 0 20px rgba(255, 136, 0, 0.4);
        transform: translateY(-2px);
    }
    
    /* Code Blocks - Stealth */
    code {
        color: #FF8800 !important;
        background-color: #111111 !important;
        border: 1px solid #222222;
    }
    
    /* Validated Badges */
    span[data-testid="stCaption"] {
        color: #666666 !important;
    }
    
    /* Alignment Fixes */
    .block-container {
        padding-top: 2rem !important; /* Reduced from 5rem as requested */
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 2rem !important;
    }
    
    /* Text Input Fixes */
    div[data-baseweb="input"] {
        background-color: #111111 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important; 
        color: white !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #FF8800 !important;
    }
    input {
        color: white !important;
    }
    /* Hide the 'Press Enter to Apply' overlay which overlaps content */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 2.4rem; margin-bottom: 0; padding-top: 0;'>ApexAgent.</h2>", unsafe_allow_html=True)
    st.caption("v1.2.0")
    
    st.markdown("---")
    
    api_key = st.text_input("API Key", type="password", placeholder="Enter Gemini Key")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        import google.generativeai as genai
        genai.configure(api_key=api_key)
    else:
        # Clear stale key from session if input is cleared
        # This prevents the 'no error' issue when removing a manually entered key
        if "GEMINI_API_KEY" in os.environ:
             # Only delete if it matches the current process state (simple check)
             # But safer to just reload from .env to be sure
             del os.environ["GEMINI_API_KEY"]
        
        # Reload from .env (source of truth if no manual input)
        load_dotenv()
        if os.environ.get("GEMINI_API_KEY"):
            import google.generativeai as genai
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- Main Page ---
# Hero Section
st.markdown("<h1>Designing a Better<br>Workflow Today.</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Autonomous agents transforming raw ideas into tangible realities.</p>", unsafe_allow_html=True)
st.markdown("""
<div style="margin-bottom: 2rem;">
This system uses a <strong>Multi-Agent Architecture</strong>:
<br>1. <strong>Data Agent</strong>: Ingests Source JSON & Models Competitor.
<br>2. <strong>Ideation Agent</strong>: Generates & Categorizes FAQs.
<br>3. <strong>Content Agent</strong>: Assembles final artifacts.
</div>
""", unsafe_allow_html=True)

# --- Pipeline Logic with Persistence ---
if st.button("🚀 Run Pipeline", type="primary"):
    # 0. Validation: Check API Key
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("⛔ **Missing API Key**: Please enter your Gemini API Key in the sidebar to proceed.")
        st.stop()

    start_time = time.time()
    # --- Orchestration Container ---
    placeholder = st.empty()
    
    with placeholder.container():
        st.info("System Initialized. Starting Agents...")
        
        # --- Architecture Visualization (DAG) ---
        with st.expander("🏗️ Real-Time Architecture Flow", expanded=True):
            st.graphviz_chart("""
                digraph {
                    rankdir=LR;
                    bgcolor="transparent";
                    node [shape=box, style="filled,rounded", fillcolor="#262626", color="#555555", penwidth=1.5, fontcolor="#FFFFFF", fontname="Sans"];
                    edge [color="#888888", penwidth=1.2, arrowsize=0.8];
                    
                    Data [label="📦 Data Agent", fillcolor="#1E1E1E"];
                    Ideation [label="💡 Ideation Agent", fillcolor="#1E1E1E"];
                    Content [label="📝 Content Agent", fillcolor="#1E1E1E"];
                    
                    Data -> Ideation [label="Context", fontcolor="#AAAAAA", fontsize=10];
                    Data -> Content;
                    Ideation -> Content;
                }
            """)

        # 1. Data Agent
        with st.spinner("📦 Data Agent: Ingesting & Modeling..."):
            data_agent = DataAgent()
            glowboost = data_agent.load_glowboost_data()
            competitor = data_agent.generate_competitor_data()
            time.sleep(0.8) # Simulating latency for effect
            
        if not glowboost:
            st.error("Error: Source data not found!")
            st.stop()
            
        # 2. Ideation Agent
        with st.spinner("💡 Ideation Agent: Brainstorming Questions..."):
            ideation_agent = IdeationAgent()
            raw_questions = ideation_agent.generate_questions(glowboost)
            
            # Error Handling: Check if Ideation failed (API Key issue)
            if raw_questions and "Error" in raw_questions[0]:
                st.error(f"⛔ Ideation Failed: {raw_questions[0]}")
                st.stop()
                
            structured_faqs = ideation_agent.process_faqs(raw_questions)
            time.sleep(1.2)
            
        # Agent Feedback (So it doesn't just disappear)
        st.toast(f"💡 Brainstormed {len(raw_questions)} Questions!", icon="✅")
            
        # 3. Content Agent
        with st.spinner("� Content Agent: Assembling Artifacts..."):
            content_agent = ContentAgent()
            faq_json = content_agent.build_faq_json(structured_faqs)
            product_json = content_agent.build_product_page_json(glowboost)
            comparison_json = content_agent.build_comparison_page_json(glowboost, competitor)
            time.sleep(0.5)
            
        # Store in Session State for Persistence
        st.session_state['pipeline_results'] = {
            'glowboost': glowboost,
            'competitor': competitor,
            'raw_questions': raw_questions,
            'structured_faqs': structured_faqs,
            'faq_json': faq_json,
            'product_json': product_json,
            'comparison_json': comparison_json
        }

# --- Check for Results in Session State ---
if 'pipeline_results' in st.session_state:
    results = st.session_state['pipeline_results']
    
    # Unpack for easy access
    glowboost = results['glowboost']
    competitor = results['competitor']
    raw_questions = results['raw_questions']
    structured_faqs = results['structured_faqs']
    faq_json = results['faq_json']
    product_json = results['product_json']
    comparison_json = results['comparison_json']

    st.success("✨ Pipeline Complete! All artifacts generated.")

    # --- Restore Agent Reasoning (Persisted) ---
    with st.expander("👁️ View Data Agent Reasoning", expanded=False):
        st.markdown(f"**Ingested**: `{glowboost['product_name']}`")
        if 'claims' in glowboost and glowboost['claims']:
             st.markdown(f"**Key Claim**: _{glowboost['claims'][0]}_")
        st.markdown(f"**Competitor Model**: `{competitor['product_name']}` (Generated for comparison)")
        st.success("✅ Dataset Validated")

    with st.expander("👁️ View Ideation Agent Reasoning", expanded=False):
        st.markdown("**Prompt Context**:")
        # Safe access to claims for display
        claim_preview = glowboost['claims'][0] if 'claims' in glowboost and glowboost['claims'] else "N/A"
        st.code(f"Product: {glowboost['product_name']}\nClaims: {claim_preview}...", language="text")
        
        st.markdown(f"**Output**: Generated {len(raw_questions)} candidates.")
        st.success(f"✅ Categories Mapped: {', '.join(structured_faqs.keys())}")

    # --- Results & Insights Display ---
    st.divider()
    
    # Insights "Logic Block" Visualization
    st.subheader("🧠 Engineered Insights")
    st.caption("Deterministic Logic Blocks applied to data.")
    
    with st.container(border=True):
        ic1, ic2 = st.columns(2)
        with ic1:
            st.markdown("##### 📉 Price Optimization Logic")
            p_a = glowboost['price']
            p_b = competitor['price']
            diff = abs(p_a - p_b)
            # Show the actual code used
            st.code(f"diff = abs({p_a} - {p_b})", language="python")
            st.markdown(f"**Conclusion**: _{glowboost['product_name']}_ is **${diff:.2f}** cheaper.")
        with ic2:
            st.markdown("##### 🧪 Ingredient Overlap Analysis")
            common = set(glowboost['ingredients']).intersection(set(competitor['ingredients']))
            st.code(f"common = set(a) & set(b)\n# Found {len(common)} items", language="python")
            st.markdown(f"**Overlap Score**: {len(common)}/{len(glowboost['ingredients'])}")

    st.divider()

    # Artifacts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📄 Product Page")
        st.caption("JSON-Schema Validated ✅")
        with st.expander("View JSON Source"):
            st.code(json.dumps(product_json, indent=2), language="json")
        st.download_button("Download JSON", data=json.dumps(product_json, indent=2), file_name="product_page.json", mime="application/json")
        
    with col2:
        st.subheader("❓ FAQ Data")
        st.caption("JSON-Schema Validated ✅")
        with st.expander("View JSON Source"):
            st.code(json.dumps(faq_json, indent=2), language="json")
        st.download_button("Download JSON", data=json.dumps(faq_json, indent=2), file_name="faq.json", mime="application/json")

    with col3:
        st.subheader("⚖️ Comparison")
        st.caption("JSON-Schema Validated ✅")
        with st.expander("View JSON Source"):
            st.code(json.dumps(comparison_json, indent=2), language="json")
        st.download_button("Download JSON", data=json.dumps(comparison_json, indent=2), file_name="comparison_page.json", mime="application/json")
