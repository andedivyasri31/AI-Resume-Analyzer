import os
import re
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()

DB_FILE = "resume_analyzer.db"

SKILLS = [
    "python", "java", "c", "c++", "sql", "mysql", "postgresql",
    "html", "css", "javascript", "react", "node.js", "flask", "django",
    "streamlit", "pandas", "numpy", "scikit-learn", "machine learning",
    "deep learning", "tensorflow", "pytorch", "nlp", "computer vision",
    "artificial intelligence", "generative ai", "llm", "api", "rest api",
    "git", "github", "aws", "azure", "docker", "kubernetes",
    "power bi", "tableau", "excel", "communication", "problem solving",
    "data analysis", "data visualization", "mongodb", "firebase"
]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            match_score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)

def normalize(text):
    return re.sub(r"[^a-z0-9+#.\- ]+", " ", text.lower())

def find_skills(text):
    clean = normalize(text)
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, clean):
            found.append(skill)
    return sorted(set(found))

def calculate_match(resume_skills, job_skills):
    if not job_skills:
        return 0.0
    return round((len(set(resume_skills) & set(job_skills)) / len(set(job_skills))) * 100, 1)

def save_analysis(file_name, score, matched, missing):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO analyses(file_name, match_score, matched_skills, missing_skills, created_at) VALUES (?, ?, ?, ?, ?)",
        (file_name, score, ", ".join(matched), ", ".join(missing), datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM analyses ORDER BY id DESC", conn)
    conn.close()
    return df

def generate_suggestions(missing):
    if not missing:
        return [
            "Your resume covers the detected skills in the job description.",
            "Keep your project descriptions measurable and mention the tools you actually used.",
            "Prepare examples that demonstrate each major skill during interviews."
        ]
    suggestions = [
        "Add relevant missing skills only if you genuinely know or have practiced them.",
        "Consider building a small project around one or two important missing skills.",
        "Mention concrete project outcomes instead of only listing technologies.",
        "Keep the resume tailored to the specific job description."
    ]
    return suggestions

def generate_questions(matched, missing):
    questions = []
    for skill in matched[:5]:
        questions.append(f"Explain your practical experience with {skill}.")
    for skill in missing[:3]:
        questions.append(f"What is {skill}, and where would you use it?")
    if not questions:
        questions = [
            "Tell me about your most important technical project.",
            "How do you debug a program when the output is incorrect?",
            "Describe a technical challenge you faced and how you solved it."
        ]
    return questions

init_db()

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & Job Match System")
st.caption("Resume analysis • Skill gap detection • Job matching • Interview preparation")

with st.sidebar:
    st.header("How it works")
    st.write("1. Upload a PDF resume")
    st.write("2. Paste a job description")
    st.write("3. Analyze skills")
    st.write("4. Review the match and gaps")
    st.write("5. Prepare for interviews")

resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area(
    "Paste the Job Description",
    height=220,
    placeholder="Paste the complete job description here..."
)

if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    if not resume:
        st.error("Please upload a PDF resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Analyzing resume..."):
        resume_text = extract_pdf_text(resume)

        if not resume_text.strip():
            st.error("Could not extract text from this PDF. Try a text-based PDF.")
            st.stop()

        resume_skills = find_skills(resume_text)
        job_skills = find_skills(job_description)

        matched = sorted(set(resume_skills) & set(job_skills))
        missing = sorted(set(job_skills) - set(resume_skills))
        score = calculate_match(resume_skills, job_skills)

        save_analysis(resume.name, score, matched, missing)

    st.success("Analysis completed!")

    c1, c2, c3 = st.columns(3)
    c1.metric("Job Match", f"{score}%")
    c2.metric("Matched Skills", len(matched))
    c3.metric("Skill Gaps", len(missing))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("✅ Matched Skills")
        if matched:
            for skill in matched:
                st.write(f"• {skill}")
        else:
            st.info("No matching skills detected.")

    with right:
        st.subheader("📌 Missing Skills")
        if missing:
            for skill in missing:
                st.write(f"• {skill}")
        else:
            st.success("No detected skill gaps.")

    st.subheader("📊 Skill Match Breakdown")
    chart_data = pd.DataFrame({
        "Category": ["Matched", "Missing"],
        "Skills": [len(matched), len(missing)]
    }).set_index("Category")
    st.bar_chart(chart_data)

    st.subheader("💡 Improvement Suggestions")
    for item in generate_suggestions(missing):
        st.write(f"• {item}")

    st.subheader("🎯 Interview Questions")
    for i, question in enumerate(generate_questions(matched, missing), 1):
        st.write(f"**{i}.** {question}")

    with st.expander("View extracted resume text"):
        st.text(resume_text[:10000])

st.divider()
st.subheader("📚 Analysis History")

history = load_history()
if history.empty:
    st.info("No analyses yet.")
else:
    display_df = history[["file_name", "match_score", "created_at"]].copy()
    display_df.columns = ["Resume", "Match %", "Analyzed At"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.caption("Built with Python, Streamlit, PDF parsing, skill matching, data visualization and SQLite.")
