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

# Load the data for all months into a dictionary
all_data = {}
for month, file_path in months_data.items():
    all_data[month] = pd.read_csv(file_path)
    all_data[month]['Date/Time'] = pd.to_datetime(all_data[month]['Date/Time'])  # Ensure datetime format
    all_data[month]['Day'] = all_data[month]['Date/Time'].dt.day_name()  # Add day of the week (e.g., Monday)

# Function to analyze a selected month and time range, filtered by day of the week
def analyze_month(selected_months, selected_days1, selected_days2, time1, time2):
    # Combine the selected months' data
    data = pd.concat([all_data[month] for month in selected_months], ignore_index=True)

    # Filter data for the desired time range
    filtered_data = data[(data['Date/Time'].dt.time >= pd.to_datetime(time1).time()) &
                         (data['Date/Time'].dt.time <= pd.to_datetime(time2).time())]

    # Group 1: Filter data by the first set of days
    group1 = filtered_data[filtered_data['Day'].isin(selected_days1)].copy()  # Use .copy() to avoid view vs. copy issues
    group1.loc[:, 'Time'] = group1['Date/Time'].dt.floor('5min').dt.strftime('%H:%M')  # Round to 5-minute intervals
    time_averages1 = group1.groupby('Time')['Wait Time'].mean().reset_index()

    # Group 2: Filter data by the second set of days (if provided)
    group2 = filtered_data[filtered_data['Day'].isin(selected_days2)].copy()  # Use .copy() here as well
    group2.loc[:, 'Time'] = group2['Date/Time'].dt.floor('5min').dt.strftime('%H:%M')  # Round to 5-minute intervals
    time_averages2 = group2.groupby('Time')['Wait Time'].mean().reset_index()

    # Calculate overall averages for each group
    avg_wait1 = group1['Wait Time'].mean()
    avg_wait2 = group2['Wait Time'].mean()

    print(f"\nAverage wait time for {', '.join(selected_days1)}: {avg_wait1:.2f} minutes.")
    print(f"Average wait time for {', '.join(selected_days2)}: {avg_wait2:.2f} minutes.")

    # Generate 5-minute intervals for plotting and 15-minute intervals for the x-axis
    time_range_5min = pd.date_range(start=time1, end=time2, freq="5min").strftime('%H:%M')  # 5-minute intervals
    time_range_15min = pd.date_range(start=time1, end=time2, freq="15min").strftime('%H:%M')  # 15-minute intervals

    # Align averages with the 5-minute interval range
    def align_time_averages(time_averages, time_range):
        avg_dict = dict(zip(time_averages["Time"], time_averages["Wait Time"]))
        return [avg_dict.get(time, None) for time in time_range]

    y_values1 = align_time_averages(time_averages1, time_range_5min)
    y_values2 = align_time_averages(time_averages2, time_range_5min)

    # Scatter Plot
    plt.figure(figsize=(12, 6))
    plt.scatter(time_range_5min, y_values1, color="blue", s=50, edgecolor="black", label=f"{', '.join(selected_days1)}")
    plt.scatter(time_range_5min, y_values2, color="orange", s=50, edgecolor="black", label=f"{', '.join(selected_days2)}")

    plt.title(f"Average Wait Time ({time1}-{time2}) Comparison", fontsize=14)
    plt.xlabel("Time Range", fontsize=12)
    plt.ylabel("Wait Time (minutes)", fontsize=12)
    plt.xticks(time_range_15min, rotation=45, fontsize=8)  # Show 15-minute intervals on x-axis
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

    # Print chart data for both groups
    print("\nChart Data for Group 1:")
    print(time_averages1)
    print("\nChart Data for Group 2:")
    print(time_averages2)

# Example usage
print("Available months:", ', '.join(months_data.keys()))
selected_months = input("Enter the months you want to analyze, separated by commas (e.g., January,February): ").split(',')
selected_months = [month.strip() for month in selected_months if month.strip() in months_data]

if selected_months:
    print("\nAvailable days of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday")
    selected_days1 = input("Enter the first set of days to analyze, separated by commas (e.g., Monday, Wednesday): ").split(',')
    selected_days1 = [day.strip() for day in selected_days1 if day.strip()]

    selected_days2 = input("Enter the second set of days to analyze (or leave blank for none), separated by commas: ").split(',')
    selected_days2 = [day.strip() for day in selected_days2 if day.strip()]

    time1 = input("\nEnter the start time (e.g., 7:30): ").strip()
    time2 = input("Enter the end time (e.g., 24:00): ").strip()

    try:
        # Ensure the time input is in valid format
        pd.to_datetime(time1, format='%H:%M')  # Check time format
        pd.to_datetime(time2, format='%H:%M')  # Check time format

        # Check if the end time is after the start time (and handle midnight case)
        if time2 == '24:00':
            time2 = '23:59'  # Set 24:00 to 23:59 since pandas doesn't support 24:00

        analyze_month(selected_months, selected_days1, selected_days2, time1, time2)

    except ValueError:
        print("Invalid time format. Please enter times in HH:MM format (e.g., 7:30).")
else:
    print("No valid months selected!")
