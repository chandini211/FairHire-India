"""
FairHire India - Enterprise Dark Plotly Visualizations
Strict dark enterprise styling, high contrast, crisp lines, and zero gradients.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from config import COLOR_PALETTE

DARK_LAYOUT = dict(
    paper_bgcolor=COLOR_PALETTE["card_bg"],
    plot_bgcolor=COLOR_PALETTE["card_bg"],
    font=dict(family="Inter, sans-serif", color=COLOR_PALETTE["main_text"], size=12),
    margin=dict(l=40, r=40, t=50, b=40),
    xaxis=dict(
        gridcolor=COLOR_PALETTE["border"],
        zerolinecolor=COLOR_PALETTE["border"],
        tickfont=dict(color=COLOR_PALETTE["secondary_text"]),
        title=dict(font=dict(color=COLOR_PALETTE["main_text"], size=12))
    ),
    yaxis=dict(
        gridcolor=COLOR_PALETTE["border"],
        zerolinecolor=COLOR_PALETTE["border"],
        tickfont=dict(color=COLOR_PALETTE["secondary_text"]),
        title=dict(font=dict(color=COLOR_PALETTE["main_text"], size=12))
    ),
    legend=dict(
        bgcolor=COLOR_PALETTE["card_bg"],
        bordercolor=COLOR_PALETTE["border"],
        borderwidth=1,
        font=dict(color=COLOR_PALETTE["main_text"])
    )
)

def plot_confusion_matrix(cm: List[List[int]], model_name: str) -> go.Figure:
    """Render 2x2 confusion matrix heatmap."""
    labels = ["Not Shortlisted (0)", "Shortlisted (1)"]
    z = cm

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=labels,
        y=labels,
        colorscale=[[0, COLOR_PALETTE["card_bg"]], [1, COLOR_PALETTE["primary_purple"]]],
        showscale=False,
        text=[[str(v) for v in row] for row in z],
        texttemplate="%{text}",
        textfont=dict(family="IBM Plex Mono", size=18, color=COLOR_PALETTE["main_text"])
    ))

    fig.update_layout(
        title=dict(text=f"Confusion Matrix — {model_name}", font=dict(family="Space Grotesk", size=14)),
        xaxis_title="Predicted Label",
        yaxis_title="Actual Label",
        **DARK_LAYOUT
    )
    return fig

def plot_roc_comparison(models_data: Dict[str, Any]) -> go.Figure:
    """Render overlay ROC curves for all evaluated models."""
    fig = go.Figure()
    colors = [COLOR_PALETTE["cyan"], COLOR_PALETTE["primary_purple"], COLOR_PALETTE["warning_amber"]]

    for idx, (name, data) in enumerate(models_data.items()):
        roc = data["metrics"]["roc_curve"]
        auc = data["metrics"]["roc_auc"]
        fig.add_trace(go.Scatter(
            x=roc["fpr"],
            y=roc["tpr"],
            mode="lines",
            name=f"{name} (AUC = {auc:.3f})",
            line=dict(color=colors[idx % len(colors)], width=2.5)
        ))

    # Diagonal random baseline
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode="lines",
        name="Random Classifier (AUC = 0.500)",
        line=dict(color=COLOR_PALETTE["secondary_text"], dash="dash", width=1.5)
    ))

    fig.update_layout(
        title=dict(text="ROC Curves — Predictive Discrimination", font=dict(family="Space Grotesk", size=14)),
        xaxis_title="False Positive Rate (FPR)",
        yaxis_title="True Positive Rate (TPR / Sensitivity)",
        **DARK_LAYOUT
    )
    return fig

def plot_feature_importance_bar(importance_dict: Dict[str, float], title: str = "Feature Importance") -> go.Figure:
    """Render horizontal bar chart for feature importances."""
    sorted_items = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    features = [item[0] for item in sorted_items][::-1]
    values = [item[1] for item in sorted_items][::-1]

    fig = go.Figure(go.Bar(
        x=values,
        y=features,
        orientation="h",
        marker=dict(color=COLOR_PALETTE["cyan"], line=dict(color=COLOR_PALETTE["border"], width=1))
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(family="Space Grotesk", size=14)),
        xaxis_title="Importance Weight",
        yaxis_title="Feature",
        **DARK_LAYOUT
    )
    return fig

def plot_fairness_parity_comparison(by_group: Dict[str, Dict[str, Any]]) -> go.Figure:
    """Render side-by-side bar chart of selection rates and TPR by demographic subgroup."""
    groups = list(by_group.keys())
    selection_rates = [by_group[g]["selection_rate"] * 100 for g in groups]
    tprs = [by_group[g]["tpr"] * 100 for g in groups]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=groups,
        y=selection_rates,
        name="Selection Rate %",
        marker=dict(color=COLOR_PALETTE["primary_purple"])
    ))
    fig.add_trace(go.Bar(
        x=groups,
        y=tprs,
        name="True Positive Rate (TPR) %",
        marker=dict(color=COLOR_PALETTE["cyan"])
    ))

    fig.update_layout(
        title=dict(text="Subgroup Selection Rate & TPR Parity", font=dict(family="Space Grotesk", size=14)),
        xaxis_title="Demographic Group",
        yaxis_title="Rate (%)",
        barmode="group",
        **DARK_LAYOUT
    )
    return fig

def plot_mitigation_radar_or_bars(comparison: Dict[str, Dict[str, Any]]) -> go.Figure:
    """Render side-by-side comparison of Baseline vs Mitigated model metrics."""
    metrics = ["Accuracy", "F1 Score", "Precision", "Recall"]
    base_vals = [
        comparison["Baseline"]["accuracy"] * 100,
        comparison["Baseline"]["f1_score"] * 100,
        comparison["Baseline"]["precision"] * 100,
        comparison["Baseline"]["recall"] * 100
    ]
    mit_vals = [
        comparison["Mitigated"]["accuracy"] * 100,
        comparison["Mitigated"]["f1_score"] * 100,
        comparison["Mitigated"]["precision"] * 100,
        comparison["Mitigated"]["recall"] * 100
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=metrics,
        y=base_vals,
        name="Baseline (Unmitigated)",
        marker=dict(color=COLOR_PALETTE["primary_purple"])
    ))
    fig.add_trace(go.Bar(
        x=metrics,
        y=mit_vals,
        name="Mitigated (Fairlearn Reductions)",
        marker=dict(color=COLOR_PALETTE["success_green"])
    ))

    fig.update_layout(
        title=dict(text="Utility vs Fairness Trade-Off Comparison", font=dict(family="Space Grotesk", size=14)),
        xaxis_title="Performance Metric",
        yaxis_title="Score (%)",
        barmode="group",
        **DARK_LAYOUT
    )
    return fig

def plot_shap_explanation(contributions: List[Dict[str, Any]], title: str = "Local SHAP Feature Contributions") -> go.Figure:
    """Render horizontal bar chart for local SHAP values."""
    sorted_c = contributions[:8][::-1]
    features = [c["feature"] for c in sorted_c]
    values = [c["shap_value"] for c in sorted_c]
    colors = [COLOR_PALETTE["success_green"] if v > 0 else COLOR_PALETTE["danger_red"] for v in values]

    fig = go.Figure(go.Bar(
        x=values,
        y=features,
        orientation="h",
        marker=dict(color=colors, line=dict(color=COLOR_PALETTE["border"], width=1))
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(family="Space Grotesk", size=14)),
        xaxis_title="SHAP Value (Impact on Log-Odds)",
        yaxis_title="Feature",
        **DARK_LAYOUT
    )
    return fig
