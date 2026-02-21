import { useState, useEffect, useCallback } from 'react'
import './App.css'

const API_BASE = 'https://ai-project-dh8a.onrender.com'

// ── Field configuration ──────────────────────────────────────────────────────
const FIELDS = [
  { key: 'CPU Usage (%)',             label: 'CPU Usage',             unit: '%',   icon: '🖥️',  placeholder: 'e.g. 68',  min: 0,  max: 100,  step: 0.1 },
  { key: 'Memory Usage (%)',          label: 'Memory Usage',          unit: '%',   icon: '🧠',  placeholder: 'e.g. 67',  min: 0,  max: 100,  step: 0.1 },
  { key: 'Clock Speed (GHz)',         label: 'Clock Speed',           unit: 'GHz', icon: '⚡',  placeholder: 'e.g. 3.5', min: 0.1,max: 10,   step: 0.01 },
  { key: 'Ambient Temperature (°C)',  label: 'Ambient Temp',          unit: '°C',  icon: '🌡️',  placeholder: 'e.g. 25',  min: -20, max: 60,  step: 0.1 },
  { key: 'Voltage (V)',               label: 'Voltage',               unit: 'V',   icon: '🔋',  placeholder: 'e.g. 1.2', min: 0,  max: 3,    step: 0.01 },
  { key: 'Current Load (A)',          label: 'Current Load',          unit: 'A',   icon: '⚙️',  placeholder: 'e.g. 10',  min: 0,  max: 100,  step: 0.1 },
  { key: 'Cache Miss Rate (%)',       label: 'Cache Miss Rate',       unit: '%',   icon: '💾',  placeholder: 'e.g. 5',   min: 0,  max: 100,  step: 0.1 },
  { key: 'Power Consumption (W)',     label: 'Power Consumption',     unit: 'W',   icon: '⚡',  placeholder: 'e.g. 80',  min: 0,  max: 1000, step: 0.1 },
]

const initialForm = Object.fromEntries(FIELDS.map(f => [f.key, '']))

// ── Temp status helper ───────────────────────────────────────────────────────
function getTempStatus(temp) {
  if (temp < 60)  return { label: '✅ Normal',   cls: 'cool',  color: '#10b981' }
  if (temp < 85)  return { label: '⚠️ Warm',     cls: 'warm',  color: '#f59e0b' }
  return              { label: '🔥 Critical',  cls: 'hot',   color: '#ef4444' }
}

// ── App ──────────────────────────────────────────────────────────────────────
export default function App() {
  const [form, setForm]         = useState(initialForm)
  const [result, setResult]     = useState(null)   // { temp } | { error }
  const [loading, setLoading]   = useState(false)
  const [apiStatus, setApiStatus] = useState('checking') // 'checking' | 'online' | 'offline'

  // Ping health endpoint on mount
  useEffect(() => {
    const check = async () => {
      try {
        const r = await fetch(`${API_BASE}/health`)
        const data = await r.json()
        setApiStatus(data.model_loaded ? 'online' : 'offline')
      } catch {
        setApiStatus('offline')
      }
    }
    check()
  }, [])

  const handleChange = useCallback((key, value) => {
    setForm(f => ({ ...f, [key]: value }))
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    // Build numeric payload
    const payload = {}
    for (const f of FIELDS) {
      const v = parseFloat(form[f.key])
      if (isNaN(v)) {
        setResult({ error: `"${f.label}" must be a valid number.` })
        setLoading(false)
        return
      }
      payload[f.key] = v
    }

    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Prediction failed.')
      setResult({ temp: data.predicted_temp })
    } catch (err) {
      setResult({ error: err.message || 'Could not connect to the API. Is the backend running?' })
    } finally {
      setLoading(false)
    }
  }

  const statusConfig = {
    checking: { cls: 'checking', text: <>Checking backend&hellip;</> },
    online:   { cls: 'online',   text: <><strong>API online</strong> — model ready</> },
    offline:  { cls: 'offline',  text: <><strong>API offline</strong> — run <code style={{fontFamily:'monospace',fontSize:'0.75rem',color:'#f59e0b'}}>python backend/app.py</code></> },
  }[apiStatus]

  const tempStatus = result?.temp != null ? getTempStatus(result.temp) : null

  return (
    <div className="page">
      {/* Header */}
      <header className="header">
        <div className="header-icon">🌡️</div>
        <h1>CPU Temperature Predictor</h1>
        <p>Enter system metrics to predict CPU temperature using Random Forest AI</p>
      </header>

      {/* Card */}
      <main className="card">

        {/* API status */}
        <div className="status-bar">
          <div className={`status-dot ${statusConfig.cls}`} />
          <span className="status-text">{statusConfig.text}</span>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <p className="section-label">System Metrics</p>

          <div className="form-grid">
            {FIELDS.map(f => (
              <div className="field" key={f.key}>
                <label htmlFor={f.key}>
                  <span>{f.icon} {f.label}</span>
                  <span className="unit">{f.unit}</span>
                </label>
                <input
                  id={f.key}
                  type="number"
                  placeholder={f.placeholder}
                  min={f.min}
                  max={f.max}
                  step={f.step}
                  value={form[f.key]}
                  onChange={e => handleChange(f.key, e.target.value)}
                  required
                  autoComplete="off"
                />
              </div>
            ))}
          </div>

          <button
            type="submit"
            className="predict-btn"
            disabled={loading || apiStatus === 'offline'}
          >
            <span className="btn-content">
              {loading
                ? <><div className="spinner" />Predicting…</>
                : <>🔮 Predict CPU Temperature</>
              }
            </span>
          </button>
        </form>

        {/* Result */}
        {result && (
          <div className={`result ${result.error ? 'error' : 'success'}`}>
            {result.error ? (
              <>
                <p className="result-label">Error</p>
                <p className="error-msg">{result.error}</p>
              </>
            ) : (
              <>
                <p className="result-label">Predicted CPU Temperature</p>
                <div className="result-temp">
                  <span
                    className="value"
                    style={{ color: tempStatus.color }}
                  >
                    {result.temp}
                  </span>
                  <span className="deg">°C</span>
                </div>
                <span className={`temp-status ${tempStatus.cls}`}>
                  {tempStatus.label}
                </span>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
