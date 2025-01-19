import pandas as pd
import matplotlib.pyplot as plt

# Load all months' CSV files into a dictionary
months_data = {
    'January': 'Matterhorn, January 2024, Disneyland.csv',
    'February': 'Matterhorn, February 2024, Disneyland.csv',
    'March': 'Matterhorn, March 2024, Disneyland.csv',
    'April': 'Matterhorn, April 2024, Disneyland.csv',
    'May': 'Matterhorn, May 2024, Disneyland.csv',
    'June': 'Matterhorn, June 2024, Disneyland.csv',
    'July': 'Matterhorn, July 2024, Disneyland.csv',
    'August': 'Matterhorn, August 2024, Disneyland.csv',
    'September': 'Matterhorn, September 2024, Disneyland.csv',
    'October': 'Matterhorn, October 2024, Disneyland.csv',
    'November': 'Matterhorn, November 2024, Disneyland.csv',
    'December': 'Matterhorn, December 2024, Disneyland.csv',
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
