"""
FairHire India - Role-Based Authorization
Controls access to restricted recruiter and candidate views.
"""
import streamlit as st
from typing import Optional, List
from auth.authentication import get_current_user, is_authenticated

def require_authenticated() -> bool:
    """Ensure user is logged in. Returns True if authorized, else switches page to login."""
    if not is_authenticated():
        st.session_state["current_page"] = "login"
        st.warning("Please sign in to access this page.")
        st.stop()
        return False
    return True

def require_role(allowed_roles: List[str]) -> bool:
    """Enforce role-based access. Halts execution if user role is not permitted."""
    require_authenticated()
    user = get_current_user()
    if not user or user.get("role") not in allowed_roles:
        st.error("Access Denied: You do not possess the required permissions to view this resource.")
        st.stop()
        return False
    return True

def is_recruiter() -> bool:
    user = get_current_user()
    return bool(user and user.get("role") in ["recruiter", "admin"])

def is_candidate() -> bool:
    user = get_current_user()
    return bool(user and user.get("role") == "candidate")
