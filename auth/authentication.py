"""
FairHire India - Authentication Service
Session management and credential verification.
"""
import streamlit as st
from typing import Optional, Dict, Any, Tuple
from database.db import get_user_by_email, log_audit
from auth.security import verify_password

def login_user(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Verify user credentials, create session in st.session_state, and record audit log."""
    if not email or not password:
        return False, "Email and password are required.", None

    user = get_user_by_email(email)
    if not user:
        return False, "Invalid email address or password.", None

    if not verify_password(password, user["password_hash"]):
        log_audit("FAILED_LOGIN_ATTEMPT", "users", str(user["id"]), f"Failed login for {email}")
        return False, "Invalid email address or password.", None

    # Safe user session object (excluding password hash)
    safe_user = {
        "id": user["id"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "phone": user["phone"]
    }

    st.session_state["user"] = safe_user
    st.session_state["authenticated"] = True
    st.session_state["role"] = user["role"]

    log_audit("USER_LOGIN_SUCCESS", "users", str(user["id"]), f"Role: {user['role']}", user_id=user["id"])
    return True, "Login successful.", safe_user

def logout_user() -> None:
    """Clear session state and log logout event."""
    user = st.session_state.get("user")
    if user:
        log_audit("USER_LOGOUT", "users", str(user["id"]), f"User {user['email']} logged out.", user_id=user["id"])
    st.session_state["user"] = None
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.session_state["current_page"] = "landing"

def get_current_user() -> Optional[Dict[str, Any]]:
    """Retrieve currently active user session from Streamlit state."""
    return st.session_state.get("user")

def is_authenticated() -> bool:
    """Check if a session is currently active."""
    return bool(st.session_state.get("authenticated") and st.session_state.get("user"))
