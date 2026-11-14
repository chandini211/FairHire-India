"""
FairHire India - Authentication & Security Package
"""
from .security import hash_password, verify_password, validate_password_strength
from .authentication import login_user, logout_user, get_current_user, is_authenticated
from .registration import register_candidate
from .authorization import require_role, require_authenticated, is_recruiter, is_candidate

__all__ = [
    "hash_password", "verify_password", "validate_password_strength",
    "login_user", "logout_user", "get_current_user", "is_authenticated",
    "register_candidate", "require_role", "require_authenticated",
    "is_recruiter", "is_candidate"
]
