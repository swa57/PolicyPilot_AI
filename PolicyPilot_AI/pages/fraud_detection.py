import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.fraud_utils import calculate_fraud_features, predict_fraud, get_fraud_indicators, check_duplicate_claims
from utils.report_generator import generate_risk_report, save_report, generate_pdf_report

def show_fraud_detection():
    st.markdown("## 🔍 AI Fraud Detection Analysis")

    tab1, tab2 = st.tabs(["🎯 Analyze Claim", "📋 Analyze Existing Claim"])

    with tab1:
        st.markdown("### Enter Claim Details for Fraud Analysis")
        col1, col2 = st.columns(2)

        with col1:
            claim_id_input = st.text_input("🆔 Claim ID", value="CLM-TEST-001")
            customer_name = st.text_input("👤 Customer Name", value="Test Customer")
            claim_amount = st.number_input("💰 Claim Amount (₹)", min_value=1000.0, value=100000.0, step=5000.0)
            hospital_name = st.text_input("🏥 Hospital Name", value="Apollo Hospital")
            claim_description = st.text_area("📝 Description", value="Treatment for accident injury")

        with col2:
            claim_frequency = st.slider("📊 Claim Frequency (this year)", 1, 10, 1)
            num_previous_claims = st.slider("📋 Previous Claims Count", 0, 10, 0)
            days_since_policy = st.number_input("📅 Days Since Policy Start", min_value=1, value=365)
            incident_to_claim_days = st.slider("⏱️ Days from Incident to Claim", 1, 30, 5)

            col_a, col_b = st.columns(2)
            with col_a:
                duplicate_claim = st.checkbox("🔄 Possible Duplicate?")
                policy_expired = st.checkbox("❌ Policy Expired?")
            with col_b:
                suspicious_keywords_flag = st.checkbox("⚠️ Suspicious Terms?")

        if st.button("🤖 Run AI Fraud Analysis", use_container_width=True, type="primary"):
            with st.spinner("🔍 Running AI analysis..."):
                is_dup, dup_count = check_duplicate_claims(claim_id_input, customer_name, claim_amount)
                if is_dup:
                    st.warning(f"⚠️ Found {dup_count} similar claim(s) in database!")
                    duplicate_claim = True

                features = calculate_fraud_features(
                    claim_amount=claim_amount,
                    claim_frequency=claim_frequency,
                    duplicate_claim=duplicate_claim,
                    has_suspicious_keywords=suspicious_keywords_flag,
                    policy_expired=policy_expired,
                    days_since_policy=days_since_policy,
                    num_previous_claims=num_previous_claims,
                    incident_to_claim_days=incident_to_claim_days
                )

                result = predict_fraud(features)
                indicators = get_fraud_indicators(features, result["fraud_probability"])

                st.markdown("---")
                st.markdown("### 📊 Analysis Results")

                fraud_prob = result["fraud_probability"]
                risk_color = "#ff4444" if fraud_prob >= 70 else "#ff8800" if fraud_prob >= 40 else "#00ff88"

                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                         border: 2px solid {risk_color}; border-radius: 15px; padding: 20px; text-align: center;">
                        <div style="font-size: 3rem; font-weight: 800; color: {risk_color};">{fraud_prob:.1f}%</div>
                        <div style="color: #a0a0b0; font-size: 0.9rem;">Fraud Probability</div>
                    </div>""", unsafe_allow_html=True)

                with col_r2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                         border: 1px solid rgba(0,212,255,0.3); border-radius: 15px; padding: 20px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #00d4ff; margin-top: 10px;">{result['risk_label']}</div>
                        <div style="color: #a0a0b0; font-size: 0.9rem; margin-top: 5px;">ML Prediction</div>
                    </div>""", unsafe_allow_html=True)

                with col_r3:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                         border: 1px solid rgba(0,212,255,0.3); border-radius: 15px; padding: 20px; text-align: center;">
                        <div style="font-size: 3rem; font-weight: 800; color: #00d4ff;">{result['confidence_score']:.0f}%</div>
                        <div style="color: #a0a0b0; font-size: 0.9rem;">Confidence Score</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=fraud_prob,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Fraud Risk Gauge", 'font': {'color': 'white', 'size': 18}},
                    delta={'reference': 40, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': "white"},
                        'bar': {'color': risk_color},
                        'bgcolor': "rgba(0,0,0,0)",
                        'bordercolor': "rgba(255,255,255,0.2)",
                        'steps': [
                            {'range': [0, 40], 'color': 'rgba(0,255,136,0.1)'},
                            {'range': [40, 70], 'color': 'rgba(255,170,0,0.1)'},
                            {'range': [70, 100], 'color': 'rgba(255,68,68,0.1)'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': 'white'},
                    height=300
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

                st.markdown("### ⚠️ Fraud Indicators")
                for indicator in indicators:
                    if "✅" in indicator:
                        st.success(indicator)
                    elif "🔴" in indicator or "❌" in indicator or "🔄" in indicator:
                        st.error(indicator)
                    else:
                        st.warning(indicator)

                claim_data = {
                    "claim_id": claim_id_input,
                    "policy_number": "N/A",
                    "customer_name": customer_name,
                    "claim_amount": claim_amount,
                    "hospital_name": hospital_name,
                    "incident_date": "N/A",
                    "claim_description": claim_description
                }

                report_text, decision = generate_risk_report(claim_data, result, indicators)
                report_path = save_report(report_text, claim_id_input)

                st.markdown("### 📄 Risk Report")
                with st.expander("View Full Report"):
                    st.text(report_text)

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        "📥 Download TXT Report",
                        data=report_text,
                        file_name=f"risk_report_{claim_id_input}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col_d2:
                    pdf_path = generate_pdf_report(report_text, claim_id_input)
                    if pdf_path and __import__('os').path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                "📥 Download PDF Report",
                                data=f.read(),
                                file_name=f"risk_report_{claim_id_input}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )

    with tab2:
        st.markdown("### Analyze Claims from Database")
        try:
            df = pd.read_csv("claims.csv")
            claim_options = df["claim_id"].tolist()
            selected_claim = st.selectbox("Select Claim to Analyze", claim_options)

            if selected_claim and st.button("🔍 Analyze Selected Claim", use_container_width=True):
                claim_row = df[df["claim_id"] == selected_claim].iloc[0]
                st.markdown("#### Claim Details")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Customer", claim_row["customer_name"])
                    st.metric("Hospital", claim_row["hospital_name"])
                with col2:
                    st.metric("Claim Amount", f"₹{claim_row['claim_amount']:,.0f}")
                    st.metric("Status", claim_row["status"])
                with col3:
                    st.metric("Fraud Score", f"{claim_row.get('fraud_score', 0):.1f}%")
                    st.metric("Risk Level", claim_row.get("risk_level", "Unknown"))

                st.info(f"📝 Description: {claim_row.get('claim_description', 'N/A')}")

        except Exception as e:
            st.error(f"Error loading claims: {e}")
