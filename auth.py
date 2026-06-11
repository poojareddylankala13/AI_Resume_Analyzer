import streamlit as st
import bcrypt
import database

def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed):
    """Check that a plain password matches a hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_user(email, password):
    """Authenticate a user."""
    user = database.get_user_by_email(email)
    if user:
        if check_password(password, user['password_hash']):
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = user['id']
            st.session_state['user_name'] = user['name']
            st.session_state['user_email'] = user['email']
            return True
    return False

def register_user(name, email, password):
    """Register a new user."""
    hashed_password = hash_password(password)
    return database.add_user(name, email, hashed_password)

def logout_user():
    """Clear session state to log out."""
    for key in ['logged_in', 'user_id', 'user_name', 'user_email']:
        if key in st.session_state:
            del st.session_state[key]

def is_authenticated():
    """Check if the user is currently logged in."""
    return st.session_state.get('logged_in', False)

def login_page():
    """Render the login and registration page."""
    st.title("AI Resume Analyzer")
    st.write("Welcome! Please login or register to continue.")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to your account")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login_user(email, password):
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
                    
    with tab2:
        st.subheader("Create a new account")
        with st.form("register_form"):
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_register = st.form_submit_button("Register")
            
            if submit_register:
                if new_password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif not new_name or not new_email:
                    st.error("Please fill all the fields.")
                else:
                    if register_user(new_name, new_email, new_password):
                        st.success("Registration successful! You can now log in.")
                    else:
                        st.error("Email already exists. Please login.")
