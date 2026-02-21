import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples=5000):
    np.random.seed(42)
    
    # Generate features
    cpu_usage = np.random.uniform(10, 100, num_samples)
    memory_usage = np.random.uniform(20, 95, num_samples)
    clock_speed = np.random.uniform(1.5, 4.5, num_samples)
    ambient_temp = np.random.uniform(15, 35, num_samples)
    voltage = np.random.uniform(0.9, 1.4, num_samples)
    current_load = np.random.uniform(2, 20, num_samples)
    cache_miss_rate = np.random.uniform(0.1, 10, num_samples)
    power_consumption = np.random.uniform(30, 150, num_samples)
    
    # Generate Target: CPU Temperature
    # Heuristic formula for realistic data
    cpu_temp = (
        0.3 * cpu_usage +
        0.1 * memory_usage +
        2.0 * clock_speed +
        1.0 * ambient_temp +
        5.0 * voltage +
        0.5 * current_load +
        0.2 * cache_miss_rate +
        0.1 * power_consumption +
        np.random.normal(0, 2, num_samples) # Add some noise
    )
    
    df = pd.DataFrame({
        'CPU Usage (%)': cpu_usage,
        'Memory Usage (%)': memory_usage,
        'Clock Speed (GHz)': clock_speed,
        'Ambient Temperature (°C)': ambient_temp,
        'Voltage (V)': voltage,
        'Current Load (A)': current_load,
        'Cache Miss Rate (%)': cache_miss_rate,
        'Power Consumption (W)': power_consumption,
        'CPU Temperature (°C)': cpu_temp
    })
    
    df.to_csv('server_cpu_dataset.csv', index=False)
    print(f"Generated {num_samples} samples and saved to server_cpu_dataset.csv")

if __name__ == "__main__":
    generate_synthetic_data()
