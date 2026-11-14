"""
FairHire India - Miscellaneous UI and Data Formatting Helpers
"""
from typing import Optional

def format_percentage(val: Optional[float], decimals: int = 1) -> str:
    if val is None:
        return "N/A"
    return f"{val * 100:.{decimals}f}%"

def format_currency_inr(amount: float) -> str:
    return f"₹{amount:,.0f}"

def get_status_color(status: str) -> str:
    mapping = {
        "Shortlisted": "#10B981",
        "Selected": "#10B981",
        "Under Review": "#F59E0B",
        "Awaiting Human Review": "#F59E0B",
        "Interview Scheduled": "#22C3D6",
        "Submitted": "#6558F5",
        "Not Selected": "#EF4444"
    }
    return mapping.get(status, "#94A3B8")
