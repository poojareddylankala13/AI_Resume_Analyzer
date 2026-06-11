import streamlit as st
import database
import pandas as pd

def render_history():
    st.title("Analysis History")
    
    user_id = st.session_state['user_id']
    analyses = database.get_user_analyses(user_id)
    
    if not analyses:
        st.info("No analysis history found.")
        return
        
    df = pd.DataFrame(analyses)
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Filter and sort options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", ["Date (Newest First)", "Date (Oldest First)", "ATS Score (Highest)", "ATS Score (Lowest)"])
    with col2:
        search_query = st.text_input("Search by Resume Name")
        
    # Apply filtering
    if search_query:
        df = df[df['resume_name'].str.contains(search_query, case=False)]
        
    # Apply sorting
    if sort_by == "Date (Newest First)":
        df = df.sort_values('created_at', ascending=False)
    elif sort_by == "Date (Oldest First)":
        df = df.sort_values('created_at', ascending=True)
    elif sort_by == "ATS Score (Highest)":
        df = df.sort_values('ats_score', ascending=False)
    elif sort_by == "ATS Score (Lowest)":
        df = df.sort_values('ats_score', ascending=True)
        
    if df.empty:
        st.warning("No results match your search.")
        return
        
    st.write(f"Showing {len(df)} results")
    
    # Display results
    for _, row in df.iterrows():
        with st.expander(f"{row['resume_name']} - {row['created_at']} - Score: {row['ats_score']}%"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("ATS Score", f"{row['ats_score']}%")
                st.metric("Keyword Match", f"{row['match_percentage']}%")
                
            with col2:
                st.write("**Missing Keywords:**")
                missing_kws = row.get('missing_keywords', [])
                if missing_kws:
                    st.write(", ".join(missing_kws[:10]))
                else:
                    st.write("None! Perfect match.")
                    
            st.markdown("---")
            st.write("**AI Suggestions:**")
            
            suggestions = row.get('suggestions', {})
            if isinstance(suggestions, dict):
                st.write(f"*{suggestions.get('summary', '')}*")
                
                if suggestions.get('skills_to_add'):
                    st.write("**Skills to Consider Adding:**")
                    for skill in suggestions['skills_to_add']:
                        st.write(f"- {skill}")
                        
                if suggestions.get('improvement_areas'):
                    st.write("**Improvement Areas:**")
                    for area in suggestions['improvement_areas']:
                        st.write(f"- {area}")
            else:
                st.write("No detailed suggestions available for this old record.")
