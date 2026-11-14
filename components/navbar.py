"""
FairHire India - Responsive Public & Authenticated Navigation Bar
Includes desktop pill navigation with active indication and mobile-friendly dropdown.
Supports all 11 required navigation destinations without horizontal overflow.
"""
import streamlit as st
from config import COLOR_PALETTE, APP_NAME, APP_TAGLINE
from auth.authentication import get_current_user, is_authenticated, logout_user

PUBLIC_NAV_ITEMS = [
    ("Home", "home", "landing"),
    ("Problem", "problem", "landing"),
    ("Solution", "solution", "landing"),
    ("Workflow", "workflow", "landing"),
    ("Methodology", "methodology", "landing"),
    ("Dataset", "dataset", "landing"),
    ("Fairness", "fairness", "landing"),
    ("Explainable AI", "xai", "landing"),
    ("About / Team", "about", "about"),
]

def render_public_navbar():
    """Render fully responsive public navigation bar with active indicators."""
    current_page = st.session_state.get("current_page", "landing")
    landing_section = st.session_state.get("landing_section", "home")

    # Header Row
    top_c1, top_c2, top_c3 = st.columns([4, 6, 2])

    with top_c1:
        st.markdown(
            f"""
            <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.35rem; color: {COLOR_PALETTE['cyan']};">
                FAIRHIRE <span style="color: {COLOR_PALETTE['primary_purple']};">INDIA</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top_c2:
        # Desktop responsive pill selector
        nav_labels = [item[0] for item in PUBLIC_NAV_ITEMS]

        # Determine current index
        cur_idx = 0
        if current_page == "about":
            cur_idx = 8
        elif current_page == "landing":
            for idx, item in enumerate(PUBLIC_NAV_ITEMS):
                if item[1] == landing_section:
                    cur_idx = idx
                    break

        selected_nav = st.selectbox(
            "Quick Navigation",
            options=nav_labels,
            index=cur_idx,
            label_visibility="collapsed",
            key="public_nav_selector"
        )

        # Handle navigation change
        for label, sec_id, target_page in PUBLIC_NAV_ITEMS:
            if selected_nav == label:
                if (target_page != current_page) or (target_page == "landing" and landing_section != sec_id):
                    st.session_state["current_page"] = target_page
                    st.session_state["landing_section"] = sec_id
                    st.rerun()
                break

    with top_c3:
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("Sign In", key="nav_signin_btn", type="secondary", use_container_width=True):
                st.session_state["current_page"] = "login"
                st.rerun()
        with btn_c2:
            if st.button("Sign Up", key="nav_signup_btn", type="primary", use_container_width=True):
                st.session_state["current_page"] = "signup"
                st.rerun()

    # Desktop category pills row for 1-click access
    pills_cols = st.columns(len(PUBLIC_NAV_ITEMS))
    for i, (label, sec_id, target_page) in enumerate(PUBLIC_NAV_ITEMS):
        with pills_cols[i]:
            is_active = (current_page == target_page) and (target_page != "landing" or landing_section == sec_id)
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"pill_{sec_id}", type=btn_type, use_container_width=True):
                st.session_state["current_page"] = target_page
                st.session_state["landing_section"] = sec_id
                st.rerun()

    st.markdown(f"<div style='border-bottom: 1px solid {COLOR_PALETTE['border']}; margin-top: 0.5rem; margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

def render_auth_header():
    """Render top authenticated user bar."""
    user = get_current_user()
    if not user:
        return

    cols = st.columns([6, 3, 1.2])
    with cols[0]:
        role_label = user.get("role", "").capitalize()
        st.markdown(
            f"<div style='padding-top: 0.25rem; font-size: 0.95rem;'>"
            f"<span style='color: {COLOR_PALETTE['secondary_text']}'>Logged in as </span>"
            f"<strong style='color: {COLOR_PALETTE['main_text']}'>{user.get('full_name')}</strong> "
            f"<span class='compliance-badge badge-purple' style='margin-left: 0.5rem;'>{role_label}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    with cols[1]:
        st.markdown(
            f"<div style='text-align: right; padding-top: 0.25rem; font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}'>"
            f"{user.get('email')}"
            f"</div>",
            unsafe_allow_html=True
        )

    with cols[2]:
        if st.button("Log Out", key="auth_logout", type="secondary", use_container_width=True):
            logout_user()
            st.rerun()

    st.markdown(f"<div style='border-bottom: 1px solid {COLOR_PALETTE['border']}; margin-top: 0.35rem; margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
