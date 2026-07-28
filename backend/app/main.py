from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .parse_resume import extract_text, analyze_resume
import uvicorn

app = FastAPI(title="AI Resume Analyser")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_description: str = Form(None)):
    contents = await file.read()
    text = extract_text(contents, file.filename)
    result = analyze_resume(text, job_description or "")
    return JSONResponse(result)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
