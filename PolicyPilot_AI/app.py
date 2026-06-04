import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="PolicyPilot AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp { background: #0a0a1a; color: #e0e0f0; }
    .stSidebar { background: linear-gradient(180deg, #0d0d1f 0%, #1a1a3e 100%) !important; }
    .stSidebar .stMarkdown { color: #c0c0d0; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #0066ff);
        color: white; border: none; border-radius: 10px;
        font-weight: 600; padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,212,255,0.4);
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: #1a1a2e !important;
        color: #e0e0f0 !important;
        border: 1px solid rgba(0,212,255,0.3) !important;
        border-radius: 10px !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 15px; padding: 15px; margin: 5px;
    }
    [data-testid="stMetricValue"] { color: #00d4ff !important; font-weight: 800; }

    /* Sidebar nav */
    .nav-item {
        display: flex; align-items: center; gap: 12px;
        padding: 12px 15px; border-radius: 12px; margin: 4px 0;
        color: #a0a0c0; cursor: pointer; transition: all 0.3s;
        text-decoration: none;
    }
    .nav-item:hover, .nav-item.active {
        background: rgba(0,212,255,0.1);
        color: #00d4ff;
        border-left: 3px solid #00d4ff;
    }

    /* Tables */
    .dataframe { border-radius: 10px !important; overflow: hidden; }

    /* Hide default streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1a1a2e, #16213e) !important;
        border-radius: 10px !important; color: #00d4ff !important;
    }

    /* Forms */
    [data-testid="stForm"] {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid rgba(0,212,255,0.15);
        border-radius: 15px; padding: 20px;
    }

    /* Alerts */
    .stSuccess { border-radius: 10px; }
    .stError { border-radius: 10px; }
    .stWarning { border-radius: 10px; }
    .stInfo { border-radius: 10px; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a2e; border-radius: 10px; padding: 5px;
    }
    .stTabs [data-baseweb="tab"] { color: #a0a0c0; border-radius: 8px; }
    .stTabs [aria-selected="true"] {
        background: rgba(0,212,255,0.15) !important;
        color: #00d4ff !important;
    }

    /* Upload */
    [data-testid="stFileUploader"] {
        background: #1a1a2e; border: 2px dashed rgba(0,212,255,0.3);
        border-radius: 15px;
    }

    /* Number inputs */
    .stNumberInput > div > div > input {
        background: #1a1a2e !important;
        color: #e0e0f0 !important;
        border: 1px solid rgba(0,212,255,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Ensure folders exist
for folder in ["uploads", "reports", "models", "dataset"]:
    os.makedirs(folder, exist_ok=True)

# Init session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

# Import auth
from utils.auth import login_page, is_logged_in, get_current_user, logout, is_admin

# Show login if not authenticated
if not is_logged_in():
    login_page()
    st.stop()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
user = get_current_user()

with st.sidebar:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0f3460, #1a1a2e);
         border: 1px solid rgba(0,212,255,0.2); border-radius: 15px; padding: 20px; margin-bottom: 20px;">
        <div style="font-size: 2.5rem; text-align: center; margin-bottom: 10px;">🛡️</div>
        <div style="color: #00d4ff; font-weight: 700; font-size: 1.2rem; text-align: center;">PolicyPilot AI</div>
        <div style="color: #a0a0b0; font-size: 0.75rem; text-align: center;">Insurance Fraud Detection</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: rgba(0,212,255,0.05); border: 1px solid rgba(0,212,255,0.15);
         border-radius: 10px; padding: 12px; margin-bottom: 15px;">
        <div style="color: #00d4ff; font-weight: 600;">👤 {user.get('full_name', 'User')}</div>
        <div style="color: #a0a0b0; font-size: 0.8rem;">
            {'🔴 Admin' if is_admin() else '🔵 Agent'} | {user.get('username', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")

    pages = [
        ("📊", "Dashboard"),
        ("📝", "Submit Claim"),
        ("🔍", "Fraud Detection"),
        ("📄", "Reports"),
        ("🤖", "AI Chatbot"),
    ]
    if is_admin():
        pages.append(("🛠️", "Admin Panel"))

    for icon, page_name in pages:
        is_active = st.session_state["page"] == page_name
        btn_style = "primary" if is_active else "secondary"

        if st.button(
            f"{icon} {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type=btn_style
        ):
            st.session_state["page"] = page_name
            st.rerun()

    st.markdown("---")

    try:
        df = pd.read_csv("claims.csv")
        total_claims = len(df)
        fraud_count = len(df[df['status'] == 'Fraudulent'])
    except:
        total_claims, fraud_count = 0, 0

    st.markdown(f"""
    <div style="background: rgba(0,0,0,0.2); border-radius: 10px; padding: 12px; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #a0a0b0; font-size: 0.8rem;">Total Claims</span>
            <span style="color: #00d4ff; font-weight: 600;">{total_claims}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #a0a0b0; font-size: 0.8rem;">Fraud Detected</span>
            <span style="color: #ff4444; font-weight: 600;">{fraud_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

    st.markdown("""
    <div style="text-align: center; color: #404060; font-size: 0.7rem; margin-top: 20px;">
        PolicyPilot AI v1.0<br>Powered by ML + Gemini AI
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
import pandas as pd

current_page = st.session_state["page"]

if current_page == "Dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()

elif current_page == "Submit Claim":
    from pages.submit_claim import show_submit_claim
    show_submit_claim()

elif current_page == "Fraud Detection":
    from pages.fraud_detection import show_fraud_detection
    show_fraud_detection()

elif current_page == "Reports":
    from pages.reports import show_reports
    show_reports()

elif current_page == "AI Chatbot":
    from pages.chatbot import show_chatbot
    show_chatbot()

elif current_page == "Admin Panel":
    from pages.admin_panel import show_admin_panel
    show_admin_panel()
