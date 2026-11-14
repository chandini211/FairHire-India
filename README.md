# FAIRHIRE INDIA
### Recruitment Without Bias. By Design.

---

### HCLTech Career Shaper Project
**Official Problem Statement:**
> *"Automate candidate shortlisting while minimizing bias using fair classification models."*

🌐 **Live Website:** [Open FairHire India](https://fairhire-india-cuymrdwvj5zrk9cqrhfbcn.streamlit.app/)

## 1. Executive Summary & Vision

Traditional talent acquisition workflows often unintentionally perpetuate and amplify historical disparities. When machine learning models are trained on raw historical recruitment decisions, they frequently internalize and reproduce systemic demographic skews, creating artificial barriers for underrepresented candidate groups.

**FairHire India** is an enterprise-grade, full-stack recruitment intelligence platform architected specifically to automate candidate shortlisting while strictly measuring, auditing, and mitigating algorithmic bias. Built with a **responsible AI by design** philosophy:
- **Demographic Isolation:** Protected attributes (Gender) are strictly excluded from predictive model training and inference pipelines.
- **Empirical Parity Auditing:** Measures group disparities, selection rates, Demographic Parity Difference/Ratio (EEOC 4/5ths standard), and Equalized Odds via Microsoft **Fairlearn**.
- **In-Processing Mitigation:** Evaluates in-processing bias mitigation using Fairlearn's `ExponentiatedGradient` reduction.
- **Dual Explainability:** Deconstructs decisions using both **SHAP** (Shapley game-theoretic attributions) and **LIME** (local surrogate decision boundaries).
- **Human-in-the-Loop Governance:** AI outputs decision-support signals only; automated candidate rejections are disabled by design.
- **Enterprise Security:** ACID-compliant **SQLite** database, **Bcrypt** salted password hashing, role-based access control (RBAC), and immutable audit logging.

---

## 2. Technology Stack

| Layer | Technologies | Version / Role |
| :--- | :--- | :--- |
| **Application Runtime** | Python | 3.11+ |
| **Interface & Presentation** | Streamlit | 1.67.0 (Custom Enterprise Dark Design) |
| **Data Processing & EDA** | Pandas, NumPy | Data cleaning, validation, stratified sampling |
| **Machine Learning** | Scikit-learn, Joblib | Pipeline, ColumnTransformer, 3 Classification Models |
| **Algorithmic Fairness** | Fairlearn | MetricFrame, ExponentiatedGradient Reductions |
| **Explainable AI (XAI)** | SHAP, LIME | TreeExplainer, LinearExplainer, LimeTabularExplainer |
| **Database & Security** | SQLite, Bcrypt | Relational schema (7 tables), salted hashing, audit logs |
| **Visualization** | Plotly | Dark enterprise themed interactive visualizations |
| **Automated Testing** | Pytest | 19 automated test cases across 6 subsystems |
| **Document Generation** | ReportLab, python-pptx | Dynamic PDF report generation & PPTX slide deck |

---

## 3. Project Directory Architecture

```
FairHire_India/
│
├── app.py                             # Main Streamlit application entry point
├── config.py                          # Global configuration, paths, and color tokens
├── requirements.txt                   # Complete pinned Python dependencies
├── README.md                          # Comprehensive project documentation
├── .gitignore                         # Git exclusion rules
├── .env.example                       # Environment configuration template
├── Deployment_Guide.md                # Cloud deployment & hosting instructions
│
├── assets/                            # Brand assets (logo.png, favicon.png)
│
├── auth/                              # Authentication & security subsystem
│   ├── __init__.py
│   ├── authentication.py              # Login verification & session management
│   ├── registration.py                # Candidate registration & validation
│   ├── authorization.py               # Role-based access control (RBAC guards)
│   └── security.py                    # Bcrypt salted hashing & password policy
│
├── database/                          # SQLite relational data layer
│   ├── __init__.py
│   ├── db.py                          # Thread-safe database operations & audit logger
│   ├── schema.sql                     # SQLite schema (7 tables, FKs, indexes)
│   ├── seed.py                        # Database initialization & sample seeding
│   └── fairhire.db                    # SQLite database file
│
├── components/                        # Enterprise Dark UI component library
│   ├── __init__.py
│   ├── ui.py                          # Global CSS injection, typography, metric cards
│   ├── navbar.py                      # Public top navbar & authenticated banner
│   ├── sidebar.py                     # Role-aware sidebar navigation
│   ├── cards.py                       # Problem, solution, and technology cards
│   ├── charts.py                      # Plotly dark-themed interactive charts
│   ├── tables.py                      # Formatted data tables with status badges
│   └── footer.py                      # Standardized enterprise compliance footer
│
├── pages/                             # 13 Application View Controllers
│   ├── landing.py                     # 10-section public enterprise landing page
│   ├── login.py                       # Secure sign-in portal
│   ├── signup.py                      # Candidate registration portal
│   ├── candidate_dashboard.py         # Candidate overview & metrics
│   ├── apply_job.py                   # Verified vacancy application workflow
│   ├── my_applications.py             # Real-time application tracker
│   ├── candidate_profile.py           # Candidate profile view & edit
│   ├── recruiter_dashboard.py         # Recruiter intelligence overview & EDA
│   ├── manage_candidates.py           # Application review & inline SHAP/LIME audit
│   ├── model_analytics.py             # ML model benchmarking & comparison
│   ├── fairness_dashboard.py          # Fairlearn parity metrics & bias mitigation
│   ├── explainability_dashboard.py    # Global & local SHAP/LIME analytics
│   └── about.py                       # HCLTech checklist & report export center
│
├── ml/                                # Machine learning pipeline
│   ├── __init__.py
│   ├── data_loader.py                 # Data validation & summary stats
│   ├── preprocessing.py               # ColumnTransformer pipeline (zero leakage)
│   ├── model_training.py              # Model 1, 2, 3 training & evaluation
│   ├── evaluation.py                  # Accuracy, Precision, Recall, F1, ROC-AUC
│   └── prediction.py                  # Single & batch candidate inference service
│
├── fairness/                          # Algorithmic fairness & mitigation
│   ├── __init__.py
│   ├── metrics.py                     # Fairlearn MetricFrame disparity calculator
│   ├── mitigation.py                  # ExponentiatedGradient reduction experiment
│   ├── group_analysis.py              # Demographic breakdowns across education/gender
│   └── fairness_report.py             # Executive compliance narrative generator
│
├── explainability/                    # Explainable AI framework
│   ├── __init__.py
│   ├── shap_explainer.py              # SHAP TreeExplainer & feature attribution
│   └── lime_explainer.py              # LIME TabularExplainer local surrogate rules
│
├── utils/                             # Utility helpers & exporters
│   ├── __init__.py
│   ├── validators.py                  # Email, phone, score range validation
│   ├── helpers.py                     # UI badge and currency formatting
│   └── exports.py                     # ReportLab PDF & python-pptx generation
│
├── data/                              # Data repository
│   ├── recruitment_data.csv           # Source 1,500-record benchmark
│   └── processed/
│       └── recruitment_data_1000.csv  # Final exact 1,000-record modeling dataset
│
├── models/                            # Serialized Joblib model artifacts
│   ├── preprocessor.joblib            # Fitted ColumnTransformer
│   ├── logistic_regression.joblib     # Model 1 artifact
│   ├── random_forest.joblib           # Model 2 artifact (Production Selected)
│   ├── decision_tree.joblib           # Model 3 artifact
│   ├── mitigated_model.joblib         # Fairlearn ExponentiatedGradient artifact
│   ├── model_metrics.joblib           # Evaluation results on 20% test partition
│   └── fairness_metrics.joblib        # Fairlearn parity & mitigation comparison
│
├── reports/                           # Generated compliance deliverables
│   ├── Project_Report.pdf             # Comprehensive technical report
│   ├── Project_Presentation.pptx      # 9-slide executive PowerPoint presentation
│   ├── Testing_Report.pdf             # Automated pytest verification report
│   ├── dataset/
│   │   └── Dataset_Source_Documentation.pdf
│   ├── model_evaluation/
│   │   └── Model_Evaluation_Report.pdf
│   ├── fairness/
│   │   └── Fairness_Evaluation_Report.pdf
│   └── exports/
│       ├── candidate_applications.csv
│       └── audit_logs.csv
│
└── tests/                             # Pytest test suite (19 test cases)
    ├── test_auth.py
    ├── test_database.py
    ├── test_preprocessing.py
    ├── test_models.py
    ├── test_fairness.py
    └── test_application.py
```

---

## 4. Dataset Source, Provenance & Exact 1,000-Record Mandate

### Source Provenance
- **Title:** Predicting Hiring Decisions in Recruitment Data
- **Publisher:** Rabie El Kharoua
- **Source URL:** https://www.kaggle.com/datasets/rabieelkharoua/predicting-hiring-decisions-in-recruitment-data
- **License:** Open Access / Community Benchmark Data License
- **Original Source Rows:** 1,500 records
- **Data Quality:** Zero (0) missing values, zero (0) duplicate records.

### Dataset Uniqueness Compliance
In strict adherence to HCLTech Career Shaper evaluation guidelines:
> *Dataset uniqueness is explicitly marked as **PENDING / UNVERIFIED** until peer group members provide their dataset names and source URLs for formal cross-schema comparison. Provenance is never fabricated.*

### Exact 1,000-Record Sampling
The official project guidelines mandate an exact modeling dataset of 1,000 valid records.
We executed reproducible stratified sampling using `sklearn.model_selection.train_test_split` with `random_state=42` over the joint stratum `(HiringDecision + '_' + Gender)`:
- **Output File:** `data/processed/recruitment_data_1000.csv`
- **Verification Assertion:** `assert len(df_1000) == 1000` (Passed)
- **Class Balance:**
  - Non-Hired (0): 690 records (69.0%)
  - Hired (1): 310 records (31.0%)
- **Demographic Balance (Gender):**
  - Group 0 (Female / Non-Traditional): 508 records (50.8%)
  - Group 1 (Male / Traditional): 492 records (49.2%)
- **Joint Subgroup Distribution:**
  - Group 0, Not Hired: 350 | Group 0, Hired: 158
  - Group 1, Not Hired: 340 | Group 1, Hired: 152

---

## 5. Machine Learning Evaluation Results

All three classification models were trained on 800 training records and evaluated on the identical 200-record held-out test partition (20% stratified split, `random_state=42`).

### Empirical Test Set Benchmark

| Algorithm | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **88.5%** | **91.5%** | 69.4% | 0.789 | **0.902** |
| **Random Forest (Production)** | 88.0% | 89.1% | 68.3% | 0.774 | 0.893 |
| **Decision Tree** | **88.5%** | 86.8% | **74.2%** | **0.803** | 0.866 |

### Model Selection Rationale
While **Decision Tree** and **Logistic Regression** achieved marginally higher raw test accuracy (88.5% vs 88.0%), **Random Forest Classifier** was selected as the primary production model for the recruiter interface because:
1. **Variance Reduction:** Bagging over 100 estimators prevents fragile decision-boundary overfitting to localized applicant credential splits.
2. **Posterior Calibration:** Produces smooth posterior probabilities essential for nuanced decision-support thresholds.
3. **SHAP TreeExplainer:** Yields exact, polynomial-time Shapley attributions without surrogate approximations.

---

## 6. Algorithmic Fairness & Bias Mitigation Results

Using Microsoft **Fairlearn**, fairness metrics were computed on held-out test data comparing Group 0 (Female / Non-Traditional, $N=102$) against Group 1 (Male / Traditional, $N=98$).

### Fairness Parity Findings
- **Demographic Parity Ratio:** `0.841` (Exceeds the US EEOC 4/5ths Rule threshold of `0.800`).
- **Demographic Parity Difference:** `0.0406` (Within ethical bounds $\le 0.1000$).
- **Equalized Odds Difference:** `0.1167` (Difference in subgroup TPR and FPR).
- **Group 0 Selection Rate:** $25.5\%$ | **Group 1 Selection Rate:** $21.4\%$
- **Group 0 True Positive Rate (TPR):** $75.0\%$ | **Group 1 True Positive Rate (TPR):** $63.3\%$

### Fairlearn Mitigation Experiment (ExponentiatedGradient)
To evaluate algorithmic debiasing, we applied Fairlearn's `ExponentiatedGradient` in-processing reduction with an `EqualizedOdds` constraint:

| Metric | Baseline (Unmitigated) | Mitigated (EqualizedOdds) | Trade-Off Impact |
| :--- | :---: | :---: | :--- |
| **Accuracy** | **88.5%** | 86.0% | $-2.5\%$ utility trade-off |
| **F1-Score** | **0.789** | 0.736 | $-0.053$ F1 score |
| **Demographic Parity Ratio** | **0.841** | 0.791 | Slight boundary shift |
| **Demographic Parity Diff** | 0.0406 | 0.0512 | Constrained optimization shift |
| **Equalized Odds Diff** | 0.1167 | 0.1854 | Bound penalty on sample |

> **Fairness-Utility Pareto Trade-Off Disclosure:**
> When the source distribution is already well-balanced across demographic groups, enforcing rigid mathematical reduction constraints can penalize overall model utility without proportional fairness gains. Transparent disclosure of these trade-offs is a core mandate of ethical AI engineering.

---

## 7. Explainable AI (SHAP & LIME)

Every candidate prediction is backed by dual explainability:
1. **SHAP (SHapley Additive exPlanations):**
   - Global importance: Identifies that Recruitment Strategy, Technical Skill Score, and Education Level dominate model discrimination.
   - Local force attribution: Quantifies the exact positive $(+)$ and negative $(-)$ contribution of each candidate credential toward the shortlisting score.
2. **LIME (Local Interpretable Model-agnostic Explanations):**
   - Generates human-readable if-then decision rules (e.g., `SkillScore > 80.00` $\to$ Supports Shortlisting).
3. **Mandatory Compliance Notice:**
   > *"Feature contribution reflects model association and is not proof of causation."*

---

## 8. Database Architecture & Security

The application is backed by an ACID-compliant SQLite relational database (`database/fairhire.db`):
- **Tables:** `users`, `candidate_profiles`, `recruiter_accounts`, `jobs`, `applications`, `predictions`, `audit_logs`.
- **Integrity:** Foreign keys enabled (`PRAGMA foreign_keys = ON`), cascading deletes, unique constraints, and secondary indexes on query keys.
- **Security:**
  - Salted **Bcrypt** password hashing (12 rounds). Zero plain-text passwords stored.
  - Parameterized SQL statements across all queries (100% SQL injection immune).
  - Role-based authorization (`require_role(["candidate"])`, `require_role(["recruiter"])`).
  - Immutable audit trail recording user logins, application reviews, and document exports.

---

## 9. Automated Testing Suite (Pytest)

The automated test suite covers all 6 subsystem domains:
```bash
pytest FairHire_India/tests -v
```
**Execution Summary:**
- Total Tests: **19 passed** (0 failed)
- Execution Duration: **9.04 seconds**
- Verified Domains:
  1. `test_auth.py`: Bcrypt hashing, password strength, duplicate prevention, session authentication.
  2. `test_database.py`: Schema initialization, foreign key constraints, CRUD workflows, audit logging.
  3. `test_preprocessing.py`: Exact 1,000-record assertion, zero missing values, zero duplicates, Gender omission from features.
  4. `test_models.py`: 3-model training, artifact persistence, evaluation metric bounds, inference pipeline.
  5. `test_fairness.py`: MetricFrame parity computations, ExponentiatedGradient mitigation artifacts.
  6. `test_application.py`: Page controller imports, PDF & PPTX report generation.

---

## 10. Quick Start & Execution Guide

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)

