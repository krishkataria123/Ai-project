import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ===============================
# 1. Load Dataset
# ===============================
server_data = pd.read_csv('server_cpu_dataset.csv')

# ===============================
# 2. Data Cleaning & Preprocessing through EDA
# ===============================
# first we will check for null values in our dataset
print(server_data.isnull().sum())
server_data = server_data.drop_duplicates()
server_data = server_data.dropna()
print(server_data.isnull().sum())# no missing data now so no EDA needed for missing data

# CPU Usage (%)               3946
# Memory Usage (%)            4011
# Clock Speed (GHz)           3907
# Ambient Temperature (°C)    4037
# Voltage (V)                 3918
# Current Load (A)            3943
# Cache Miss Rate (%)         4062
# Power Consumption (W)       3996
# CPU Temperature (°C)        4067
# dtype: int64
# CPU Usage (%)               0
# Memory Usage (%)            0
# Clock Speed (GHz)           0
# Ambient Temperature (°C)    0
# Voltage (V)                 0
# Current Load (A)            0
# Cache Miss Rate (%)         0
# Power Consumption (W)       0
# CPU Temperature (°C)        0
# dtype: int64

# Convert numeric columns safely
# creating a list named numeric_cols which contains the names of the columns as a string which are
# supposed to be numeric in excel
numeric_cols = [
    'CPU Usage (%)',
    'Memory Usage (%)',
    'Clock Speed (GHz)',
    'Ambient Temperature (°C)',
    'Voltage (V)',
    'Current Load (A)',
    'Cache Miss Rate (%)',
    'Power Consumption (W)',
    'CPU Temperature (°C)'
]
# converting all our numeric columns to numeric using pd.to_numeric and error is set to 'coerce' so that
# if there are any invalid values they are converted to NaN
for col in numeric_cols:
    server_data[col] = pd.to_numeric(server_data[col], errors='coerce')
# Remove rows that had invalid values
server_data = server_data.dropna()


# ===============================
# 3. Exploratory Data Analysis (EDA)
# ===============================
# -------- EDA 1: Distribution of CPU Temperature  --------
plt.figure()
plt.scatter(
    server_data['CPU Temperature (°C)'],
    server_data['CPU Usage (%)'],
    alpha=0.05# to change the transparency of the points so that we can see the density of points in areas where they overlap
)

# Trend line
z = np.polyfit( #fits the curve to the data points
    server_data['CPU Temperature (°C)'], #x-value independent variable
    server_data['CPU Usage (%)'], #y-value dependent variable
    1 # straight line degree of the polynomial
)
p = np.poly1d(z) # to convert curve into a mathematical function taht we used to plot the trend line
plt.plot(
    server_data['CPU Temperature (°C)'],
    p(server_data['CPU Temperature (°C)'])
)

plt.xlabel('CPU Temperature (°C)')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage vs CPU Temperature')
# plt.show()

# -------- EDA 2: Distribution of CPU Temperature  --------
plt.figure()
plt.hist(server_data['CPU Temperature (°C)'], bins=30)
plt.xlabel('CPU Temperature (°C)')
plt.ylabel('Frequency')
plt.title('Distribution of CPU Temperature')
# plt.show()

# -------- EDA 3: Power Consumption vs CPU Temperature  --------
plt.figure()
plt.scatter(
    server_data['Power Consumption (W)'],
    server_data['CPU Temperature (°C)'],
    alpha=0.05
)
plt.xlabel('Power Consumption (W)')
plt.ylabel('CPU Temperature (°C)')
plt.title('Power Consumption vs CPU Temperature')
# plt.show()

# -------- EDA 4: Voltage vs CPU Temperature  --------
plt.figure(figsize=(8, 6))

# Scatter plot
plt.scatter(
    server_data['Voltage (V)'],
    server_data['CPU Temperature (°C)'],
    alpha=0.05
)
# Trend line
z = np.polyfit(
    server_data['Voltage (V)'],
    server_data['CPU Temperature (°C)'],
    1
)
p = np.poly1d(z)

plt.plot(
    server_data['Voltage (V)'],
    p(server_data['Voltage (V)'])
)

