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
            df['Date/Time'] = pd.to_datetime(df['Date/Time'])
            df['Day'] = df['Date/Time'].dt.day_name()  # Day of the week
            df['Wait Time'] = pd.to_numeric(df['Wait Time'], errors='coerce')
            all_month_data.append(df)
            print(f"Loaded data for {ride} in {month}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    rides_df[ride] = pd.concat(all_month_data, ignore_index=True) if all_month_data else pd.DataFrame()

# Reorder days to start from Monday to Sunday
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Calculate average wait time by day of the week for each ride
avg_wait_by_day = {}
for ride, df in rides_df.items():
    avg_wait_by_day[ride] = df.groupby('Day')['Wait Time'].mean()

# Plotting the comparison of average wait times by day of the week for all rides
plt.figure(figsize=(12, 6))
for ride, avg_wait in avg_wait_by_day.items():
    avg_wait = avg_wait.reindex(days_order)  # Reindex to match the days_order
    avg_wait.plot(label=ride)

plt.title('Average Wait Times by Day of the Week for Different Rides', fontsize=14)
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Average Wait Time (minutes)', fontsize=12)
plt.legend(title='Ride', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
