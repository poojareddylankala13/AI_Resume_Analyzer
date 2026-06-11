import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer

def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF file."""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def clean_text(text):
    """Clean and standardize text for comparison."""
    if not text:
        return ""
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_keywords(text, num_keywords=20):
    """Extract top keywords from text using CountVectorizer."""
    if not text.strip():
        return []
    
    # Simple stop words list
    stop_words = ['and', 'the', 'to', 'of', 'in', 'for', 'with', 'on', 'as', 'a', 'an', 'is', 'it', 'this', 'that', 'by', 'from', 'or']
    
    try:
        vectorizer = CountVectorizer(stop_words=stop_words, max_features=num_keywords, ngram_range=(1, 2))
        vectorizer.fit_transform([text])
        return list(vectorizer.vocabulary_.keys())
    except ValueError:
        # Fallback if text is too short or empty after removing stop words
        words = text.split()
        return list(set([w for w in words if w not in stop_words]))[:num_keywords]

def analyze_resume(resume_text, job_description_text):
    """
    Compare resume text with job description and return metrics.
    """
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_description_text)
    
    jd_keywords = extract_keywords(clean_jd, num_keywords=30)
    
    if not jd_keywords:
        return {
            "ats_score": 0.0,
            "match_percentage": 0.0,
            "missing_keywords": [],
            "matched_keywords": [],
            "suggestions": {"error": "Job description is too short or invalid."}
        }
    
    matched_keywords = []
    missing_keywords = []
    
    for kw in jd_keywords:
        if kw in clean_resume:
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)
            
    # Calculate scores
    total_keywords = len(jd_keywords)
    matched_count = len(matched_keywords)
    
    match_percentage = (matched_count / total_keywords) * 100 if total_keywords > 0 else 0
    
    # Calculate a somewhat realistic ATS score (factors in both keyword match and length/formatting mock)
    # In a real scenario, this would be much more complex.
    ats_score = min(100.0, match_percentage * 1.1) 
    
    # Generate Mock AI Suggestions
    suggestions = generate_mock_ai_suggestions(ats_score, missing_keywords, matched_keywords)
    
    return {
        "ats_score": round(ats_score, 2),
        "match_percentage": round(match_percentage, 2),
        "missing_keywords": missing_keywords,
        "matched_keywords": matched_keywords,
        "suggestions": suggestions
    }

def generate_mock_ai_suggestions(ats_score, missing_keywords, matched_keywords):
    """Generate mock AI suggestions based on the analysis results."""
    suggestions = {
        "summary": "",
        "improvement_areas": [],
        "skills_to_add": [],
        "formatting_tips": []
    }
    
    if ats_score >= 80:
        suggestions["summary"] = "Excellent match! Your resume is highly tailored to the job description."
    elif ats_score >= 50:
        suggestions["summary"] = "Good potential, but needs more specific keyword optimization."
    else:
        suggestions["summary"] = "Your resume needs significant tailoring to align with the requirements of this role."
        
    if missing_keywords:
        suggestions["skills_to_add"] = missing_keywords[:10]
        suggestions["improvement_areas"].append("Consider adding the missing keywords naturally into your experience section.")
        
    if len(matched_keywords) < 5:
        suggestions["improvement_areas"].append("Your resume lacks core competencies mentioned in the job description.")
        
    suggestions["formatting_tips"] = [
        "Ensure you are using standard headings (Experience, Education, Skills).",
        "Avoid using complex tables or graphics that ATS systems might struggle to parse.",
        "Use bullet points to describe your achievements, starting with action verbs."
    ]
    
    return suggestions
