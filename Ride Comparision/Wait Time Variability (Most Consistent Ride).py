import pandas as pd
import matplotlib.pyplot as plt

# Define the rides and months for the data
rides = ['Matterhorn', 'Space Mountain', 'Big Thunder Mountain Railroad']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Base directory path where the CSV files are stored
base_path = r'C:\Users\luked\PycharmProjects\disneyland'

# Define file paths for the rides for all months
ride_data = {
    'Matterhorn': 'Matterhorn, {} 2024, Disneyland.csv',
    'Space Mountain': 'Space Mountain, {} 2024, Disneyland.csv',
    'Big Thunder Mountain Railroad': 'Big Thunder Mountain Railroad, {} 2024, Disneyland.csv'
}

# Load data for all months
rides_df = {}

for ride, file_pattern in ride_data.items():
    all_month_data = []
    for month in months:
        file_path = f"{base_path}\\{ride}\\{file_pattern.format(month)}"
        try:
            df = pd.read_csv(file_path)
            df['Wait Time'] = pd.to_numeric(df['Wait Time'], errors='coerce')
            all_month_data.append(df)
            print(f"Loaded data for {ride} in {month}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    rides_df[ride] = pd.concat(all_month_data, ignore_index=True) if all_month_data else pd.DataFrame()

# Calculate the standard deviation of wait times for each ride (this gives us variability)
variability = {}
for ride, df in rides_df.items():
    if not df.empty:
        variability[ride] = df['Wait Time'].std()

# Find the ride with the least variability
least_variability_ride = min(variability, key=variability.get)

# Plotting the comparison of wait time variability for all rides
plt.figure(figsize=(8, 5))
plt.bar(variability.keys(), variability.values(), color=['green', 'red', 'blue'])
plt.title('Wait Time Variability (Standard Deviation) for Different Rides', fontsize=14)
plt.xlabel('Ride', fontsize=12)
plt.ylabel('Wait Time Variability (minutes)', fontsize=12)
plt.tight_layout()
plt.show()

print(f"The most consistent ride with the least variability is {least_variability_ride} with a standard deviation of {variability[least_variability_ride]:.2f} minutes.")
