"""
Automated Tests — Application Integration & Report Deliverables Suite
Verifies all 20 Streamlit page controller imports, notifications, job management, and document export files.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from utils.exports import (
    generate_dataset_doc_pdf, generate_model_evaluation_pdf,
    generate_fairness_report_pdf, generate_project_report_pdf,
    generate_presentation_pptx
)
from database.db import create_notification, get_notifications_by_user, mark_notification_as_read, update_job, get_job_by_id

def test_page_modules_importability():
    """Verify all 20 Streamlit page controllers import cleanly without syntax or import errors."""
    import pages.landing
    import pages.login
    import pages.signup
    import pages.candidate_dashboard
    import pages.browse_jobs
    import pages.apply_job
    import pages.my_applications
    import pages.candidate_profile
    import pages.notifications
    import pages.recruiter_dashboard
    import pages.manage_jobs
    import pages.manage_candidates
    import pages.candidate_search
    import pages.candidate_profiles_view
    import pages.model_analytics
    import pages.fairness_dashboard
    import pages.explainability_dashboard
    import pages.reports_exports
    import pages.audit_logs_view
    import pages.about

    assert pages.landing.render_landing_page is not None
    assert pages.recruiter_dashboard.render_recruiter_dashboard is not None
    assert pages.candidate_dashboard.render_candidate_dashboard is not None
    assert pages.browse_jobs.render_browse_jobs_page is not None
    assert pages.notifications.render_notifications_page is not None
    assert pages.manage_jobs.render_manage_jobs_page is not None
    assert pages.candidate_search.render_candidate_search_page is not None

def test_notification_operations():
    """Verify notification insertion, retrieval, and read status toggling."""
    nid = create_notification(
        user_id=1,
        title="Test Notification",
        message="Verifying notification system operation",
        link_page="my_applications"
    )
    assert nid > 0

    notifs = get_notifications_by_user(1)
    assert any(n["id"] == nid for n in notifs)

    success = mark_notification_as_read(nid)
    assert success is True

def test_candidate_apply_and_score():
    """Verify candidate application workflow, ML prediction generation, and shortlisting score."""
    from database.db import create_user, create_job, create_application, save_prediction, get_application_by_id
    from ml.prediction import predict_candidate
    import uuid

    uid_str = uuid.uuid4().hex[:6]
    uid = create_user(
        email=f"candidate_{uid_str}@fairhire.in",
        password_hash="testhash123",
        full_name="Chandi Priya",
        role="candidate"
    )
    assert uid > 0

    jid = create_job(
        title=f"Python Developer - {uid_str}",
        department="Engineering",
        description="Enterprise Python role.",
        required_skills="Python, SQL",
        education_requirements="Bachelor's",
        experience_requirements=2,
        location="Visakhapatnam",
        employment_type="Full-time",
        created_by=1
    )
    assert jid > 0

    app_id = create_application(
        job_id=jid,
        candidate_id=uid,
        candidate_name="Chandi Priya",
        candidate_email=f"candidate_{uid_str}@fairhire.in",
        candidate_phone="+91-9876543210",
        education_level=2,
        experience_years=3,
        previous_companies=1,
        distance_from_company=8.5,
        skill_score=85.0,
        personality_score=80.0,
        interview_score=82.0,
        recruitment_strategy=1
    )
    assert app_id > 0

    pred_res = predict_candidate({
        "Age": 27,
        "EducationLevel": 2,
        "ExperienceYears": 3,
        "PreviousCompanies": 1,
        "DistanceFromCompany": 8.5,
        "InterviewScore": 82.0,
        "SkillScore": 85.0,
        "PersonalityScore": 80.0,
        "RecruitmentStrategy": 1
    }, model_name="Random Forest")

    assert "prediction_probability" in pred_res
    assert 0.0 <= pred_res["prediction_probability"] <= 1.0

    pred_id = save_prediction(
        application_id=app_id,
        model_name=pred_res["model_name"],
        prediction_label=pred_res["prediction_label"],
        prediction_probability=pred_res["prediction_probability"],
        recommendation=pred_res["recommendation"]
    )
    assert pred_id > 0

    app = get_application_by_id(app_id)
    assert app is not None
    assert app["prediction_probability"] == pred_res["prediction_probability"]
    assert app["application_number"].startswith("FH-")

def test_plotly_charts_and_dark_layout():
    """Verify that all Plotly figures in components/charts.py compile without ValueError or deprecated properties."""
    from components.charts import (
        plot_confusion_matrix, plot_roc_comparison,
        plot_feature_importance_bar, plot_fairness_parity_comparison,
        plot_mitigation_radar_or_bars, plot_shap_explanation, DARK_LAYOUT
    )

    # Verify axis configuration doesn't have invalid 'titlefont'
    assert "titlefont" not in DARK_LAYOUT.get("xaxis", {})
    assert "titlefont" not in DARK_LAYOUT.get("yaxis", {})

    fig_cm = plot_confusion_matrix([[40, 10], [5, 45]], "Random Forest")
    assert fig_cm is not None

    fig_roc = plot_roc_comparison({
        "Random Forest": {
            "metrics": {
                "roc_curve": {"fpr": [0, 0.1, 1], "tpr": [0, 0.85, 1]},
                "roc_auc": 0.92
            }
        }
    })
    assert fig_roc is not None

    fig_fi = plot_feature_importance_bar({"SkillScore": 0.5, "Interview": 0.3})
    assert fig_fi is not None

def test_metric_card_html_rendering():
    """Verify that render_metric_card produces valid HTML without 4-space markdown code-block indentation."""
    from components.ui import render_metric_card
    import streamlit as st

    rendered_content = []
    orig_markdown = st.markdown

    def capture_markdown(body, *args, **kwargs):
        rendered_content.append(body)
        return orig_markdown(body, *args, **kwargs)

    st.markdown = capture_markdown
    try:
        render_metric_card("Total Candidates", "42", "Registered Applicants")
        assert len(rendered_content) > 0
        card = rendered_content[-1]
        # Verify card starts with HTML tag and has no markdown code-block indentation on line 1
        assert card.startswith('<div class="fairhire-card"')
        assert not card.startswith("    ")
    finally:
        st.markdown = orig_markdown

def test_deliverable_artifacts_generation():
    """Verify PDF reports and PPTX presentation generate successfully."""
    p1 = generate_dataset_doc_pdf()
    p2 = generate_model_evaluation_pdf()
    p3 = generate_fairness_report_pdf()
    p4 = generate_project_report_pdf()
    p5 = generate_presentation_pptx()

    assert p1.exists() and p1.stat().st_size > 0
    assert p2.exists() and p2.stat().st_size > 0
    assert p3.exists() and p3.stat().st_size > 0
    assert p4.exists() and p4.stat().st_size > 0
    assert p5.exists() and p5.stat().st_size > 0
