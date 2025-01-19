import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the rides and months for the data
rides = ['Matterhorn', 'Space Mountain', 'Big Thunder Mountain Railroad']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

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
            df['Hour'] = df['Date/Time'].dt.hour
            df['Day'] = df['Date/Time'].dt.day_name()  # Day of the week
            df['Wait Time'] = pd.to_numeric(df['Wait Time'], errors='coerce')
            all_month_data.append(df)
            print(f"Loaded data for {ride} in {month}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    rides_df[ride] = pd.concat(all_month_data, ignore_index=True) if all_month_data else pd.DataFrame()

# Prepare data for heatmap
heatmap_data = {}
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']  # Ensuring correct day order

for ride, df in rides_df.items():
    if not df.empty:
        pivot = df.pivot_table(values='Wait Time', index='Day', columns='Hour', aggfunc='mean')
        pivot = pivot.reindex(days_order)  # Reindex days to ensure the correct order
        heatmap_data[ride] = pivot

# Plotting heatmaps for each ride
plt.figure(figsize=(15, 10))
for i, (ride, pivot) in enumerate(heatmap_data.items(), 1):
    plt.subplot(1, len(heatmap_data), i)
    sns.heatmap(pivot, cmap='coolwarm', annot=False, fmt='.1f', cbar_kws={'label': 'Wait Time (min)'})
    plt.title(f'{ride} - Wait Time Heatmap')

plt.tight_layout()
plt.show()