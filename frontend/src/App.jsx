import { useState, useEffect } from "react";
import "./index.css";

const API_BASE = "https://ai-project-dh8a.onrender.com";

const FIELDS = [
  { key: "CPU Usage (%)", label: "CPU Usage (%)" },
  { key: "Memory Usage (%)", label: "Memory Usage (%)" },
  { key: "Clock Speed (GHz)", label: "Clock Speed (GHz)" },
  { key: "Ambient Temperature (°C)", label: "Ambient Temperature (°C)" },
  { key: "Voltage (V)", label: "Voltage (V)" },
  { key: "Current Load (A)", label: "Current Load (A)" },
  { key: "Cache Miss Rate (%)", label: "Cache Miss Rate (%)" },
  { key: "Power Consumption (W)", label: "Power Consumption (W)" },
];

const initialForm = Object.fromEntries(FIELDS.map(f => [f.key, ""]));

function getTempStatus(temp) {
  if (temp < 60) return { label: "Normal", color: "green" };
  if (temp < 85) return { label: "Warm", color: "orange" };
  return { label: "Critical", color: "red" };
}

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState("Checking...");

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
    <div className="container">
      <h1>CPU Temperature Predictor</h1>
      <p className="subtitle">
        Predict CPU temperature using system utilization metrics.
      </p>

      <div className="status">
        Backend Status: <strong>{apiStatus}</strong>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="grid">
          {FIELDS.map(field => (
            <div className="input-group" key={field.key}>
              <label>{field.label}</label>
              <input
                type="number"
                value={form[field.key]}
                onChange={(e) => handleChange(field.key, e.target.value)}
                required
              />
            </div>
          ))}
        </div>

        <button type="submit" disabled={loading || apiStatus === "Offline"}>
          {loading ? "Predicting..." : "Predict Temperature"}
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
  );
}