plt.xlabel('Voltage (V)')
plt.ylabel('CPU Temperature (°C)')
plt.title('Voltage vs CPU Temperature')
# plt.show()

# -------- EDA 5: Current Load vs CPU Temperature  --------
plt.figure(figsize=(8, 6))
# Scatter plot
plt.scatter(
    server_data['Current Load (A)'],
    server_data['CPU Temperature (°C)'],
    alpha=0.05
)
# Trend line
z = np.polyfit(
    server_data['Current Load (A)'],
    server_data['CPU Temperature (°C)'],
    1
)
p = np.poly1d(z)
plt.plot(
    server_data['Current Load (A)'],
    p(server_data['Current Load (A)'])
)

plt.xlabel('Current Load (A)')
plt.ylabel('CPU Temperature (°C)')
plt.title('Current Load vs CPU Temperature')
# plt.show()

# ===============================
# 4. Random Forest Regression
# ===============================

# -------- Feature Selection --------
X = server_data[
    [
        'CPU Usage (%)',
        'Memory Usage (%)',
        'Clock Speed (GHz)',
        'Ambient Temperature (°C)',
        'Voltage (V)',
        'Current Load (A)',
        'Cache Miss Rate (%)',
        'Power Consumption (W)',
    ]
]
y = server_data['CPU Temperature (°C)']

#-------- Train/Test Split --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)
# -------- Model Initialization --------
best_rf_model = RandomForestRegressor(
    n_estimators=500,    #number of trees in forest
    max_depth=12,        #maximum depth of the tree to prevent overfitting
    min_samples_split=5, #minimumm number of samples required to split an internal node
    min_samples_leaf=2,  # minimum number of samples required to be at a aleaf node
    max_features="sqrt", # to chose the  number of features to consider when looking for the best split. "sqrt" means it will use the square root of the total number of features, which is a common choice for regression tasks.
    random_state=42
)
# -------- Training --------
best_rf_model.fit(X_train, y_train)

# Save trained model to disk
joblib.dump(best_rf_model, 'model.pkl')
print("Model saved to model.pkl")

# -------- Prediction --------
y_pred = best_rf_model.predict(X_test)

# -------- Evaluation --------
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Random Forest (0.2 Split) MAE:", mae) #mean absolute error
print("Random Forest (0.2 Split) RMSE:", rmse) # root mean squared error
print("Random Forest (0.2 Split) R2 Score:", r2)

# Random Forest (0.2 Split) MAE: 7.193665283551417
# Random Forest (0.2 Split) RMSE: 9.075823284160261
# Random Forest (0.2 Split) R2 Score: 0.8883728148859321

#-------- Train/Test Split --------
X2_train, X2_test, y2_train, y2_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)
# -------- Model Initialization --------
rf_model = RandomForestRegressor(
    n_estimators=500,   #number of trees in the forest
    max_depth=12,       # maximum depth of the tree to prevent overfitting
    min_samples_split=5,# minimum number of samples required to split an internal node
    min_samples_leaf=2, # minimum number of samples required to be at a leaf node
    max_features="sqrt", # to choose the number of features to consider when looking for the best split. "sqrt" means it will use the square root of the total number of features, which is a common choice for regression tasks.
    random_state=42
)
# -------- Training --------
rf_model.fit(X2_train, y2_train)

# -------- Prediction --------
y2_pred = rf_model.predict(X2_test)

# -------- Evaluation --------
mae = mean_absolute_error(y2_test, y2_pred)
rmse = np.sqrt(mean_squared_error(y2_test, y2_pred))
r2 = r2_score(y2_test, y2_pred)

print("Random Forest MAE:", mae) #mean absolute error
print("Random Forest RMSE:", rmse) #root mean squared error
print("Random Forest R2 Score:", r2)

# Random Forest MAE: 7.271379928910313
# Random Forest RMSE: 9.168695380278407
# Random Forest R2 Score: 0.8858259822065697

print("Train R2:", best_rf_model.score(X2_train, y2_train))
print("Test R2:", best_rf_model.score(X2_test, y2_test))


# ===============================
# 5. Done — Use the React frontend or backend API to make predictions
# ===============================
print("\nTraining complete. Model saved as model.pkl")
print("Run 'python backend/app.py' to start the prediction API.")