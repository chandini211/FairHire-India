"""
FairHire India - Input Validation Helpers
Email format, phone format, and numeric range bounds.
"""
import re
from typing import Tuple

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PHONE_REGEX = r"^\+?[0-9\s-]{10,15}$"

def validate_email(email: str) -> bool:
    return bool(email and re.match(EMAIL_REGEX, email.strip()))

def validate_phone(phone: str) -> bool:
    return bool(phone and re.match(PHONE_REGEX, phone.strip()))

def validate_application_scores(skill_score: float, personality_score: float, interview_score: float) -> Tuple[bool, str]:
    for name, val in [("Skill Score", skill_score), ("Personality Score", personality_score), ("Interview Score", interview_score)]:
        if not (0.0 <= val <= 100.0):
            return False, f"{name} must be between 0 and 100."
    return True, "Scores within valid boundaries."
