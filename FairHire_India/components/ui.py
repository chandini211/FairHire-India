"""
FairHire India - Enterprise Dark Design System & CSS Injections
Strictly flat solid backgrounds, crisp borders, Google Fonts, and zero glowing/gradient effects.
Fully responsive across desktop (1920px), laptop (1366px), tablet (768px), and mobile (390px).
"""
import streamlit as st
from config import COLOR_PALETTE

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

/* Global Reset & Horizontal Overflow Prevention */
*, *::before, *::after {{
    box-sizing: border-box !important;
}}

html, body {{
    background-color: {COLOR_PALETTE["main_bg"]} !important;
    color: {COLOR_PALETTE["main_text"]} !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    overflow-x: hidden !important;
    max-width: 100vw !important;
}}

[data-testid="stAppViewContainer"] {{
    background-color: {COLOR_PALETTE["main_bg"]} !important;
    color: {COLOR_PALETTE["main_text"]} !important;
    overflow-x: hidden !important;
}}

[data-testid="stAppViewBlockContainer"] {{
    padding-top: 1.25rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1440px !important;
    margin: 0 auto !important;
}}

/* Sidebar Canvas */
[data-testid="stSidebar"] {{
    background-color: {COLOR_PALETTE["sidebar_bg"]} !important;
    border-right: 1px solid {COLOR_PALETTE["border"]} !important;
}}

[data-testid="stSidebar"] * {{
    color: {COLOR_PALETTE["main_text"]} !important;
}}

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Space Grotesk', -apple-system, sans-serif !important;
    color: {COLOR_PALETTE["main_text"]} !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}}

/* Monospace Numbers & Metrics */
.mono-stat, .stMetric [data-testid="stMetricValue"] {{
    font-family: 'IBM Plex Mono', monospace !important;
    color: {COLOR_PALETTE["cyan"]} !important;
    font-weight: 600 !important;
}}

/* Cards & Containers */
.fairhire-card {{
    background-color: {COLOR_PALETTE["card_bg"]};
    border: 1px solid {COLOR_PALETTE["border"]};
    border-radius: 6px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    word-wrap: break-word;
}}

.fairhire-card-header {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: {COLOR_PALETTE["main_text"]};
    margin-bottom: 0.5rem;
    border-bottom: 1px solid {COLOR_PALETTE["border"]};
    padding-bottom: 0.5rem;
}}

/* Standard Buttons */
.stButton > button {{
    background-color: {COLOR_PALETTE["primary_purple"]} !important;
    color: #FFFFFF !important;
    border: 1px solid {COLOR_PALETTE["primary_purple"]} !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.45rem 1rem !important;
    transition: background-color 0.15s ease, border-color 0.15s ease !important;
    white-space: nowrap !important;
}}

.stButton > button:hover {{
    background-color: #5346E0 !important;
    border-color: #5346E0 !important;
}}

/* Secondary Buttons */
.stButton > button[kind="secondary"] {{
    background-color: {COLOR_PALETTE["card_bg"]} !important;
    color: {COLOR_PALETTE["main_text"]} !important;
    border: 1px solid {COLOR_PALETTE["border"]} !important;
}}

.stButton > button[kind="secondary"]:hover {{
    background-color: {COLOR_PALETTE["sidebar_bg"]} !important;
    border-color: {COLOR_PALETTE["cyan"]} !important;
    color: {COLOR_PALETTE["cyan"]} !important;
}}

/* Primary Buttons */
.stButton > button[kind="primary"] {{
    background-color: {COLOR_PALETTE["primary_purple"]} !important;
    color: #FFFFFF !important;
    border: 1px solid {COLOR_PALETTE["primary_purple"]} !important;
}}

/* Active Navigation Buttons */
.nav-btn-active > button {{
    background-color: {COLOR_PALETTE["primary_purple"]} !important;
    color: #FFFFFF !important;
    border: 1px solid {COLOR_PALETTE["cyan"]} !important;
    font-weight: 600 !important;
}}

