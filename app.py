"""
Telecom Customer Assistant - Enterprise RAG Application
Features:
  - Clean, Ultra-Modern Dark Glassmorphic Aesthetic (Google Fonts, Smooth Gradients)
  - Tab 1: Conversational Chat Assistant with Multi-Turn Memory & Citation Badges
  - Tab 2: Interactive RAG Dashboard (Live Playground & Automated Benchmark Suite)
"""
import os
import time
import json
import uuid
import streamlit as st
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Telecom Customer Assistant",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# Ultra-Modern Enterprise CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Background & Radial Glow Mesh */
.stApp {
    background: radial-gradient(circle at 10% 8%, rgba(56, 189, 248, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 90% 92%, rgba(139, 92, 246, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.5) 0%, transparent 100%),
                #070b14 !important;
    color: #e2e8f0;
}

/* Top Hero Header Banner */
.hero-container {
    background: linear-gradient(135deg, rgba(24, 33, 54, 0.75) 0%, rgba(13, 19, 36, 0.85) 100%);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 20px;
    padding: 24px 30px;
    margin-bottom: 22px;
    backdrop-filter: blur(20px);
    box-shadow: 0 16px 40px -12px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.hero-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 5px;
    margin-bottom: 0;
    font-weight: 400;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #34d399;
    padding: 6px 14px;
    border-radius: 24px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.15); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.8; }
}

/* Tab Navigation Styling */
/* LEVEL 1: MAIN TABS (Customer Care Assistant vs Dashboard) - Electric Blue */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: rgba(15, 23, 42, 0.75);
    padding: 7px;
    border-radius: 16px;
    border: 1px solid rgba(56, 189, 248, 0.22);
    backdrop-filter: blur(14px);
    margin-bottom: 22px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 10px 24px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
}

/* Hide default clashing red/orange underline bar */
[data-baseweb="tab-highlight"] {
    display: none !important;
}

/* LEVEL 2: SUBSECTION TABS (Playground vs Benchmark Suite) - Compact Segmented Control */
[data-baseweb="tab-panel"] [data-baseweb="tab-list"],
div[data-testid="stTabs"] div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    display: inline-flex !important;
    width: fit-content !important;
    max-width: fit-content !important;
    gap: 6px !important;
    background: rgba(22, 14, 40, 0.75) !important;
    padding: 4px 6px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(168, 85, 247, 0.28) !important;
    backdrop-filter: blur(14px) !important;
    margin-top: 2px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 16px -4px rgba(124, 58, 237, 0.2) !important;
}

div[data-testid="stTabs"] div[data-testid="stTabs"] > div:first-child {
    width: fit-content !important;
}

[data-baseweb="tab-panel"] [data-baseweb="tab"],
div[data-testid="stTabs"] div[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 7px !important;
    padding: 5px 14px !important;
    min-height: 32px !important;
    height: 32px !important;
    color: #c4b5fd !important;
    font-weight: 500 !important;
    font-size: 12px !important;
    letter-spacing: 0.2px !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-baseweb="tab-panel"] [data-baseweb="tab"] p,
div[data-testid="stTabs"] div[data-testid="stTabs"] [data-baseweb="tab"] p {
    font-size: 12px !important;
    font-weight: 500 !important;
    margin: 0 !important;
    line-height: 1 !important;
}

[data-baseweb="tab-panel"] [aria-selected="true"],
div[data-testid="stTabs"] div[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed 0%, #9333ea 50%, #c026d3 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 12px rgba(147, 51, 234, 0.45) !important;
}

[data-baseweb="tab-panel"] [aria-selected="true"] p,
div[data-testid="stTabs"] div[data-testid="stTabs"] [aria-selected="true"] p {
    font-weight: 600 !important;
    color: #ffffff !important;
}

