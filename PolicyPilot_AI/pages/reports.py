import streamlit as st
import os
import pandas as pd
import plotly.express as px

def show_reports():
    st.markdown("## 📄 Reports Center")

    tab1, tab2 = st.tabs(["📂 Saved Reports", "📊 Analytics Reports"])

    with tab1:
        st.markdown("### 📁 Generated Risk Reports")
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)

        report_files = [f for f in os.listdir(reports_dir) if f.endswith(('.txt', '.pdf'))]

        if not report_files:
            st.info("📭 No reports generated yet. Run a fraud analysis to generate reports.")
        else:
            st.success(f"✅ Found {len(report_files)} report(s)")

            for report_file in sorted(report_files, reverse=True):
                report_path = os.path.join(reports_dir, report_file)
                file_size = os.path.getsize(report_path) / 1024

                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    icon = "📄" if report_file.endswith('.txt') else "📋"
                    st.markdown(f"{icon} **{report_file}**")
                    st.caption(f"Size: {file_size:.1f} KB")
                with col2:
                    with open(report_path, "rb") as f:
                        mime = "text/plain" if report_file.endswith('.txt') else "application/pdf"
                        st.download_button(
                            "⬇️ Download",
                            data=f.read(),
                            file_name=report_file,
                            mime=mime,
                            key=f"dl_{report_file}"
                        )
                with col3:
                    if report_file.endswith('.txt'):
                        if st.button("👁️ View", key=f"view_{report_file}"):
                            with open(report_path, "r", encoding="utf-8") as f:
                                content = f.read()
                            st.text_area("Report Content", content, height=400)
                st.markdown("---")

    with tab2:
        st.markdown("### 📊 Claims Analytics Reports")
        try:
            df = pd.read_csv("claims.csv")

            st.markdown("#### 💰 Financial Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Claimed", f"₹{df['claim_amount'].sum():,.0f}")
            with col2:
                approved_df = df[df['status'] == 'Approved']
                st.metric("Total Approved", f"₹{approved_df['claim_amount'].sum():,.0f}")
            with col3:
                fraud_df = df[df['status'] == 'Fraudulent']
                st.metric("Fraud Amount", f"₹{fraud_df['claim_amount'].sum():,.0f}")
            with col4:
                st.metric("Avg Claim", f"₹{df['claim_amount'].mean():,.0f}")

            col_l, col_r = st.columns(2)
            with col_l:
                agent_claims = df.groupby("submitted_by").agg(
                    count=("claim_id", "count"),
                    total_amount=("claim_amount", "sum")
                ).reset_index()
                fig_agent = px.bar(
                    agent_claims, x="submitted_by", y="count",
                    title="📊 Claims by Agent",
                    color="count",
                    color_continuous_scale="Blues"
                )
                fig_agent.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                st.plotly_chart(fig_agent, use_container_width=True)

            with col_r:
                if "risk_level" in df.columns:
                    risk_amount = df.groupby("risk_level")["claim_amount"].sum().reset_index()
                    fig_risk = px.pie(
                        risk_amount, values="claim_amount", names="risk_level",
                        title="💰 Amount by Risk Level",
                        color="risk_level",
                        color_discrete_map={"Low": "#00ff88", "Medium": "#ffaa00", "High": "#ff4444"},
                        hole=0.3
                    )
                    fig_risk.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig_risk, use_container_width=True)

            st.markdown("#### 📋 Full Claims Report")
            export_df = df[["claim_id", "customer_name", "claim_amount", "status", "risk_level", "fraud_score", "submitted_date"]].copy()
            export_df["claim_amount"] = export_df["claim_amount"].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(export_df, use_container_width=True, hide_index=True)

            csv_data = df.to_csv(index=False)
            st.download_button(
                "📥 Export Full Report (CSV)",
                data=csv_data,
                file_name="policypilot_claims_report.csv",
                mime="text/csv",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Error generating analytics: {e}")
