"""
FairHire India - Candidate Dashboard
Live database-derived metrics, recent application tracker, and career opportunities.
"""
import streamlit as st
import textwrap
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_applications_by_candidate, get_jobs, get_candidate_profile
from components.ui import (
    render_section_heading, render_metric_card, render_disclaimer,
    render_candidate_hero_banner
)
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.tables import render_applications_table
from components.footer import render_footer

def render_candidate_dashboard():
    """Render the Candidate Dashboard portal."""
    require_role(["candidate"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    # Top Candidate Hero Banner with Navigation Pills
    render_candidate_hero_banner(active_tab="candidate_dashboard")

    render_section_heading(f"Welcome back, {user.get('full_name')} 👋", "Track your active applications, status updates, and new verified job openings.")
    render_disclaimer()

    # Query live database metrics for current candidate
    apps = get_applications_by_candidate(user["id"])
    all_jobs = get_jobs(status="Published")
    profile = get_candidate_profile(user["id"])

    total_apps = len(apps)
    shortlisted = len([a for a in apps if a.get("status") in ["Shortlisted", "Selected"]])
    pending = len([a for a in apps if a.get("status") in ["Submitted", "Under Review", "Awaiting Human Review"]])
    active_jobs = len(all_jobs)

    # Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("My Applications", str(total_apps), "Total Submissions")
    with c2:
        render_metric_card("Shortlisted", str(shortlisted), "Positive Signals", is_positive=True)
    with c3:
        render_metric_card("Under Review", str(pending), "Human Evaluation Pending")
    with c4:
        render_metric_card("Active Openings", str(active_jobs), "Verified Vacancies")

    # Quick action banner
    banner_card = textwrap.dedent(f"""
    <div class="fairhire-card" style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem;">
        <div>
            <strong style="color: {COLOR_PALETTE['cyan']}; font-size: 1.05rem;">Explore New Career Opportunities</strong>
            <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.25rem;">
                Submit your credentials to published positions audited for demographic parity.
            </div>
        </div>
    </div>
    """).strip()
    st.markdown(banner_card, unsafe_allow_html=True)

    c_btn1, c_btn2, _ = st.columns([2.5, 2.5, 5])
    with c_btn1:
        if st.button("Browse & Apply for Jobs", type="primary", use_container_width=True):
            st.session_state["current_page"] = "apply_job"
            st.rerun()
    with c_btn2:
        if st.button("Update Profile", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "candidate_profile"
            st.rerun()

    # Recent Applications Section
    render_section_heading("My Recent Submissions", "Real-time human recruiter evaluation status.")
    render_applications_table(apps[:5])

    render_footer()
