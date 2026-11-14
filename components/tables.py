"""
FairHire India - Custom Formatted Tables
Renders dataframes and lists with dark enterprise styling and status badges.
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from config import COLOR_PALETTE

def render_applications_table(applications: List[Dict[str, Any]]):
    """Render formatted applications list with interactive indicators."""
    if not applications:
        st.markdown(
            f"""
            <div class="fairhire-card" style="text-align: center; padding: 2rem;">
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.95rem;">No applications found matching the selected criteria.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    table_rows = []
    for app in applications:
        status = app.get("status", "Submitted")
        if status in ["Shortlisted", "Selected"]:
            badge_class = "badge-green"
        elif status in ["Under Review", "Awaiting Human Review"]:
            badge_class = "badge-amber"
        else:
            badge_class = "badge-purple"

        prob = app.get("prediction_probability")
        prob_str = f"{prob * 100:.1f}%" if prob is not None else "N/A"

        table_rows.append({
            "App #": app.get("application_number"),
            "Candidate": app.get("candidate_name"),
            "Job Title": app.get("job_title"),
            "Experience": f"{app.get('experience_years', 0)} Yrs",
            "Skill Score": f"{app.get('skill_score', 0):.0f}/100",
            "AI Match Score": prob_str,
            "Status": status,
            "Applied Date": str(app.get("created_at", ""))[:10]
        })

    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
