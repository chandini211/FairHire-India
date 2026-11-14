"""
Automated Tests — SQLite Database Layer
Verifies schema constraints, transactions, CRUD methods, foreign keys, and audit logging.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import sqlite3
import tempfile
from config import SCHEMA_PATH
from database.db import (
    get_connection, init_db, create_user, get_user_by_email,
    create_job, get_jobs, create_application, get_application_by_id,
    log_audit, get_audit_logs
)
from auth.security import hash_password

@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_path = Path(f.name)

    # Initialize schema
    init_db(temp_path)
    yield temp_path
    if temp_path.exists():
        temp_path.unlink()

def test_database_initialization(temp_db):
    conn = get_connection(temp_db)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()

    expected_tables = {"users", "candidate_profiles", "recruiter_accounts", "jobs", "applications", "predictions", "audit_logs"}
    assert expected_tables.issubset(tables)

def test_foreign_key_enforcement(temp_db):
    conn = get_connection(temp_db)
    # Attempting to insert application with non-existent job_id should raise IntegrityError
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("""
            INSERT INTO applications (application_number, job_id, candidate_id, candidate_name, candidate_email)
            VALUES ('APP-FAIL', 9999, 9999, 'Ghost', 'ghost@example.com')
        """)
    conn.close()

def test_crud_job_and_application(temp_db):
    # 1. Create Recruiter User
    recruiter_id = create_user(
        email="lead.recruiter@fairhire.in",
        password_hash=hash_password("Pass@1234"),
        full_name="Lead Recruiter",
        role="recruiter",
        db_path=temp_db
    )

    # 2. Create Job
    job_id = create_job(
        title="AI Engineer",
        department="AI Lab",
        description="Build ethical models",
        required_skills="Python, Fairlearn",
        education_requirements="B.Tech",
        experience_requirements=2,
        location="Bengaluru",
        created_by=recruiter_id,
        db_path=temp_db
    )
    assert job_id > 0

    # 3. Create Candidate User
    candidate_id = create_user(
        email="dev.candidate@fairhire.in",
        password_hash=hash_password("Pass@1234"),
        full_name="Dev Candidate",
        role="candidate",
        db_path=temp_db
    )

    # 4. Create Application
    app_id = create_application(
        job_id=job_id,
        candidate_id=candidate_id,
        candidate_name="Dev Candidate",
        candidate_email="dev.candidate@fairhire.in",
        candidate_phone="+91-9988776655",
        education_level=2,
        experience_years=3,
        previous_companies=1,
        distance_from_company=10.0,
        skill_score=85.0,
        personality_score=80.0,
        interview_score=85.0,
        recruitment_strategy=1,
        db_path=temp_db
    )
    assert app_id > 0

    # 5. Fetch application
    app = get_application_by_id(app_id, db_path=temp_db)
    assert app is not None
    assert app["candidate_name"] == "Dev Candidate"

def test_audit_logging(temp_db):
    log_id = log_audit(
        action="TEST_ACTION",
        resource_type="system",
        resource_id="101",
        details="Verifying audit logging integrity",
        db_path=temp_db
    )
    assert log_id > 0

    logs = get_audit_logs(limit=10, db_path=temp_db)
    assert any(l["action"] == "TEST_ACTION" for l in logs)
