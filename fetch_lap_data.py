import requests

def fetch_lap_data(session_key, driver_number, lap_number):
    url = f"https://api.openf1.org/v1/laps?session_key=9161&driver_number=63&lap_number=8"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for entry in data:
            print(f"Lap Time: {entry.get('lap_time')}, Driver Number: {entry.get('driver_number')}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    # Example parameters; replace with actual values
    session_key = 9161
    driver_number = 63
    lap_number = 8
    fetch_lap_data(session_key, driver_number, lap_number)
