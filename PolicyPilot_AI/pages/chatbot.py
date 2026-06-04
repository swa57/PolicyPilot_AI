import streamlit as st
from utils.gemini_chat import get_gemini_response, get_claim_analysis_prompt

def show_chatbot():
    st.markdown("## 🤖 PolicyPilot AI Chatbot")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
         border: 1px solid rgba(0,212,255,0.3); border-radius: 15px; padding: 20px; margin-bottom: 20px;">
        <h4 style="color: #00d4ff; margin: 0 0 10px 0;">🧠 Powered by Google Gemini AI</h4>
        <p style="color: #a0a0b0; margin: 0; font-size: 0.9rem;">
        Ask me anything about insurance claims, fraud indicators, or claim analysis.
        I can explain suspicious patterns, summarize documents, and help with insurance-related questions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("### 💬 Quick Prompts")
    quick_col = st.columns(4)
    quick_prompts = [
        "Explain fraud indicators",
        "How to verify a claim?",
        "What makes a claim suspicious?",
        "Explain the fraud score"
    ]
    for i, prompt in enumerate(quick_prompts):
        with quick_col[i]:
            if st.button(f"💡 {prompt}", use_container_width=True, key=f"qp_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.spinner("🤖 Thinking..."):
                    response = get_gemini_response(prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

    st.markdown("---")
    st.markdown("### 💬 Chat")

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                    <div style="background: #0f3460; color: white; border-radius: 15px 15px 0 15px;
                         padding: 12px 18px; max-width: 70%; font-size: 0.9rem;">
                        👤 {msg['content']}
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                         border: 1px solid rgba(0,212,255,0.2);
                         color: #e0e0e0; border-radius: 15px 15px 15px 0;
                         padding: 12px 18px; max-width: 75%; font-size: 0.9rem;">
                        🤖 {msg['content']}
                    </div>
                </div>""", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your Message",
            placeholder="Ask about claims, fraud detection, or insurance...",
            height=80,
            label_visibility="collapsed"
        )
        col_send, col_clear = st.columns([4, 1])
        with col_send:
            send = st.form_submit_button("📤 Send Message", use_container_width=True, type="primary")
        with col_clear:
            clear = st.form_submit_button("🗑️ Clear", use_container_width=True)

        if send and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("🤖 Generating response..."):
                response = get_gemini_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

        if clear:
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Analyze Specific Claim with AI")
    try:
        import pandas as pd
        df = pd.read_csv("claims.csv")
        selected = st.selectbox("Select a claim to analyze with AI:", df["claim_id"].tolist())
        if selected and st.button("🤖 Get AI Analysis for This Claim", use_container_width=True):
            claim_row = df[df["claim_id"] == selected].iloc[0]
            claim_data = claim_row.to_dict()
            fraud_result = {
                "fraud_probability": claim_row.get("fraud_score", 0),
                "risk_level": claim_row.get("risk_level", "Unknown"),
                "risk_label": claim_row.get("status", "Unknown")
            }
            from utils.fraud_utils import get_fraud_indicators, calculate_fraud_features
            indicators = ["No detailed indicators available for historical claims"]
            prompt = get_claim_analysis_prompt(claim_data, fraud_result, indicators)
            with st.spinner("🤖 Analyzing claim with AI..."):
                response = get_gemini_response(prompt)
            st.markdown("#### 🤖 AI Analysis:")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                 border: 1px solid rgba(0,212,255,0.2); border-radius: 15px; padding: 20px;">
                <p style="color: #e0e0e0;">{response}</p>
            </div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")
