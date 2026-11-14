"""
FairHire India - Recruiter Candidate Search Engine
Multi-attribute talent discovery filtering across skills, credentials, experience, and score metrics.
"""
import streamlit as st
import pandas as pd
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_all_applications, get_candidate_profiles_list
from components.ui import render_section_heading, render_disclaimer
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

def render_candidate_search_page():
    """Render advanced recruiter candidate search engine."""
    require_role(["recruiter", "admin"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Candidate Search Engine", "Multi-criteria talent discovery across verified applicant profiles.")
    render_disclaimer()

    apps = get_all_applications()
    profiles = get_candidate_profiles_list()

    # Search & Filter Controls
    with st.expander("🔍 Search & Filter Controls", expanded=True):
        sc1, sc2, sc3 = st.columns([5, 3.5, 3.5])
        with sc1:
            q_text = st.text_input("Candidate Name, Email, or Skill Keyword", placeholder="e.g. Ananya, Python, SQL...")
        with sc2:
            edu_filter = st.selectbox("Education Level", options=["All Levels", "Bachelor's", "Master's", "PhD", "Other / Diploma"])
        with sc3:
            status_filter = st.selectbox("Application Status", options=["All Statuses", "Shortlisted", "Under Review", "Submitted", "Selected", "Not Selected"])

        sc4, sc5, sc6 = st.columns(3)
        with sc4:
            min_exp, max_exp = st.slider("Experience Range (Years)", 0, 30, (0, 20))
        with sc5:
            min_skill = st.slider("Min Skill Assessment Score", 0.0, 100.0, 50.0)
        with sc6:
            min_match = st.slider("Min AI Match Probability (%)", 0.0, 100.0, 0.0)

    # Filter Applications
    results = apps.copy()

    if q_text:
        term = q_text.lower()
        results = [
            a for a in results
            if term in a["candidate_name"].lower()
            or term in a["candidate_email"].lower()
            or term in a.get("candidate_skills", "").lower()
            or term in a["job_title"].lower()
        ]

    if edu_filter != "All Levels":
        edu_num_map = {"Bachelor's": 1, "Master's": 2, "PhD": 3, "Other / Diploma": 4}
        req_num = edu_num_map.get(edu_filter)
        results = [a for a in results if a.get("education_level") == req_num]

    if status_filter != "All Statuses":
        results = [a for a in results if a.get("status") == status_filter]

    results = [a for a in results if min_exp <= a.get("experience_years", 0) <= max_exp]
    results = [a for a in results if a.get("skill_score", 0) >= min_skill]
    results = [a for a in results if (a.get("prediction_probability") or 0.0) * 100 >= min_match]

    st.markdown(f"<div style='font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin: 1rem 0;'>Found <strong>{len(results)}</strong> candidate dossier(s) matching criteria</div>", unsafe_allow_html=True)

    if not results:
        st.info("No candidates match your current filter parameters. Try broadening your score or experience criteria.")
        render_footer()
        return

    # Results Table
    rows = []
    for a in results:
        prob = a.get("prediction_probability")
        prob_str = f"{prob * 100:.1f}%" if prob is not None else "Pending"
        rows.append({
            "App Ref": a.get("application_number"),
            "Candidate Name": a.get("candidate_name"),
            "Role Applied": a.get("job_title"),
            "Experience": f"{a.get('experience_years', 0)} Yrs",
            "Skill Score": f"{a.get('skill_score', 0):.0f}/100",
            "AI Match Score": prob_str,
            "Status": a.get("status"),
            "Audit Demographic": a.get("gender_audit", "Not Disclosed")
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Candidate Detail Card Selector
    st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.5rem;'>Quick Candidate Dossier Selector</div>", unsafe_allow_html=True)
    c_opts = {f"{a['candidate_name']} ({a['job_title']} — {a['application_number']})": a["id"] for a in results}
    sel_cand_label = st.selectbox("Inspect Full Dossier in Application Manager", options=list(c_opts.keys()))
    sel_cand_id = c_opts[sel_cand_label]

    if st.button("Open in Application Reviewer →", type="primary"):
        st.session_state["selected_app_id"] = sel_cand_id
        st.session_state["current_page"] = "manage_candidates"
        st.rerun()

    render_footer()
