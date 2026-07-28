# Backend (FastAPI) - AI Resume Analyser

## Setup

1. Create and activate a virtual environment (recommended):

   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate

2. Install dependencies:

   pip install -r backend/requirements.txt

3. Install spaCy English model:

   python -m spacy download en_core_web_sm

4. Run the API:

   uvicorn backend.app.main:app --reload --port 8000

The API exposes POST /analyze which accepts a file upload (form field `file`) and an optional `job_description` form field.
