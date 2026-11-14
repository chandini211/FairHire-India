"""
FairHire India — AI-Powered Fair Candidate Shortlisting System
Recruitment Without Bias. By Design.

Main Application Entry Point.
Run with: streamlit run app.py
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st

# Streamlit Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="FairHire India — Recruitment Without Bias. By Design.",
    page_icon=str(BASE_DIR / "assets" / "favicon.png") if (BASE_DIR / "assets" / "favicon.png").exists() else "⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System CSS
from components.ui import inject_custom_css
inject_custom_css()

# Database & Environment Bootstrapping
from database.db import init_db
from database.seed import seed_database
from config import DB_PATH, MODEL_METRICS_PATH, FAIRNESS_METRICS_PATH

@st.cache_resource
def bootstrap_system():
    """Ensure database schema, seed data, and ML artifacts exist."""
    if not DB_PATH.exists():
        seed_database()
    else:
        init_db()

    if not MODEL_METRICS_PATH.exists():
        from ml.model_training import train_all_models
        train_all_models()

    if not FAIRNESS_METRICS_PATH.exists():
        from fairness.mitigation import run_mitigation_experiment
        run_mitigation_experiment()

bootstrap_system()

# Import Page Controllers
from pages.landing import render_landing_page
from pages.login import render_login_page
from pages.signup import render_signup_page
from pages.candidate_dashboard import render_candidate_dashboard
from pages.browse_jobs import render_browse_jobs_page
from pages.apply_job import render_apply_job_page
from pages.my_applications import render_my_applications_page
from pages.candidate_profile import render_candidate_profile_page
from pages.notifications import render_notifications_page

from pages.recruiter_dashboard import render_recruiter_dashboard
from pages.manage_jobs import render_manage_jobs_page
from pages.manage_candidates import render_manage_candidates_page
from pages.candidate_search import render_candidate_search_page
from pages.candidate_profiles_view import render_candidate_profiles_view
from pages.model_analytics import render_model_analytics_page
from pages.fairness_dashboard import render_fairness_dashboard_page
from pages.explainability_dashboard import render_explainability_dashboard_page
from pages.reports_exports import render_reports_exports_page
from pages.audit_logs_view import render_audit_logs_view
from pages.about import render_about_page

# Route Dispatcher
def main():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "landing"

    page = st.session_state["current_page"]

    page_router = {
        # Public Pages
        "landing": render_landing_page,
        "login": render_login_page,
        "signup": render_signup_page,
        "about": render_about_page,

        # Candidate Portal (Section 5)
        "candidate_dashboard": render_candidate_dashboard,
        "browse_jobs": render_browse_jobs_page,
        "apply_job": render_apply_job_page,
        "my_applications": render_my_applications_page,
        "candidate_profile": render_candidate_profile_page,
        "notifications": render_notifications_page,

        # Recruiter Portal (Section 6)
        "recruiter_dashboard": render_recruiter_dashboard,
        "manage_jobs": render_manage_jobs_page,
        "manage_candidates": render_manage_candidates_page,
        "candidate_search": render_candidate_search_page,
        "candidate_profiles_view": render_candidate_profiles_view,
        "model_analytics": render_model_analytics_page,
        "fairness_dashboard": render_fairness_dashboard_page,
        "explainability_dashboard": render_explainability_dashboard_page,
        "reports_exports": render_reports_exports_page,
        "audit_logs_view": render_audit_logs_view
    }

    controller = page_router.get(page, render_landing_page)
    controller()

if __name__ == "__main__":
    main()
