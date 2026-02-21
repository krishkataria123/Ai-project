import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

# Load data and model
data = pd.read_csv('server_cpu_dataset.csv')
model = joblib.load('model.pkl')

FEATURE_COLS = [
    'CPU Usage (%)',
    'Memory Usage (%)',
    'Clock Speed (GHz)',
    'Ambient Temperature (°C)',
    'Voltage (V)',
    'Current Load (A)',
    'Cache Miss Rate (%)',
    'Power Consumption (W)',
]

X = data[FEATURE_COLS]
y = data['CPU Temperature (°C)']

# Use the same split as project.py to verify results
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"--- Model Accuracy Report ---")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R2 Score (Variance Explained): {r2:.4f}")
print(f"-----------------------------")
