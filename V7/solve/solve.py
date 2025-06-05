import requests

# Define login credentials
username = "your_username"
password = "your_password"

# Define the proxy configuration
proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}

# Define the Flask server URL
base_url = "http://127.0.0.1:5000"

# Login endpoint
login_url = f"{base_url}/login"

# Create a session to persist cookies
session = requests.Session()

# Login payload
payload = {
    "username": username,
    "password": password
}

# Send POST request to login
response = session.post(login_url, data=payload, proxies=proxies)

# Check if login was successful
if response.status_code == 200:
    print("Login successful!")
else:
    print(f"Login failed! Status code: {response.status_code}")
    print(response.text)