/* Form Inputs */
input, select, textarea, .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
    background-color: {COLOR_PALETTE["card_bg"]} !important;
    color: {COLOR_PALETTE["main_text"]} !important;
    border: 1px solid {COLOR_PALETTE["border"]} !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
}}

input:focus, textarea:focus {{
    border-color: {COLOR_PALETTE["cyan"]} !important;
    box-shadow: none !important;
}}

/* Selectbox Dropdowns */
[data-baseweb="select"] > div {{
    background-color: {COLOR_PALETTE["card_bg"]} !important;
    border: 1px solid {COLOR_PALETTE["border"]} !important;
    color: {COLOR_PALETTE["main_text"]} !important;
}}

/* Metrics */
[data-testid="stMetric"] {{
    background-color: {COLOR_PALETTE["card_bg"]};
    border: 1px solid {COLOR_PALETTE["border"]};
    border-radius: 6px;
    padding: 1rem;
}}

[data-testid="stMetricLabel"] {{
    color: {COLOR_PALETTE["secondary_text"]} !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px !important;
    border-bottom: 1px solid {COLOR_PALETTE["border"]} !important;
    background-color: transparent !important;
}}

.stTabs [data-baseweb="tab"] {{
    background-color: {COLOR_PALETTE["card_bg"]} !important;
    border: 1px solid {COLOR_PALETTE["border"]} !important;
    border-radius: 4px 4px 0 0 !important;
    color: {COLOR_PALETTE["secondary_text"]} !important;
    padding: 8px 18px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}}

.stTabs [aria-selected="true"] {{
    background-color: {COLOR_PALETTE["primary_purple"]} !important;
    color: #FFFFFF !important;
    border-color: {COLOR_PALETTE["primary_purple"]} !important;
}}

/* Expanders */
[data-testid="stExpander"] {{
    background-color: {COLOR_PALETTE["card_bg"]} !important;
    border: 1px solid {COLOR_PALETTE["border"]} !important;
    border-radius: 4px !important;
    margin-bottom: 0.75rem !important;
}}

/* Disclaimers & Alert Banners */
.disclaimer-banner {{
    background-color: {COLOR_PALETTE["card_bg"]};
    border-left: 4px solid {COLOR_PALETTE["warning_amber"]};
    border-top: 1px solid {COLOR_PALETTE["border"]};
    border-right: 1px solid {COLOR_PALETTE["border"]};
    border-bottom: 1px solid {COLOR_PALETTE["border"]};
    border-radius: 4px;
    padding: 0.85rem 1.25rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: {COLOR_PALETTE["main_text"]};
    line-height: 1.5;
}}

/* Candidate Hero Banner (Matching Exact Layout) */
.candidate-hero-banner {{
    background-color: #5544E6;
    border: 1px solid #6E61F7;
    border-radius: 14px;
    padding: 1.75rem 2rem;
    color: #FFFFFF;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 24px rgba(85, 68, 230, 0.25);
}}

.candidate-hero-banner .banner-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 0.4rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}

.candidate-hero-banner .banner-subtitle {{
    font-size: 0.95rem;
    color: #E2E8F0;
    margin: 0 0 1rem 0;
    line-height: 1.45;
}}

/* Candidate Shortlisting Score Card (Exact Match to Requirement) */
.candidate-score-card {{
    background-color: rgba(16, 185, 129, 0.12);
    border: 2px solid #10B981;
    border-radius: 16px;
    padding: 2.25rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}}

.candidate-score-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(16, 185, 129, 0.25);
}}

.candidate-score-card.review-card {{
    background-color: rgba(245, 158, 11, 0.12);
    border-color: #F59E0B;
}}

.candidate-score-card.review-card:hover {{
    box-shadow: 0 12px 32px rgba(245, 158, 11, 0.25);
}}

.candidate-score-icon-box {{
    width: 44px;
    height: 44px;
    background-color: #10B981;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 auto 0.85rem auto;
}}

.candidate-score-card.review-card .candidate-score-icon-box {{
    background-color: #F59E0B;
}}

.candidate-score-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: {COLOR_PALETTE["main_text"]};
    margin-bottom: 0.75rem;
    letter-spacing: -0.01em;
}}

