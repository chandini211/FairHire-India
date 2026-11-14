-- FairHire India Database Schema
-- SQLite 3 Database Definition with Foreign Keys, Constraints, and Indexes

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT NOT NULL CHECK(role IN ('candidate', 'recruiter', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. Candidate Profiles Table
CREATE TABLE IF NOT EXISTS candidate_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    gender_audit TEXT DEFAULT 'Not Disclosed',
    highest_education TEXT,
    college_university TEXT,
    state TEXT,
    city TEXT,
    experience_years INTEGER DEFAULT 0,
    skills TEXT,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON candidate_profiles(user_id);

-- 3. Recruiter Accounts Table
CREATE TABLE IF NOT EXISTS recruiter_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    department TEXT NOT NULL,
    designation TEXT NOT NULL,
    employee_id TEXT UNIQUE NOT NULL,
    is_approved INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_recruiters_user_id ON recruiter_accounts(user_id);

-- 4. Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT NOT NULL,
    education_requirements TEXT NOT NULL,
    experience_requirements INTEGER NOT NULL DEFAULT 0,
    location TEXT NOT NULL,
    employment_type TEXT NOT NULL DEFAULT 'Full-time',
    status TEXT NOT NULL DEFAULT 'Published' CHECK(status IN ('Draft', 'Published', 'Closed')),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);

-- 5. Applications Table
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_number TEXT UNIQUE NOT NULL,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    candidate_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    candidate_name TEXT NOT NULL,
    candidate_email TEXT NOT NULL,
    candidate_phone TEXT,
    education_level INTEGER NOT NULL DEFAULT 2,
    experience_years INTEGER NOT NULL DEFAULT 0,
    previous_companies INTEGER NOT NULL DEFAULT 1,
    distance_from_company REAL NOT NULL DEFAULT 10.0,
    skill_score REAL NOT NULL DEFAULT 70.0,
    personality_score REAL NOT NULL DEFAULT 70.0,
    interview_score REAL NOT NULL DEFAULT 70.0,
    recruitment_strategy INTEGER NOT NULL DEFAULT 2,
    status TEXT NOT NULL DEFAULT 'Submitted' CHECK(status IN ('Submitted', 'Under Review', 'Shortlisted', 'Awaiting Human Review', 'Interview Scheduled', 'Selected', 'Not Selected')),
    recruiter_notes TEXT,
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, candidate_id)
);

CREATE INDEX IF NOT EXISTS idx_applications_job ON applications(job_id);
CREATE INDEX IF NOT EXISTS idx_applications_candidate ON applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);

-- 6. Model Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER UNIQUE NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    model_name TEXT NOT NULL,
    prediction_label INTEGER NOT NULL,
    prediction_probability REAL NOT NULL,
    recommendation TEXT NOT NULL,
    is_mitigated INTEGER DEFAULT 0,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_predictions_app ON predictions(application_id);

-- 7. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    details TEXT,
    ip_address TEXT DEFAULT '127.0.0.1',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);


-- 8. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    link_page TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
