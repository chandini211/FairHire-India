"""
FairHire India - Reusable Card Components
Provides problem, solution, architecture, and metric cards.
"""
import streamlit as st
import textwrap
from config import COLOR_PALETTE

def render_problem_card(title: str, subtitle: str, description: str, icon_tag: str):
    """Render challenge card for recruitment gap section."""
    html = f"""<div class="fairhire-card" style="height: 100%;">
<div style="font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace; color: {COLOR_PALETTE['cyan']}; margin-bottom: 0.4rem;">{icon_tag}</div>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-bottom: 0.35rem;">{title}</div>
<div style="font-size: 0.85rem; font-weight: 500; color: {COLOR_PALETTE['warning_amber']}; margin-bottom: 0.75rem;">{subtitle}</div>
<div style="font-size: 0.875rem; color: {COLOR_PALETTE['secondary_text']}; line-height: 1.5;">{description}</div>
</div>"""
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)

def render_solution_card(pillar: str, title: str, description: str, tag: str):
    """Render solution pillar card."""
    html = f"""<div class="fairhire-card" style="height: 100%; border-top: 3px solid {COLOR_PALETTE['primary_purple']};">
<div style="font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace; color: {COLOR_PALETTE['primary_purple']}; margin-bottom: 0.4rem;">{pillar}</div>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-bottom: 0.5rem;">{title}</div>
<div style="font-size: 0.875rem; color: {COLOR_PALETTE['secondary_text']}; line-height: 1.5; margin-bottom: 0.75rem;">{description}</div>
<span class="compliance-badge badge-purple">{tag}</span>
</div>"""
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)

def render_tech_card(tech_name: str, category: str, version_or_role: str):
    """Render technology stack card."""
    html = f"""<div class="fairhire-card" style="text-align: center; padding: 1rem 0.5rem; height: 100%;">
<div style="font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace; color: {COLOR_PALETTE['secondary_text']};">{category}</div>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin: 0.25rem 0;">{tech_name}</div>
<div style="font-size: 0.75rem; color: {COLOR_PALETTE['cyan']};">{version_or_role}</div>
</div>"""
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)
