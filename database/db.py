"""
FairHire India - Database Operations Layer
Thread-safe SQLite connection management, parameterized queries, and audit logging.
"""
import sqlite3
import contextlib
from typing import Optional, List, Dict, Any
from pathlib import Path
from config import DB_PATH, SCHEMA_PATH

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Return a configured SQLite connection with foreign keys enabled."""
    target_path = db_path or DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path), check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextlib.contextmanager
def get_db(db_path: Optional[Path] = None):
    """Context manager for database operations with automatic commit and rollback."""
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db(db_path: Optional[Path] = None) -> None:
    """Initialize database tables from schema.sql."""
    with get_db(db_path) as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_script = f.read()
        conn.executescript(schema_script)

# ----------------- AUDIT LOGGING -----------------
def log_audit(action: str, resource_type: str, resource_id: Optional[str] = None,
              details: Optional[str] = None, user_id: Optional[int] = None,
              ip_address: str = "127.0.0.1", db_path: Optional[Path] = None) -> int:
    """
    Log security, administrative, and model actions without storing passwords or tokens.
    """
    query = """
        INSERT INTO audit_logs (user_id, action, resource_type, resource_id, details, ip_address)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (user_id, action, resource_type, resource_id, details, ip_address))
        return cursor.lastrowid

def get_audit_logs(limit: int = 100, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Retrieve recent audit logs joined with user email."""
    query = """
        SELECT a.id, a.user_id, u.email as user_email, a.action, a.resource_type,
               a.resource_id, a.details, a.ip_address, a.timestamp
        FROM audit_logs a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.timestamp DESC
        LIMIT ?
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (limit,))
        return [dict(row) for row in cursor.fetchall()]

