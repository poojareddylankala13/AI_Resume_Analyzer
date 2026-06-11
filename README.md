# AI Resume Analyzer

A complete web application to analyze resumes against job descriptions, calculate ATS compatibility, and provide AI-powered feedback. Built with Python, Streamlit, and SQLite.

## Features
- **User Authentication**: Secure login and registration.
- **Dashboard**: Track your resume analysis statistics.
- **Resume Analyzer**: Upload a PDF resume and a job description to get an ATS score, keyword matches, missing keywords, and AI suggestions.
- **Analysis History**: View, search, and sort past analyses.
- **User Profile**: View user information.

## Technology Stack
- **Frontend/Backend**: Streamlit (Python)
- **Database**: SQLite
- **PDF Processing**: PyPDF2
- **NLP/Keyword Extraction**: scikit-learn (CountVectorizer)
- **Authentication**: bcrypt
- **Data Visualization**: plotly

## Setup Instructions

1. **Clone or Download the Repository**
2. **Navigate to the Project Directory**
   ```bash
   cd resume_analyzer
   ```
3. **Install Dependencies**
   Make sure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```bash
   streamlit run app.py
   ```
5. **Open in Browser**
   The application will typically be available at `http://localhost:8501`.

## Database
The SQLite database (`database.db`) will be created automatically upon the first run of the application.
