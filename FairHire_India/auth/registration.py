"""
FairHire India - Candidate Registration Service
Form validation, duplicate checks, Bcrypt hashing, and candidate profile creation.
"""
import re
from typing import Tuple, Optional
from database.db import get_user_by_email, create_user, create_candidate_profile
from auth.security import hash_password, validate_password_strength

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

def register_candidate(
    full_name: str,
    email: str,
    phone: str,
    password: str,
    confirm_password: str,
    highest_education: str,
    college_university: str,
    state: str,
    city: str,
    gender_audit: str = "Not Disclosed",
    experience_years: int = 0,
    skills: str = "",
    bio: str = ""
) -> Tuple[bool, str, Optional[int]]:
    """Validate and register a new candidate user and profile."""

    # 1. Required fields validation
    if not full_name.strip():
        return False, "Full name is required.", None
    if not email.strip():
        return False, "Email address is required.", None
    if not phone.strip():
        return False, "Contact phone number is required.", None

    # 2. Email format validation
    if not re.match(EMAIL_REGEX, email.strip()):
        return False, "Please enter a valid email address.", None

    # 3. Duplicate email prevention
    if get_user_by_email(email.strip()):
        return False, "An account with this email address already exists. Please sign in.", None

    # 4. Password confirmation check
    if password != confirm_password:
        return False, "Passwords do not match.", None

    # 5. Password strength check
    is_strong, msg = validate_password_strength(password)
    if not is_strong:
        return False, msg, None

    # 6. Bcrypt password hashing
    password_hash = hash_password(password)

    # 7. Create User Record
    try:
        user_id = create_user(
            email=email.strip().lower(),
            password_hash=password_hash,
            full_name=full_name.strip(),
            role="candidate",
            phone=phone.strip()
        )

        # 8. Create Candidate Profile
        create_candidate_profile(
            user_id=user_id,
            gender_audit=gender_audit,
            highest_education=highest_education,
            college_university=college_university.strip(),
            state=state.strip(),
            city=city.strip(),
            experience_years=experience_years,
            skills=skills.strip(),
            bio=bio.strip()
        )

        return True, "Registration successful! You may now sign in.", user_id
    except Exception as e:
        return False, f"Registration failed due to a database error: {str(e)}", None
