import pandas as pd
import matplotlib.pyplot as plt

# Load all months' CSV files into a dictionary
months_data = {
    'January': 'Space Mountain, January 2024, Disneyland.csv',
    'February': 'Space Mountain, February 2024, Disneyland.csv',
    'March': 'Space Mountain, March 2024, Disneyland.csv',
    'April': 'Space Mountain, April 2024, Disneyland.csv',
    'June': 'Space Mountain, June 2024, Disneyland.csv',
    'July': 'Space Mountain, July 2024, Disneyland.csv',
    'August': 'Space Mountain, August 2024, Disneyland.csv',
    'September': 'Space Mountain, September 2024, Disneyland.csv',
    'October': 'Space Mountain, October 2024, Disneyland.csv',
    'November': 'Space Mountain, November 2024, Disneyland.csv',
    'December': 'Space Mountain, December 2024, Disneyland.csv',
}

# Combine all months' data into a single DataFrame
all_data = []
for file_path in months_data.values():
    month_data = pd.read_csv(file_path)
    month_data['Date/Time'] = pd.to_datetime(month_data['Date/Time'])
    all_data.append(month_data)

all_data_df = pd.concat(all_data, ignore_index=True)

# Extract hour from 'Date/Time' and group by hour
all_data_df['Hour'] = all_data_df['Date/Time'].dt.hour
hourly_avg_wait_times = all_data_df.groupby('Hour')['Wait Time'].mean()

# Identify the busiest and slowest times of the day
busiest_hour = hourly_avg_wait_times.idxmax()
slowest_hour = hourly_avg_wait_times.idxmin()

print(f"\nBusiest Hour: {busiest_hour}:00 with an average wait time of {hourly_avg_wait_times[busiest_hour]:.2f} minutes.")
print(f"Slowest Hour: {slowest_hour}:00 with an average wait time of {hourly_avg_wait_times[slowest_hour]:.2f} minutes.")

# Plot the average wait times by hour
plt.figure(figsize=(12, 6))
plt.plot(hourly_avg_wait_times.index, hourly_avg_wait_times.values, marker='o', color='blue')
plt.axvline(x=busiest_hour, color='red', linestyle='--', label=f"Busiest: {busiest_hour}:00")
plt.axvline(x=slowest_hour, color='green', linestyle='--', label=f"Slowest: {slowest_hour}:00")
plt.title("Average Wait Time by Hour of the Day", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Average Wait Time (minutes)", fontsize=12)
plt.xticks(range(0, 24), labels=[f"{hour}:00" for hour in range(24)], rotation=45)
plt.legend(fontsize=10)
plt.grid(alpha=0.5)
plt.tight_layout()
plt.show()
