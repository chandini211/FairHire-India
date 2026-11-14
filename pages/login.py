"""
FairHire India - Secure Sign In Page
Enterprise dark authentication portal with Bcrypt verification and role-based redirection.
"""
import streamlit as st
from config import COLOR_PALETTE
from auth.authentication import login_user, is_authenticated, get_current_user
from components.ui import render_section_heading

def render_login_page():
    """Render the user sign-in interface."""
    # If already logged in, redirect based on role
    if is_authenticated():
        user = get_current_user()
        if user["role"] == "candidate":
            st.session_state["current_page"] = "candidate_dashboard"
        else:
            st.session_state["current_page"] = "recruiter_dashboard"
        st.rerun()

    # Back to landing page button
    cols_top = st.columns([1, 8, 2])
    with cols_top[0]:
        if st.button("← Home", key="back_home_login"):
            st.session_state["current_page"] = "landing"
            st.rerun()

    st.markdown("<div style='max-width: 480px; margin: 2rem auto 0 auto;'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.75rem; font-weight: 700; color: {COLOR_PALETTE['cyan']};">
                FAIRHIRE <span style="color: {COLOR_PALETTE['primary_purple']};">INDIA</span>
            </div>
            <div style="font-size: 0.9rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.25rem;">
                Sign in to your candidate or recruiter portal
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email Address", placeholder="name@company.com or candidate@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        submit = st.form_submit_button("Sign In to FairHire", use_container_width=True, type="primary")

        if submit:
            success, msg, user = login_user(email, password)
            if success:
                st.success(msg)
                if user["role"] == "candidate":
                    st.session_state["current_page"] = "candidate_dashboard"
                else:
                    st.session_state["current_page"] = "recruiter_dashboard"
                st.rerun()
            else:
                st.error(msg)

    # Demo credentials helper widget
    st.markdown(
        f"""
        <div class="fairhire-card" style="margin-top: 1.5rem; font-size: 0.8rem; border-color: {COLOR_PALETTE['border']};">
            <strong style="color: {COLOR_PALETTE['cyan']};">DEMO ACCESS CREDENTIALS:</strong><br/>
            <span style="color: {COLOR_PALETTE['secondary_text']};">Recruiter:</span> <code>recruiter@fairhire.in</code> / <code>FairHire@Admin2026</code><br/>
            <span style="color: {COLOR_PALETTE['secondary_text']};">Candidate:</span> <code>ananya.sen@example.com</code> / <code>Candidate@Pass123</code>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']};">
            Don't have an account yet?
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Create Candidate Account", key="btn_to_signup", use_container_width=True, type="secondary"):
        st.session_state["current_page"] = "signup"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
