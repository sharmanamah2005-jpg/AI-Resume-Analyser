from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_empty_txt():
    files = {'file': ('test.txt', b'Test skills: Python, SQL\nExperience: 3 years', 'text/plain')}
    data = {'job_description': 'Looking for Python and Docker'}
    resp = client.post("/analyze", files=files, data=data)
    assert resp.status_code == 200
    body = resp.json()
    assert 'score' in body
