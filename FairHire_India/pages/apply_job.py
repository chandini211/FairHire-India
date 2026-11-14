"""
FairHire India - Job Application Workflow
Allows candidates to browse active vacancies and submit applications with automated fairness pre-checks.
Includes the high-impact candidate score card with checkmark and percentage score.
"""
import streamlit as st
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import (
    get_jobs, get_candidate_profile, create_application,
    save_prediction, get_applications_by_candidate, get_application_by_id,
    update_candidate_profile, create_job
)
from ml.prediction import predict_candidate
from components.ui import (
    render_section_heading, render_disclaimer,
    render_candidate_hero_banner, render_candidate_score_card
)
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

INDIAN_STATES = [
    "Andhra Pradesh", "Karnataka", "Maharashtra", "Tamil Nadu", "Telangana",
    "Delhi NCR", "Uttar Pradesh", "West Bengal", "Gujarat", "Kerala",
    "Rajasthan", "Madhya Pradesh", "Punjab", "Haryana", "Odisha",
    "Bihar", "Assam", "Goa", "Uttarakhand", "Jharkhand", "Other"
]

INDIAN_CITIES = [
    "Visakhapatnam", "Bengaluru", "Hyderabad", "Mumbai", "Pune",
    "Chennai", "New Delhi", "Noida", "Gurugram", "Kolkata",
    "Ahmedabad", "Jaipur", "Kochi", "Coimbatore", "Indore",
    "Chandigarh", "Bhubaneswar", "Lucknow", "Nagpur", "Other"
]

TECH_ROLES = [
    "Python Developer",
    "Machine Learning Engineer - Responsible AI",
    "Senior Python Developer - Enterprise SaaS",
    "Data Scientist - People Analytics",
    "Cybersecurity & Compliance Specialist",
    "Data Scientist",
    "Full Stack Developer",
    "Cloud Solutions Architect"
]

