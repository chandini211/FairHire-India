"""
FairHire India - Candidate Notifications Center
Real-time alerts regarding application review stages, status updates, and recruiter feedback.
"""
import streamlit as st
from config import COLOR_PALETTE
from auth.authentication import get_current_user
from auth.authorization import require_role
from database.db import get_notifications_by_user, mark_notification_as_read
from components.ui import render_section_heading, render_disclaimer
from components.navbar import render_auth_header
from components.sidebar import render_sidebar
from components.footer import render_footer

def render_notifications_page():
    """Render the candidate notifications workspace."""
    require_role(["candidate"])
    user = get_current_user()

    render_sidebar()
    render_auth_header()

    render_section_heading("Candidate Notification Center", "Live updates and feedback on your submitted job applications.")
    render_disclaimer()

    notifications = get_notifications_by_user(user["id"])
    unread_count = len([n for n in notifications if not n.get("is_read")])

    c_stat1, c_stat2, _ = st.columns([3, 3, 6])
    with c_stat1:
        st.markdown(
            f"""
            <div class="fairhire-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">TOTAL ALERTS</div>
                <div class="mono-stat" style="font-size: 1.75rem;">{len(notifications)}</div>
            </div>
            """, unsafe_allow_html=True
        )
    with c_stat2:
        st.markdown(
            f"""
            <div class="fairhire-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: {COLOR_PALETTE['secondary_text']};">UNREAD ALERTS</div>
                <div class="mono-stat" style="font-size: 1.75rem; color: {COLOR_PALETTE['cyan'] if unread_count > 0 else COLOR_PALETTE['success_green']};">{unread_count}</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    if not notifications:
        st.info("You have no notifications at this time.")
        render_footer()
        return

    for n in notifications:
        n_id = n["id"]
        is_read = bool(n.get("is_read"))
        badge_class = "badge-green" if is_read else "badge-amber"
        status_text = "READ" if is_read else "NEW / UNREAD"

        st.markdown(
            f"""
            <div class="fairhire-card" style="border-left: 4px solid {COLOR_PALETTE['primary_purple'] if not is_read else COLOR_PALETTE['border']}; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span class="compliance-badge {badge_class}">{status_text}</span>
                        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 600; color: {COLOR_PALETTE['main_text']}; margin-top: 0.35rem;">
                            {n['title']}
                        </div>
                        <div style="font-size: 0.9rem; color: {COLOR_PALETTE['secondary_text']}; margin-top: 0.35rem; line-height: 1.5;">
                            {n['message']}
                        </div>
                    </div>
                    <div style="text-align: right; font-size: 0.75rem; color: {COLOR_PALETTE['secondary_text']};">
                        {str(n.get('created_at', ''))[:16]}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        btn_c1, btn_c2, _ = st.columns([2.5, 2.5, 7])
        with btn_c1:
            if not is_read:
                if st.button("Mark as Read", key=f"mark_read_{n_id}", type="secondary", use_container_width=True):
                    mark_notification_as_read(n_id)
                    st.rerun()
        with btn_c2:
            link = n.get("link_page") or "my_applications"
            if st.button("View Application →", key=f"link_act_{n_id}", type="primary", use_container_width=True):
                st.session_state["current_page"] = link
                st.rerun()

    render_footer()
