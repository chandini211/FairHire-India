"""
FairHire India - Recruiter Job Management Portal
Create, edit, publish, close, and monitor applicant pipelines for job vacancies.
"""
import streamlit as st
import pandas as pd
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_jobs, get_job_by_id, create_job, update_job, update_job_status, get_all_applications
from components.ui import render_section_heading, render_disclaimer, render_metric_card
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

def render_manage_jobs_page():
    """Render recruiter vacancy management portal."""
    require_role(["recruiter", "admin"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Manage Job Vacancies", "Create, edit, and govern recruitment campaigns across talent pipelines.")
    render_disclaimer()

    all_jobs = get_jobs()
    all_apps = get_all_applications()

    # Application count per job
    app_counts = {}
    for a in all_apps:
        jid = a["job_id"]
        app_counts[jid] = app_counts.get(jid, 0) + 1

    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Campaigns", str(len(all_jobs)), "Configured Vacancies")
    with c2:
        pub_count = len([j for j in all_jobs if j["status"] == "Published"])
        render_metric_card("Published Jobs", str(pub_count), "Accepting Candidates", is_positive=True)
    with c3:
        draft_count = len([j for j in all_jobs if j["status"] == "Draft"])
        render_metric_card("Draft Jobs", str(draft_count), "Under Preparation")
    with c4:
        closed_count = len([j for j in all_jobs if j["status"] == "Closed"])
        render_metric_card("Closed Jobs", str(closed_count), "Completed Campaigns")

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    tab_list, tab_create, tab_edit = st.tabs(["Active Vacancies", "Create New Vacancy", "Edit Existing Job"])

    # ---------------- TAB 1: ACTIVE VACANCIES LIST ----------------
    with tab_list:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Current Job Openings Directory</div>", unsafe_allow_html=True)

        job_table_rows = []
        for j in all_jobs:
            jid = j["id"]
            job_table_rows.append({
                "Job ID": f"JOB-{jid:03d}",
                "Job Title": j["title"],
                "Department": j["department"],
                "Location": j["location"],
                "Type": j["employment_type"],
                "Status": j["status"],
                "Min Exp": f"{j['experience_requirements']} Yrs",
                "Applicants": app_counts.get(jid, 0),
                "Created Date": str(j["created_at"])[:10]
            })

        df_jobs = pd.DataFrame(job_table_rows)
        st.dataframe(df_jobs, use_container_width=True, hide_index=True)

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        # Quick Status Toggle Box
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-bottom: 0.5rem;'>Quick Status Controller</div>", unsafe_allow_html=True)
        q_c1, q_c2, q_c3 = st.columns([4, 3, 2])
        with q_c1:
            toggle_options = {f"{j['title']} ({j['status']})": j["id"] for j in all_jobs}
            sel_toggle_label = st.selectbox("Select Target Campaign", options=list(toggle_options.keys()))
            target_toggle_id = toggle_options[sel_toggle_label]
        with q_c2:
            new_st = st.selectbox("Update Campaign Status", options=["Published", "Draft", "Closed"])
        with q_c3:
            st.markdown("<div style='padding-top: 1.7rem;'></div>", unsafe_allow_html=True)
            if st.button("Apply Status Change", type="primary", use_container_width=True):
                update_job_status(target_toggle_id, new_st, user_id=user["id"])
                st.success("Campaign status updated.")
                st.rerun()

    # ---------------- TAB 2: CREATE NEW VACANCY ----------------
    with tab_create:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Post a New Position</div>", unsafe_allow_html=True)

        with st.form("create_job_form", clear_on_submit=True):
            f1, f2 = st.columns(2)
            with f1:
                title = st.text_input("Job Title *", placeholder="e.g. Lead Machine Learning Engineer")
                dept = st.selectbox("Department *", options=[
                    "AI & Advanced Analytics", "Platform Engineering", "Human Capital Intelligence",
                    "Information Security", "Cloud Infrastructure", "Product & Design", "Quality Assurance"
                ])
                loc = st.text_input("Location *", placeholder="e.g. Bengaluru, Karnataka (Hybrid)")
                emp_type = st.selectbox("Employment Type", options=["Full-time", "Contract", "Hybrid", "Remote"])
            with f2:
                req_skills = st.text_input("Required Skills (comma-separated) *", placeholder="Python, Fairlearn, SHAP, PyTorch, SQL")
                edu_req = st.text_input("Education Requirements *", value="Bachelor's or Master's in Computer Science or related STEM field")
                min_exp = st.number_input("Minimum Required Experience (Years)", min_value=0, max_value=25, value=3)
                init_status = st.selectbox("Initial Publish Status", options=["Published", "Draft"])

            desc = st.text_area("Detailed Job Description *", placeholder="Outline core responsibilities, technical expectations, and collaborative team goals...", height=120)

            post_btn = st.form_submit_button("Create and Deploy Campaign", type="primary", use_container_width=True)

            if post_btn:
                if not title.strip() or not req_skills.strip() or not desc.strip():
                    st.error("Please fill in all required fields (Title, Skills, Description).")
                else:
                    new_id = create_job(
                        title=title.strip(),
                        department=dept,
                        description=desc.strip(),
                        required_skills=req_skills.strip(),
                        education_requirements=edu_req.strip(),
                        experience_requirements=int(min_exp),
                        location=loc.strip(),
                        employment_type=emp_type,
                        status=init_status,
                        created_by=user["id"]
                    )
                    st.success(f"Job campaign '{title}' successfully created with ID #{new_id}!")
                    st.rerun()

    # ---------------- TAB 3: EDIT EXISTING JOB ----------------
    with tab_edit:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Modify Existing Vacancy Details</div>", unsafe_allow_html=True)

        edit_job_options = {f"{j['title']} (ID: {j['id']})": j["id"] for j in all_jobs}
        sel_edit_label = st.selectbox("Select Job to Edit", options=list(edit_job_options.keys()))
        target_edit_id = edit_job_options[sel_edit_label]
        target_job = get_job_by_id(target_edit_id)

        if target_job:
            with st.form(f"edit_form_{target_edit_id}"):
                ef1, ef2 = st.columns(2)
                with ef1:
                    e_title = st.text_input("Job Title", value=target_job["title"])
                    e_dept = st.text_input("Department", value=target_job["department"])
                    e_loc = st.text_input("Location", value=target_job["location"])
                    e_emp_type = st.selectbox("Employment Type", options=["Full-time", "Contract", "Hybrid", "Remote"],
                                              index=["Full-time", "Contract", "Hybrid", "Remote"].index(target_job["employment_type"]) if target_job["employment_type"] in ["Full-time", "Contract", "Hybrid", "Remote"] else 0)
                with ef2:
                    e_skills = st.text_input("Required Skills", value=target_job["required_skills"])
                    e_edu = st.text_input("Education Requirements", value=target_job["education_requirements"])
                    e_exp = st.number_input("Minimum Experience", min_value=0, max_value=25, value=target_job["experience_requirements"])
                    e_status = st.selectbox("Campaign Status", options=["Published", "Draft", "Closed"],
                                            index=["Published", "Draft", "Closed"].index(target_job["status"]) if target_job["status"] in ["Published", "Draft", "Closed"] else 0)

                e_desc = st.text_area("Job Description", value=target_job["description"], height=120)

                save_edit_btn = st.form_submit_button("Save Changes to Vacancy", type="primary", use_container_width=True)

                if save_edit_btn:
                    success = update_job(
                        job_id=target_edit_id,
                        title=e_title,
                        department=e_dept,
                        description=e_desc,
                        required_skills=e_skills,
                        education_requirements=e_edu,
                        experience_requirements=int(e_exp),
                        location=e_loc,
                        employment_type=e_emp_type,
                        status=e_status,
                        user_id=user["id"]
                    )
                    if success:
                        st.success("Vacancy details successfully updated.")
                        st.rerun()
                    else:
                        st.error("Failed to update vacancy.")

    render_footer()
