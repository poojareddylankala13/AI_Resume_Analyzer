import sqlite3
import json
from datetime import datetime

DB_NAME = "database.db"

def get_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    # Return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Analysis table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_name TEXT NOT NULL,
            job_description TEXT,
            ats_score REAL,
            match_percentage REAL,
            missing_keywords TEXT,
            suggestions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(name, email, password_hash):
    """Add a new user to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        ''', (name, email, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    """Retrieve user details by email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_analysis(user_id, resume_name, job_description, ats_score, match_percentage, missing_keywords, suggestions):
    """Save an analysis record."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Convert lists/dicts to JSON strings for SQLite storage
    missing_keywords_json = json.dumps(missing_keywords)
    suggestions_json = json.dumps(suggestions)
    
    cursor.execute('''
        INSERT INTO analysis (user_id, resume_name, job_description, ats_score, match_percentage, missing_keywords, suggestions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, resume_name, job_description, ats_score, match_percentage, missing_keywords_json, suggestions_json))
    
    conn.commit()
    conn.close()

def get_user_analyses(user_id):
    """Retrieve all analyses for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM analysis WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    analyses = cursor.fetchall()
    conn.close()
    
    # Parse JSON strings back to Python objects
    parsed_analyses = []
    for row in analyses:
        r = dict(row)
        if r['missing_keywords']:
            r['missing_keywords'] = json.loads(r['missing_keywords'])
        if r['suggestions']:
            r['suggestions'] = json.loads(r['suggestions'])
        parsed_analyses.append(r)
        
    return parsed_analyses

def get_user_stats(user_id):
    """Retrieve aggregate statistics for a user's dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM analysis WHERE user_id = ?', (user_id,))
    total_analyses = cursor.fetchone()['total']
    
    cursor.execute('SELECT AVG(ats_score) as avg_score, MAX(ats_score) as max_score FROM analysis WHERE user_id = ?', (user_id,))
    stats = cursor.fetchone()
    
    conn.close()
    
    return {
        'total': total_analyses,
        'avg_score': stats['avg_score'] if stats['avg_score'] is not None else 0.0,
        'max_score': stats['max_score'] if stats['max_score'] is not None else 0.0
    }
