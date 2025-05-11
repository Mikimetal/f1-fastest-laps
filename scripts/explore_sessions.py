import requests
import json  # To print nicely

# Step 1: Make the API call
url = "https://api.openf1.org/v1/sessions?year=2025&session_type=Race"
response = requests.get(url)

# Step 2: Convert the response to JSON
data = response.json()

# Step 3: Print the number of items
print(f"Total sessions returned: {len(data)}")

# Step 4: Print the first session (or any one item) to inspect its keys
print("\nFirst session data structure:")
print(json.dumps(data[0], indent=2))  # Pretty-print the JSON
