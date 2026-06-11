import streamlit as st
import analyzer

# ---------------- SESSION SETUP ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- AUTH ----------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")


def register():
    st.title("📝 Register")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if username in st.session_state.users:
            st.warning("User already exists")
        else:
            st.session_state.users[username] = password
            st.success("Registered successfully! Go to login.")


# ---------------- DASHBOARD ----------------
def dashboard():
    st.title(f"👋 Welcome {st.session_state.username}")

    menu = st.sidebar.radio(
        "Navigation",
        ["Resume Analyzer", "History", "Profile", "Logout"]
    )

    if menu == "Resume Analyzer":
        analyzer_page()
    elif menu == "History":
        history_page()
    elif menu == "Profile":
        profile_page()
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()


# ---------------- ANALYZER PAGE ----------------
def analyzer_page():
    st.header("📄 AI Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_description = st.text_area("Paste Job Description")

    mode = st.radio("AI Mode", ["Ollama (Local)", "BYOK (OpenAI)"])

    api_key = None
    if mode == "BYOK (OpenAI)":
        api_key = st.text_input("Enter API Key", type="password")

    if st.button("Analyze Resume"):
        if uploaded_file and job_description:

            with st.spinner("Analyzing..."):

                resume_text = analyzer.extract_text_from_pdf(uploaded_file)

                results = analyzer.analyze_resume(
                    resume_text,
                    job_description,
                    mode="ollama" if mode == "Ollama (Local)" else "openai",
                    api_key=api_key
                )

                # SAVE HISTORY
                st.session_state.history.append(results)

                # DISPLAY RESULTS
                st.subheader("📊 ATS Score")
                st.metric("Score", results["ats_score"])

                st.subheader("📈 Match Percentage")
                st.progress(results["match_percentage"] / 100)

                st.subheader("✅ Matched Keywords")
                st.write(results["matched_keywords"])

                st.subheader("❌ Missing Keywords")
                st.write(results["missing_keywords"])

                st.subheader("💡 Suggestions")

                if "error" in results["suggestions"]:
                    st.error(results["suggestions"]["error"])
                else:
                    st.write("**Summary:**")
                    st.write(results["suggestions"]["summary"])

                    st.write("**Improvements:**")
                    for item in results["suggestions"]["improvement_areas"]:
                        st.write(f"- {item}")

                    st.write("**Formatting Tips:**")
                    for item in results["suggestions"]["formatting_tips"]:
                        st.write(f"- {item}")

        else:
            st.warning("Please upload resume and job description")


# ---------------- HISTORY ----------------
def history_page():
    st.header("📜 Analysis History")

    if not st.session_state.history:
        st.info("No history yet")
        return

    for i, item in enumerate(st.session_state.history[::-1]):
        st.subheader(f"Analysis {i+1}")
        st.write(f"ATS Score: {item['ats_score']}")
        st.write(f"Match: {item['match_percentage']}%")
        st.write("---")


# ---------------- PROFILE ----------------
def profile_page():
    st.header("👤 Profile")

    st.write(f"Username: {st.session_state.username}")
    st.write(f"Total Analyses: {len(st.session_state.history)}")


# ---------------- MAIN ----------------
def main():
    st.sidebar.title("AI Resume Analyzer")

    if not st.session_state.logged_in:
        choice = st.sidebar.radio("Menu", ["Login", "Register"])

        if choice == "Login":
            login()
        else:
            register()
    else:
        dashboard()


if __name__ == "__main__":
    main()
