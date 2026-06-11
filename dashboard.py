import streamlit as st
import database
import pandas as pd
import plotly.express as px

def render_dashboard():
    st.title(f"Welcome back, {st.session_state['user_name']}!")
    st.markdown("---")
    
    user_id = st.session_state['user_id']
    stats = database.get_user_stats(user_id)
    analyses = database.get_user_analyses(user_id)
    
    # Dashboard Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Resumes Analyzed", value=stats['total'])
        
    with col2:
        st.metric(label="Average ATS Score", value=f"{stats['avg_score']:.1f}%")
        
    with col3:
        st.metric(label="Highest ATS Score", value=f"{stats['max_score']:.1f}%")
        
    st.markdown("---")
    
    if analyses:
        st.subheader("Recent Analysis Activity")
        
        # Prepare data for chart
        df = pd.DataFrame(analyses)
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Take the 10 most recent for the chart, reverse to chronological order
        recent_df = df.head(10).iloc[::-1]
        
        # Line chart for ATS scores over time
        if not recent_df.empty:
            fig = px.line(
                recent_df, 
                x='created_at', 
                y='ats_score', 
                markers=True,
                title='ATS Score Trend',
                labels={'created_at': 'Date Analyzed', 'ats_score': 'ATS Score (%)'}
            )
            fig.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
            
        st.subheader("Recent Uploads")
        # Display a simplified table of recent analyses
        display_df = df.head(5)[['resume_name', 'ats_score', 'created_at']]
        display_df.columns = ['Resume File', 'ATS Score', 'Date']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
    else:
        st.info("You haven't analyzed any resumes yet. Go to the 'Resume Analyzer' page to get started!")
