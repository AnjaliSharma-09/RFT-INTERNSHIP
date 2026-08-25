import streamlit as st
import pandas as pd
import re
import io

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)


# ---------------------------------------------------------
# SKILL DATABASE
# ---------------------------------------------------------

SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "azure",
    "docker",
    "git",
    "github",
    "streamlit",
    "flask",
    "django"
]


# ---------------------------------------------------------
# EXTRACT SKILLS
# ---------------------------------------------------------

def extract_skills(text):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


# ---------------------------------------------------------
# EXTRACT NAME
# ---------------------------------------------------------

def extract_name(text, filename="Unknown"):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    for line in lines[:10]:

        if re.search(r"name\s*:", line, re.I):

            name = re.split(r":", line, maxsplit=1)[1].strip()

            if name:
                return name

    # Try first suitable line
    for line in lines[:5]:

        clean = re.sub(r"[^A-Za-z .]", "", line).strip()

        words = clean.split()

        if 2 <= len(words) <= 5:
            return clean

    return filename.rsplit(".", 1)[0]


# ---------------------------------------------------------
# EXTRACT EXPERIENCE
# ---------------------------------------------------------

def extract_experience(text):

    text_lower = text.lower()

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|year|yrs|yr)",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)"
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(pattern, text_lower)

        for value in matches:

            try:
                values.append(float(value))
            except:
                pass

    if values:
        return max(values)

    return 0.0


# ---------------------------------------------------------
# EXTRACT EDUCATION
# ---------------------------------------------------------

def extract_education(text):

    education_keywords = [
        "phd",
        "doctorate",
        "master",
        "m.tech",
        "mtech",
        "mba",
        "msc",
        "m.sc",
        "b.tech",
        "btech",
        "b.e",
        "be",
        "bachelor",
        "bsc",
        "b.sc",
        "diploma"
    ]

    text_lower = text.lower()

    found = []

    for keyword in education_keywords:

        if keyword in text_lower:
            found.append(keyword.upper())

    return ", ".join(sorted(set(found)))


# ---------------------------------------------------------
# READ TXT RESUME
# ---------------------------------------------------------

def read_txt(file):

    content = file.read()

    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="ignore")

    return content


# ---------------------------------------------------------
# READ CSV RESUMES
# ---------------------------------------------------------

def read_csv(file):

    df = pd.read_csv(file)

    return df


# ---------------------------------------------------------
# CONVERT CSV ROW TO RESUME TEXT
# ---------------------------------------------------------

def csv_to_resumes(df):

    resumes = []

    for index, row in df.iterrows():

        text_parts = []

        for column in df.columns:

            value = row[column]

            if pd.notna(value):

                text_parts.append(
                    f"{column}: {value}"
                )

        text = "\n".join(text_parts)

        resumes.append({
            "filename": f"candidate_{index + 1}.csv",
            "text": text
        })

    return resumes


# ---------------------------------------------------------
# TEXT SIMILARITY
# ---------------------------------------------------------

def calculate_similarity(resume_text, job_description):

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return similarity * 100

    except:

        return 0


# ---------------------------------------------------------
# SKILL MATCH SCORE
# ---------------------------------------------------------

def calculate_skill_score(resume_skills, required_skills):

    if not required_skills:
        return 100

    matched = set(resume_skills).intersection(
        set(required_skills)
    )

    return (
        len(matched) /
        len(required_skills)
    ) * 100


# ---------------------------------------------------------
# EXPERIENCE SCORE
# ---------------------------------------------------------

def calculate_experience_score(
    candidate_experience,
    required_experience
):

    if required_experience <= 0:
        return 100

    score = (
        candidate_experience /
        required_experience
    ) * 100

    return min(score, 100)


# ---------------------------------------------------------
# EDUCATION SCORE
# ---------------------------------------------------------

def calculate_education_score(
    education,
    job_description
):

    education_lower = education.lower()
    jd_lower = job_description.lower()

    education_terms = [
        "phd",
        "doctorate",
        "master",
        "m.tech",
        "mtech",
        "mba",
        "msc",
        "m.sc",
        "b.tech",
        "btech",
        "bachelor",
        "bsc",
        "b.sc"
    ]

    required = [
        term
        for term in education_terms
        if term in jd_lower
    ]

    if not required:
        return 100

    matched = [
        term
        for term in required
        if term in education_lower
    ]

    return (
        len(matched) /
        len(required)
    ) * 100


# ---------------------------------------------------------
# MAIN RESUME ANALYSIS
# ---------------------------------------------------------

