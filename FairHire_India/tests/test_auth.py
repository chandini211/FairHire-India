"""
Automated Tests — Authentication & Security Subsystem
Verifies candidate registration, duplicate prevention, password strength, and Bcrypt hashing.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import sqlite3
from auth.security import hash_password, verify_password, validate_password_strength
from auth.registration import register_candidate
from auth.authentication import login_user
from database.db import get_user_by_email

def test_password_hashing():
    raw_pwd = "Secure@Password2026"
    hashed = hash_password(raw_pwd)
    assert hashed != raw_pwd
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_password_strength_enforcement():
    # Weak passwords
    assert validate_password_strength("short")[0] is False
    assert validate_password_strength("nouppercase123!")[0] is False
    assert validate_password_strength("NOLOWERCASE123!")[0] is False
    assert validate_password_strength("NoNumberSpecial!")[0] is False
    assert validate_password_strength("NoSpecialChar123")[0] is False

    # Valid strong password
    assert validate_password_strength("Valid@Pass123")[0] is True

def test_candidate_registration_and_duplicate_prevention():
    import uuid
    unique_email = f"test_{uuid.uuid4().hex[:6]}@fairhire.in"

    success, msg, uid = register_candidate(
        full_name="Test Candidate",
        email=unique_email,
        phone="+91-9988776655",
        password="Valid@Pass123",
        confirm_password="Valid@Pass123",
        highest_education="Master's",
        college_university="IIT Bombay",
        state="Maharashtra",
        city="Mumbai",
        gender_audit="Female"
    )
    assert success is True
    assert uid is not None

    # Duplicate registration check
    dup_success, dup_msg, _ = register_candidate(
        full_name="Duplicate Attempt",
        email=unique_email,
        phone="+91-9988776655",
        password="Valid@Pass123",
        confirm_password="Valid@Pass123",
        highest_education="Master's",
        college_university="IIT Bombay",
        state="Maharashtra",
        city="Mumbai"
    )
    assert dup_success is False
    assert "already exists" in dup_msg.lower()

def test_user_login():
    # Attempt login with seeded recruiter
    success, msg, user = login_user("recruiter@fairhire.in", "FairHire@Admin2026")
    assert success is True
    assert user["role"] == "recruiter"

    # Invalid password attempt
    fail_success, fail_msg, _ = login_user("recruiter@fairhire.in", "WrongPassword123!")
    assert fail_success is False
