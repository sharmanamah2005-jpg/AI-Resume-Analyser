import React, {useState} from 'react';

function App(){
  const [file, setFile] = useState(null);
  const [job, setJob] = useState("");
  const [result, setResult] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    if(!file) return;
    const form = new FormData();
    form.append('file', file);
    form.append('job_description', job);
    const res = await fetch('http://localhost:8000/analyze', {method:'POST', body:form});
    const json = await res.json();
    setResult(json);
  };

  return (
    <div style={{padding:20}}>
      <h1>AI Resume Analyser</h1>
      <form onSubmit={submit}>
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <br/>
        <textarea placeholder="Paste job description..." value={job} onChange={e=>setJob(e.target.value)} style={{width:400,height:120}} />
        <br/>
        <button type="submit">Analyze</button>
      </form>
      {result && (
        <div style={{marginTop:20}}>
          <h2>Score: {result.score}</h2>
          <h3>Matched Skills</h3>
          <ul>{result.matched_skills.map(s=> <li key={s}>{s}</li>)}</ul>
          <h3>Resume Skills</h3>
          <ul>{result.resume_skills.map(s=> <li key={s}>{s}</li>)}</ul>
          <h3>Top Experience</h3>
          <pre>{result.top_experience_snippets.join("\n\n")}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