def analyze_resume(
    filename,
    resume_text,
    job_description
):

    candidate_name = extract_name(
        resume_text,
        filename
    )

    skills = extract_skills(
        resume_text
    )

    experience = extract_experience(
        resume_text
    )

    education = extract_education(
        resume_text
    )

    required_skills = extract_skills(
        job_description
    )

    skill_score = calculate_skill_score(
        skills,
        required_skills
    )

    required_experience = extract_experience(
        job_description
    )

    experience_score = calculate_experience_score(
        experience,
        required_experience
    )

    education_score = calculate_education_score(
        education,
        job_description
    )

    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )

    missing_skills = sorted(
        set(required_skills) - set(skills)
    )

    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    final_score = (
        skill_score * 0.40 +
        experience_score * 0.15 +
        education_score * 0.15 +
        similarity_score * 0.30
    )

    return {
        "Candidate": candidate_name,
        "Skills": ", ".join(skills),
        "Experience": experience,
        "Education": education,
        "Skill Score": round(skill_score, 2),
        "Experience Score": round(experience_score, 2),
        "Education Score": round(education_score, 2),
        "Similarity Score": round(similarity_score, 2),
        "Match Score": round(final_score, 2),
        "Missing Skills": ", ".join(missing_skills),
        "File": filename
    }


# =========================================================
# STREAMLIT UI
# =========================================================

st.title("🤖 AI Resume Screening & Ranking System")

st.markdown(
    """
    Upload multiple resumes and enter a job description.
    The system extracts candidate information, compares
    resumes with the job requirements and ranks candidates.
    """
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("⚙️ Screening Settings")

threshold = st.sidebar.slider(
    "Shortlisting Score (%)",
    min_value=0,
    max_value=100,
    value=60
)


# ---------------------------------------------------------
# JOB DESCRIPTION
# ---------------------------------------------------------

st.header("📋 Job Description")

job_description = st.text_area(
    "Enter the Job Description",
    height=200,
    placeholder="""
Example:

We are looking for a Machine Learning Engineer.

Requirements:
Python
Machine Learning
Pandas
NumPy
Scikit-learn
SQL
Deep Learning
2 years experience
B.Tech or M.Tech
"""
)


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

st.header("📂 Upload Resumes")

uploaded_files = st.file_uploader(
    "Upload TXT or CSV resumes",
    type=["txt", "csv"],
    accept_multiple_files=True
)


# ---------------------------------------------------------
# ANALYZE
# ---------------------------------------------------------

if st.button("🚀 Screen Resumes"):

    if not job_description.strip():

        st.error(
            "Please enter a job description."
        )

        st.stop()

    if not uploaded_files:

        st.error(
            "Please upload at least one resume."
        )

        st.stop()

    resumes = []

    for file in uploaded_files:

        if file.name.lower().endswith(".txt"):

            text = read_txt(file)

            resumes.append({
                "filename": file.name,
                "text": text
            })

        elif file.name.lower().endswith(".csv"):

            df = read_csv(file)

            csv_resumes = csv_to_resumes(df)

            resumes.extend(csv_resumes)


    results = []

    for resume in resumes:

        result = analyze_resume(
            resume["filename"],
            resume["text"],
            job_description
        )

        results.append(result)


    results_df = pd.DataFrame(results)


    # -----------------------------------------------------
    # RANK CANDIDATES
    # -----------------------------------------------------

    results_df = results_df.sort_values(
        by="Match Score",
        ascending=False
    ).reset_index(drop=True)

    results_df.insert(
        0,
        "Rank",
        range(1, len(results_df) + 1)
    )


    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    st.success(
        f"Successfully analyzed {len(results_df)} candidates."
    )

    st.header("🏆 Candidate Ranking")

    st.dataframe(
        results_df,
        use_container_width=True
    )


    # -----------------------------------------------------
    # SHORTLIST
    # -----------------------------------------------------

    shortlisted = results_df[
        results_df["Match Score"] >= threshold
    ]

    st.header("✅ Shortlisted Candidates")

    if len(shortlisted) > 0:

        st.dataframe(
            shortlisted,
            use_container_width=True
        )

    else:

        st.warning(
            "No candidates reached the shortlist threshold."
        )


    # -----------------------------------------------------
    # CANDIDATE DETAILS
    # -----------------------------------------------------

    st.header("🔎 Candidate Details")

    for _, candidate in results_df.iterrows():

        with st.expander(
            f"#{candidate['Rank']} "
            f"{candidate['Candidate']} "
            f"— {candidate['Match Score']}%"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Name:**",
                    candidate["Candidate"]
                )

                st.write(
                    "**Experience:**",
                    f"{candidate['Experience']} years"
                )

                st.write(
                    "**Education:**",
                    candidate["Education"]
                )

            with col2:

                st.write(
                    "**Skills:**",
                    candidate["Skills"]
                )

                st.write(
                    "**Missing Skills:**",
                    candidate["Missing Skills"]
                    if candidate["Missing Skills"]
                    else "None 🎉"
                )

            st.progress(
                min(
                    int(candidate["Match Score"]),
                    100
                )
            )


    # -----------------------------------------------------
    # EXPORT
    # -----------------------------------------------------

    st.header("📥 Export Results")

    csv_data = shortlisted.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Shortlisted Candidates",
        data=csv_data,
        file_name="shortlisted_candidates.csv",
        mime="text/csv"
    )


    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    st.header("📊 Screening Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Candidates",
        len(results_df)
    )

    col2.metric(
        "Shortlisted",
        len(shortlisted)
    )

    col3.metric(
        "Highest Score",
        f"{results_df['Match Score'].max():.2f}%"
    )

    col4.metric(
        "Average Score",
        f"{results_df['Match Score'].mean():.2f}%"
    )