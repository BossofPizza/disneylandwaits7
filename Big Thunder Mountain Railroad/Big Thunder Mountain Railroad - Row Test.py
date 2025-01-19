import pandas as pd
import os

# Base directory where CSV files are stored (adjust this path)
base_path = r'C:\Users\luked\PycharmProjects\disneyland'

# List of months to process
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

# Loop through each month and load the corresponding CSV files
for month in months:
    file_path = os.path.join(base_path, 'Big Thunder Mountain Railroad', f'Big Thunder Mountain Railroad, {month} 2024, Disneyland.csv')

    try:
        # Load the CSV file for the current month
        df = pd.read_csv(file_path)

        # Output the number of rows for the current month's data
        print(f"{month}: {len(df)} rows")

    except FileNotFoundError:
        print(f"File not found for {month}, skipping.")
