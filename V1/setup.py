import requests
import json
import random
import string
import sys
import time

# Load tasks from data.json
with open('setup/data.json') as f:
    data = json.load(f)
    tasks = data['tasks']

# Function to generate a random username
def generate_username(length=10):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# Function to generate a random password
def generate_password(length=12):
    letters_and_digits = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# Function to create a new account
def create_account(username, password):
    url = 'http://localhost:1111/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 201:
        return True
    else:
        return False

# Function to login to an existing account
def login_account(username, password):
    url = 'http://localhost:1111/login'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 201:
        return response.cookies['sessionID']
    else:
        return None

# Function to create a new task
def create_task(session_id, task_data):
    url = 'http://localhost:1111/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    data = {'title': task_data['title'], 'description': task_data['description'], 'dueDate': (int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))))
}
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        return True
    else:
        return False


def setup_account():
    # Generate random username and password
    username = generate_username()
    password = generate_password()

    # Create a new account
    if create_account(username, password):
        print(f'Account created for {username} with password {password}')
    else:
        print(f'Failed to create account for {username}')

    # Login to the new account
    session_id = login_account(username, password)
    if session_id:
        print(f'Logged in as {username} with session ID {session_id}')
    else:
        print(f'Failed to login as {username}')

    # Create tasks for the new account
    num_tasks = random.randint(1, 5)
    for i in range(num_tasks):
        task_data = random.choice(tasks)
        if create_task(session_id, task_data):
            print(f'Task created: {task_data["title"]}')
        else:
            print(f'Failed to create task: {task_data["title"]}')

n = len(sys.argv)
if n != 2:
    raise("Error did not enter 1 arg")


try:
    amount = int(sys.argv[1])
except:
    raise("Not INT")

for i in range(int(sys.argv[1])):
    setup_account()