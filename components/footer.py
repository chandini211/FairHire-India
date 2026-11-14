"""
FairHire India - Enterprise Dark Footer Component
Displays project compliance, technology governance, and HCLTech Career Shaper attribution.
"""
import streamlit as st
from config import COLOR_PALETTE, APP_NAME, APP_TAGLINE, OFFICIAL_PROBLEM_STATEMENT

def render_footer():
    """Render standardized enterprise footer across public and internal pages."""
    html = f"""
    <div style="border-top: 1px solid {COLOR_PALETTE['border']}; margin-top: 4rem; padding: 2.5rem 0 1.5rem 0; background-color: {COLOR_PALETTE['main_bg']};">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 2rem;">
            <div style="max-width: 480px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; color: {COLOR_PALETTE['cyan']};">
                    FAIRHIRE <span style="color: {COLOR_PALETTE['primary_purple']};">INDIA</span>
                </div>
                <div style="font-size: 0.85rem; font-weight: 500; color: {COLOR_PALETTE['main_text']}; margin-top: 0.25rem;">
                    {APP_TAGLINE}
                </div>
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.5rem; line-height: 1.5;">
                    Developed for the HCLTech Career Shaper Project.<br>
                    Official Problem Statement: <em>"{OFFICIAL_PROBLEM_STATEMENT}"</em>
                </div>
            </div>

            <div>
                <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: {COLOR_PALETTE['secondary_text']}; margin-bottom: 0.5rem;">Core Stack</div>
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['main_text']}; line-height: 1.6; font-family: 'IBM Plex Mono', monospace;">
                    Python 3.11+ · Streamlit<br>
                    Scikit-Learn · Fairlearn<br>
                    SHAP · LIME · SQLite
                </div>
            </div>

            <div>
                <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: {COLOR_PALETTE['secondary_text']}; margin-bottom: 0.5rem;">Governance</div>
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['main_text']}; line-height: 1.6;">
                    Human-in-the-Loop Review<br>
                    Four-Fifths Parity Auditing<br>
                    No Autonomous Rejections
                </div>
            </div>
        </div>

        <div style="border-top: 1px solid {COLOR_PALETTE['border']}; margin-top: 1.75rem; padding-top: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']};">
            <div>© 2026 FairHire India. Built strictly for the HCLTech Career Shaper evaluation.</div>
            <div>Protected under Apache 2.0 / Open Source AI Governance</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
