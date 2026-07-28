import io
import re
import tempfile
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = set([
    "python","java","c++","c#","sql","javascript","react","node","django","flask","fastapi",
    "git","docker","kubernetes","aws","azure","gcp","pandas","numpy","tensorflow","pytorch",
    "nlp","machine learning","deep learning","data analysis","excel","tableau","spark"
])

def extract_text(file_bytes: bytes, filename: str):
    fname = filename.lower()
    if fname.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            return pdf_extract_text(tmp.name)
    elif fname.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except:
            return ""

def extract_skills(text: str):
    text_low = text.lower()
    skills_found = [s for s in SKILLS if s in text_low]
    return skills_found

def extract_experience(text: str):
    doc = nlp(text)
    exp_sentences = [sent.text.strip() for sent in doc.sents if re.search(r'\b\d{4}\b', sent.text) or 'experience' in sent.text.lower()]
    return exp_sentences[:10]

def analyze_resume(resume_text: str, job_description: str):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    matched = resume_skills & job_skills
    score = 0
    if job_skills:
        score = int(100 * len(matched) / len(job_skills))
    else:
        score = min(100, len(resume_skills) * 10)
    doc = nlp(resume_text)
    summary = " ".join([sent.text for sent in list(doc.sents)[:2]])
    return {
        "summary": summary,
        "resume_skills": list(resume_skills),
        "job_skills": list(job_skills),
        "matched_skills": list(matched),
        "score": score,
        "top_experience_snippets": extract_experience(resume_text)
    }