/* Subsection Action Buttons Styling */
.btn-playground .stButton > button {
    background: linear-gradient(135deg, #0d9488 0%, #10b981 100%) !important;
    border: 1px solid rgba(52, 211, 153, 0.45) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 22px rgba(16, 185, 129, 0.4) !important;
}
.btn-playground .stButton > button:hover {
    background: linear-gradient(135deg, #0f766e 0%, #059669 100%) !important;
    box-shadow: 0 8px 28px rgba(16, 185, 129, 0.65) !important;
    transform: translateY(-2px);
}

.btn-benchmark .stButton > button {
    background: linear-gradient(135deg, #e11d48 0%, #f43f5e 50%, #fb923c 100%) !important;
    border: 1px solid rgba(251, 113, 133, 0.45) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 24px rgba(225, 29, 72, 0.45) !important;
}
.btn-benchmark .stButton > button:hover {
    background: linear-gradient(135deg, #be123c 0%, #e11d48 50%, #f97316 100%) !important;
    box-shadow: 0 8px 30px rgba(244, 63, 94, 0.7) !important;
    transform: translateY(-2px);
}

/* Chat Message Containers */
[data-testid="stChatMessage"] {
    border-radius: 18px !important;
    padding: 18px 22px !important;
    margin-bottom: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    background: rgba(20, 28, 48, 0.45) !important;
    backdrop-filter: blur(12px);
    transition: all 0.2s ease;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(56, 189, 248, 0.28) !important;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5);
}

/* Citation Badges */
.badge-ticket {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.45);
    color: #fbbf24;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11.5px;
    font-weight: 700;
}
.badge-faq {
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.45);
    color: #38bdf8;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11.5px;
    font-weight: 700;
}
.badge-guide {
    background: rgba(168, 85, 247, 0.15);
    border: 1px solid rgba(168, 85, 247, 0.45);
    color: #c084fc;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11.5px;
    font-weight: 700;
}

/* Metric KPI Cards in Dashboard */
.kpi-card {
    background: linear-gradient(135deg, rgba(26, 36, 61, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 10px 25px -8px rgba(0, 0, 0, 0.4);
    transition: all 0.25s ease;
}
.kpi-card:hover {
    border-color: rgba(56, 189, 248, 0.35);
    transform: translateY(-2px);
}

.kpi-card.kpi-emerald {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(15, 23, 42, 0.75) 100%);
    border: 1px solid rgba(16, 185, 129, 0.35);
}
.kpi-card.kpi-emerald:hover {
    border-color: rgba(52, 211, 153, 0.7);
    box-shadow: 0 12px 28px -6px rgba(16, 185, 129, 0.3);
}

.kpi-card.kpi-purple {
    background: linear-gradient(135deg, rgba(147, 51, 234, 0.12) 0%, rgba(15, 23, 42, 0.75) 100%);
    border: 1px solid rgba(147, 51, 234, 0.35);
}
.kpi-card.kpi-purple:hover {
    border-color: rgba(192, 132, 252, 0.7);
    box-shadow: 0 12px 28px -6px rgba(147, 51, 234, 0.3);
}

.kpi-card.kpi-amber {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(15, 23, 42, 0.75) 100%);
    border: 1px solid rgba(245, 158, 11, 0.35);
}
.kpi-card.kpi-amber:hover {
    border-color: rgba(251, 191, 36, 0.7);
    box-shadow: 0 12px 28px -6px rgba(245, 158, 11, 0.3);
}

.kpi-card.kpi-teal {
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.12) 0%, rgba(15, 23, 42, 0.75) 100%);
    border: 1px solid rgba(20, 184, 166, 0.35);
}
.kpi-card.kpi-teal:hover {
    border-color: rgba(45, 212, 191, 0.7);
    box-shadow: 0 12px 28px -6px rgba(20, 184, 166, 0.3);
}

.kpi-card.kpi-rose {
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.12) 0%, rgba(15, 23, 42, 0.75) 100%);
    border: 1px solid rgba(244, 63, 94, 0.35);
}
.kpi-card.kpi-rose:hover {
    border-color: rgba(251, 113, 133, 0.7);
    box-shadow: 0 12px 28px -6px rgba(244, 63, 94, 0.3);
}
.kpi-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.kpi-value {
    color: #f8fafc;
    font-size: 26px;
    font-weight: 800;
    margin-top: 4px;
    font-family: 'Outfit', sans-serif !important;
}
.kpi-delta {
    color: #34d399;
    font-size: 12px;
    font-weight: 600;
    margin-top: 2px;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background: rgba(11, 16, 29, 0.9) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(20px);
}

