"""
FairHire India - Candidate Sign Up Page
Enterprise candidate registration with form validation, password strength checks, and Bcrypt hashing.
"""
import streamlit as st
from config import COLOR_PALETTE
from auth.registration import register_candidate
from components.ui import render_section_heading

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Delhi (NCT)", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

EDUCATION_LEVELS = [
    "Bachelor's (B.Tech / B.E / B.Sc / B.Com / BCA)",
    "Master's (M.Tech / M.E / M.Sc / MCA / MBA)",
    "PhD / Doctorate",
    "Other / Diploma / Secondary"
]

def render_signup_page():
    """Render the candidate registration portal."""
    cols_top = st.columns([1, 8, 2])
    with cols_top[0]:
        if st.button("← Home", key="back_home_signup"):
            st.session_state["current_page"] = "landing"
            st.rerun()

    st.markdown("<div style='max-width: 680px; margin: 1.5rem auto 0 auto;'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 1.75rem;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.75rem; font-weight: 700; color: {COLOR_PALETTE['cyan']};">
                Create Candidate Account
            </div>
            <div style="font-size: 0.9rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.25rem;">
                Join FairHire India for unbiased, transparent opportunity evaluation
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("signup_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("Full Name *", placeholder="e.g. Ananya Sen")
            email = st.text_input("Email Address *", placeholder="name@example.com")
            phone = st.text_input("Phone Number *", placeholder="+91-9876543210")
        with c2:
            password = st.text_input("Password *", type="password", help="Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 symbol")
            confirm_password = st.text_input("Confirm Password *", type="password")
            gender_audit = st.selectbox(
                "Demographic Audit Disclosure (Voluntary)",
                options=["Prefer not to say", "Female", "Male", "Non-Binary / Other"],
                help="Protected attributes are NEVER used for candidate shortlisting models. Used solely for aggregate Fairlearn compliance auditing."
            )

        st.markdown(f"<div style='border-top: 1px solid {COLOR_PALETTE['border']}; margin: 1rem 0;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.5rem;'>Educational & Regional Profile</div>", unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            highest_education = st.selectbox("Highest Education Level *", options=EDUCATION_LEVELS)
            college_university = st.text_input("College / University *", placeholder="e.g. Jadavpur University, Kolkata")
            experience_years = st.number_input("Years of Experience", min_value=0, max_value=40, value=2)
        with c4:
            state = st.selectbox("Current State *", options=INDIAN_STATES)
            city = st.text_input("City *", placeholder="e.g. Kolkata")
            skills = st.text_input("Key Skills (comma-separated)", placeholder="Python, Machine Learning, SQL, PyTorch")

        bio = st.text_area("Professional Summary", placeholder="Brief overview of your technical background and career objectives...")

        st.markdown(
            f"""
            <div style="font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']}; margin: 0.75rem 0;">
                By signing up, you acknowledge that candidate evaluations on FairHire India are reviewed by human talent partners.
                Automated rejections are disabled by design.
            </div>
            """,
            unsafe_allow_html=True
        )

        submit = st.form_submit_button("Complete Registration", type="primary", use_container_width=True)

        if submit:
            success, msg, uid = register_candidate(
                full_name=full_name,
                email=email,
                phone=phone,
                password=password,
                confirm_password=confirm_password,
                highest_education=highest_education,
                college_university=college_university,
                state=state,
                city=city,
                gender_audit=gender_audit,
                experience_years=experience_years,
                skills=skills,
                bio=bio
            )
            if success:
                st.success(f"{msg} Redirecting to sign in...")
                st.session_state["current_page"] = "login"
                st.rerun()
            else:
                st.error(msg)

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']};">
            Already registered on FairHire?
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Sign In to Existing Account", key="btn_to_login_from_signup", use_container_width=True, type="secondary"):
        st.session_state["current_page"] = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