# ----------------- USERS -----------------
def create_user(email: str, password_hash: str, full_name: str, role: str,
                phone: Optional[str] = None, db_path: Optional[Path] = None) -> int:
    """Create a new user with bcrypt-hashed password."""
    query = """
        INSERT INTO users (email, password_hash, full_name, phone, role)
        VALUES (?, ?, ?, ?, ?)
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (email.lower().strip(), password_hash, full_name.strip(), phone, role))
        user_id = cursor.lastrowid
    log_audit("USER_REGISTERED", "users", str(user_id), f"Role: {role}", user_id=user_id, db_path=db_path)
    return user_id

def get_user_by_email(email: str, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Retrieve user record by email."""
    query = "SELECT * FROM users WHERE email = ? COLLATE NOCASE"
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (email.lower().strip(),))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_by_id(user_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Retrieve user record by ID."""
    query = "SELECT * FROM users WHERE id = ?"
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_users(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Retrieve list of users without password hashes."""
    query = "SELECT id, email, full_name, phone, role, created_at FROM users ORDER BY created_at DESC"
    with get_db(db_path) as conn:
        cursor = conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

# ----------------- CANDIDATE PROFILES -----------------
def create_candidate_profile(user_id: int, gender_audit: str = "Not Disclosed",
                             highest_education: str = "Bachelor's",
                             college_university: str = "",
                             state: str = "", city: str = "",
                             experience_years: int = 0, skills: str = "",
                             bio: str = "", db_path: Optional[Path] = None) -> int:
    query = """
        INSERT INTO candidate_profiles (
            user_id, gender_audit, highest_education, college_university,
            state, city, experience_years, skills, bio
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (
            user_id, gender_audit, highest_education, college_university,
            state, city, experience_years, skills, bio
        ))
        return cursor.lastrowid

def get_candidate_profile(user_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    query = """
        SELECT p.*, u.email, u.full_name, u.phone
        FROM candidate_profiles p
        JOIN users u ON p.user_id = u.id
        WHERE p.user_id = ?
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_candidate_profile(user_id: int, highest_education: str, college_university: str,
                             state: str, city: str, experience_years: int, skills: str,
                             bio: str, gender_audit: Optional[str] = None,
                             db_path: Optional[Path] = None) -> bool:
    if gender_audit is not None:
        query = """
            UPDATE candidate_profiles
            SET highest_education = ?, college_university = ?, state = ?, city = ?,
                experience_years = ?, skills = ?, bio = ?, gender_audit = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """
        params = (highest_education, college_university, state, city, experience_years, skills, bio, gender_audit, user_id)
    else:
        query = """
            UPDATE candidate_profiles
            SET highest_education = ?, college_university = ?, state = ?, city = ?,
                experience_years = ?, skills = ?, bio = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """
        params = (highest_education, college_university, state, city, experience_years, skills, bio, user_id)

    with get_db(db_path) as conn:
        cursor = conn.execute(query, params)
        return cursor.rowcount > 0

# ----------------- RECRUITER ACCOUNTS -----------------
def create_recruiter_account(user_id: int, department: str, designation: str,
                             employee_id: str, is_approved: int = 1,
                             db_path: Optional[Path] = None) -> int:
    query = """
        INSERT INTO recruiter_accounts (user_id, department, designation, employee_id, is_approved)
        VALUES (?, ?, ?, ?, ?)
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (user_id, department, designation, employee_id, is_approved))
        return cursor.lastrowid

def get_recruiter_account(user_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    query = """
        SELECT r.*, u.email, u.full_name, u.phone
        FROM recruiter_accounts r
        JOIN users u ON r.user_id = u.id
        WHERE r.user_id = ?
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

# ----------------- JOBS -----------------
def create_job(title: str, department: str, description: str, required_skills: str,
               education_requirements: str, experience_requirements: int,
               location: str, employment_type: str = "Full-time",
               status: str = "Published", created_by: Optional[int] = None,
               db_path: Optional[Path] = None) -> int:
    query = """
        INSERT INTO jobs (
            title, department, description, required_skills, education_requirements,
            experience_requirements, location, employment_type, status, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (
            title, department, description, required_skills, education_requirements,
            experience_requirements, location, employment_type, status, created_by
        ))
        job_id = cursor.lastrowid
    log_audit("JOB_CREATED", "jobs", str(job_id), f"Title: {title}", user_id=created_by, db_path=db_path)
    return job_id

def get_jobs(status: Optional[str] = None, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    query = "SELECT * FROM jobs"
    params = []
    if status:
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY created_at DESC"
    with get_db(db_path) as conn:
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_job_by_id(job_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    query = "SELECT * FROM jobs WHERE id = ?"
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (job_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_job_status(job_id: int, status: str, user_id: Optional[int] = None,
                      db_path: Optional[Path] = None) -> bool:
    query = "UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (status, job_id))
        success = cursor.rowcount > 0
    if success:
        log_audit("JOB_STATUS_UPDATED", "jobs", str(job_id), f"New status: {status}", user_id=user_id, db_path=db_path)
    return success

# ----------------- APPLICATIONS -----------------
def create_application(job_id: int, candidate_id: int, candidate_name: str,
                       candidate_email: str, candidate_phone: str,
                       education_level: int, experience_years: int,
                       previous_companies: int, distance_from_company: float,
                       skill_score: float, personality_score: float,
                       interview_score: float, recruitment_strategy: int,
                       db_path: Optional[Path] = None) -> int:
    import datetime
    import random
    # Generate realistic application identifier matching FH-YYYYMMDDHHMMSSXXX format
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand_suffix = f"{random.randint(100, 999)}"
    app_num = f"FH-{now_str}{rand_suffix}"
    query = """
        INSERT INTO applications (
            application_number, job_id, candidate_id, candidate_name, candidate_email,
            candidate_phone, education_level, experience_years, previous_companies,
            distance_from_company, skill_score, personality_score, interview_score,
            recruitment_strategy, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Submitted')
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (
            app_num, job_id, candidate_id, candidate_name, candidate_email,
            candidate_phone, education_level, experience_years, previous_companies,
            distance_from_company, skill_score, personality_score, interview_score,
            recruitment_strategy
        ))
        app_id = cursor.lastrowid
    log_audit("APPLICATION_SUBMITTED", "applications", str(app_id), f"Number: {app_num}", user_id=candidate_id, db_path=db_path)
    return app_id

def get_applications_by_candidate(candidate_id: int, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    query = """
        SELECT a.*, j.title as job_title, j.department, j.location as job_location,
               p.prediction_probability, p.recommendation, p.model_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        LEFT JOIN predictions p ON a.id = p.application_id
        WHERE a.candidate_id = ?
        ORDER BY a.created_at DESC
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (candidate_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_application_by_id(app_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    query = """
        SELECT a.*, j.title as job_title, j.department, j.location as job_location,
               p.prediction_label, p.prediction_probability, p.recommendation, p.model_name,
               cp.gender_audit, cp.highest_education as profile_education, cp.skills as candidate_skills
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        LEFT JOIN predictions p ON a.id = p.application_id
        LEFT JOIN candidate_profiles cp ON a.candidate_id = cp.user_id
        WHERE a.id = ?
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (app_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_applications(db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    query = """
        SELECT a.*, j.title as job_title, j.department,
               p.prediction_label, p.prediction_probability, p.recommendation, p.model_name,
               cp.gender_audit
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        LEFT JOIN predictions p ON a.id = p.application_id
        LEFT JOIN candidate_profiles cp ON a.candidate_id = cp.user_id
        ORDER BY a.created_at DESC
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

def update_application_status(app_id: int, status: str, recruiter_notes: Optional[str] = None,
                              reviewed_by: Optional[int] = None, db_path: Optional[Path] = None) -> bool:
    """Update human review status, recruiter notes, and notify candidate."""
    query = """
        UPDATE applications
        SET status = ?, recruiter_notes = COALESCE(?, recruiter_notes),
            reviewed_by = ?, reviewed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (status, recruiter_notes, reviewed_by, app_id))
        success = cursor.rowcount > 0

        # Retrieve candidate details to generate live notification
        cand_row = conn.execute("""
            SELECT a.candidate_id, a.application_number, j.title as job_title
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.id = ?
        """, (app_id,)).fetchone()

    if success:
        log_audit("APPLICATION_STATUS_UPDATED", "applications", str(app_id),
                  f"New status: {status} by Recruiter ID: {reviewed_by}", user_id=reviewed_by, db_path=db_path)
        if cand_row:
            create_notification(
                user_id=cand_row["candidate_id"],
                title=f"Application {status}: {cand_row['job_title']}",
                message=f"Your application #{cand_row['application_number']} status was updated to '{status}'. Check recruiter notes for details.",
                link_page="my_applications",
                db_path=db_path
            )
    return success

# ----------------- NOTIFICATIONS -----------------
def create_notification(user_id: int, title: str, message: str, link_page: str = "my_applications", db_path: Optional[Path] = None) -> int:
    query = """
        INSERT INTO notifications (user_id, title, message, link_page, is_read)
        VALUES (?, ?, ?, ?, 0)
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (user_id, title, message, link_page))
        return cursor.lastrowid

def get_notifications_by_user(user_id: int, unread_only: bool = False, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    query = "SELECT * FROM notifications WHERE user_id = ?"
    if unread_only:
        query += " AND is_read = 0"
    query += " ORDER BY created_at DESC"
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (user_id,))
        return [dict(row) for row in cursor.fetchall()]

def mark_notification_as_read(notification_id: int, db_path: Optional[Path] = None) -> bool:
    query = "UPDATE notifications SET is_read = 1 WHERE id = ?"
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (notification_id,))
        return cursor.rowcount > 0

# ----------------- EXTENDED JOB OPERATIONS -----------------
def update_job(job_id: int, title: str, department: str, description: str,
               required_skills: str, education_requirements: str,
               experience_requirements: int, location: str,
               employment_type: str = "Full-time", status: str = "Published",
               user_id: Optional[int] = None, db_path: Optional[Path] = None) -> bool:
    query = """
        UPDATE jobs
        SET title = ?, department = ?, description = ?, required_skills = ?,
            education_requirements = ?, experience_requirements = ?, location = ?,
            employment_type = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (
            title, department, description, required_skills, education_requirements,
            experience_requirements, location, employment_type, status, job_id
        ))
        success = cursor.rowcount > 0
    if success:
        log_audit("JOB_UPDATED", "jobs", str(job_id), f"Title: {title}, Status: {status}", user_id=user_id, db_path=db_path)
    return success

# ----------------- CANDIDATE SEARCH & DIRECTORY -----------------
def get_candidate_profiles_list(query_text: str = "", db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    sql = """
        SELECT cp.*, u.full_name, u.email, u.phone, u.created_at as member_since,
               COUNT(a.id) as application_count
        FROM candidate_profiles cp
        JOIN users u ON cp.user_id = u.id
        LEFT JOIN applications a ON cp.user_id = a.candidate_id
        WHERE u.role = 'candidate'
    """
    params = []
    if query_text:
        sql += " AND (u.full_name LIKE ? OR u.email LIKE ? OR cp.skills LIKE ? OR cp.city LIKE ? OR cp.state LIKE ?)"
        term = f"%{query_text.strip()}%"
        params.extend([term, term, term, term, term])
    sql += " GROUP BY cp.id ORDER BY u.full_name ASC"
    with get_db(db_path) as conn:
        cursor = conn.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

# ----------------- PREDICTIONS -----------------
def save_prediction(application_id: int, model_name: str, prediction_label: int,
                    prediction_probability: float, recommendation: str,
                    is_mitigated: int = 0, db_path: Optional[Path] = None) -> int:
    query = """
        INSERT OR REPLACE INTO predictions (
            application_id, model_name, prediction_label, prediction_probability,
            recommendation, is_mitigated, generated_at
        ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """
    with get_db(db_path) as conn:
        cursor = conn.execute(query, (
            application_id, model_name, prediction_label, prediction_probability,
            recommendation, is_mitigated
        ))
        pred_id = cursor.lastrowid
    log_audit("PREDICTION_GENERATED", "predictions", str(pred_id),
              f"App ID: {application_id}, Label: {prediction_label}, Prob: {prediction_probability:.4f}",
              db_path=db_path)
    return pred_id

# ----------------- SYSTEM STATS -----------------
def get_dashboard_stats(db_path: Optional[Path] = None) -> Dict[str, Any]:
    with get_db(db_path) as conn:
        total_candidates = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'candidate'").fetchone()[0]
        total_applications = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        shortlisted = conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'Shortlisted'").fetchone()[0]
        pending_review = conn.execute("SELECT COUNT(*) FROM applications WHERE status IN ('Submitted', 'Under Review', 'Awaiting Human Review')").fetchone()[0]
        published_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Published'").fetchone()[0]
        selected = conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'Selected'").fetchone()[0]

    return {
        "total_candidates": total_candidates,
        "total_applications": total_applications,
        "shortlisted": shortlisted,
        "pending_review": pending_review,
        "published_jobs": published_jobs,
        "selected": selected
    }
