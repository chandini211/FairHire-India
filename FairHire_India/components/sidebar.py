"""
FairHire India - Role-Aware Sidebar Navigation Component
Strictly implements Section 5 (Candidate Navigation) and Section 6 (Recruiter Navigation).
"""
import streamlit as st
import textwrap
from config import COLOR_PALETTE
from auth.authentication import get_current_user, is_authenticated, logout_user

def render_sidebar():
    """Render role-specific sidebar navigation."""
    with st.sidebar:
        # App branding
        brand_html = textwrap.dedent(f"""
        <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid {COLOR_PALETTE['border']}; margin-bottom: 1.25rem;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 700; color: {COLOR_PALETTE['cyan']}; letter-spacing: -0.01em;">
                FAIRHIRE <span style="color: {COLOR_PALETTE['primary_purple']};">INDIA</span>
            </div>
            <div style="font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.2rem; font-family: 'Inter', sans-serif;">
                Recruitment Without Bias. By Design.
            </div>
        </div>
        """).strip()
        st.markdown(brand_html, unsafe_allow_html=True)

        user = get_current_user()

        if not user:
            # Public navigation
            st.markdown(f"<div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: {COLOR_PALETTE['secondary_text']}; margin-bottom: 0.5rem;'>Public Navigation</div>", unsafe_allow_html=True)

            if st.button("🌐 Explore Platform", key="sb_home", use_container_width=True):
                st.session_state["current_page"] = "landing"
                st.session_state["landing_section"] = "home"
                st.rerun()

            if st.button("🔐 Sign In", key="sb_login", use_container_width=True):
                st.session_state["current_page"] = "login"
                st.rerun()

            if st.button("✨ Create Candidate Account", key="sb_signup", type="primary", use_container_width=True):
                st.session_state["current_page"] = "signup"
                st.rerun()

            if st.button("⚖️ About / Governance", key="sb_about_pub", use_container_width=True):
                st.session_state["current_page"] = "about"
                st.rerun()

        elif user.get("role") == "candidate":
            # Section 5 — Candidate Navigation
            user_box_html = textwrap.dedent(f"""
            <div style="background-color: {COLOR_PALETTE['card_bg']}; padding: 0.75rem; border: 1px solid {COLOR_PALETTE['border']}; border-radius: 4px; margin-bottom: 1.25rem;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">Candidate Portal</div>
                <div style="font-weight: 600; font-size: 0.95rem; color: {COLOR_PALETTE['main_text']}; margin-top: 0.2rem;">{user.get('full_name')}</div>
                <div style="font-size: 0.75rem; color: {COLOR_PALETTE['cyan']};">{user.get('email')}</div>
            </div>
            """).strip()
            st.markdown(user_box_html, unsafe_allow_html=True)

            current = st.session_state.get("current_page", "candidate_dashboard")

            # Section 5 candidate items
            candidate_menu = [
                ("candidate_dashboard", "📊 Dashboard"),
                ("browse_jobs", "💼 Browse Jobs"),
                ("apply_job", "📝 Apply for Job"),
                ("my_applications", "📋 My Applications"),
                ("candidate_profile", "👤 My Profile"),
                ("notifications", "🔔 Notifications"),
                ("about", "⚖️ About / Governance")
            ]

            for page_id, label in candidate_menu:
                is_cur = (current == page_id)
                btn_type = "primary" if is_cur else "secondary"
                if st.button(label, key=f"sb_cand_{page_id}", type=btn_type, use_container_width=True):
                    st.session_state["current_page"] = page_id
                    st.rerun()

            st.markdown(f"<div style='margin-top: 2rem; border-top: 1px solid {COLOR_PALETTE['border']}; padding-top: 1rem;'></div>", unsafe_allow_html=True)
            if st.button("🚪 Logout", key="sb_logout_cand", type="secondary", use_container_width=True):
                logout_user()
                st.rerun()

        elif user.get("role") in ["recruiter", "admin"]:
            # Section 6 — Recruiter Navigation
            rec_box_html = textwrap.dedent(f"""
            <div style="background-color: {COLOR_PALETTE['card_bg']}; padding: 0.75rem; border: 1px solid {COLOR_PALETTE['border']}; border-radius: 4px; margin-bottom: 1.25rem;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">Recruiter Workspace</div>
                <div style="font-weight: 600; font-size: 0.95rem; color: {COLOR_PALETTE['main_text']}; margin-top: 0.2rem;">{user.get('full_name')}</div>
                <div style="font-size: 0.75rem; color: {COLOR_PALETTE['primary_purple']};">Talent Acquisition Partner</div>
            </div>
            """).strip()
            st.markdown(rec_box_html, unsafe_allow_html=True)

            current = st.session_state.get("current_page", "recruiter_dashboard")

            # Section 6 recruiter items
            recruiter_menu = [
                ("recruiter_dashboard", "📈 Overview"),
                ("manage_jobs", "💼 Manage Jobs"),
                ("manage_candidates", "📋 Applications"),
                ("candidate_search", "🔍 Candidate Search"),
                ("candidate_profiles_view", "👥 Candidate Profiles"),
                ("model_analytics", "🧠 Model Analytics"),
                ("fairness_dashboard", "⚖️ Fairness Analytics"),
                ("explainability_dashboard", "🔬 Explainable AI"),
                ("reports_exports", "📦 Reports & Exports"),
                ("audit_logs_view", "🛡️ Audit Logs"),
                ("about", "🏛️ About / Governance")
            ]

            for page_id, label in recruiter_menu:
                is_cur = (current == page_id)
                btn_type = "primary" if is_cur else "secondary"
                if st.button(label, key=f"sb_rec_{page_id}", type=btn_type, use_container_width=True):
                    st.session_state["current_page"] = page_id
                    st.rerun()

            st.markdown(f"<div style='margin-top: 2rem; border-top: 1px solid {COLOR_PALETTE['border']}; padding-top: 1rem;'></div>", unsafe_allow_html=True)
            if st.button("🚪 Logout", key="sb_logout_rec", type="secondary", use_container_width=True):
                logout_user()
                st.rerun()

        # Footer notice
        footer_html = textwrap.dedent(f"""
        <div style="font-size: 0.7rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 2rem; text-align: center;">
            FairHire India Enterprise SaaS<br>
            v1.2.0 · Audited & Production Ready
        </div>
        """).strip()
        st.markdown(footer_html, unsafe_allow_html=True)
