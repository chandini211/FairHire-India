"""
FairHire India - Candidate Profile Management
Allows candidates to inspect and update their professional profile and contact details.
"""
import streamlit as st
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_candidate_profile, update_candidate_profile
from components.ui import render_section_heading
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Delhi (NCT)", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

def render_candidate_profile_page():
    """Render profile view and edit portal."""
    require_role(["candidate"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("My Candidate Profile", "Maintain your verified professional credentials and regional background.")

    profile = get_candidate_profile(user["id"]) or {}

    with st.form("edit_profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Full Name", value=user.get("full_name", ""), disabled=True)
            st.text_input("Registered Email", value=user.get("email", ""), disabled=True)
            phone = st.text_input("Contact Phone", value=user.get("phone", "") or "+91-9876543210")
            highest_education = st.selectbox(
                "Highest Education Level",
                options=["Bachelor's", "Master's", "PhD", "Other / Diploma"],
                index=1
            )
            college = st.text_input("College / University", value=profile.get("college_university", ""))

        with c2:
            current_state = profile.get("state", "Karnataka")
            state_idx = INDIAN_STATES.index(current_state) if current_state in INDIAN_STATES else 11
            state = st.selectbox("State of Residence", options=INDIAN_STATES, index=state_idx)
            city = st.text_input("City", value=profile.get("city", "Bengaluru"))
            experience_years = st.number_input("Total Years of Experience", min_value=0, max_value=40, value=profile.get("experience_years", 3))
            skills = st.text_input("Technical Skills", value=profile.get("skills", "Python, Machine Learning, SQL"))
            gender_audit = st.selectbox(
                "Demographic Audit Disclosure (Voluntary)",
                options=["Prefer not to say", "Female", "Male", "Non-Binary / Other"],
                index=0
            )

        bio = st.text_area("Professional Summary", value=profile.get("bio", "Experienced technologist committed to high-impact software engineering."))

        save_btn = st.form_submit_button("Save Profile Updates", type="primary", use_container_width=True)

        if save_btn:
            success = update_candidate_profile(
                user_id=user["id"],
                highest_education=highest_education,
                college_university=college,
                state=state,
                city=city,
                experience_years=int(experience_years),
                skills=skills,
                bio=bio,
                gender_audit=gender_audit
            )
            if success:
                st.success("Profile successfully updated.")
                st.rerun()
            else:
                st.error("Failed to update profile.")

    render_footer()