### Installation
```bash
# Clone or navigate to the project directory
cd FairHire_India

# Install dependencies
python -m pip install -r requirements.txt
```

### Launch Application
```bash
# From within the FairHire_India directory:
streamlit run app.py

# OR from the root workspace directory:
streamlit run app.py
```

### Demo Credentials
| Portal | Email | Password | Role |
| :--- | :--- | :--- | :--- |
| **Recruiter Portal** | `recruiter@fairhire.in` | `FairHire@Admin2026` | Lead Recruiter / Admin |
| **Candidate Portal** | `ananya.sen@example.com` | `Candidate@Pass123` | Registered Candidate |

---

## 11. HCLTech Project Deliverables

All required technical deliverables are generated dynamically and stored under `FairHire_India/reports/`:
1. `Project_Report.pdf`: Comprehensive technical report.
2. `Project_Presentation.pptx`: 9-slide executive PowerPoint presentation.
3. `Dataset_Source_Documentation.pdf`: Provenance and sampling documentation.
4. `Model_Evaluation_Report.pdf`: 3-model benchmark report.
5. `Fairness_Evaluation_Report.pdf`: Fairlearn parity and mitigation audit.
6. `Testing_Report.pdf`: Automated pytest execution report.
7. `README.md`: This master technical specification.
8. `Deployment_Guide.md`: Cloud deployment instructions.
9. `FairHire_India_Final.zip`: Clean, production-ready submission archive.

---

## 12. Ethical AI Governance & Limitations

- **Synthetic Benchmark Limitation:** The dataset utilized is a synthetic recruitment benchmark. While ideal for algorithmic fairness auditing, it may not reflect all localized nuances of Indian industry sectors.
- **Database Scaling:** While SQLite provides ACID compliance for single-instance applications, enterprise production scale requires migration to PostgreSQL.
- **Intersectional Parity:** Current mitigation audits focus on gender. Future iterations will evaluate intersectional fairness across regional background, language, and socioeconomic metrics.
- **Zero Automated Rejection:** AI outputs decision-support probabilities only. Human recruiter sign-off is mandatory for all employment determinations.
