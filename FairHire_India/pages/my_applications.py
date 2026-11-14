"""
FairHire India - My Applications Tracker
Provides candidates with real-time status visibility and recruiter feedback.
Displays shortlisting scores and decision-support status transparently.
"""
import streamlit as st
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_applications_by_candidate
from components.ui import (
    render_section_heading, render_disclaimer,
    render_candidate_hero_banner, render_candidate_score_card
)
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

def render_my_applications_page():
    """Render candidate application history."""
    require_role(["candidate"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    # Top Candidate Hero Banner with Navigation Pills
    render_candidate_hero_banner(active_tab="my_applications")

    render_section_heading("My Job Applications", "Track the evaluation stage and decision-support score of all submitted profiles.")
    render_disclaimer()

    apps = get_applications_by_candidate(user["id"])

    if not apps:
        st.markdown(
            f"""
            <div class="fairhire-card" style="text-align: center; padding: 2.5rem;">
                <div style="font-size: 1.1rem; color: {COLOR_PALETTE['main_text']}; font-weight: 600;">No Applications Submitted Yet</div>
                <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin: 0.5rem 0 1.25rem 0;">
                    You have not applied for any vacancies. Explore our open roles to get started.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Explore Available Openings", type="primary"):
            st.session_state["current_page"] = "apply_job"
            st.rerun()
        render_footer()
        return

    for idx, app in enumerate(apps):
        status = app.get("status", "Submitted")
        badge_style = "badge-purple"
        if status in ["Shortlisted", "Selected"]:
            badge_style = "badge-green"
        elif status in ["Under Review", "Awaiting Human Review"]:
            badge_style = "badge-amber"
        elif status == "Interview Scheduled":
            badge_style = "badge-cyan"

        prob = app.get("prediction_probability")
        score_html = ""
        score_val = None
        if prob is not None:
            score_val = int(round(float(prob) * 100))
            score_color = COLOR_PALETTE["success_green"] if score_val >= 50 else COLOR_PALETTE["warning_amber"]
            score_html = f"""
            <div style="background-color: {COLOR_PALETTE['card_bg']}; border: 1px solid {score_color}; border-radius: 8px; padding: 0.5rem 0.85rem; text-align: center; display: inline-block;">
                <div style="font-size: 0.72rem; color: {COLOR_PALETTE['secondary_text']}; text-transform: uppercase;">Shortlisting Score</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 700; color: {score_color}; line-height: 1.1;">{score_val}%</div>
            </div>
            """

        recruiter_notes = app.get("recruiter_notes") or "Application under preliminary talent review. You will receive updates here as the review progresses."

        st.markdown(
            f"""
            <div class="fairhire-card" style="margin-bottom: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
                    <div style="flex: 1; min-width: 250px;">
                        <span class="compliance-badge {badge_style}">{status}</span>
                        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem; font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-top: 0.4rem;">
                            {app.get('job_title')}
                        </div>
                        <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.2rem;">
                            Ref: <strong style="color: {COLOR_PALETTE['cyan']};">{app.get('application_number')}</strong> · Dept: <strong>{app.get('department')}</strong> · Location: <strong>{app.get('job_location')}</strong>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        {score_html}
                        <div style="font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.4rem;">
                            Submitted: {str(app.get('created_at', ''))[:10]}
                        </div>
                    </div>
                </div>

                <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; padding: 0.75rem 1rem; border-radius: 4px; border: 1px solid {COLOR_PALETTE['border']}; margin-top: 1rem;">
                    <div style="font-size: 0.8rem; font-weight: 600; color: {COLOR_PALETTE['cyan']};">Talent Acquisition Feedback:</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['main_text']}; margin-top: 0.25rem;">
                        {recruiter_notes}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Toggleable Full Scorecard Inspection
        if score_val is not None:
            with st.expander(f"🔍 View Official Shortlisting Scorecard ({app.get('application_number')})"):
                render_candidate_score_card(
                    score_pct=score_val,
                    is_shortlisted=(score_val >= 50),
                    application_id=app.get("application_number"),
                    recommendation=app.get("recommendation")
                )

    render_footer()
