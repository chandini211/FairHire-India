"""
FairHire India - Recruiter Overview Dashboard
Executive recruitment metrics, live application analytics, and distribution charts derived from SQLite.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_dashboard_stats, get_all_applications, get_jobs
from components.ui import render_section_heading, render_metric_card, render_disclaimer
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.charts import DARK_LAYOUT
from components.footer import render_footer

def render_recruiter_dashboard():
    """Render executive recruiter overview."""
    require_role(["recruiter", "admin"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Recruitment Intelligence Overview", "Live talent acquisition metrics, pipeline velocity, and audit compliance.")
    render_disclaimer()

    # Query live database metrics
    stats = get_dashboard_stats()
    apps = get_all_applications()
    jobs = get_jobs()

    # Metric KPI Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Candidates", str(stats["total_candidates"]), "Registered Applicants")
    with c2:
        render_metric_card("Total Applications", str(stats["total_applications"]), "Active Dossiers")
    with c3:
        render_metric_card("Shortlisted", str(stats["shortlisted"]), "Recruiter Endorsed", is_positive=True)
    with c4:
        render_metric_card("Pending Review", str(stats["pending_review"]), "Awaiting Human Sign-Off")

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Charts Grid
    if apps:
        df_apps = pd.DataFrame(apps)

        ch_col1, ch_col2 = st.columns(2)

        with ch_col1:
            # Job-wise application distribution
            job_counts = df_apps["job_title"].value_counts().reset_index()
            job_counts.columns = ["Job Title", "Applications"]

            fig_job = px.bar(
                job_counts,
                x="Applications",
                y="Job Title",
                orientation="h",
                color_discrete_sequence=[COLOR_PALETTE["cyan"]]
            )
            fig_job.update_layout(
                title=dict(text="Application Volume by Job Opening", font=dict(family="Space Grotesk, sans-serif", size=15, color=COLOR_PALETTE["main_text"])),
                xaxis=dict(title=dict(text="Applications", font=dict(color=COLOR_PALETTE["cyan"], size=13)), tickfont=dict(color=COLOR_PALETTE["main_text"], size=11)),
                yaxis=dict(title=dict(text="Job Title", font=dict(color=COLOR_PALETTE["cyan"], size=13)), tickfont=dict(color=COLOR_PALETTE["main_text"], size=11)),
                **DARK_LAYOUT
            )
            st.plotly_chart(fig_job, use_container_width=True)

        with ch_col2:
            # Application status distribution
            status_counts = df_apps["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]

            fig_status = px.pie(
                status_counts,
                names="Status",
                values="Count",
                hole=0.45,
                color_discrete_sequence=[
                    COLOR_PALETTE["primary_purple"],
                    COLOR_PALETTE["cyan"],
                    COLOR_PALETTE["success_green"],
                    COLOR_PALETTE["warning_amber"],
                    COLOR_PALETTE["danger_red"]
                ]
            )
            fig_status.update_layout(
                title=dict(text="Pipeline Status Breakdown", font=dict(family="Space Grotesk, sans-serif", size=15, color=COLOR_PALETTE["main_text"])),
                legend=dict(font=dict(color=COLOR_PALETTE["main_text"], size=12)),
                **DARK_LAYOUT
            )
            st.plotly_chart(fig_status, use_container_width=True)

        ch_col3, ch_col4 = st.columns(2)

        with ch_col3:
            # Experience distribution
            fig_exp = px.histogram(
                df_apps,
                x="experience_years",
                nbins=10,
                color_discrete_sequence=[COLOR_PALETTE["primary_purple"]]
            )
            fig_exp.update_layout(
                title=dict(text="Candidate Experience Distribution (Years)", font=dict(family="Space Grotesk, sans-serif", size=15, color=COLOR_PALETTE["main_text"])),
                xaxis=dict(title=dict(text="Years of Experience", font=dict(color=COLOR_PALETTE["cyan"], size=13)), tickfont=dict(color=COLOR_PALETTE["main_text"], size=11)),
                yaxis=dict(title=dict(text="Count", font=dict(color=COLOR_PALETTE["cyan"], size=13)), tickfont=dict(color=COLOR_PALETTE["main_text"], size=11)),
                **DARK_LAYOUT
            )
            st.plotly_chart(fig_exp, use_container_width=True)

        with ch_col4:
            # Education distribution
            edu_labels = {1: "Bachelor's", 2: "Master's", 3: "PhD", 4: "Other / Diploma"}
            df_apps["edu_named"] = df_apps["education_level"].map(edu_labels).fillna("Master's")
            edu_counts = df_apps["edu_named"].value_counts().reset_index()
            edu_counts.columns = ["Education", "Count"]

            fig_edu = px.bar(
                edu_counts,
                x="Education",
                y="Count",
                color_discrete_sequence=[COLOR_PALETTE["warning_amber"]]
            )
            fig_edu.update_layout(
                title=dict(text="Candidate Educational Qualifications", font=dict(family="Space Grotesk, sans-serif", size=15, color=COLOR_PALETTE["main_text"])),
                xaxis=dict(title=dict(text="Education", font=dict(color=COLOR_PALETTE["cyan"], size=13)), tickfont=dict(color=COLOR_PALETTE["main_text"], size=11)),
                yaxis=dict(title=dict(text="Count", font=dict(color=COLOR_PALETTE["cyan"], size=13)), tickfont=dict(color=COLOR_PALETTE["main_text"], size=11)),
                **DARK_LAYOUT
            )
            st.plotly_chart(fig_edu, use_container_width=True)

    else:
        st.info("No applications submitted in the database yet.")

    render_footer()
