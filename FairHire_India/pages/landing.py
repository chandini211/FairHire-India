"""
FairHire India - Public Enterprise Landing Page
Compliant with Section 4 requirements:
- Main Heading: "India's Recruitment Gap Is Real."
- Tagline: "Recruitment Without Bias. By Design."
- Removed badge entirely (no replacement badge).
- Clean section transitions, responsive layout, and interactive charts.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import COLOR_PALETTE, OFFICIAL_PROBLEM_STATEMENT
from components.ui import render_section_heading, render_disclaimer
from components.navbar import render_public_navbar
from components.cards import render_problem_card, render_solution_card, render_tech_card
from components.charts import DARK_LAYOUT
from components.footer import render_footer

def render_landing_page():
    """Render the public enterprise landing page."""
    # Top Public Navbar
    render_public_navbar()

    # Active landing section
    active_sec = st.session_state.get("landing_section", "home")

    # Hero Section
    st.markdown(
        f"""
        <div style="padding: 2rem 0 1.5rem 0; text-align: center; max-width: 960px; margin: 0 auto;">
            <h1 style="font-size: 3.4rem; font-weight: 700; color: {COLOR_PALETTE['main_text']}; margin: 0 0 0.85rem 0; line-height: 1.15; letter-spacing: -0.02em;">
                India's Recruitment Gap Is Real.
            </h1>
            <h3 style="font-size: 1.6rem; font-weight: 500; color: {COLOR_PALETTE['cyan']}; margin: 0 0 1.25rem 0;">
                Recruitment Without Bias. By Design.
            </h3>
            <p style="font-size: 1.125rem; color: {COLOR_PALETTE['secondary_text']}; line-height: 1.65; max-width: 820px; margin: 0 auto 2rem auto;">
                Traditional recruitment systems can unintentionally amplify bias. FairHire India combines machine learning,
                fairness-aware classification and explainable AI to support transparent, responsible and data-driven candidate shortlisting.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Hero Action Buttons
    c_btn1, c_space, c_btn2 = st.columns([2.5, 5, 2.5])
    with c_btn1:
        if st.button("Get Started — Candidate Portal", key="hero_get_started", type="primary", use_container_width=True):
            st.session_state["current_page"] = "signup"
            st.rerun()
    with c_btn2:
        if st.button("Explore Recruiter Portal", key="hero_recruiter", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "login"
            st.rerun()

    # Hero Stats Banner
    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 2.5rem; margin-bottom: 3.5rem;">
            <div class="fairhire-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; font-weight: 500; text-transform: uppercase;">MODELING RECORDS</div>
                <div class="mono-stat" style="font-size: 2rem; margin-top: 0.3rem;">1,000</div>
                <div style="font-size: 0.75rem; color: {COLOR_PALETTE['success_green']};">Exact Stratified Sample</div>
            </div>
            <div class="fairhire-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; font-weight: 500; text-transform: uppercase;">PEAK TEST ACCURACY</div>
                <div class="mono-stat" style="font-size: 2rem; margin-top: 0.3rem;">88.5%</div>
                <div style="font-size: 0.75rem; color: {COLOR_PALETTE['cyan']};">Decision Tree / LogReg</div>
            </div>
            <div class="fairhire-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; font-weight: 500; text-transform: uppercase;">PARITY RATIO</div>
                <div class="mono-stat" style="font-size: 2rem; margin-top: 0.3rem;">0.841</div>
                <div style="font-size: 0.75rem; color: {COLOR_PALETTE['success_green']};">EEOC 4/5ths Compliant</div>
            </div>
            <div class="fairhire-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; font-weight: 500; text-transform: uppercase;">DECISION AUDITING</div>
                <div class="mono-stat" style="font-size: 2rem; margin-top: 0.3rem;">100%</div>
                <div style="font-size: 0.75rem; color: {COLOR_PALETTE['primary_purple']};">Human-in-the-Loop Review</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SECTION 1 — RECRUITMENT CHALLENGES
    st.markdown("<div id='problem'></div>", unsafe_allow_html=True)
    render_section_heading("Recruitment Challenges in Modern Hiring", "Critical structural biases that distort talent selection across industry pipelines.")

    col1, col2, col3 = st.columns(3)
    with col1:
        render_problem_card(
            title="Gender Disparity",
            subtitle="Unequal Selection Outcomes",
            description="Historical hiring decisions frequently produce skewed gender representations in technical and leadership roles. Without conscious algorithmic safeguards, machine learning models treat past imbalances as predictive truth.",
            icon_tag="CHALLENGE // 01"
        )
    with col2:
        render_problem_card(
            title="Algorithmic Amplification",
            subtitle="Compounding Past Discrimination",
            description="Unconstrained black-box models often magnify subtle historical correlations, penalizing applicants from non-traditional or underrepresented backgrounds even when their objective skill scores match top performers.",
            icon_tag="CHALLENGE // 02"
        )
    with col3:
        render_problem_card(
            title="Geographic Inequity",
            subtitle="Regional Opportunity Bottlenecks",
            description="Location and socioeconomic proxies disproportionately restrict talent from Tier-2 and Tier-3 Indian cities, constraining access to high-growth opportunities regardless of candidate potential.",
            icon_tag="CHALLENGE // 03"
        )

    st.markdown("<div style='margin-bottom: 3.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 2 — OUR SOLUTION
    st.markdown("<div id='solution'></div>", unsafe_allow_html=True)
    render_section_heading("Our Solution Architecture", "Five responsible engineering pillars designed to eliminate bias by construction.")

    s_cols = st.columns(5)
    pillars = [
        ("01", "Machine Learning", "Trained on stratified datasets with strict train/test separation and data leakage prevention.", "3 BENCHMARKS"),
        ("02", "Fair Classification", "Protected demographic attributes (Gender) are strictly excluded from prediction models.", "ZERO LEAKAGE"),
        ("03", "Bias Mitigation", "In-processing reductions using Fairlearn ExponentiatedGradient to enforce Equalized Odds.", "FAIRLEARN REDUCTION"),
        ("04", "Explainable AI", "Dual explainability using SHAP TreeExplainer and LIME tabular local surrogate rules.", "LOCAL + GLOBAL"),
        ("05", "Human-in-the-Loop", "AI outputs decision-support signals only; automated candidate rejection is disabled.", "MANDATORY REVIEW")
    ]
    for idx, (p_num, p_title, p_desc, p_tag) in enumerate(pillars):
        with s_cols[idx]:
            render_solution_card(f"PILLAR // {p_num}", p_title, p_desc, p_tag)

    st.markdown("<div style='margin-bottom: 3.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 3 — HOW IT WORKS
    st.markdown("<div id='workflow'></div>", unsafe_allow_html=True)
    render_section_heading("Candidate Evaluation Workflow", "Step-by-step pipeline from applicant submission to recruiter interview decision.")

    workflow_html = f"""
    <div class="fairhire-card" style="padding: 1.5rem; overflow-x: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; min-width: 860px; font-size: 0.85rem;">
            <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; border: 1px solid {COLOR_PALETTE['border']}; padding: 0.75rem 1rem; border-radius: 4px; text-align: center; flex: 1;">
                <div style="color: {COLOR_PALETTE['cyan']}; font-weight: 600;">1. Application</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.75rem;">Profile & Assessment</div>
            </div>
            <div style="color: {COLOR_PALETTE['border']}; padding: 0 0.5rem; font-size: 1.25rem;">→</div>
            <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; border: 1px solid {COLOR_PALETTE['border']}; padding: 0.75rem 1rem; border-radius: 4px; text-align: center; flex: 1;">
                <div style="color: {COLOR_PALETTE['cyan']}; font-weight: 600;">2. Validation</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.75rem;">Schema & Bounds</div>
            </div>
            <div style="color: {COLOR_PALETTE['border']}; padding: 0 0.5rem; font-size: 1.25rem;">→</div>
            <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; border: 1px solid {COLOR_PALETTE['border']}; padding: 0.75rem 1rem; border-radius: 4px; text-align: center; flex: 1;">
                <div style="color: {COLOR_PALETTE['cyan']}; font-weight: 600;">3. Preprocessing</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.75rem;">Drop Protected Attr</div>
            </div>
            <div style="color: {COLOR_PALETTE['border']}; padding: 0 0.5rem; font-size: 1.25rem;">→</div>
            <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; border: 1px solid {COLOR_PALETTE['border']}; padding: 0.75rem 1rem; border-radius: 4px; text-align: center; flex: 1;">
                <div style="color: {COLOR_PALETTE['primary_purple']}; font-weight: 600;">4. ML Prediction</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.75rem;">Shortlisting Probability</div>
            </div>
            <div style="color: {COLOR_PALETTE['border']}; padding: 0 0.5rem; font-size: 1.25rem;">→</div>
            <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; border: 1px solid {COLOR_PALETTE['border']}; padding: 0.75rem 1rem; border-radius: 4px; text-align: center; flex: 1;">
                <div style="color: {COLOR_PALETTE['warning_amber']}; font-weight: 600;">5. Fairness Audit</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.75rem;">MetricFrame Check</div>
            </div>
            <div style="color: {COLOR_PALETTE['border']}; padding: 0 0.5rem; font-size: 1.25rem;">→</div>
            <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; border: 1px solid {COLOR_PALETTE['border']}; padding: 0.75rem 1rem; border-radius: 4px; text-align: center; flex: 1;">
                <div style="color: {COLOR_PALETTE['cyan']}; font-weight: 600;">6. SHAP & LIME</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.75rem;">Feature Attribution</div>
            </div>
            <div style="color: {COLOR_PALETTE['border']}; padding: 0 0.5rem; font-size: 1.25rem;">→</div>
            <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; border: 1px solid {COLOR_PALETTE['success_green']}; padding: 0.75rem 1rem; border-radius: 4px; text-align: center; flex: 1;">
                <div style="color: {COLOR_PALETTE['success_green']}; font-weight: 600;">7. Recruiter Decision</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.75rem;">Human Final Sign-Off</div>
            </div>
        </div>
    </div>
    """
    st.markdown(workflow_html, unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 3.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 4 — METHODOLOGY
    st.markdown("<div id='methodology'></div>", unsafe_allow_html=True)
    render_section_heading("Classification Methodology & Multi-Model Benchmarking", "Rigorous evaluation across linear, ensemble, and tree-based paradigms.")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(
            f"""
            <div class="fairhire-card" style="height: 100%;">
                <div class="compliance-badge badge-purple" style="margin-bottom: 0.5rem;">MODEL 01 // LINEAR</div>
                <div style="font-family: Space Grotesk; font-size: 1.15rem; font-weight: 600; color: {COLOR_PALETTE['main_text']};">Logistic Regression</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.85rem; margin-top: 0.4rem; line-height: 1.5;">
                    L2-regularized linear baseline. Delivers transparent coefficients with <strong>88.5%</strong> test accuracy and <strong>0.902</strong> ROC-AUC.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    with m_col2:
        st.markdown(
            f"""
            <div class="fairhire-card" style="height: 100%;">
                <div class="compliance-badge badge-cyan" style="margin-bottom: 0.5rem;">MODEL 02 // ENSEMBLE (SELECTED)</div>
                <div style="font-family: Space Grotesk; font-size: 1.15rem; font-weight: 600; color: {COLOR_PALETTE['main_text']};">Random Forest Classifier</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.85rem; margin-top: 0.4rem; line-height: 1.5;">
                    100-tree bagging ensemble with max depth of 8. Prevents overfitting, delivers <strong>88.0%</strong> test accuracy, and pairs natively with SHAP TreeExplainer.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    with m_col3:
        st.markdown(
            f"""
            <div class="fairhire-card" style="height: 100%;">
                <div class="compliance-badge badge-amber" style="margin-bottom: 0.5rem;">MODEL 03 // TREE</div>
                <div style="font-family: Space Grotesk; font-size: 1.15rem; font-weight: 600; color: {COLOR_PALETTE['main_text']};">Decision Tree Classifier</div>
                <div style="color: {COLOR_PALETTE['secondary_text']}; font-size: 0.85rem; margin-top: 0.4rem; line-height: 1.5;">
                    Constrained depth-6 decision tree. Delivers <strong>88.5%</strong> test accuracy and top F1-score (<strong>0.803</strong>) with intuitive rule boundaries.
                </div>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom: 3.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 5 — DATASET
    st.markdown("<div id='dataset'></div>", unsafe_allow_html=True)
    render_section_heading("Dataset Provenance & Exact 1,000 Record Mandate", "Empirically audited source benchmark and reproducible sampling pipeline.")

    st.markdown(
        f"""
        <div class="fairhire-card">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div>
                    <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">SOURCE BENCHMARK</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-top: 0.2rem;">Kaggle Recruitment Benchmark</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">SOURCE RECORDS</div>
                    <div class="mono-stat" style="font-size: 1.1rem; margin-top: 0.2rem;">1,500 Rows</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">FINAL MODELING SIZE</div>
                    <div class="mono-stat" style="font-size: 1.1rem; margin-top: 0.2rem; color: {COLOR_PALETTE['success_green']};">Exactly 1,000 Records</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">UNIQUENESS STATUS</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['warning_amber']}; font-weight: 600; margin-top: 0.2rem;">Pending Peer Comparison</div>
                </div>
            </div>
            <div style="border-top: 1px solid {COLOR_PALETTE['border']}; margin-top: 1rem; padding-top: 0.75rem; font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']};">
                Reproducible stratified sampling was performed using <code>random_state=42</code> over joint stratum (HiringDecision + Gender). Exactly zero missing values and zero duplicate records exist in the modeling dataset.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-bottom: 3.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 6 — FAIRNESS
    st.markdown("<div id='fairness'></div>", unsafe_allow_html=True)
    render_section_heading("Algorithmic Fairness & Fairlearn Auditing", "Demographic parity, equalized odds, and responsible mitigation trade-offs.")

    st.markdown(
        f"""
        <div class="fairhire-card">
            <p style="color: {COLOR_PALETTE['secondary_text']}; line-height: 1.6; margin: 0 0 1rem 0;">
                Fairness cannot be captured by accuracy alone. A high-accuracy model can still exhibit disparate impact.
                FairHire India integrates Fairlearn to quantify two primary fairness standards across held-out test data:
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
                <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; padding: 1.25rem; border-radius: 4px; border: 1px solid {COLOR_PALETTE['border']};">
                    <strong style="color: {COLOR_PALETTE['cyan']}; font-size: 1.05rem;">Demographic Parity</strong>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.5rem; line-height: 1.5;">
                        Requires selection rates to be statistically equal across demographic subgroups, regardless of ground-truth outcomes.
                        Measured via Demographic Parity Difference and Ratio (EEOC 4/5ths standard).
                    </div>
                </div>
                <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; padding: 1.25rem; border-radius: 4px; border: 1px solid {COLOR_PALETTE['border']};">
                    <strong style="color: {COLOR_PALETTE['primary_purple']}; font-size: 1.05rem;">Equalized Odds</strong>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.5rem; line-height: 1.5;">
                        Requires both True Positive Rate (TPR) and False Positive Rate (FPR) to be equal across groups. Ensures equally qualified applicants share equal chances of shortlisting.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-bottom: 3.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 7 — EXPLAINABLE AI
    st.markdown("<div id='xai'></div>", unsafe_allow_html=True)
    render_section_heading("Explainable AI (SHAP & LIME)", "Converting black-box decisions into transparent recruiter insights.")

    st.markdown(
        f"""
        <div class="fairhire-card">
            <p style="color: {COLOR_PALETTE['secondary_text']}; line-height: 1.6; margin: 0 0 1rem 0;">
                To ensure trust and auditability, FairHire India implements complementary local and global explanation methods:
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
                <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; padding: 1.25rem; border-radius: 4px; border: 1px solid {COLOR_PALETTE['border']};">
                    <strong style="color: {COLOR_PALETTE['success_green']}; font-size: 1.05rem;">SHAP (Shapley Additive exPlanations)</strong>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.5rem; line-height: 1.5;">
                        Rooted in cooperative game theory. Computes exact Shapley values showing how much each candidate credential increased or decreased the shortlisting score against baseline expected values.
                    </div>
                </div>
                <div style="background-color: {COLOR_PALETTE['sidebar_bg']}; padding: 1.25rem; border-radius: 4px; border: 1px solid {COLOR_PALETTE['border']};">
                    <strong style="color: {COLOR_PALETTE['warning_amber']}; font-size: 1.05rem;">LIME (Local Interpretable Explanations)</strong>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.5rem; line-height: 1.5;">
                        Fits an interpretable local surrogate model around an individual candidate's feature space, generating intuitive if-then rules explaining recruiter interview recommendations.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-bottom: 3.5rem;'></div>", unsafe_allow_html=True)

    # SECTION 8 — TECHNOLOGY STACK
    render_section_heading("Enterprise Technology Stack", "Open-source data science, responsible AI, and secure application framework.")
    t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5)
    with t_col1:
        render_tech_card("Python", "RUNTIME", "3.11.9 (64-bit)")
        render_tech_card("Streamlit", "APPLICATION", "1.67.0")
    with t_col2:
        render_tech_card("Pandas", "DATA PROCESSING", "3.1.1")
        render_tech_card("NumPy", "ARRAY MATH", "2.4.6")
    with t_col3:
        render_tech_card("Scikit-Learn", "MODELING", "1.9.1")
        render_tech_card("Fairlearn", "FAIRNESS REDUCTIONS", "0.15.0")
    with t_col4:
        render_tech_card("SHAP", "EXPLAINABLE AI", "0.51.0")
        render_tech_card("LIME", "LOCAL SURROGATES", "0.2.0")
    with t_col5:
        render_tech_card("SQLite", "DATABASE", "ACID / Thread-Safe")
        render_tech_card("Plotly", "VISUALIZATION", "7.1.0 Dark Theme")

    # Footer
    render_footer()
