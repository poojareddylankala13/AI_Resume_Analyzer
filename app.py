import streamlit as st
import auth
import database
import dashboard
import history
import profile
import analyzer
import time

# Set page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
database.init_db()

def render_analyzer_page():
    st.title("📄 AI Resume Analyzer")
    st.write("Upload your resume and provide a job description to get AI-powered insights.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Upload Resume")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
    with col2:
        st.subheader("2. Job Description")
        job_description = st.text_area("Paste the job description here", height=200)
        
    if st.button("Analyze Resume", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("Please upload a resume (PDF).")
        elif not job_description.strip():
            st.error("Please provide a job description.")
        else:
            with st.spinner("Analyzing resume against job description..."):
                # Extract text
                resume_text = analyzer.extract_text_from_pdf(uploaded_file)
                
                if not resume_text:
                    st.error("Could not extract text from the PDF. Please try a different file.")
                    return
                
                # Analyze
                results = analyzer.analyze_resume(resume_text, job_description)
                
                # Save to database
                database.save_analysis(
                    st.session_state['user_id'],
                    uploaded_file.name,
                    job_description,
                    results['ats_score'],
                    results['match_percentage'],
                    results['missing_keywords'],
                    results['suggestions']
                )
                
                st.success("Analysis Complete!")
                
                # Display Results
                st.markdown("---")
                st.header("Analysis Results")
                
                score_col, chart_col = st.columns([1, 2])
                
                with score_col:
                    st.metric(label="ATS Match Score", value=f"{results['ats_score']}%")
                    st.progress(results['ats_score'] / 100.0)
                    
                with chart_col:
                    st.subheader("Keyword Match")
                    st.write(f"**Matched:** {len(results['matched_keywords'])} | **Missing:** {len(results['missing_keywords'])}")
                    
                st.markdown("---")
                
                tab1, tab2, tab3 = st.tabs(["AI Suggestions", "Missing Keywords", "Matched Keywords"])
                
                with tab1:
                    st.subheader("AI Feedback")
                    suggestions = results['suggestions']
                    if "error" in suggestions:
                        st.error(suggestions["error"])
                    else:
                        st.write(f"**Overall Assessment:** {suggestions['summary']}")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write("**Areas for Improvement:**")
                            for area in suggestions.get('improvement_areas', []):
                                st.write(f"- {area}")
                                
                        with col_b:
                            st.write("**Formatting Tips:**")
                            for tip in suggestions.get('formatting_tips', []):
                                st.write(f"- {tip}")
                                
                with tab2:
                    st.subheader("Missing Keywords")
                    st.write("These keywords are present in the job description but missing from your resume. Consider adding them if you have the relevant experience.")
                    if results['missing_keywords']:
                        for kw in results['missing_keywords']:
                            st.markdown(f"- `{kw}`")
                    else:
                        st.write("Great job! You matched all major keywords.")
                        
                with tab3:
                    st.subheader("Matched Keywords")
                    if results['matched_keywords']:
                        for kw in results['matched_keywords']:
                            st.markdown(f"- ✅ `{kw}`")

def main():
    if not auth.is_authenticated():
        auth.login_page()
    else:
        # Sidebar Navigation
        with st.sidebar:
            st.title("Menu")
            st.write(f"Hello, **{st.session_state['user_name']}**!")
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                ["Dashboard", "Resume Analyzer", "Analysis History", "Profile"]
            )
            
            st.markdown("---")
            if st.button("Logout"):
                auth.logout_user()
                st.rerun()
                
        # Page Routing
        if page == "Dashboard":
            dashboard.render_dashboard()
        elif page == "Resume Analyzer":
            render_analyzer_page()
        elif page == "Analysis History":
            history.render_history()
        elif page == "Profile":
            profile.render_profile()

if __name__ == "__main__":
    main()