.candidate-score-value {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 4.25rem;
    font-weight: 800;
    color: #10B981;
    line-height: 1;
    margin: 0.5rem 0;
    letter-spacing: -0.03em;
}}

.candidate-score-card.review-card .candidate-score-value {{
    color: #F59E0B;
}}

.candidate-score-subtitle {{
    font-size: 0.95rem;
    color: {COLOR_PALETTE["secondary_text"]};
    font-weight: 500;
    margin-bottom: 1rem;
}}

.candidate-score-appid {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background-color: {COLOR_PALETTE["card_bg"]};
    border: 1px solid {COLOR_PALETTE["border"]};
    border-radius: 6px;
    padding: 0.45rem 1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: {COLOR_PALETTE["cyan"]};
}}

.compliance-badge {{
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 3px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
}}

.badge-green {{
    background-color: rgba(16, 185, 129, 0.15);
    color: {COLOR_PALETTE["success_green"]};
    border: 1px solid {COLOR_PALETTE["success_green"]};
}}

.badge-amber {{
    background-color: rgba(245, 158, 11, 0.15);
    color: {COLOR_PALETTE["warning_amber"]};
    border: 1px solid {COLOR_PALETTE["warning_amber"]};
}}

.badge-purple {{
    background-color: rgba(101, 88, 245, 0.15);
    color: {COLOR_PALETTE["primary_purple"]};
    border: 1px solid {COLOR_PALETTE["primary_purple"]};
}}

.badge-cyan {{
    background-color: rgba(34, 195, 214, 0.15);
    color: {COLOR_PALETTE["cyan"]};
    border: 1px solid {COLOR_PALETTE["cyan"]};
}}

/* Tables & DataFrames */
[data-testid="stDataFrame"] {{
    border: 1px solid {COLOR_PALETTE["border"]} !important;
    border-radius: 4px !important;
}}

/* Hide Default Streamlit Controls cleanly */
#MainMenu {{ visibility: hidden; }}
header[data-testid="stHeader"] {{
    background-color: {COLOR_PALETTE["main_bg"]} !important;
    border-bottom: 1px solid {COLOR_PALETTE["border"]} !important;
}}
footer {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}

/* Responsive Breakpoints */
@media (max-width: 1024px) {{
    [data-testid="stAppViewBlockContainer"] {{
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }}
}}

