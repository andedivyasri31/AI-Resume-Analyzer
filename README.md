# AI Resume Analyzer & Job Match System

A beginner-friendly portfolio project built with Python and Streamlit.

## Features

- Upload a PDF resume
- Extract resume text
- Detect technical skills
- Compare resume skills with a job description
- Calculate a job-match percentage
- Identify matched and missing skills
- Generate improvement suggestions
- Generate interview questions
- Store analysis history using SQLite
- Display a simple skill-match chart

## Tech Stack

- Python
- Streamlit
- PyPDF2
- Pandas
- SQLite
- Regular Expressions
- Git/GitHub

## Run locally

### 1. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
streamlit run app.py
```

The browser will open the application automatically.

## Project workflow

```text
Resume PDF
    ↓
PDF Text Extraction
    ↓
Skill Detection
    ↓
Job Description Skill Detection
    ↓
Matched / Missing Skills
    ↓
Match Percentage
    ↓
Suggestions + Interview Questions
    ↓
SQLite History
```

## Resume description

**AI-Powered Resume Analyzer & Job Match System**
- Developed a Python and Streamlit-based application to analyze resumes and compare candidate skills with job descriptions.
- Implemented PDF text extraction, automated skill detection, job-match scoring, and skill-gap identification.
- Added SQLite-based analysis history and an interactive dashboard with improvement suggestions and role-specific interview questions.

## Future enhancements

- LLM-based semantic resume analysis
- ATS keyword analysis
- Resume section detection
- Resume improvement rewriting
- Job recommendations
- Authentication
- Cloud deployment
