import urllib.request
import json

url = "https://ai-project-dh8a.onrender.com"
data = {
    "CPU Usage (%)": 50.0,
    "Memory Usage (%)": 40.0,
    "Clock Speed (GHz)": 3.0,
    "Ambient Temperature (°C)": 25.0,
    "Voltage (V)": 1.1,
    "Current Load (A)": 5.0,
    "Cache Miss Rate (%)": 2.0,
    "Power Consumption (W)": 60.0
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'), 
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        status = response.getcode()
        body = response.read().decode('utf-8')
        print(f"Status Code: {status}")
        print(f"Response: {body}")
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(f"Error body: {e.read().decode('utf-8')}")