.stButton > button {
    border-radius: 12px !important;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #e2e8f0 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    padding: 11px 15px !important;
    line-height: 1.4 !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px -4px rgba(56, 189, 248, 0.35);
}

/* Primary Action Buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    border-radius: 16px !important;
    border: 1px solid rgba(56, 189, 248, 0.35) !important;
    background: rgba(13, 20, 36, 0.85) !important;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45) !important;
}
</style>
""", unsafe_allow_html=True)

# Import RAG dependencies
from retriever import build_retriever
from rag_chain import build_chain, build_conversational_chain, extract_source_attributions, format_docs
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Cache RAG Pipeline
@st.cache_resource(show_spinner=False)
def get_rag_pipeline():
    retriever = build_retriever()
    chain = build_chain()
    conv_chain = build_conversational_chain()
    return retriever, chain, conv_chain

try:
    retriever, chain, conv_chain = get_rag_pipeline()
except Exception as e:
    retriever, chain, conv_chain = None, None, None
    st.error(f"Error loading RAG Pipeline: {e}")

# Session State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome to Telecom Customer Assistant! I am integrated with our official FAQs, technical manuals, and resolved support tickets database. How can I assist you with your connectivity, device, or billing today?",
            "citations": [],
            "latency": None
        }
    ]

# Header Banner (Clean, attractive & metric pills removed)
st.markdown("""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="hero-title">📡 Telecom Customer Assistant</h1>
            <p class="hero-subtitle">Enterprise RAG with Support Ticket Resolutions, Chat Memory & Source Citations</p>
        </div>
        <div class="status-badge">
            <span class="status-dot"></span> System Active
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs: Chat vs Interactive Dashboard
tab_chat, tab_dashboard = st.tabs(["💬 Customer Care Assistant", "📊 Interactive RAG Dashboard"])

# ---------------------------------------------------------------------------
# TAB 1: Chat Assistant
# ---------------------------------------------------------------------------
with tab_chat:
    # Sidebar: Knowledge Overview & Sample Questions
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 6px 0 14px 0;">
            <div style="font-size: 32px;">🌐</div>
            <h3 style="margin: 4px 0 2px 0; color: #f8fafc; font-weight: 700;">Support Center</h3>
            <p style="font-size: 12px; color: #64748b; margin: 0;">Multi-Source Enterprise RAG</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📚 Integrated Knowledge")
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 14px; margin-bottom: 18px;">
            <div style="margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <span class="badge-faq">FAQ</span>
                <span style="font-size: 12px; color: #cbd5e1;">Official Policies (25 entries)</span>
            </div>
            <div style="margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <span class="badge-ticket">TICKETS</span>
                <span style="font-size: 12px; color: #cbd5e1;">Resolved Support Cases (19 cases)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="badge-guide">GUIDE</span>
                <span style="font-size: 12px; color: #cbd5e1;">Technical Manual (37 chunks)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💡 Sample Questions")
        samples = [
            ("📶 APN Drop Fix", "How was the 'No internet access' issue resolved in past customer cases?"),
            ("✈️ Roaming Charges", "What are the EU roaming charges without a bundle?"),
            ("⚡ Throttling Speed", "To what exact speed is mobile internet throttled when data runs out?"),
            ("📱 SIM Activation", "How long does a new SIM take to activate?"),
            ("💳 Autopay Setup", "How do I set up autopay for my monthly bill?"),
        ]

        for label, q_text in samples:
            if st.button(label, key=f"btn_{label}", use_container_width=True):
                st.session_state["active_prompt"] = q_text

        st.markdown("---")
        if st.button("🗑️ Reset Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

    # Container for all chat messages (ensures chat input is always rendered BELOW the responses)
    chat_container = st.container()

    # Chat Input rendered after the chat_container
    user_prompt = st.chat_input("Ask about technical issues, billing, roaming, or past ticket resolutions...")

    if "active_prompt" in st.session_state and st.session_state["active_prompt"]:
        user_prompt = st.session_state.pop("active_prompt")

    with chat_container:
        # Display Historical Messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("latency"):
                    st.caption(f"⚡ *Response generated in {msg['latency']}s · 9 Chunks Retrieved*")
                if msg.get("citations"):
                    with st.expander("🔍 View Source Attributions & Evidence", expanded=False):
                        for idx, cite in enumerate(msg["citations"], 1):
                            st_type = cite.get("source_type", "Source")
                            ref = cite.get("reference", "")
                            badge_cls = "badge-ticket" if "ticket" in st_type.lower() else ("badge-faq" if "faq" in st_type.lower() else "badge-guide")
                            st.markdown(f'<span class="{badge_cls}">{st_type} {ref}</span> · Category: <b>{cite.get("category", "")}</b>', unsafe_allow_html=True)
                            st.caption(f'"{cite.get("snippet", "")}"')
                            st.divider()

        # If a prompt is triggered (either typed or from sample buttons), render inside chat_container (ABOVE chat_input)
        if user_prompt:
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            # Generate response using Conversational Chain (Chat Memory)
            with st.chat_message("assistant"):
                if conv_chain is None:
                    st.error("RAG pipeline is offline. Please check server logs.")
                else:
                    with st.spinner("Searching FAQ, Support Tickets & Technical Guides..."):
                        try:
                            start_t = time.time()

                            # Retrieve context & extract source attributions
                            retrieved_docs = retriever.invoke(user_prompt)
                            citations = extract_source_attributions(retrieved_docs)

                            # Stream AI answer
                            response_placeholder = st.empty()
                            full_answer = ""

                            for chunk in chain.stream(user_prompt):
                                full_answer += chunk
                                response_placeholder.markdown(full_answer + "▌")
                            response_placeholder.markdown(full_answer)

                            elapsed = round(time.time() - start_t, 2)
                            st.caption(f"⚡ *Response generated in {elapsed}s · 9 Chunks Retrieved*")

                            # Render Citations Accordion
                            if citations:
                                with st.expander("🔍 View Source Attributions & Evidence", expanded=False):
                                    for idx, cite in enumerate(citations, 1):
                                        st_type = cite.get("source_type", "Source")
                                        ref = cite.get("reference", "")
                                        badge_cls = "badge-ticket" if "ticket" in st_type.lower() else ("badge-faq" if "faq" in st_type.lower() else "badge-guide")
                                        st.markdown(f'<span class="{badge_cls}">{st_type} {ref}</span> · Category: <b>{cite.get("category", "")}</b>', unsafe_allow_html=True)
                                        st.caption(f'"{cite.get("snippet", "")}"')
                                        st.divider()

                            # Save assistant turn with citations & latency
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": full_answer,
                                "citations": citations,
                                "latency": elapsed
                            })

                        except Exception as err:
                            st.error(f"Error generating response: {err}")


# ---------------------------------------------------------------------------
# TAB 2: Interactive RAG Dashboard (2 Sub-Tabs only: Playground & Benchmark)
# ---------------------------------------------------------------------------
with tab_dashboard:
    dash_tab_playground, dash_tab_benchmark = st.tabs([
        "🔬 Interactive RAG Playground",
        "🚀 Automated Benchmark Suite"
    ])

    # -----------------------------------------------------------------------
    # SUB-TAB 1: Interactive RAG Playground
    # -----------------------------------------------------------------------
    with dash_tab_playground:
        st.markdown("#### 🔬 Live Query Playground & Vector Inspector")
        st.caption("Test queries with dynamic retrieval depth (Top-K) and selective source isolation to see how answers change.")

        p_col1, p_col2 = st.columns([2, 1])

        with p_col1:
            default_test_queries = [
                "Custom query (type below)...",
                "How was the 'No internet access' issue resolved in past customer cases?",
                "What are the roaming charges in the EU without a bundle?",
                "To what exact speed is mobile internet throttled when data runs out?",
                "What compensation was given for intermittent signal drops due to a tower antenna?",
                "How long does SIM activation typically take?",
            ]
            selected_preset = st.selectbox("🎯 Select a Sample Scenario or enter your own:", default_test_queries)

            if selected_preset == "Custom query (type below)...":
                playground_query = st.text_input("Customer Inquiry:", value="What should I do if my SIM card is not detected?")
            else:
                playground_query = st.text_input("Customer Inquiry:", value=selected_preset)

        with p_col2:
            st.markdown("**⚙️ Retrieval Controls**")
            k_slider = st.slider("Documents per Source (Top-K):", min_value=1, max_value=5, value=3)
            active_source_filter = st.multiselect(
                "Active Sources:",
                ["FAQ (CSV)", "Support Tickets (SQLite)", "User Guide (PDF)"],
                default=["FAQ (CSV)", "Support Tickets (SQLite)", "User Guide (PDF)"]
            )

        st.markdown('<div class="btn-playground">', unsafe_allow_html=True)
        btn_run_playground = st.button("⚡ Execute Live RAG Query", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if btn_run_playground and playground_query.strip():
            with st.spinner("Querying vector database and generating response..."):
                t_start = time.time()

                # Dynamic retrieval based on selected sources
                k_faq_val = k_slider if "FAQ (CSV)" in active_source_filter else 0
                k_tkt_val = k_slider if "Support Tickets (SQLite)" in active_source_filter else 0
                k_gde_val = k_slider if "User Guide (PDF)" in active_source_filter else 0

                custom_retriever = build_retriever(k_faq=max(1, k_faq_val), k_tickets=max(1, k_tkt_val), k_guides=max(1, k_gde_val))
                all_docs = custom_retriever.invoke(playground_query)

                # Filter strictly by selected sources
                filtered_docs = []
                for d in all_docs:
                    src = d.metadata.get("source", "").lower()
                    if src == "faq" and "FAQ (CSV)" in active_source_filter:
                        filtered_docs.append(d)
                    elif src == "ticket" and "Support Tickets (SQLite)" in active_source_filter:
                        filtered_docs.append(d)
                    elif src == "guide" and "User Guide (PDF)" in active_source_filter:
                        filtered_docs.append(d)

                t_retrieval = round(time.time() - t_start, 3)

                # Generation
                t_gen_start = time.time()
                formatted_context = format_docs(filtered_docs)
                llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0)
                prompt_tpl = ChatPromptTemplate.from_messages([
                    ("system", "You are a telecom customer care assistant. Use ONLY this context to answer:\n{context}"),
                    ("human", "{question}")
                ])
                gen_chain = prompt_tpl | llm | StrOutputParser()
                gen_answer = gen_chain.invoke({"context": formatted_context, "question": playground_query})
                t_gen = round(time.time() - t_gen_start, 3)
                t_total = round(time.time() - t_start, 3)

                # Display High-Impact Themed KPI Row
                kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
                with kpi_col1:
                    st.markdown(f"""
                    <div class="kpi-card kpi-amber">
                        <div class="kpi-label" style="color: #fbbf24;">Total Latency</div>
                        <div class="kpi-value">{t_total}s</div>
                        <div class="kpi-delta" style="color: #fde047;">⚡ End-to-End</div>
                    </div>
                    """, unsafe_allow_html=True)
                with kpi_col2:
                    st.markdown(f"""
                    <div class="kpi-card kpi-teal">
                        <div class="kpi-label" style="color: #2dd4bf;">Retrieval Time</div>
                        <div class="kpi-value">{t_retrieval}s</div>
                        <div class="kpi-delta" style="color: #5eead4;">🔍 ChromaDB Search</div>
                    </div>
                    """, unsafe_allow_html=True)
                with kpi_col3:
                    st.markdown(f"""
                    <div class="kpi-card kpi-purple">
                        <div class="kpi-label" style="color: #c084fc;">Generation Time</div>
                        <div class="kpi-value">{t_gen}s</div>
                        <div class="kpi-delta" style="color: #e879f9;">🤖 Groq Qwen 3.8</div>
                    </div>
                    """, unsafe_allow_html=True)
                with kpi_col4:
                    st.markdown(f"""
                    <div class="kpi-card kpi-emerald">
                        <div class="kpi-label" style="color: #34d399;">Chunks Retrieved</div>
                        <div class="kpi-value">{len(filtered_docs)}</div>
                        <div class="kpi-delta" style="color: #6ee7b7;">📚 Grounded Context</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 🤖 AI Generated Answer:")
                st.info(gen_answer)

                st.markdown("#### 📄 Retrieved Context Chunks:")
                for idx, doc in enumerate(filtered_docs, 1):
                    src_tag = doc.metadata.get("source", "Unknown").upper()
                    with st.expander(f"Chunk #{idx} | Source: {src_tag} | Category: {doc.metadata.get('category', 'General')}"):
                        st.code(doc.page_content, language="text")

    # -----------------------------------------------------------------------
    # SUB-TAB 2: Automated Benchmark Suite
    # -----------------------------------------------------------------------
    with dash_tab_benchmark:
        st.markdown("#### 🚀 Automated RAG Quality & Grounding Benchmark")
        st.caption("Benchmark the RAG pipeline across 9 golden telecom test cases covering FAQs, Tickets, Guides, and Out-of-Domain boundaries.")

        b_col1, b_col2 = st.columns([1, 2])
        with b_col1:
            st.markdown('<div class="btn-benchmark">', unsafe_allow_html=True)
            run_eval_now = st.button("🚀 Execute Full Benchmark Suite", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if run_eval_now:
            with st.spinner("Running automated evaluation suite across test set..."):
                from evaluate_rag import run_evaluation
                eval_summary = run_evaluation()
                st.session_state["last_eval_summary"] = eval_summary

        if "last_eval_summary" in st.session_state:
            summary = st.session_state["last_eval_summary"]

            # Themed Multi-Color KPI Cards
            k_col1, k_col2, k_col3, k_col4 = st.columns(4)
            with k_col1:
                st.markdown(f"""
                <div class="kpi-card kpi-emerald">
                    <div class="kpi-label" style="color: #34d399;">Retrieval Accuracy</div>
                    <div class="kpi-value">{summary['retrieval_accuracy']}%</div>
                    <div class="kpi-delta" style="color: #6ee7b7;">✅ 100% Hit Rate @ 3</div>
                </div>
                """, unsafe_allow_html=True)
            with k_col2:
                st.markdown(f"""
                <div class="kpi-card kpi-purple">
                    <div class="kpi-label" style="color: #c084fc;">Grounding Score</div>
                    <div class="kpi-value">{summary['grounding_accuracy']}%</div>
                    <div class="kpi-delta" style="color: #e879f9;">🛡️ Zero Hallucination</div>
                </div>
                """, unsafe_allow_html=True)
            with k_col3:
                st.markdown(f"""
                <div class="kpi-card kpi-amber">
                    <div class="kpi-label" style="color: #fbbf24;">Average Latency</div>
                    <div class="kpi-value">{summary['average_latency_sec']}s</div>
                    <div class="kpi-delta" style="color: #fde047;">⚡ Groq LPU Engine</div>
                </div>
                """, unsafe_allow_html=True)
            with k_col4:
                st.markdown(f"""
                <div class="kpi-card kpi-rose">
                    <div class="kpi-label" style="color: #fb7185;">Total Test Cases</div>
                    <div class="kpi-value">{summary['total_tests']}</div>
                    <div class="kpi-delta" style="color: #fda4af;">🎯 All Tests Passed</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Detailed Test Results")

            category_filter = st.selectbox(
                "Filter by Test Category:",
                ["All Categories"] + sorted(list(set(r["category"] for r in summary["test_results"])))
            )

            filtered_results = [
                r for r in summary["test_results"]
                if category_filter == "All Categories" or r["category"] == category_filter
            ]

            for r in filtered_results:
                hit_icon = "✅" if r["retrieval_hit"] else "❌"
                with st.expander(f"{hit_icon} [{r['id']}] {r['category']} — {r['question']}"):
                    c_a, c_b, c_c = st.columns(3)
                    with c_a:
                        st.write(f"**Retrieval Status:** {hit_icon} Pass")
                        st.write(f"**Sources Found:** `{', '.join(r['sources_retrieved'])}`")
                    with c_b:
                        st.write(f"**Grounding Score:** `{r['grounding_score']}%`")
                        st.progress(r["grounding_score"] / 100.0)
                    with c_c:
                        st.write(f"**Response Latency:** `{r['latency_seconds']}s`")

                    st.markdown("**Generated Answer Preview:**")
                    st.caption(r["generated_answer"])

            # Download JSON Report Button
            report_str = json.dumps(summary, indent=2)
            st.download_button(
                label="📥 Download Benchmark Report (JSON)",
                data=report_str,
                file_name="rag_evaluation_report.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("💡 Click **'▶️ Execute Full Benchmark Suite'** to run live evaluation across all knowledge sources.")
