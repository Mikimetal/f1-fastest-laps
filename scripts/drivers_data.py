import requests
import pandas as pd

## Remove Verstappen filter, will fetch all drivers

# Define the years you want to include
years = [2023, 2024, 2025]


# Fetch all drivers info for mapping driver_number to broadcast_name
drivers_url = "https://api.openf1.org/v1/drivers"
drivers_response = requests.get(drivers_url)
if drivers_response.status_code == 200:
    drivers_data = drivers_response.json()
    driver_map = {str(d['driver_number']): d.get('broadcast_name', 'Unknown') for d in drivers_data}
else:
    print("Warning: Could not fetch drivers info.")
    driver_map = {}

# Initialize a list to store race details
race_details = []

for year in years:
    # Step 1: Fetch all sessions for the year
    sessions_url = f"https://api.openf1.org/v1/sessions?year={year}"
    sessions_response = requests.get(sessions_url)
    sessions_data = sessions_response.json()

    # Step 2: Sort sessions by start date
    sessions_sorted = sorted(sessions_data, key=lambda x: x['date_start'])

    for session in sessions_sorted:
        session_key = session.get('session_key')
        location = session.get('location', 'Unknown')
        country = session.get('country_name', 'Unknown')
        date = session.get('date_start', 'N/A')[:10]  # Extract YYYY-MM-DD
        session_name = session.get('session_name', 'Unknown')
        session_type = session.get('session_type', 'Unknown')

        # Fetch lap data for ALL drivers in this session
        laps_url = f"https://api.openf1.org/v1/laps?session_key={session_key}"
        laps_response = requests.get(laps_url)

        # Check if the response is valid JSON with content
        if laps_response.status_code == 200 and laps_response.content:
            try:
                laps_data = laps_response.json()
            except ValueError:
                print(f"Warning: Invalid JSON for session {session_key}")
                laps_data = []
        else:
            print(f"Warning: No valid data for session {session_key} (status: {laps_response.status_code})")
            laps_data = []

        # Filter laps that include valid lap_duration
        valid_laps = [lap for lap in laps_data if 'lap_duration' in lap and lap['lap_duration'] is not None]

        if valid_laps:
            fastest_lap = min(valid_laps, key=lambda x: x['lap_duration'])
            lap_time_seconds = fastest_lap['lap_duration']
            minutes = int(lap_time_seconds // 60)
            seconds = lap_time_seconds % 60
            lap_time_formatted = f"{minutes}:{seconds:.3f}"
            fastest_driver_number = str(fastest_lap.get('driver_number', 'Unknown'))
            fastest_driver_name = driver_map.get(fastest_driver_number, 'Unknown')
        else:
            lap_time_formatted = "N/A"
            fastest_driver_name = "N/A"
            fastest_driver_number = "N/A"

        race_details.append({
            "Year": year,
            "Driver Name": fastest_driver_name,
            "Driver Number": fastest_driver_number,
            "Race Location": f"{location}, {country}",
            "Date": date,
            "Session Name": session_name,
            "Session Type": session_type,
            "Fastest Lap Time": lap_time_formatted
        })

# Step 4: Display results in a table
df = pd.DataFrame(race_details)

# Save the DataFrame to a CSV file
df.to_csv("all_drivers_fastest_laps.csv", index=False)

# Optionally, print the DataFrame to the console
print(df.to_string(index=False))
