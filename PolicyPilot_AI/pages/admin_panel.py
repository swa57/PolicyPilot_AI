import streamlit as st
import pandas as pd
import os

def show_admin_panel():
    from utils.auth import is_admin

    if not is_admin():
        st.error("🔒 Access Denied. Admin privileges required.")
        return

    st.markdown("## 🛠️ Admin Panel")

    tab1, tab2, tab3 = st.tabs(["📋 All Claims", "👥 Users", "📁 Uploaded Files"])

    with tab1:
        st.markdown("### 📋 Claims Management")
        try:
            df = pd.read_csv("claims.csv")

            col1, col2, col3 = st.columns(3)
            with col1:
                search_term = st.text_input("🔍 Search Claims", placeholder="Customer name or Claim ID")
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "Approved", "Pending", "Suspicious", "Fraudulent"])
            with col3:
                risk_filter = st.selectbox("Filter by Risk", ["All", "Low", "Medium", "High"])

            filtered_df = df.copy()
            if search_term:
                filtered_df = filtered_df[
                    filtered_df["customer_name"].str.contains(search_term, case=False, na=False) |
                    filtered_df["claim_id"].str.contains(search_term, case=False, na=False)
                ]
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df["status"] == status_filter]
            if risk_filter != "All" and "risk_level" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["risk_level"] == risk_filter]

            st.markdown(f"**Showing {len(filtered_df)} of {len(df)} claims**")

            for _, row in filtered_df.iterrows():
                status_colors = {
                    "Approved": "#00ff88", "Pending": "#ffaa00",
                    "Fraudulent": "#ff4444", "Suspicious": "#ff8800"
                }
                status_color = status_colors.get(row["status"], "#ffffff")

                with st.expander(f"📋 {row['claim_id']} | {row['customer_name']} | ₹{row['claim_amount']:,.0f} | "
                                 f"**:{status_color[1:]}[{row['status']}]**"):
                    col_d1, col_d2, col_d3 = st.columns(3)
                    with col_d1:
                        st.write(f"**Policy:** {row['policy_number']}")
                        st.write(f"**Hospital:** {row['hospital_name']}")
                        st.write(f"**Date:** {row['incident_date']}")
                    with col_d2:
                        st.write(f"**Amount:** ₹{row['claim_amount']:,.0f}")
                        st.write(f"**Fraud Score:** {row.get('fraud_score', 0):.1f}%")
                        st.write(f"**Risk Level:** {row.get('risk_level', 'N/A')}")
                    with col_d3:
                        st.write(f"**Submitted by:** {row.get('submitted_by', 'N/A')}")
                        st.write(f"**Date:** {row.get('submitted_date', 'N/A')}")

                    st.write(f"**Description:** {row.get('claim_description', 'N/A')}")

                    if row.get("document_path") and os.path.exists(str(row.get("document_path", ""))):
                        st.success(f"📎 Document: {row['document_path']}")

                    action_col1, action_col2, action_col3 = st.columns(3)
                    with action_col1:
                        if st.button("✅ Approve", key=f"approve_{row['claim_id']}", use_container_width=True):
                            update_claim_status(row['claim_id'], "Approved")
                            st.success(f"✅ Claim {row['claim_id']} approved!")
                            st.rerun()
                    with action_col2:
                        if st.button("❌ Reject", key=f"reject_{row['claim_id']}", use_container_width=True):
                            update_claim_status(row['claim_id'], "Rejected")
                            st.error(f"❌ Claim {row['claim_id']} rejected!")
                            st.rerun()
                    with action_col3:
                        if st.button("🚨 Flag Fraud", key=f"fraud_{row['claim_id']}", use_container_width=True):
                            update_claim_status(row['claim_id'], "Fraudulent")
                            st.warning(f"🚨 Claim {row['claim_id']} flagged as fraud!")
                            st.rerun()

        except Exception as e:
            st.error(f"Error loading claims: {e}")

    with tab2:
        st.markdown("### 👥 User Management")
        try:
            users_df = pd.read_csv("users.csv")
            display_users = users_df[["username", "role", "full_name", "email"]].copy()

            def style_role(val):
                if val == "admin":
                    return "color: #ff4444; font-weight: bold"
                return "color: #00d4ff"

            st.dataframe(
                display_users.style.applymap(style_role, subset=["role"]),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("#### ➕ Add New User")
            with st.form("add_user_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_username = st.text_input("Username")
                    new_password = st.text_input("Password", type="password")
                    new_role = st.selectbox("Role", ["agent", "admin"])
                with col2:
                    new_fullname = st.text_input("Full Name")
                    new_email = st.text_input("Email")

                if st.form_submit_button("➕ Add User", use_container_width=True):
                    if new_username and new_password and new_fullname:
                        new_user = {
                            "username": new_username,
                            "password": new_password,
                            "role": new_role,
                            "full_name": new_fullname,
                            "email": new_email
                        }
                        users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)
                        users_df.to_csv("users.csv", index=False)
                        st.success(f"✅ User '{new_username}' added!")
                        st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

    with tab3:
        st.markdown("### 📁 Uploaded Files")
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        files = os.listdir(uploads_dir)

        if not files:
            st.info("📭 No files uploaded yet.")
        else:
            st.success(f"✅ {len(files)} file(s) in uploads folder")
            for f in files:
                file_path = os.path.join(uploads_dir, f)
                file_size = os.path.getsize(file_path) / 1024
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"📄 **{f}** ({file_size:.1f} KB)")
                with col2:
                    with open(file_path, "rb") as fp:
                        st.download_button(
                            "⬇️ Download",
                            data=fp.read(),
                            file_name=f,
                            key=f"admin_dl_{f}"
                        )
                st.markdown("---")

def update_claim_status(claim_id, new_status):
    """Update claim status in CSV"""
    try:
        df = pd.read_csv("claims.csv")
        df.loc[df["claim_id"] == claim_id, "status"] = new_status
        df.to_csv("claims.csv", index=False)
    except Exception as e:
        st.error(f"Error updating claim: {e}")
