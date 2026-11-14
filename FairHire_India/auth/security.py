"""
FairHire India - Cryptographic Security & Password Hashing
Bcrypt implementation for salted password hashing and secure verification.
"""
import bcrypt
import re
import secrets
from typing import Tuple

def hash_password(password: str) -> str:
    """Hash password using Bcrypt with automatic salt generation."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against stored Bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Enforce strong password policy:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special symbol
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character (!@#$%^&*...)."
    return True, "Password meets security requirements."

def generate_session_token() -> str:
    """Generate cryptographically secure 256-bit session token."""
    return secrets.token_urlsafe(32)
