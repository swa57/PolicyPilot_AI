import streamlit as st
import pandas as pd
import os
import datetime
from utils.ocr_utils import extract_text_from_pdf, extract_text_from_image, analyze_document, validate_file, save_uploaded_file

def show_submit_claim():
    st.markdown("## 📝 Submit New Insurance Claim")

    with st.form("claim_form", clear_on_submit=False):
        st.markdown("### 📋 Claim Information")
        col1, col2 = st.columns(2)

        with col1:
            claim_id = st.text_input("🆔 Claim ID", placeholder="CLM-2024-XXX")
            customer_name = st.text_input("👤 Customer Name", placeholder="Full name")
            hospital_name = st.text_input("🏥 Hospital Name", placeholder="Hospital/clinic name")
            incident_date = st.date_input("📅 Incident Date", value=datetime.date.today())

        with col2:
            policy_number = st.text_input("📄 Policy Number", placeholder="POL-XXXX-XXXX")
            claim_amount = st.number_input("💰 Claim Amount (₹)", min_value=0.0, step=1000.0, format="%.2f")
            claim_description = st.text_area("📝 Claim Description", placeholder="Describe the incident and treatment...", height=100)

        st.markdown("### 📁 Upload Documents")
        uploaded_file = st.file_uploader(
            "Upload Claim Documents (PDF, JPG, PNG)",
            type=["pdf", "jpg", "jpeg", "png"],
            help="Max size: 10MB"
        )

        submitted = st.form_submit_button("🚀 Submit Claim", use_container_width=True)

        if submitted:
            errors = []
            if not claim_id: errors.append("Claim ID is required")
            if not policy_number: errors.append("Policy Number is required")
            if not customer_name: errors.append("Customer Name is required")
            if claim_amount <= 0: errors.append("Claim Amount must be greater than 0")
            if not hospital_name: errors.append("Hospital Name is required")
            if not claim_description: errors.append("Claim Description is required")

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                doc_path = ""
                if uploaded_file:
                    is_valid, msg = validate_file(uploaded_file)
                    if not is_valid:
                        st.error(f"❌ {msg}")
                        return
                    doc_path = save_uploaded_file(uploaded_file, claim_id)
                    st.success(f"✅ File uploaded: {uploaded_file.name}")

                user = st.session_state.get("user", {})
                new_claim = {
                    "claim_id": claim_id,
                    "policy_number": policy_number,
                    "customer_name": customer_name,
                    "claim_amount": claim_amount,
                    "hospital_name": hospital_name,
                    "incident_date": str(incident_date),
                    "claim_description": claim_description,
                    "status": "Pending",
                    "fraud_score": 0,
                    "risk_level": "Unknown",
                    "submitted_by": user.get("username", "unknown"),
                    "submitted_date": str(datetime.date.today()),
                    "document_path": doc_path
                }

                try:
                    df = pd.read_csv("claims.csv")
                except:
                    df = pd.DataFrame()

                if claim_id in df.get("claim_id", pd.Series()).values:
                    st.error("❌ Claim ID already exists!")
                    return

                df = pd.concat([df, pd.DataFrame([new_claim])], ignore_index=True)
                df.to_csv("claims.csv", index=False)

                st.success(f"✅ Claim **{claim_id}** submitted successfully!")
                st.balloons()

                if uploaded_file and doc_path:
                    st.markdown("### 🔍 Document Analysis")
                    with st.spinner("Analyzing document..."):
                        if uploaded_file.type == "application/pdf":
                            uploaded_file.seek(0)
                            extracted_text = extract_text_from_pdf(uploaded_file)
                        else:
                            uploaded_file.seek(0)
                            extracted_text = extract_text_from_image(uploaded_file)

                        analysis = analyze_document(extracted_text)

                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("📊 Document Completeness", f"{analysis['completeness_score']}%")
                            st.metric("📝 Word Count", analysis['word_count'])

                        with col_b:
                            if analysis['missing_fields']:
                                st.warning(f"⚠️ Missing: {', '.join(analysis['missing_fields'])}")
                            if analysis['suspicious_keywords']:
                                st.error(f"🚨 Suspicious terms: {', '.join(analysis['suspicious_keywords'])}")

                        with st.expander("📄 Extracted Text"):
                            st.text_area("", extracted_text[:2000] + ("..." if len(extracted_text) > 2000 else ""), height=200)

                        st.markdown("**✅ Detected Fields:**")
                        cols = st.columns(3)
                        for i, (field, status) in enumerate(analysis['found_fields'].items()):
                            with cols[i % 3]:
                                st.write(f"{status} {field}")
