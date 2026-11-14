"""
FairHire India - Explainable AI Dashboard (SHAP & LIME)
Global and local feature attribution for algorithmic transparency and auditability.
"""
import streamlit as st
import pandas as pd
import joblib

from config import COLOR_PALETTE, MODEL_METRICS_PATH
from auth.authorization import require_role
from explainability.shap_explainer import explain_candidate_shap, get_global_shap_importance
from explainability.lime_explainer import explain_candidate_lime
from database.db import get_all_applications
from components.ui import render_section_heading, render_disclaimer
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.charts import plot_shap_explanation, plot_feature_importance_bar
from components.footer import render_footer

def render_explainability_dashboard_page():
    """Render SHAP and LIME transparency analytics."""
    require_role(["recruiter", "admin"])

    render_sidebar()
    render_auth_header()

    render_section_heading("Explainable AI (SHAP & LIME)", "Deconstruct black-box predictions into interpretable local feature attributions and global dynamics.")
    render_disclaimer()

    tab_local, tab_global, tab_simulator = st.tabs(["Candidate-Level Explanations", "Global Feature Dynamics", "Interactive Scenario Tester"])

    # ---------------- TAB 1: LOCAL CANDIDATE EXPLANATIONS ----------------
    with tab_local:
        apps = get_all_applications()
        if not apps:
            st.info("No applications submitted in database to explain.")
        else:
            app_options = {f"{a['candidate_name']} ({a['job_title']} — App #{a['application_number']})": a["id"] for a in apps}
            sel_label = st.selectbox("Select Applicant to Explain", options=list(app_options.keys()))
            sel_app_id = app_options[sel_label]
            target_app = next((a for a in apps if a["id"] == sel_app_id), None)

            if target_app:
                cand_data = {
                    "Age": 28,
                    "EducationLevel": target_app.get("education_level", 2),
                    "ExperienceYears": target_app.get("experience_years", 3),
                    "PreviousCompanies": target_app.get("previous_companies", 1),
                    "DistanceFromCompany": target_app.get("distance_from_company", 10.0),
                    "InterviewScore": target_app.get("interview_score", 75.0),
                    "SkillScore": target_app.get("skill_score", 75.0),
                    "PersonalityScore": target_app.get("personality_score", 75.0),
                    "RecruitmentStrategy": target_app.get("recruitment_strategy", 2)
                }

                shap_res = explain_candidate_shap(cand_data, model_name="Random Forest")
                lime_res = explain_candidate_lime(cand_data, model_name="Random Forest")

                c_shap, c_lime = st.columns(2)

                with c_shap:
                    st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.5rem;'>SHAP Local Attribution</div>", unsafe_allow_html=True)
                    fig_shap = plot_shap_explanation(shap_res["contributions"], title=f"SHAP Values — {target_app['candidate_name']}")
                    st.plotly_chart(fig_shap, use_container_width=True)

                    st.markdown("<strong style='font-size: 0.85rem; color: #10B981;'>Top Positive Drivers:</strong>", unsafe_allow_html=True)
                    for p in shap_res["top_positive"][:3]:
                        st.markdown(f"<div style='font-size: 0.8rem; color: {COLOR_PALETTE['main_text']};'>• <code>{p['feature']}</code> (+{p['shap_value']:.3f})</div>", unsafe_allow_html=True)

                    st.markdown("<strong style='font-size: 0.85rem; color: #EF4444; margin-top: 0.5rem; display: block;'>Top Negative Restraints:</strong>", unsafe_allow_html=True)
                    for n in shap_res["top_negative"][:3]:
                        st.markdown(f"<div style='font-size: 0.8rem; color: {COLOR_PALETTE['main_text']};'>• <code>{n['feature']}</code> ({n['shap_value']:.3f})</div>", unsafe_allow_html=True)

                with c_lime:
                    st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['primary_purple']}; margin-bottom: 0.5rem;'>LIME Local Surrogate Rules</div>", unsafe_allow_html=True)

                    rules_rows = []
                    for r in lime_res["rules"]:
                        rules_rows.append({
                            "Local Condition Rule": r["rule"],
                            "Surrogate Weight": f"{r['weight']:.4f}",
                            "Direction": r["direction"]
                        })
                    st.dataframe(pd.DataFrame(rules_rows), use_container_width=True, hide_index=True)

                    st.markdown(
                        f"""
                        <div class="fairhire-card" style="margin-top: 1rem; font-size: 0.8rem;">
                            <strong style="color: {COLOR_PALETTE['primary_purple']};">LIME Surrogate Interpretation:</strong><br/>
                            LIME creates a perturbation neighborhood around {target_app['candidate_name']}'s credentials
                            and computes local linear boundary weights.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(f"<div class='disclaimer-banner' style='margin-top: 1rem;'><strong>MANDATORY TRANSPARENCY NOTICE:</strong> {shap_res['disclaimer']}</div>", unsafe_allow_html=True)

    # ---------------- TAB 2: GLOBAL FEATURE DYNAMICS ----------------
    with tab_global:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Global Mean Absolute SHAP Importance</div>", unsafe_allow_html=True)
        global_shap = get_global_shap_importance(model_name="Random Forest", sample_size=150)
        shap_dict = {item["feature"]: item["mean_abs_shap"] for item in global_shap}
        fig_global_shap = plot_feature_importance_bar(shap_dict, title="Global SHAP Feature Importance (Background Sample)")
        st.plotly_chart(fig_global_shap, use_container_width=True)

        st.markdown(
            f"""
            <div class="fairhire-card">
                <strong style="color: {COLOR_PALETTE['cyan']};">Key Global Takeaways:</strong>
                <ul style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.6;">
                    <li><strong>Recruitment Strategy & Skill Score:</strong> Consistently exert the highest global Shapley impact on shortlisting probabilities.</li>
                    <li><strong>Education Level & Experience:</strong> Function as primary qualification filters across candidate distributions.</li>
                    <li><strong>Demographic Safety:</strong> Protected demographic features (Gender) have exactly 0.00 global SHAP impact because they are strictly omitted from model input features.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- TAB 3: SCENARIO TESTER ----------------
    with tab_simulator:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Real-Time Credential Sensitivity Simulator</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color: #94A3B8;'>Adjust applicant features to observe live changes in model prediction and Shapley attribution.</p>", unsafe_allow_html=True)

        sim_c1, sim_c2, sim_c3 = st.columns(3)
        with sim_c1:
            sim_exp = st.slider("Experience (Years)", 0, 20, 4)
            sim_edu = st.selectbox("Education Level", ["Bachelor's", "Master's", "PhD", "Other"], index=1)
            sim_edu_code = {"Bachelor's": 1, "Master's": 2, "PhD": 3, "Other": 4}[sim_edu]
        with sim_c2:
            sim_skill = st.slider("Skill Assessment Score", 0.0, 100.0, 85.0)
            sim_int = st.slider("Interview Score", 0.0, 100.0, 80.0)
        with sim_c3:
            sim_pers = st.slider("Personality Score", 0.0, 100.0, 75.0)
            sim_dist = st.slider("Distance from Company (km)", 1.0, 50.0, 10.0)

        sim_cand = {
            "Age": 28,
            "EducationLevel": sim_edu_code,
            "ExperienceYears": sim_exp,
            "PreviousCompanies": 2,
            "DistanceFromCompany": sim_dist,
            "InterviewScore": sim_int,
            "SkillScore": sim_skill,
            "PersonalityScore": sim_pers,
            "RecruitmentStrategy": 1
        }

        sim_shap = explain_candidate_shap(sim_cand, model_name="Random Forest")
        fig_sim_shap = plot_shap_explanation(sim_shap["contributions"], title="Simulated Candidate SHAP Profile")
        st.plotly_chart(fig_sim_shap, use_container_width=True)

    render_footer()