def render_apply_job_page():
    """Render job application portal with exact user form and scorecard."""
    require_role(["candidate"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    # Top Candidate Hero Banner with Navigation Pills
    render_candidate_hero_banner(active_tab="apply_job")

    # If an application was just submitted, show success message and score card
    if "submitted_result" in st.session_state and st.session_state["submitted_result"]:
        res = st.session_state["submitted_result"]
        st.success("Application submitted successfully.")

        render_candidate_score_card(
            score_pct=res["score_pct"],
            is_shortlisted=res["is_shortlisted"],
            application_id=res["app_num"],
            recommendation=res.get("recommendation")
        )

        # Quick action buttons under scorecard
        btn_c1, btn_c2, btn_c3 = st.columns([3, 3, 3])
        with btn_c1:
            if st.button("📋 View in My Applications", type="primary", use_container_width=True):
                st.session_state["submitted_result"] = None
                st.session_state["current_page"] = "my_applications"
                st.rerun()
        with btn_c2:
            if st.button("📝 Submit Another Application", type="secondary", use_container_width=True):
                st.session_state["submitted_result"] = None
                st.rerun()
        with btn_c3:
            if st.button("ℹ️ About FairHire Governance", type="secondary", use_container_width=True):
                st.session_state["submitted_result"] = None
                st.session_state["current_page"] = "about"
                st.rerun()

        st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Candidate Application Form Header
    render_section_heading("Candidate Application Form", "Complete your details. Location can be updated via profile.")
    render_disclaimer()

    profile = get_candidate_profile(user["id"]) or {}
    jobs = get_jobs(status="Published")

    # Map candidate profile defaults
    prof_gender = profile.get("gender_audit") or "Female"
    if prof_gender not in ["Female", "Male", "Other / Non-binary", "Prefer not to disclose"]:
        prof_gender = "Female"

    prof_state = profile.get("state") or "Andhra Pradesh"
    if prof_state not in INDIAN_STATES:
        prof_state = "Andhra Pradesh"

    prof_city = profile.get("city") or "Visakhapatnam"
    if prof_city not in INDIAN_CITIES:
        prof_city = "Visakhapatnam"

    edu_options = ["Bachelor's Degree", "Master's Degree", "Doctorate / PhD", "Diploma / Other"]
    prof_edu = profile.get("highest_education") or "Bachelor's Degree"
    if prof_edu not in edu_options:
        prof_edu = "Bachelor's Degree"

    # Job Application Form
    with st.form("candidate_application_form", clear_on_submit=False):
        c1, c2 = st.columns(2)

        with c1:
            full_name = st.text_input("Candidate Full Name *", value=user.get("full_name", ""))
            gender = st.selectbox("Gender", options=["Female", "Male", "Other / Non-binary", "Prefer not to disclose"], index=["Female", "Male", "Other / Non-binary", "Prefer not to disclose"].index(prof_gender))
            education_selection = st.selectbox("Education Level *", options=edu_options, index=edu_options.index(prof_edu))
            experience_years = st.number_input("Years of Experience *", min_value=0, max_value=35, value=int(profile.get("experience_years", 1)))
            skills_input = st.text_area("Skills *", value=profile.get("skills", "Python, Machine Learning, SQL"), height=85)

        with c2:
            st.text_input("Country", value="India", disabled=True)
            state_selection = st.selectbox("Indian State / Union Territory *", options=INDIAN_STATES, index=INDIAN_STATES.index(prof_state))
            city_selection = st.selectbox("Indian City *", options=INDIAN_CITIES, index=INDIAN_CITIES.index(prof_city))
            desired_salary = st.number_input("Desired Annual Salary (₹) *", min_value=100000, max_value=10000000, value=400000, step=50000)
            role_selection = st.selectbox("Desired Job Role *", options=TECH_ROLES, index=0)

        # Technical Competency & Evaluation Details
        with st.expander("Technical Assessment & Screening Scores", expanded=False):
            st.caption("Standardized assessment scores calibrated for technical evaluation. Demographics are excluded from scoring.")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                skill_score = st.slider("Technical Assessment Score (0-100)", min_value=0.0, max_value=100.0, value=82.0)
                previous_companies = st.number_input("Previous Employers", min_value=0, max_value=10, value=1)
            with col_b:
                personality_score = st.slider("Workplace Competency / Culture Score (0-100)", min_value=0.0, max_value=100.0, value=80.0)
                distance = st.number_input("Distance from Company Office (km)", min_value=1.0, max_value=80.0, value=12.0)
            with col_c:
                interview_score = st.slider("Screening / Interview Score (0-100)", min_value=0.0, max_value=100.0, value=85.0)
                age = st.number_input("Candidate Age", min_value=18, max_value=65, value=28)

        st.markdown(
            f"""
            <div style="font-size: 0.78rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.5rem; margin-bottom: 1rem;">
                <strong>Responsible AI Transparency:</strong> Candidate gender is strictly excluded from feature vectors during machine learning inference. AI predictions serve as decision-support signals for human recruiters.
            </div>
            """,
            unsafe_allow_html=True
        )

        submit = st.form_submit_button("✨ Analyze Candidate", type="primary", use_container_width=True)

        if submit:
            try:
                # 1. Map Education to Numeric encoding
                edu_map = {"Bachelor's Degree": 1, "Master's Degree": 2, "Doctorate / PhD": 3, "Diploma / Other": 4}
                education_level = edu_map.get(education_selection, 2)

                # 2. Match or locate Target Job in SQLite
                target_job = next((j for j in jobs if j["title"].lower() == role_selection.lower()), None)
                if not target_job:
                    # Find closest match or fallback to first job, or create it
                    if jobs:
                        target_job = jobs[0]
                    else:
                        job_id = create_job(
                            title=role_selection,
                            department="Engineering",
                            description=f"Opportunity for {role_selection} in high-growth enterprise environment.",
                            required_skills=skills_input,
                            education_requirements=education_selection,
                            experience_requirements=int(experience_years),
                            location=city_selection,
                            employment_type="Full-time",
                            status="Published",
                            created_by=1
                        )
                        target_job = {"id": job_id, "title": role_selection}

                job_id = target_job["id"]

                # 3. Check for existing application for this job
                existing_apps = get_applications_by_candidate(user["id"])
                if any(a["job_id"] == job_id for a in existing_apps):
                    # Delete old application to allow re-analysis
                    from database.db import get_db
                    with get_db() as conn:
                        conn.execute("DELETE FROM applications WHERE candidate_id = ? AND job_id = ?", (user["id"], job_id))

                # 4. Insert Application into SQLite
                phone = user.get("phone", "") or "+91-9876543210"
                app_id = create_application(
                    job_id=job_id,
                    candidate_id=user["id"],
                    candidate_name=full_name or user.get("full_name", "Candidate"),
                    candidate_email=user.get("email", ""),
                    candidate_phone=phone,
                    education_level=education_level,
                    experience_years=int(experience_years),
                    previous_companies=int(previous_companies),
                    distance_from_company=float(distance),
                    skill_score=float(skill_score),
                    personality_score=float(personality_score),
                    interview_score=float(interview_score),
                    recruitment_strategy=1 # Online application
                )

                # 5. Update Candidate Profile in SQLite
                update_candidate_profile(
                    user_id=user["id"],
                    highest_education=education_selection,
                    college_university=profile.get("college_university") or "State University",
                    state=state_selection,
                    city=city_selection,
                    experience_years=int(experience_years),
                    skills=skills_input,
                    bio=profile.get("bio") or f"Experienced {role_selection} seeking impact-driven engineering roles.",
                    gender_audit=gender
                )

                # 6. Run Machine Learning Shortlisting Prediction (Random Forest)
                pred_input = {
                    "Age": int(age),
                    "EducationLevel": education_level,
                    "ExperienceYears": int(experience_years),
                    "PreviousCompanies": int(previous_companies),
                    "DistanceFromCompany": float(distance),
                    "InterviewScore": float(interview_score),
                    "SkillScore": float(skill_score),
                    "PersonalityScore": float(personality_score),
                    "RecruitmentStrategy": 1
                }

                pred_result = predict_candidate(pred_input, model_name="Random Forest")

                # Save prediction to database
                save_prediction(
                    application_id=app_id,
                    model_name=pred_result["model_name"],
                    prediction_label=pred_result["prediction_label"],
                    prediction_probability=pred_result["prediction_probability"],
                    recommendation=pred_result["recommendation"]
                )

                # Fetch application to retrieve generated application number
                created_app = get_application_by_id(app_id)
                app_num = created_app.get("application_number") if created_app else f"FH-APP{app_id}"

                score_pct = int(round(pred_result["prediction_probability"] * 100))
                is_shortlisted = (pred_result["prediction_label"] == 1 or score_pct >= 50)

                # Update application status in DB
                if is_shortlisted:
                    from database.db import update_application_status
                    update_application_status(app_id, "Shortlisted", "Automated pre-screening qualified for technical recruiter review.")

                # Save result in session state to render immediate scorecard
                st.session_state["submitted_result"] = {
                    "app_id": app_id,
                    "app_num": app_num,
                    "score_pct": score_pct,
                    "is_shortlisted": is_shortlisted,
                    "recommendation": pred_result["recommendation"]
                }

                st.rerun()

            except Exception as e:
                st.error(f"Failed to submit application: {str(e)}")

    render_footer()
