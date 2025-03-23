import requests

# Correct API endpoint for login
login_url = "http://data.7c0.link/auth/login"

# Replace these with your actual credentials
username = "ajh4ep@Virginia.edu"
password = "MaoMao37#"

# Payload structure
payload = {
    "username": username,
    "password": password,
    "redirect": "/browse/2-dire"
}

# Send POST request
try:
    response = requests.post(
        login_url,
        data=payload  # Use data if the server expects form-encoded payload
    )
    response.raise_for_status()  # Check for HTTP errors

    # Extract response
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