@media (max-width: 768px) {{
    [data-testid="stAppViewBlockContainer"] {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    h1 {{ font-size: 2.25rem !important; }}
    h2 {{ font-size: 1.5rem !important; }}
    h3 {{ font-size: 1.2rem !important; }}
    .mono-stat {{ font-size: 1.5rem !important; }}
}}

@media (max-width: 480px) {{
    [data-testid="stAppViewBlockContainer"] {{
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }}
    h1 {{ font-size: 1.85rem !important; }}
    .fairhire-card {{ padding: 1rem !important; }}
}}
</style>
"""

import textwrap

def inject_custom_css():
    """Inject global design system stylesheet."""
    if hasattr(st, "html"):
        st.html(CUSTOM_CSS)
    else:
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_metric_card(label: str, value: str, subtitle: str = "", delta: str = "", is_positive: bool = True):
    """Render structured dark enterprise KPI widget using native st.html to prevent any code-block wrapping."""
    delta_html = ""
    if delta:
        delta_color = COLOR_PALETTE["success_green"] if is_positive else COLOR_PALETTE["danger_red"]
        delta_html = f"<div style='font-size: 0.8rem; color: {delta_color}; margin-top: 0.25rem;'>{delta}</div>"

    sub_html = ""
    if subtitle:
        sub_html = f"<div style='font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.35rem;'>{subtitle}</div>"

    card_html = f"""<div class="fairhire-card" style="margin-bottom: 0.75rem;">
<div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']}; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
<div class="mono-stat" style="font-size: 1.85rem; margin-top: 0.35rem; line-height: 1.1;">{value}</div>
{delta_html}
{sub_html}
</div>"""

    if hasattr(st, "html"):
        st.html(card_html)
    else:
        st.markdown(card_html, unsafe_allow_html=True)

def render_disclaimer():
    """Render mandatory human-in-the-loop decision-support disclaimer."""
    html = f"""<div class="disclaimer-banner">
<strong style="color: {COLOR_PALETTE['warning_amber']};">DECISION-SUPPORT NOTICE:</strong>
AI-generated shortlisting predictions are decision-support signals, not final recruitment decisions.
In accordance with responsible AI standards, human recruiter review is required for all candidate evaluations. Automated rejection is strictly disabled.
</div>"""
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)

def render_section_heading(title: str, subtitle: str = ""):
    """Render standardized page or section heading with crisp typography."""
    sub_tag = f"<p style='color: {COLOR_PALETTE['secondary_text']}; font-size: 0.95rem; margin-top: -0.25rem; margin-bottom: 1.25rem;'>{subtitle}</p>" if subtitle else ""
    html = f"""<div style="margin-top: 0.5rem; margin-bottom: 0.75rem;">
<h2 style="margin: 0; font-size: 1.5rem; color: {COLOR_PALETTE['main_text']};">{title}</h2>
{sub_tag}
</div>"""
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)

def render_candidate_hero_banner(active_tab: str = "apply_job"):
    """Render the top banner with quick navigation pills matching user layout."""
    banner_html = f"""<div class="candidate-hero-banner">
<div class="banner-title">
    <span style="font-size: 1.6rem;">🇮🇳</span> FairHire India
</div>
<div class="banner-subtitle">
    Discover jobs, apply online and track your application status through one simple recruitment platform.
</div>
</div>"""
    if hasattr(st, "html"):
        st.html(banner_html)
    else:
        st.markdown(banner_html, unsafe_allow_html=True)

    # Navigation pills row
    col1, col2, col3, col_space = st.columns([2.2, 2.2, 2.2, 5.4])
    with col1:
        btn_type = "primary" if active_tab == "apply_job" else "secondary"
        if st.button("📝 Apply for a Job", key=f"chb_apply_{active_tab}", type=btn_type, use_container_width=True):
            st.session_state["current_page"] = "apply_job"
            st.rerun()
    with col2:
        btn_type = "primary" if active_tab == "my_applications" else "secondary"
        if st.button("📋 My Applications", key=f"chb_myapps_{active_tab}", type=btn_type, use_container_width=True):
            st.session_state["current_page"] = "my_applications"
            st.rerun()
    with col3:
        btn_type = "primary" if active_tab == "about" else "secondary"
        if st.button("ℹ️ About FairHire", key=f"chb_about_{active_tab}", type=btn_type, use_container_width=True):
            st.session_state["current_page"] = "about"
            st.rerun()

    st.markdown("<div style='margin-bottom: 1.25rem;'></div>", unsafe_allow_html=True)

def render_candidate_score_card(score_pct: int, is_shortlisted: bool, application_id: str, recommendation: str = None):
    """Render the high-impact candidate score card with checkmark and large score."""
    card_class = "candidate-score-card" if is_shortlisted else "candidate-score-card review-card"
    icon = "✔" if is_shortlisted else "⏳"
    title = "Candidate is Shortlisted" if is_shortlisted else "Candidate Under Recruiter Review"
    rec_text = recommendation or (
        "Candidate matches core role criteria and is forwarded for human technical review."
        if is_shortlisted else
        "Application dossier routed to Talent Acquisition for holistic review."
    )

    html = f"""<div class="{card_class}">
<div class="candidate-score-icon-box">{icon}</div>
<div class="candidate-score-title">{title}</div>
<div class="candidate-score-value">{score_pct}%</div>
<div class="candidate-score-subtitle">Shortlisting Score</div>
<div style="margin-bottom: 1rem;">
    <div class="candidate-score-appid">
        <span>🪪</span> Application ID: {application_id}
    </div>
</div>
<div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; max-width: 600px; margin: 0 auto; line-height: 1.5;">
    {rec_text}
</div>
</div>"""
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)
