# AI Resume Analyzer

An AI-powered web application that analyzes resumes against a given Job Description (JD) and provides a resume-to-job match score along with relevant insights.

## Features

* Upload resume in PDF format
* Enter a Job Description
* Extract and analyze resume content
* Compare resume skills with job requirements
* Generate a resume-to-JD match score
* Identify relevant and missing skills
* Simple and interactive Streamlit interface

## Technologies Used

* Python
* Streamlit
* Natural Language Processing (NLP)
* PDF Processing
* Text Matching
* Git & GitHub

## Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── architecture.txt
├── sample_job_description.txt
├── resume_project_description.txt
├── .gitignore
└── .env.example
```

## How to Run

1. Clone the repository.
2. Open the project folder in VS Code.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit application:

```bash
streamlit run app.py
```

5. Open the local URL shown in the terminal.

## Use Case

This project helps job seekers understand how well their resume matches a specific job description and identify skills that may need to be highlighted or improved.

## Future Enhancements

* Improved semantic matching using embeddings
* Better skill extraction
* Resume improvement suggestions
* Support for multiple resume formats
* More detailed ATS analysis

## Author

**Ande Divyasri**
