import pandas as pd
import matplotlib.pyplot as plt

# Define base directory path where the CSV files are stored
base_path = r'C:\Users\luked\PycharmProjects\disneyland'

# Define file paths for the three rides for all months
ride_data = {
    'Matterhorn': r'Matterhorn\Matterhorn, {} 2024, Disneyland.csv',
    'Space Mountain': r'Space Mountain\Space Mountain, {} 2024, Disneyland.csv',
    'Big Thunder Mountain Railroad': r'Big Thunder Mountain Railroad\Big Thunder Mountain Railroad, {} 2024, Disneyland.csv'
}

# Load data for all months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
rides_df = {}

for ride, file_pattern in ride_data.items():
    all_month_data = []
    for month in months:
        file_path = f'{base_path}\\{file_pattern.format(month)}'
        try:
            df = pd.read_csv(file_path)
            df['Date/Time'] = pd.to_datetime(df['Date/Time'])
            df['Wait Time'] = pd.to_numeric(df['Wait Time'], errors='coerce')
            all_month_data.append(df)
            print(f"Loaded data for {ride} in {month}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    rides_df[ride] = pd.concat(all_month_data, ignore_index=True) if all_month_data else pd.DataFrame()

# Calculate average wait time for each ride
avg_wait_times = {}
for ride, df in rides_df.items():
    if not df.empty:
        avg_wait_times[ride] = df['Wait Time'].mean()

# Find the fastest and slowest ride (based on average wait time)
sorted_rides = sorted(avg_wait_times.items(), key=lambda x: x[1])

# Plot the fastest vs slowest rides
plt.figure(figsize=(8, 5))
plt.bar([ride[0] for ride in sorted_rides], [ride[1] for ride in sorted_rides], color=['green', 'red', "blue"])
plt.title('Fastest and Slowest Rides Based on Average Wait Time', fontsize=14)
plt.xlabel('Ride', fontsize=12)
plt.ylabel('Average Wait Time (minutes)', fontsize=12)
plt.tight_layout()
plt.show()

# Print the results
print(f"Fastest Ride: {sorted_rides[0][0]} with {sorted_rides[0][1]:.2f} minutes wait time")
print(f"Slowest Ride: {sorted_rides[-1][0]} with {sorted_rides[-1][1]:.2f} minutes wait time")
