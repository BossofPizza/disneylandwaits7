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
            df['Hour'] = df['Date/Time'].dt.hour
            df['Wait Time'] = pd.to_numeric(df['Wait Time'], errors='coerce')
            all_month_data.append(df)
            print(f"Loaded data for {ride} in {month}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    rides_df[ride] = pd.concat(all_month_data, ignore_index=True) if all_month_data else pd.DataFrame()

# Calculate average wait time by hour for each ride
avg_wait_times = {}
for ride, df in rides_df.items():
    if not df.empty:
        avg_wait_times[ride] = df.groupby('Hour')['Wait Time'].mean()

# Plotting the comparison of average wait times for all rides
plt.figure(figsize=(12, 6))
for ride, avg_times in avg_wait_times.items():
    plt.plot(avg_times.index, avg_times.values, label=ride)

plt.title('Average Wait Times for Different Rides by Hour of the Day', fontsize=14)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Average Wait Time (minutes)', fontsize=12)
plt.xticks(range(0, 24), labels=[f'{hour}:00' for hour in range(0, 24)], rotation=45)
plt.legend(title='Ride', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
