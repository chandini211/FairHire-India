"""
FairHire India - UI & Component Library
"""
from .ui import inject_custom_css, render_metric_card, render_disclaimer, render_section_heading
from .navbar import render_public_navbar, render_auth_header
from .sidebar import render_sidebar
from .cards import render_problem_card, render_solution_card, render_tech_card
from .charts import (
    plot_confusion_matrix, plot_roc_comparison, plot_feature_importance_bar,
    plot_fairness_parity_comparison, plot_mitigation_radar_or_bars, plot_shap_explanation
)
from .tables import render_applications_table
from .footer import render_footer

__all__ = [
    "inject_custom_css", "render_metric_card", "render_disclaimer", "render_section_heading",
    "render_public_navbar", "render_auth_header", "render_sidebar",
    "render_problem_card", "render_solution_card", "render_tech_card",
    "plot_confusion_matrix", "plot_roc_comparison", "plot_feature_importance_bar",
    "plot_fairness_parity_comparison", "plot_mitigation_radar_or_bars", "plot_shap_explanation",
    "render_applications_table", "render_footer"
]
