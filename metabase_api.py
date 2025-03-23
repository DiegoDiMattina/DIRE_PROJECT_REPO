import requests

BASE_URL = "http://data.7c0.link"  # Replace with your Metabase instance URL
LOGIN_URL = f"{BASE_URL}/api/session"

# Your Metabase credentials
USERNAME = "ajh4ep@virginia.edu"
PASSWORD = "MaoMao37#"

def get_metabase_token(USERNAME, PASSWORD):
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
    }
    response = requests.post(LOGIN_URL, json=payload)
    if response.status_code == 200:
        try:
            return response.json().get("id")
        except ValueError:
            print("Error: No JSON response returned")
            return None
    else:
        print(f"Failed to authenticate: {response.status_code} - {response.text}")
        return None

def get_databases_with_token(token):
    headers = {
        "X-Metabase-Session": token
    }
    response = requests.get(f"{BASE_URL}/api/database", headers=headers)
    if response.status_code == 200:
        try:
            response_json = response.json()
            print("Response JSON:", response_json)  # Print the full response for debugging
            return response_json.get('data', [])  # Access the 'data' key containing the list of databases
        except ValueError:
            print("Error: No JSON response returned")
            return None
    else:
        print(f"Failed to fetch databases: {response.status_code} - {response.text}")
        return None

# Example usage
token = get_metabase_token(USERNAME, PASSWORD)
if token:
    # Get the list of databases
    databases = get_databases_with_token(token)
    if databases:
        # Print the database details (including the ID)
        for db in databases:
            print(f"Database ID: {db.get('id', 'N/A')} - Name: {db.get('name', 'N/A')}")
    else:
        print("No databases found.")