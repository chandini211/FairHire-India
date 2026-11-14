"""
FairHire India - Recruiter Candidate Profiles Directory
Inspect comprehensive applicant profiles, educational backgrounds, and verified technical credentials.
"""
import streamlit as st
import pandas as pd
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_candidate_profiles_list, get_applications_by_candidate
from components.ui import render_section_heading, render_disclaimer
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

def render_candidate_profiles_view():
    """Render full candidate directory and deep-dive profile view."""
    require_role(["recruiter", "admin"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Candidate Profiles Directory", "Browse comprehensive professional credentials, academic history, and regional distribution.")
    render_disclaimer()

    q_search = st.text_input("🔍 Filter Profiles by Name, Skill, or Institution", placeholder="e.g. Jadavpur, Python, Bengaluru...")
    profiles = get_candidate_profiles_list(query_text=q_search)

    st.markdown(f"<div style='font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-bottom: 1.25rem;'>Showing <strong>{len(profiles)}</strong> registered talent profile(s)</div>", unsafe_allow_html=True)

    if not profiles:
        st.info("No candidate profiles found matching your query.")
        render_footer()
        return

    # Two-column grid layout of candidate profile cards
    cols = st.columns(2)
    for idx, p in enumerate(profiles):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="fairhire-card" style="height: 100%; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 600; color: {COLOR_PALETTE['main_text']};">
                                {p['full_name']}
                            </div>
                            <div style="font-size: 0.85rem; color: {COLOR_PALETTE['cyan']}; margin-top: 0.15rem;">
                                {p['email']} · {p.get('phone', 'N/A')}
                            </div>
                        </div>
                        <div>
                            <span class="compliance-badge badge-purple">{p.get('highest_education', 'Graduate')}</span>
                        </div>
                    </div>

                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin: 0.75rem 0 0.5rem 0; line-height: 1.5;">
                        🏫 <strong>Institution:</strong> {p.get('college_university', 'N/A')}<br/>
                        📍 <strong>Location:</strong> {p.get('city', 'N/A')}, {p.get('state', 'N/A')}<br/>
                        💼 <strong>Experience:</strong> {p.get('experience_years', 0)} Years<br/>
                        🛠️ <strong>Key Skills:</strong> {p.get('skills', 'N/A')}
                    </div>

                    <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; padding: 0.6rem 0.85rem; border-radius: 4px; border: 1px solid {COLOR_PALETTE['border']}; font-size: 0.8rem; color: {COLOR_PALETTE['main_text']}; margin-top: 0.5rem;">
                        <em>"{p.get('bio', 'Passionate technology professional.')}"</em>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']};">
                        <div>Total Applications: <strong>{p.get('application_count', 0)}</strong></div>
                        <div>Member Since: {str(p.get('member_since', ''))[:10]}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    render_footer()
