import requests

BASE_URL = "http://data.7c0.link"
LOGIN_URL = f"{BASE_URL}/api/session"

USERNAME = "ajh4ep@Virginia.edu"
PASSWORD = "MaoMao37#"

def get_metabase_token(USERNAME, PASSWORD):
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
    }
    # Use JSON payload
    response = requests.post(LOGIN_URL, json=payload)
    print(f"Response text: {response.text}")
    print(f"Response headers: {response.headers}")
    if response.status_code == 200:
        print("Login successful")
        # Parse JSON response safely
        try:
            return response.json().get("id")
        except ValueError:
            print("Error: No JSON response returned")
            return None
    else:
        print(f"Failed to authenticate: {response.status_code} - {response.text}")
        return None

def get_data_with_token(token, endpoint):
    headers = {
        "X-Metabase-Session": token
    }
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Error: No JSON response returned")
            return None
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return None

# Example usage
token = get_metabase_token(USERNAME, PASSWORD)
if token:
    # Example: Get user details (modify endpoint as needed)
    user_details = get_data_with_token(token, "/api/user/current")
    print(user_details)