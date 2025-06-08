import requests

# Define login credentials
username = "grandadmiralthrawn@imperial.mil"
password = "emperor'sfavoritegrandAdmiral!"

# Define the proxy configuration
proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}

# Define the Flask server URL
base_url = "http://172.20.20.17:5000"

# Login endpoint
login_url = f"{base_url}/login"

def compleate(session_id, planet):
    url = f'{base_url}/tasks?completed=false'
    headers = {'Cookie': f'session={session_id}'}
    response = requests.get(url, headers=headers, proxies=proxies)
    try:
        tasks = response.json().get('tasks', [])
    except Exception:
        return "None Error"

    for task in tasks:
        description = task.get('description', '')
        title = task.get('title', '')
        if planet in description.lower() or planet in title:
            taskid = task.get('taskid', '')
            url = f'{base_url}/task'
            headers = {
                'Content-Type': 'application/json'
            }
            data = {"taskid": f'{taskid}'}
            response = requests.post(url, json=data, headers=headers, allow_redirects=False)
            if response.status_code == 200:
                return "Done"
            else:
                return response.text

# Create a session to persist cookies
session = requests.Session()

# Login payload
payload = {
    "username": username,
    "password": password
}

# Send POST request to login
response = session.post(login_url, data=payload, proxies=proxies, allow_redirects=False)

id = response.cookies['session']

print(compleate(id, "TF-139"))