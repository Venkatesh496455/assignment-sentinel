import { useState } from 'react'
import './App.css'

function App() {
  const [owner, setOwner] = useState('Venkatesh496455')
  const [repo, setRepo] = useState('assignment-sentinel')
  const [prNumber, setPrNumber] = useState('1')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleReview = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/review?owner=${owner}&repo=${repo}&pr_number=${prNumber}`
      )
      const data = await res.json()

      if (!res.ok) {
        setError(data.detail || 'Something went wrong')
      } else {
        setResult(data)
      }
    } catch (err) {
      setError('Could not connect to backend. Is the server running?')
    } finally {
      setLoading(false)
    }
  }

  const gradeColor = (grade) => {
    if (grade === 'A') return '#22c55e'
    if (grade === 'B') return '#84cc16'
    if (grade === 'C') return '#eab308'
    if (grade === 'D') return '#f97316'
    return '#ef4444'
  }

  return (
    <div style={{ maxWidth: '700px', margin: '40px auto', fontFamily: 'sans-serif', padding: '0 20px' }}>
      <h1>🛡️ Assignment Sentinel</h1>
      <p style={{ color: '#666' }}>AI-powered code review for GitHub pull requests</p>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <input
          value={owner}
          onChange={(e) => setOwner(e.target.value)}
          placeholder="Owner"
          style={{ padding: '8px', flex: 1 }}
        />
        <input
          value={repo}
          onChange={(e) => setRepo(e.target.value)}
          placeholder="Repo"
          style={{ padding: '8px', flex: 1 }}
        />
        <input
          value={prNumber}
          onChange={(e) => setPrNumber(e.target.value)}
          placeholder="PR #"
          style={{ padding: '8px', width: '80px' }}
        />
        <button onClick={handleReview} disabled={loading} style={{ padding: '8px 20px' }}>
          {loading ? 'Reviewing...' : 'Review'}
        </button>
      </div>

      {error && (
        <div style={{ background: '#fee2e2', color: '#991b1b', padding: '12px', borderRadius: '8px', marginBottom: '20px' }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ border: '1px solid #e5e7eb', borderRadius: '12px', padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
            <div
              style={{
                background: gradeColor(result.grade),
                color: 'white',
                width: '60px',
                height: '60px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '24px',
                fontWeight: 'bold'
              }}
            >
              {result.grade}
            </div>
            <div>
              <div style={{ fontSize: '20px', fontWeight: 'bold' }}>{result.score}/10</div>
              <div style={{ color: '#666' }}>{result.summary}</div>
            </div>
          </div>

          <Section title="🐛 Bugs & Logic Errors" items={result.bugs} />
          <Section title="⚠️ Bad Practices" items={result.bad_practices} />
          <Section title="🔒 Security Issues" items={result.security_issues} />

          {result.positives?.length > 0 && (
            <div style={{ marginTop: '15px' }}>
              <strong>✅ Done Well</strong>
              <ul>
                {result.positives.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function Section({ title, items }) {
  if (!items || items.length === 0) return null
  return (
    <div style={{ marginBottom: '15px' }}>
      <strong>{title} ({items.length})</strong>
      <ul>
        {items.map((item, i) => (
          <li key={i}>
            <span style={{ fontWeight: 'bold', textTransform: 'uppercase', fontSize: '12px' }}>
              [{item.severity}]
            </span>{' '}
            {item.description}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App