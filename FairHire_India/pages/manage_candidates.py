"""
FairHire India - Candidate Application Management & Review Portal
Comprehensive candidate screening, interactive status updates, and inline SHAP/LIME decision audit.
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any

from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_all_applications, get_application_by_id, update_application_status, get_jobs
from explainability.shap_explainer import explain_candidate_shap
from explainability.lime_explainer import explain_candidate_lime
from components.ui import render_section_heading, render_disclaimer
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.charts import plot_shap_explanation
from components.footer import render_footer

def render_manage_candidates_page():
    """Render the recruiter candidate management workspace."""
    require_role(["recruiter", "admin"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Candidate Application Management", "Filter, inspect AI shortlisting recommendations, and record human evaluation decisions.")
    render_disclaimer()

    apps = get_all_applications()
    jobs = get_jobs()

    if not apps:
        st.info("No applications currently exist in the database.")
        render_footer()
        return

    # Filters Toolbar
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        search_query = st.text_input("🔍 Search Name or Email", placeholder="Filter by candidate...")
    with f_col2:
        job_titles = ["All Jobs"] + sorted(list({a["job_title"] for a in apps}))
        selected_job = st.selectbox("Filter by Opening", options=job_titles)
    with f_col3:
        status_options = ["All Statuses", "Submitted", "Under Review", "Shortlisted", "Awaiting Human Review", "Interview Scheduled", "Selected", "Not Selected"]
        selected_status = st.selectbox("Filter by Status", options=status_options)
    with f_col4:
        sort_by = st.selectbox("Sort Applications", options=["Highest Match %", "Lowest Match %", "Most Recent", "Years of Experience"])

    # Apply Filters
    filtered = apps.copy()
    if search_query:
        q = search_query.lower()
        filtered = [a for a in filtered if q in a["candidate_name"].lower() or q in a["candidate_email"].lower()]
    if selected_job != "All Jobs":
        filtered = [a for a in filtered if a["job_title"] == selected_job]
    if selected_status != "All Statuses":
        filtered = [a for a in filtered if a["status"] == selected_status]

    # Sort
    if sort_by == "Highest Match %":
        filtered.sort(key=lambda x: (x.get("prediction_probability") or 0.0), reverse=True)
    elif sort_by == "Lowest Match %":
        filtered.sort(key=lambda x: (x.get("prediction_probability") or 0.0))
    elif sort_by == "Years of Experience":
        filtered.sort(key=lambda x: x.get("experience_years", 0), reverse=True)
    else: # Most Recent
        filtered.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)

    st.markdown(f"<div style='font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-bottom: 1rem;'>Showing <strong>{len(filtered)}</strong> matching application(s)</div>", unsafe_allow_html=True)

    # Main split layout: Candidate list on left (7 cols), Detailed Inspector on right (5 cols)
    c_left, c_right = st.columns([6, 6])

    with c_left:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Candidate Submissions</div>", unsafe_allow_html=True)

        for app in filtered:
            app_id = app["id"]
            prob = app.get("prediction_probability")
            prob_pct = f"{prob * 100:.1f}%" if prob is not None else "Pending"
            status = app.get("status", "Submitted")

            badge_style = "badge-purple"
            if status in ["Shortlisted", "Selected"]:
                badge_style = "badge-green"
            elif status in ["Under Review", "Awaiting Human Review"]:
                badge_style = "badge-amber"
            elif status == "Interview Scheduled":
                badge_style = "badge-cyan"

            is_selected = st.session_state.get("selected_app_id") == app_id

            st.markdown(
                f"""
                <div class="fairhire-card" style="border-left: 4px solid {COLOR_PALETTE['primary_purple'] if not is_selected else COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="compliance-badge {badge_style}">{status}</span>
                            <div style="font-weight: 600; font-size: 1.05rem; color: {COLOR_PALETTE['main_text']}; margin-top: 0.25rem;">
                                {app['candidate_name']}
                            </div>
                            <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">
                                {app['job_title']} · {app.get('experience_years', 0)} Yrs Exp
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']};">AI Match</div>
                            <div class="mono-stat" style="font-size: 1.25rem;">{prob_pct}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(f"Inspect Candidate #{app_id}", key=f"sel_app_{app_id}", use_container_width=True, type="secondary"):
                st.session_state["selected_app_id"] = app_id
                st.rerun()

    # Detailed Candidate Dossier & Human Decision Form
    with c_right:
        sel_id = st.session_state.get("selected_app_id")
        if not sel_id and filtered:
            sel_id = filtered[0]["id"]
            st.session_state["selected_app_id"] = sel_id

        target_app = get_application_by_id(sel_id) if sel_id else None

        if target_app:
            st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Candidate Dossier & AI Explainability</div>", unsafe_allow_html=True)

            prob = target_app.get("prediction_probability")
            prob_str = f"{prob * 100:.1f}%" if prob is not None else "Pending"

            st.markdown(
                f"""
                <div class="fairhire-card">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 600; color: {COLOR_PALETTE['main_text']};">
                        {target_app['candidate_name']}
                    </div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;">
                        {target_app['candidate_email']} · {target_app.get('candidate_phone', 'N/A')}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']};">
                        <div><strong>Target Role:</strong> {target_app['job_title']}</div>
                        <div><strong>Experience:</strong> {target_app.get('experience_years', 0)} years</div>
                        <div><strong>Skill Score:</strong> {target_app.get('skill_score', 0):.0f}/100</div>
                        <div><strong>Interview Score:</strong> {target_app.get('interview_score', 0):.0f}/100</div>
                        <div><strong>Commute:</strong> {target_app.get('distance_from_company', 0):.1f} km</div>
                        <div><strong>Previous Employers:</strong> {target_app.get('previous_companies', 0)}</div>
                    </div>
                    <div style="border-top: 1px solid {COLOR_PALETTE['border']}; margin-top: 0.75rem; padding-top: 0.5rem;">
                        <span style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">Audit Demographic: </span>
                        <span class="compliance-badge badge-purple">{target_app.get('gender_audit', 'Not Disclosed')}</span>
                        <span style="font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']}; margin-left: 0.5rem;">(Omitted from AI Scoring)</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # AI Recommendation Box
            rec_text = target_app.get("recommendation") or "Pending evaluation."
            st.markdown(
                f"""
                <div class="fairhire-card" style="border-left: 4px solid {COLOR_PALETTE['cyan']};">
                    <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; text-transform: uppercase;">AI Decision-Support Signal</div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-top: 0.2rem;">
                        {rec_text}
                    </div>
                    <div class="mono-stat" style="font-size: 1.5rem; margin-top: 0.2rem;">Shortlisting Match: {prob_str}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # SHAP Feature Explanations
            cand_features = {
                "Age": 28,
                "EducationLevel": target_app.get("education_level", 2),
                "ExperienceYears": target_app.get("experience_years", 3),
                "PreviousCompanies": target_app.get("previous_companies", 1),
                "DistanceFromCompany": target_app.get("distance_from_company", 10.0),
                "InterviewScore": target_app.get("interview_score", 75.0),
                "SkillScore": target_app.get("skill_score", 75.0),
                "PersonalityScore": target_app.get("personality_score", 75.0),
                "RecruitmentStrategy": target_app.get("recruitment_strategy", 2)
            }

            with st.expander("🔬 View SHAP & LIME Feature Attribution", expanded=True):
                shap_res = explain_candidate_shap(cand_features, model_name="Random Forest")
                fig_shap = plot_shap_explanation(shap_res["contributions"], title=f"SHAP Impact for {target_app['candidate_name']}")
                st.plotly_chart(fig_shap, use_container_width=True)

                st.markdown(f"<div style='font-size: 0.75rem; color: {COLOR_PALETTE['warning_amber']}; margin-bottom: 0.75rem;'>{shap_res['disclaimer']}</div>", unsafe_allow_html=True)

                # LIME Rules
                lime_res = explain_candidate_lime(cand_features, model_name="Random Forest")
                st.markdown(f"<strong style='font-size: 0.85rem; color: {COLOR_PALETTE['cyan']};'>LIME Local Rules:</strong>", unsafe_allow_html=True)
                for r in lime_res["rules"][:3]:
                    rule_color = COLOR_PALETTE["success_green"] if r["weight"] > 0 else COLOR_PALETTE["danger_red"]
                    st.markdown(f"<div style='font-size: 0.8rem; color: {COLOR_PALETTE['main_text']};'>• <code>{r['rule']}</code> → <span style='color: {rule_color};'>{r['direction']}</span> (Weight: {r['weight']:.3f})</div>", unsafe_allow_html=True)

            # Human Recruiter Decision Form
            st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-top: 1rem; margin-bottom: 0.5rem;'>Record Recruiter Evaluation</div>", unsafe_allow_html=True)

            with st.form(f"review_form_{sel_id}"):
                cur_status = target_app.get("status", "Submitted")
                available_statuses = ["Submitted", "Under Review", "Shortlisted", "Awaiting Human Review", "Interview Scheduled", "Selected", "Not Selected"]
                cur_idx = available_statuses.index(cur_status) if cur_status in available_statuses else 0

                new_status = st.selectbox("Update Pipeline Status", options=available_statuses, index=cur_idx)
                recruiter_notes = st.text_area("Recruiter Evaluation Notes", value=target_app.get("recruiter_notes") or "", placeholder="Enter detailed notes regarding candidate technical proficiency, communication, and interview justification...")

                save_decision = st.form_submit_button("Confirm Human Evaluation Decision", type="primary", use_container_width=True)

                if save_decision:
                    update_application_status(
                        app_id=sel_id,
                        status=new_status,
                        recruiter_notes=recruiter_notes,
                        reviewed_by=user["id"]
                    )
                    st.success(f"Status for {target_app['candidate_name']} updated to '{new_status}' with audit trail entry.")
                    st.rerun()

        else:
            st.info("Select a candidate from the left panel to inspect credentials and record evaluation decisions.")

    render_footer()
