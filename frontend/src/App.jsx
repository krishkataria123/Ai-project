import { useState, useEffect } from "react";
import "./App.css";

const API_BASE = "https://ai-project-dh8a.onrender.com";

const FIELDS = [
  { key: "CPU Usage (%)", label: "CPU Usage", placeholder: "e.g. 68" },
  { key: "Memory Usage (%)", label: "Memory Usage", placeholder: "e.g. 67" },
  { key: "Clock Speed (GHz)", label: "Clock Speed", placeholder: "e.g. 3.5" },
  { key: "Ambient Temperature (°C)", label: "Ambient Temp", placeholder: "e.g. 25" },
  { key: "Voltage (V)", label: "Voltage", placeholder: "e.g. 1.2" },
  { key: "Current Load (A)", label: "Current Load", placeholder: "e.g. 10" },
  { key: "Cache Miss Rate (%)", label: "Cache Miss Rate", placeholder: "e.g. 5" },
  { key: "Power Consumption (W)", label: "Power Consumption", placeholder: "e.g. 80" },
];

const initialForm = Object.fromEntries(FIELDS.map(f => [f.key, ""]));

function getTempStatus(temp) {
  if (temp < 60) return { label: "Normal", color: "#16a34a" };
  if (temp < 85) return { label: "Warm", color: "#f59e0b" };
  return { label: "Critical", color: "#dc2626" };
}

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState("Checking");

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then(res => res.json())
      .then(data => {
        setApiStatus(data.model_loaded ? "Online" : "Offline");
      })
      .catch(() => setApiStatus("Offline"));
  }, []);

  const handleChange = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const payload = {};
    for (const f of FIELDS) {
      const value = parseFloat(form[f.key]);
      if (isNaN(value)) {
        setResult({ error: `${f.label} must be a valid number.` });
        setLoading(false);
        return;
      }
      payload[f.key] = value;
    }

    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Prediction failed");

      setResult({ temp: data.predicted_temp });
    } catch (err) {
      setResult({ error: err.message });
    }

    setLoading(false);
  };

  const tempStatus = result?.temp ? getTempStatus(result.temp) : null;

  return (
    <div className="page">
      <div className="container">
        <h1>CPU Temperature Predictor</h1>
        <p className="subtitle">
          Enter system metrics to predict CPU temperature using Random Forest AI
        </p>

        <div className={`status ${apiStatus.toLowerCase()}`}>
          <span className="dot"></span>
          API {apiStatus} — model ready
        </div>

        <form onSubmit={handleSubmit}>
          <p className="section-label">SYSTEM METRICS</p>

          <div className="grid">
            {FIELDS.map(field => (
              <div className="input-group" key={field.key}>
                <label>{field.label}</label>
                <input
                  type="number"
                  placeholder={field.placeholder}
                  value={form[field.key]}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                  required
                />
              </div>
            ))}
          </div>

          <button type="submit" disabled={loading || apiStatus === "Offline"}>
            {loading ? "Predicting..." : "Predict CPU Temperature"}
          </button>
        </form>

        {result && (
          <div className="result">
            {result.error ? (
              <p className="error">{result.error}</p>
            ) : (
              <>
                <h2>
                  Predicted Temperature:{" "}
                  <span style={{ color: tempStatus.color }}>
                    {result.temp} °C
                  </span>
                </h2>
                <p>Status: {tempStatus.label}</p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}