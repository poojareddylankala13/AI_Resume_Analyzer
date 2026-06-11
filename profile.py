import streamlit as st
import database

def render_profile():
    st.title("User Profile")
    
    user_id = st.session_state['user_id']
    user = database.get_connection().cursor().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    stats = database.get_user_stats(user_id)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://api.dicebear.com/7.x/initials/svg?seed=" + user['name'], width=150)
        
    with col2:
        st.subheader("Profile Information")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Member Since:** {user['created_at']}")
        
    st.markdown("---")
    
    st.subheader("Account Statistics")
    st.write(f"**Total Resumes Analyzed:** {stats['total']}")
    
    st.markdown("---")
    
    st.subheader("Update Profile (Mock)")
    st.info("Profile updating is disabled in this demonstration version.")
    with st.form("update_profile"):
        st.text_input("New Name", value=user['name'], disabled=True)
        st.text_input("New Email", value=user['email'], disabled=True)
        st.form_submit_button("Update", disabled=True)
