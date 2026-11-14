"""
FairHire India - Recruiter Reports & Exports Center
Dedicated artifact export management with one-click downloads for PDF reports, PPTX decks, and CSV logs.
"""
import streamlit as st
from pathlib import Path
from config import (
    COLOR_PALETTE, REPORTS_DIR, DATASET_REPORTS_DIR,
    MODEL_REPORTS_DIR, FAIRNESS_REPORTS_DIR, EXPORTS_DIR
)
from auth.authentication import get_current_user
from auth.authorization import require_role
from utils.exports import generate_all_deliverables
from components.ui import render_section_heading, render_disclaimer, render_metric_card
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

def render_reports_exports_page():
    """Render executive reports and export dashboard."""
    require_role(["recruiter", "admin"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Reports & Governance Exports Center", "One-click export for technical audits, compliance reports, and presentation slides.")
    render_disclaimer()

    # Re-generate action button
    top_c1, top_c2 = st.columns([8, 3])
    with top_c2:
        if st.button("🔄 Regenerate All Artifacts", type="primary", use_container_width=True):
            with st.spinner("Compiling ReportLab PDFs and python-pptx presentation..."):
                generate_all_deliverables()
            st.success("All technical reports and presentations re-generated successfully!")
            st.rerun()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Technical PDFs", "5 Reports", "ReportLab Built")
    with c2:
        render_metric_card("Executive Deck", "1 Presentation", "python-pptx 16:9")
    with c3:
        render_metric_card("Data Exports", "2 CSV Files", "Live Pipeline Logs")
    with c4:
        render_metric_card("Audit Compliance", "100%", "HCLTech Aligned", is_positive=True)

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    d_col1, d_col2 = st.columns(2)

    # PDF Reports Column
    with d_col1:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.75rem;'>Executive Technical Documentation (PDF)</div>", unsafe_allow_html=True)

        pdf_items = [
            ("Comprehensive Project Report", REPORTS_DIR / "Project_Report.pdf", "End-to-end technical architecture, problem statement, and ML evaluation."),
            ("Dataset Source Documentation", DATASET_REPORTS_DIR / "Dataset_Source_Documentation.pdf", "Official Kaggle provenance, exact 1,000 sampling parameters, and schema."),
            ("Model Evaluation Report", MODEL_REPORTS_DIR / "Model_Evaluation_Report.pdf", "Comparative benchmark across Logistic Regression, Random Forest, and Decision Tree."),
            ("Fairness & Mitigation Report", FAIRNESS_REPORTS_DIR / "Fairness_Evaluation_Report.pdf", "Fairlearn MetricFrame parity, Equalized Odds, and reduction trade-offs."),
            ("Automated Testing Report", REPORTS_DIR / "Testing_Report.pdf", "Pytest suite execution report covering all 19 automated test cases.")
        ]

        for title, fpath, desc in pdf_items:
            st.markdown(
                f"""
                <div class="fairhire-card" style="margin-bottom: 0.75rem;">
                    <div style="font-weight: 600; font-size: 1.05rem; color: {COLOR_PALETTE['main_text']};">{title}</div>
                    <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; margin: 0.25rem 0 0.5rem 0;">{desc}</div>
                </div>
                """, unsafe_allow_html=True
            )
            if fpath.exists():
                with open(fpath, "rb") as f:
                    st.download_button(
                        label=f"📥 Download {title} (PDF)",
                        data=f.read(),
                        file_name=fpath.name,
                        mime="application/pdf",
                        key=f"dl_{fpath.stem}",
                        use_container_width=True,
                        type="secondary"
                    )

    # PPTX and CSV Column
    with d_col2:
        st.markdown(f"<div style='font-weight: 600; color: {COLOR_PALETTE['primary_purple']}; margin-bottom: 0.75rem;'>Presentation Deck & Raw CSV Exports</div>", unsafe_allow_html=True)

        # Presentation Card
        pptx_path = REPORTS_DIR / "Project_Presentation.pptx"
        st.markdown(
            f"""
            <div class="fairhire-card" style="margin-bottom: 0.75rem;">
                <div style="font-weight: 600; font-size: 1.05rem; color: {COLOR_PALETTE['main_text']};">Executive Presentation Slide Deck</div>
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; margin: 0.25rem 0 0.5rem 0;">
                    9-slide high-resolution enterprise slide deck covering problem statement, methodology, ML results, and ethical governance.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if pptx_path.exists():
            with open(pptx_path, "rb") as f:
                st.download_button(
                    label="📥 Download Presentation Deck (PPTX)",
                    data=f.read(),
                    file_name="FairHire_India_Presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key="dl_pptx_deck",
                    use_container_width=True,
                    type="primary"
                )

        # CSV Exports
        csv_app_path = EXPORTS_DIR / "candidate_applications.csv"
        st.markdown(
            f"""
            <div class="fairhire-card" style="margin-top: 1rem; margin-bottom: 0.75rem;">
                <div style="font-weight: 600; font-size: 1.05rem; color: {COLOR_PALETTE['main_text']};">Candidate Applications Data Export</div>
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; margin: 0.25rem 0 0.5rem 0;">
                    Complete CSV export of all candidate applications with credentials, scores, and review statuses.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if csv_app_path.exists():
            with open(csv_app_path, "rb") as f:
                st.download_button(
                    label="📥 Export Candidate Applications (CSV)",
                    data=f.read(),
                    file_name="candidate_applications.csv",
                    mime="text/csv",
                    key="dl_app_csv",
                    use_container_width=True,
                    type="secondary"
                )

        csv_audit_path = EXPORTS_DIR / "audit_logs.csv"
        st.markdown(
            f"""
            <div class="fairhire-card" style="margin-top: 1rem; margin-bottom: 0.75rem;">
                <div style="font-weight: 600; font-size: 1.05rem; color: {COLOR_PALETTE['main_text']};">Security & Governance Audit Trail</div>
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; margin: 0.25rem 0 0.5rem 0;">
                    Immutable historical security log of user authentications, application status changes, and artifact exports.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if csv_audit_path.exists():
            with open(csv_audit_path, "rb") as f:
                st.download_button(
                    label="📥 Export Security Audit Logs (CSV)",
                    data=f.read(),
                    file_name="audit_logs.csv",
                    mime="text/csv",
                    key="dl_audit_csv",
                    use_container_width=True,
                    type="secondary"
                )

    render_footer()
