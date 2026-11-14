"""
FairHire India - Database Seeding Script
Initializes database schema, seeds the bootstrap recruiter account, sample job vacancies,
diverse candidate profiles, and realistic candidate applications.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DB_PATH
from database.db import (
    init_db, create_user, get_user_by_email, create_candidate_profile,
    create_recruiter_account, create_job, create_application,
    update_application_status, log_audit
)
from auth.security import hash_password

def seed_database():
    print(f"Initializing database at: {DB_PATH}")
    init_db()

    # 1. Bootstrap Recruiter Account
    recruiter_email = "recruiter@fairhire.in"
    recruiter = get_user_by_email(recruiter_email)
    if not recruiter:
        recruiter_id = create_user(
            email=recruiter_email,
            password_hash=hash_password("FairHire@Admin2026"),
            full_name="Priya Sharma (Lead Talent Partner)",
            role="recruiter",
            phone="+91-9876543210"
        )
        create_recruiter_account(
            user_id=recruiter_id,
            department="Talent Acquisition & Diversity",
            designation="Principal Technical Recruiter",
            employee_id="HCLT-REC-1042"
        )
        print(f"Recruiter account seeded: {recruiter_email} (ID: {recruiter_id})")
    else:
        recruiter_id = recruiter["id"]
        print("Recruiter account already exists.")

    # 2. Seed Jobs
    sample_jobs = [
        {
            "title": "Machine Learning Engineer - Responsible AI",
            "department": "AI & Advanced Analytics",
            "description": "Design, benchmark, and deploy fair and explainable machine learning systems. Focus on algorithmic auditing, fairness metrics, and robust model governance across Indian hiring workflows.",
            "required_skills": "Python, Scikit-learn, Fairlearn, SHAP, PyTorch, SQL, Model Monitoring",
            "education_requirements": "Bachelor's or Master's in Computer Science, Data Science, or related STEM field",
            "experience_requirements": 3,
            "location": "Bengaluru, Karnataka (Hybrid)",
            "employment_type": "Full-time",
            "status": "Published"
        },
        {
            "title": "Senior Python Developer - Enterprise SaaS",
            "department": "Platform Engineering",
            "description": "Build high-throughput backend services, data processing pipelines, and intuitive Streamlit/FastAPI enterprise recruitment platforms with strict security standards.",
            "required_skills": "Python 3.11+, SQLite/PostgreSQL, REST APIs, Streamlit, Docker, Unit Testing",
            "education_requirements": "Bachelor's in Engineering, Technology, or Computer Applications",
            "experience_requirements": 4,
            "location": "Noida, Uttar Pradesh (On-site)",
            "employment_type": "Full-time",
            "status": "Published"
        },
        {
            "title": "Data Scientist - People Analytics",
            "department": "Human Capital Intelligence",
            "description": "Conduct exploratory data analysis, build predictive candidate shortlisting pipelines, compute group parity metrics, and translate complex demographic metrics for recruiter review.",
            "required_skills": "Pandas, NumPy, Statistical Modeling, Plotly, LIME, Feature Engineering",
            "education_requirements": "Master's or PhD in Statistics, Mathematics, or Data Science",
            "experience_requirements": 2,
            "location": "Hyderabad, Telangana (Hybrid)",
            "employment_type": "Full-time",
            "status": "Published"
        },
        {
            "title": "Cybersecurity & Compliance Specialist",
            "department": "Information Security",
            "description": "Audit enterprise web applications, enforce RBAC, Bcrypt credential protection, input sanitization, and data protection in compliance with Indian DPDP Act 2023.",
            "required_skills": "Application Security, OWASP Top 10, Penetration Testing, Cryptography, SQLite Security",
            "education_requirements": "Bachelor's in Cyber Security, IT, or Computer Science",
            "experience_requirements": 3,
            "location": "Chennai, Tamil Nadu (Hybrid)",
            "employment_type": "Full-time",
            "status": "Published"
        }
    ]

    from database.db import get_jobs
    existing_jobs = get_jobs()
    job_ids = [j["id"] for j in existing_jobs]

    if not job_ids:
        for job in sample_jobs:
            jid = create_job(
                title=job["title"],
                department=job["department"],
                description=job["description"],
                required_skills=job["required_skills"],
                education_requirements=job["education_requirements"],
                experience_requirements=job["experience_requirements"],
                location=job["location"],
                employment_type=job["employment_type"],
                status=job["status"],
                created_by=recruiter_id
            )
            job_ids.append(jid)
        print(f"Seeded {len(job_ids)} active job openings.")

    # 3. Seed Sample Candidates and Applications
    sample_candidates = [
        {
            "name": "Ananya Sen",
            "email": "ananya.sen@example.com",
            "phone": "+91-9811223344",
            "gender_audit": "Female",
            "education": "Master's",
            "education_level": 2, # Master's
            "college": "Jadavpur University, Kolkata",
            "state": "West Bengal",
            "city": "Kolkata",
            "exp": 4,
            "skills": "Python, Scikit-learn, Fairness in ML, SHAP, SQL",
            "job_idx": 0,
            "prev_comp": 2,
            "dist": 12.5,
            "skill_score": 88.0,
            "personality_score": 82.0,
            "interview_score": 85.0,
            "strategy": 1
        },
        {
            "name": "Rahul Verma",
            "email": "rahul.verma@example.com",
            "phone": "+91-9822334455",
            "gender_audit": "Male",
            "education": "Bachelor's",
            "education_level": 1, # Bachelor's
            "college": "Delhi Technological University",
            "state": "Delhi",
            "city": "New Delhi",
            "exp": 5,
            "skills": "Python, Streamlit, PostgreSQL, Docker, Microservices",
            "job_idx": 1,
            "prev_comp": 3,
            "dist": 8.0,
            "skill_score": 84.0,
            "personality_score": 79.0,
            "interview_score": 80.0,
            "strategy": 2
        },
        {
            "name": "Kavitha Raman",
            "email": "kavitha.raman@example.com",
            "phone": "+91-9833445566",
            "gender_audit": "Female",
            "education": "PhD",
            "education_level": 3, # PhD
            "college": "IIT Madras",
            "state": "Tamil Nadu",
            "city": "Chennai",
            "exp": 3,
            "skills": "Statistical Modeling, Fairlearn, MetricFrame, Pandas, LIME",
            "job_idx": 2,
            "prev_comp": 1,
            "dist": 15.0,
            "skill_score": 92.0,
            "personality_score": 86.0,
            "interview_score": 90.0,
            "strategy": 1
        },
        {
            "name": "Arjun Patel",
            "email": "arjun.patel@example.com",
            "phone": "+91-9844556677",
            "gender_audit": "Male",
            "education": "Bachelor's",
            "education_level": 1,
            "college": "NIT Surat",
            "state": "Gujarat",
            "city": "Surat",
            "exp": 2,
            "skills": "Python, AppSec, OWASP, Penetration Testing",
            "job_idx": 3,
            "prev_comp": 1,
            "dist": 22.0,
            "skill_score": 78.0,
            "personality_score": 75.0,
            "interview_score": 72.0,
            "strategy": 2
        },
        {
            "name": "Meera Krishnan",
            "email": "meera.krishnan@example.com",
            "phone": "+91-9855667788",
            "gender_audit": "Female",
            "education": "Master's",
            "education_level": 2,
            "college": "Anna University, Chennai",
            "state": "Tamil Nadu",
            "city": "Coimbatore",
            "exp": 6,
            "skills": "Machine Learning, Deep Learning, Explainable AI, PyTorch",
            "job_idx": 0,
            "prev_comp": 3,
            "dist": 5.5,
            "skill_score": 91.0,
            "personality_score": 88.0,
            "interview_score": 89.0,
            "strategy": 1
        },
        {
            "name": "Vikram Singh",
            "email": "vikram.singh@example.com",
            "phone": "+91-9866778899",
            "gender_audit": "Male",
            "education": "Bachelor's",
            "education_level": 1,
            "college": "Manipal Institute of Technology",
            "state": "Karnataka",
            "city": "Bengaluru",
            "exp": 1,
            "skills": "Python, Basic ML, Pandas, Git",
            "job_idx": 0,
            "prev_comp": 1,
            "dist": 30.0,
            "skill_score": 62.0,
            "personality_score": 65.0,
            "interview_score": 60.0,
            "strategy": 3
        }
    ]

    for cand in sample_candidates:
        existing = get_user_by_email(cand["email"])
        if not existing:
            uid = create_user(
                email=cand["email"],
                password_hash=hash_password("Candidate@Pass123"),
                full_name=cand["name"],
                role="candidate",
                phone=cand["phone"]
            )
            create_candidate_profile(
                user_id=uid,
                gender_audit=cand["gender_audit"],
                highest_education=cand["education"],
                college_university=cand["college"],
                state=cand["state"],
                city=cand["city"],
                experience_years=cand["exp"],
                skills=cand["skills"],
                bio=f"Passionate tech professional specializing in {cand['skills'].split(',')[0]}."
            )
            target_job_id = job_ids[cand["job_idx"] % len(job_ids)]
            app_id = create_application(
                job_id=target_job_id,
                candidate_id=uid,
                candidate_name=cand["name"],
                candidate_email=cand["email"],
                candidate_phone=cand["phone"],
                education_level=cand["education_level"],
                experience_years=cand["exp"],
                previous_companies=cand["prev_comp"],
                distance_from_company=cand["dist"],
                skill_score=cand["skill_score"],
                personality_score=cand["personality_score"],
                interview_score=cand["interview_score"],
                recruitment_strategy=cand["strategy"]
            )
            # Give first candidate Shortlisted status
            if cand["name"] in ["Ananya Sen", "Meera Krishnan"]:
                update_application_status(app_id, "Shortlisted", "Excellent algorithmic reasoning and fairness audit knowledge.", reviewed_by=recruiter_id)
            elif cand["name"] == "Vikram Singh":
                update_application_status(app_id, "Under Review", "Profile submitted; awaiting assessment review.", reviewed_by=recruiter_id)
            print(f"Candidate seeded: {cand['name']} (App ID: {app_id})")

    log_audit("DATABASE_SEEDED", "database", "ALL", "Initial seed data loaded successfully.", user_id=recruiter_id)
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
