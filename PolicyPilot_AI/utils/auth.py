import pandas as pd
import streamlit as st
import os

USERS_FILE = "users.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=["username", "password", "role", "full_name", "email"])

def verify_login(username, password):
    users = load_users()
    user = users[(users["username"] == username) & (users["password"] == password)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def is_logged_in():
    return st.session_state.get("logged_in", False)

def get_current_user():
    return st.session_state.get("user", {})

def is_admin():
    user = get_current_user()
    return user.get("role") == "admin"

def logout():
    for key in ["logged_in", "user"]:
        if key in st.session_state:
            del st.session_state[key]

def login_page():
    st.markdown("""
    <style>
    .login-container {
        max-width: 420px;
        margin: 80px auto;
        padding: 40px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .login-title {
        text-align: center;
        color: #00d4ff;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .login-subtitle {
        text-align: center;
        color: #a0a0b0;
        font-size: 14px;
        margin-bottom: 30px;
    }
    .login-logo {
        text-align: center;
        font-size: 60px;
        margin-bottom: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-logo">🛡️</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">PolicyPilot AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Insurance Claim Verification & Fraud Analysis</div>', unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)

            if submit:
                if username and password:
                    user = verify_login(username, password)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["user"] = user
                        st.success(f"✅ Welcome, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")

        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.code("Admin: admin / admin123\nAgent: agent1 / agent123")
