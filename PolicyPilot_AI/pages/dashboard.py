import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def show_dashboard():
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #00d4ff; }
    .metric-label { font-size: 0.85rem; color: #a0a0b0; margin-top: 5px; }
    .metric-icon { font-size: 2rem; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Claims Dashboard")

    try:
        df = pd.read_csv("claims.csv")
    except:
        st.error("❌ claims.csv not found")
        return

    total = len(df)
    approved = len(df[df["status"] == "Approved"])
    pending = len(df[df["status"] == "Pending"])
    fraudulent = len(df[df["status"] == "Fraudulent"])
    suspicious = len(df[df["status"] == "Suspicious"])

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-value">{total}</div>
            <div class="metric-label">Total Claims</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">✅</div>
            <div class="metric-value" style="color:#00ff88">{approved}</div>
            <div class="metric-label">Approved</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">⏳</div>
            <div class="metric-value" style="color:#ffaa00">{pending}</div>
            <div class="metric-label">Pending</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">🚨</div>
            <div class="metric-value" style="color:#ff4444">{fraudulent}</div>
            <div class="metric-label">Fraudulent</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">⚠️</div>
            <div class="metric-value" style="color:#ff8800">{suspicious}</div>
            <div class="metric-label">Suspicious</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        status_counts = df["status"].value_counts()
        colors = {"Approved": "#00ff88", "Pending": "#ffaa00",
                  "Fraudulent": "#ff4444", "Suspicious": "#ff8800"}
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="📊 Claim Status Distribution",
            color=status_counts.index,
            color_discrete_map=colors,
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font=dict(size=16, color='#00d4ff')
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        if "risk_level" in df.columns:
            risk_counts = df["risk_level"].value_counts()
            fig_bar = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                title="🎯 Risk Level Distribution",
                color=risk_counts.index,
                color_discrete_map={"Low": "#00ff88", "Medium": "#ffaa00", "High": "#ff4444"},
                labels={"x": "Risk Level", "y": "Number of Claims"}
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(size=16, color='#00d4ff'),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        if "fraud_score" in df.columns:
            fig_hist = px.histogram(
                df, x="fraud_score",
                title="📈 Fraud Score Distribution",
                nbins=10,
                color_discrete_sequence=["#00d4ff"]
            )
            fig_hist.add_vline(x=40, line_dash="dash", line_color="orange",
                              annotation_text="Suspicious Threshold")
            fig_hist.add_vline(x=70, line_dash="dash", line_color="red",
                              annotation_text="Fraud Threshold")
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(size=16, color='#00d4ff')
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    with col4:
        if "claim_amount" in df.columns:
            fig_box = px.box(
                df, x="status", y="claim_amount",
                title="💰 Claim Amount by Status",
                color="status",
                color_discrete_map={
                    "Approved": "#00ff88", "Pending": "#ffaa00",
                    "Fraudulent": "#ff4444", "Suspicious": "#ff8800"
                }
            )
            fig_box.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font=dict(size=16, color='#00d4ff'),
                showlegend=False
            )
            st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("### 📋 Recent Claims")
    display_df = df.tail(5)[["claim_id", "customer_name", "claim_amount", "status", "risk_level"]].copy()
    display_df["claim_amount"] = display_df["claim_amount"].apply(lambda x: f"₹{x:,.0f}")

    def style_status(val):
        colors_map = {
            "Approved": "color: #00ff88; font-weight: bold",
            "Pending": "color: #ffaa00; font-weight: bold",
            "Fraudulent": "color: #ff4444; font-weight: bold",
            "Suspicious": "color: #ff8800; font-weight: bold",
        }
        return colors_map.get(val, "")

    st.dataframe(
        display_df.style.applymap(style_status, subset=["status"]),
        use_container_width=True,
        hide_index=True
    )
