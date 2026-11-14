"""
FairHire India - Candidate Job Browsing Portal
Browse published job vacancies with search, department filtering, and direct application routing.
"""
import streamlit as st
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_jobs, get_applications_by_candidate
from components.ui import render_section_heading, render_disclaimer
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

def render_browse_jobs_page():
    """Render the candidate job discovery and application portal."""
    require_role(["candidate"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Verified Career Opportunities", "Explore published positions audited for demographic parity and ethical recruitment.")
    render_disclaimer()

    jobs = get_jobs(status="Published")
    apps = get_applications_by_candidate(user["id"])
    applied_job_ids = {a["job_id"] for a in apps}

    # Filters Toolbar
    c_search, c_dept, c_loc = st.columns([5, 3.5, 3.5])
    with c_search:
        search_query = st.text_input("🔍 Search Vacancies", placeholder="Search by title, skills, or keywords...")
    with c_dept:
        departments = ["All Departments"] + sorted(list({j["department"] for j in jobs}))
        sel_dept = st.selectbox("Department", options=departments)
    with c_loc:
        locations = ["All Locations"] + sorted(list({j["location"].split("(")[0].strip() for j in jobs}))
        sel_loc = st.selectbox("Location", options=locations)

    # Filter logic
    filtered = jobs.copy()
    if search_query:
        q = search_query.lower()
        filtered = [j for j in filtered if q in j["title"].lower() or q in j["required_skills"].lower() or q in j["description"].lower()]
    if sel_dept != "All Departments":
        filtered = [j for j in filtered if j["department"] == sel_dept]
    if sel_loc != "All Locations":
        filtered = [j for j in filtered if sel_loc.lower() in j["location"].lower()]

    st.markdown(f"<div style='font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-bottom: 1rem;'>Showing <strong>{len(filtered)}</strong> open position(s)</div>", unsafe_allow_html=True)

    if not filtered:
        st.info("No job openings match the selected filters. Please adjust your criteria.")
        render_footer()
        return

    for job in filtered:
        job_id = job["id"]
        is_applied = job_id in applied_job_ids

        st.markdown(
            f"""
            <div class="fairhire-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                    <div>
                        <span class="compliance-badge badge-cyan">{job['department']}</span>
                        <span class="compliance-badge badge-purple" style="margin-left: 0.4rem;">{job['employment_type']}</span>
                        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-top: 0.4rem;">
                            {job['title']}
                        </div>
                        <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.2rem;">
                            📍 {job['location']} · Minimum Experience: <strong>{job['experience_requirements']} years</strong>
                        </div>
                    </div>
                    <div style="text-align: right; margin-top: 0.25rem;">
                        {'<span class="compliance-badge badge-green">APPLICATION SUBMITTED</span>' if is_applied else ''}
                    </div>
                </div>

                <div style="font-size: 0.9rem; color: {COLOR_PALETTE['main_text']}; line-height: 1.5; margin: 0.85rem 0;">
                    {job['description']}
                </div>

                <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; padding: 0.75rem 1rem; border-radius: 4px; border: 1px solid {COLOR_PALETTE['border']}; font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']};">
                    <strong style="color: {COLOR_PALETTE['primary_purple']};">Required Skills:</strong> {job['required_skills']}<br/>
                    <strong style="color: {COLOR_PALETTE['primary_purple']};">Education Requirement:</strong> {job['education_requirements']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, _ = st.columns([2.5, 2.5, 7])
        with c1:
            if is_applied:
                if st.button(f"View Status #{job_id}", key=f"view_app_{job_id}", type="secondary", use_container_width=True):
                    st.session_state["current_page"] = "my_applications"
                    st.rerun()
            else:
                if st.button(f"Apply Now →", key=f"apply_btn_{job_id}", type="primary", use_container_width=True):
                    st.session_state["target_job_id"] = job_id
                    st.session_state["current_page"] = "apply_job"
                    st.rerun()

    render_footer()
