"""
FairHire India - Machine Learning Model Analytics
Comparative evaluation of Logistic Regression, Random Forest, and Decision Tree on held-out test data.
"""
import streamlit as st
import pandas as pd
import joblib

from config import COLOR_PALETTE, MODEL_METRICS_PATH
from auth.authorization import require_role
from components.ui import render_section_heading, render_disclaimer, render_metric_card
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.charts import (
    plot_confusion_matrix, plot_roc_comparison, plot_feature_importance_bar
)
from components.footer import render_footer

def render_model_analytics_page():
    """Render machine learning model benchmark and comparison view."""
    require_role(["recruiter", "admin"])

    render_sidebar()
    render_auth_header()

    render_section_heading("Machine Learning Model Analytics", "Rigorous performance evaluation across held-out test data (200 candidate samples).")
    render_disclaimer()

    if not MODEL_METRICS_PATH.exists():
        st.warning("Model evaluation metrics not found. Run model training to generate evaluation benchmarks.")
        render_footer()
        return

    metrics_data = joblib.load(MODEL_METRICS_PATH)
    models = metrics_data["models"]

    # Top KPI comparison row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Evaluation Test Set", f"{metrics_data.get('sample_size_test', 200)} Samples", "20% Stratified Split")
    with c2:
        top_acc = max(m["metrics"]["accuracy"] for m in models.values())
        render_metric_card("Peak Test Accuracy", f"{top_acc*100:.1f}%", "Decision Tree / LogReg", is_positive=True)
    with c3:
        top_f1 = max(m["metrics"]["f1_score"] for m in models.values())
        render_metric_card("Peak Test F1-Score", f"{top_f1:.3f}", "Decision Tree Classifier", is_positive=True)
    with c4:
        top_auc = max(m["metrics"]["roc_auc"] for m in models.values())
        render_metric_card("Peak ROC-AUC", f"{top_auc:.3f}", "Logistic Regression", is_positive=True)

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Comparative Performance Table
    render_section_heading("Model Comparison Benchmark", "Side-by-side metric comparison across all candidate algorithms.")

    comp_rows = []
    for name, data in models.items():
        m = data["metrics"]
        comp_rows.append({
            "Algorithm": name,
            "Accuracy": f"{m['accuracy']*100:.1f}%",
            "Precision": f"{m['precision']*100:.1f}%",
            "Recall": f"{m['recall']*100:.1f}%",
            "F1-Score": f"{m['f1_score']:.3f}",
            "ROC-AUC": f"{m['roc_auc']:.3f}",
            "True Positives (TP)": m["confusion_matrix"]["tp"],
            "False Positives (FP)": m["confusion_matrix"]["fp"],
            "True Negatives (TN)": m["confusion_matrix"]["tn"],
            "False Negatives (FN)": m["confusion_matrix"]["fn"]
        })

    df_comp = pd.DataFrame(comp_rows)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

    # ROC Curves & Model Selection
    ch_col1, ch_col2 = st.columns(2)
    with ch_col1:
        fig_roc = plot_roc_comparison(models)
        st.plotly_chart(fig_roc, use_container_width=True)

    with ch_col2:
        st.markdown(
            f"""
            <div class="fairhire-card" style="height: 100%;">
                <div class="compliance-badge badge-green" style="margin-bottom: 0.5rem;">PRODUCTION MODEL SELECTION</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 600; color: {COLOR_PALETTE['cyan']};">
                    Random Forest Classifier
                </div>
                <div style="font-size: 0.85rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.5rem; line-height: 1.6;">
                    <strong>Selection Rationale:</strong><br/>
                    While Decision Tree and Logistic Regression achieve marginally higher raw accuracy (88.5% vs 88.0%),
                    <strong>Random Forest</strong> is chosen as the primary production model because:
                    <ul style="margin-top: 0.4rem; padding-left: 1.25rem;">
                        <li><strong>Variance Reduction:</strong> Bagging over 100 diverse trees prevents fragile overfitting to localized applicant credential splits.</li>
                        <li><strong>Robust Probability Calibration:</strong> Produces smoother posterior confidence scores necessary for ethical decision-support thresholds.</li>
                        <li><strong>SHAP Compatibility:</strong> Integrates optimally with TreeExplainer for instantaneous polynomial-time Shapley attributions.</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Confusion Matrices and Feature Importances
    render_section_heading("Confusion Matrices & Global Feature Importances", "Inspecting misclassifications and predictive feature weights.")

    selected_model_inspect = st.selectbox("Select Model to Inspect in Detail", options=list(models.keys()), index=1)
    target_model_data = models[selected_model_inspect]

    c_mat, c_imp = st.columns(2)
    with c_mat:
        cm_data = target_model_data["metrics"]["confusion_matrix"]["matrix"]
        fig_cm = plot_confusion_matrix(cm_data, selected_model_inspect)
        st.plotly_chart(fig_cm, use_container_width=True)

    with c_imp:
        imp_data = target_model_data["feature_importance"]
        fig_imp = plot_feature_importance_bar(imp_data, title=f"Feature Importances — {selected_model_inspect}")
        st.plotly_chart(fig_imp, use_container_width=True)

    render_footer()
