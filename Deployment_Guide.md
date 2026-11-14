# FairHire India — Streamlit Deployment & Cloud Hosting Guide
### HCLTech Career Shaper Project

---

## 1. Overview
FairHire India is a production-ready, modular Streamlit enterprise web application. This guide outlines how to deploy the application locally, on virtual machines, or on **Streamlit Community Cloud**.

---

## 2. Local Environment Execution

### Step 1: Verify Python Version
Ensure Python 3.11 or higher is installed:
```bash
python --version
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 4: Run Application
```bash
streamlit run app.py
```
The browser will automatically open to `http://localhost:8501`.

---

## 3. Deployment to Streamlit Community Cloud

### Step 1: Repository Structure
Ensure the repository has the following files in the deployment root:
```
├── app.py
├── config.py
├── requirements.txt
├── database/
│   ├── schema.sql
│   └── seed.py
├── ml/
├── fairness/
├── explainability/
├── components/
├── pages/
├── data/
│   └── processed/
│       └── recruitment_data_1000.csv
└── models/
```

### Step 2: Connect to Streamlit Cloud
1. Push the code to a GitHub repository (e.g. `github.com/your-username/FairHire_India`).
2. Log into [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New App"**.
4. Select your repository, branch (`main`), and set the main file path to `app.py`.
5. Under **Advanced Settings**, ensure Python version is set to **3.11**.
6. Click **"Deploy!"**.

---

## 4. SQLite Persistence on Cloud Hosting

> [!WARNING]
> **Ephemeral Container Storage Limitation:**
> On serverless and free-tier hosting platforms like Streamlit Community Cloud, local filesystem storage (including SQLite `.db` files) is ephemeral. Whenever the application container restarts, updates, or scales down due to inactivity, any dynamic database writes made during that session will revert to the initial repository commit state.
>
> **Production Scaling Recommendation:**
> For true persistent enterprise deployment:
> 1. Use an external managed PostgreSQL database (e.g. Supabase, Neon, AWS RDS).
> 2. Set the connection string via Streamlit Secrets: `st.secrets["DATABASE_URL"]`.
> 3. For academic evaluation and evaluation demos, FairHire India automatically seeds the database on initial container boot if `fairhire.db` does not exist.

---

## 5. Environment Secrets Management

When deploying in production, configure environment variables in `.streamlit/secrets.toml`:

```toml
FAIRHIRE_ENV = "production"
SECRET_KEY = "your-cryptographically-secure-random-key"
INITIAL_RECRUITER_EMAIL = "recruiter@fairhire.in"
INITIAL_RECRUITER_PASSWORD = "YourSecurePassword2026!"
```

---

## 6. Verification Checklist
- [x] Python 3.11+ runtime verified
- [x] All relative imports and sys.path configured
- [x] Exact 1,000-record dataset included under `data/processed/`
- [x] Model and preprocessor artifacts generated and cached
- [x] Automated test suite passed: `pytest tests -v` (19 passed)
- [x] Report generation tested and operational
