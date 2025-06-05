import requests
import json
import random
import string
import sys
import time
import threading
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from package.hintInput import input_with_hints

domain = 'http://172.20.20.13:5000'

proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}

# Load tasks from data.json
with open('setup/data.json') as f:
    data = json.load(f)
    tasks = data['tasks']

def threeTriesInput(requirements):
    i = 0
    while i != 3:
        user_input = input()
        if user_input.lower() == requirements.lower():
            return True
        else:
            print("Wrong answer")
        i += 1
    return False

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
    url = f'{domain}/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data, allow_redirects=False, proxies=proxies)
    if response.status_code in [201, 200, 302]:
        return response.cookies['sessionID']
    else:
        return None

# Function to create a new task
def create_task(session_id, task_data):
    url = f'{domain}/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    data = {
        'title': task_data['title'],
        'description': task_data['description'],
        'dueDate': int(time.time() * 1000 + random.randint(0, 400) * 86400000)
    }
    response = requests.put(url, headers=headers, json=data, proxies=proxies)
    if response.status_code in [201, 200, 302]:
        return True
    else:
        return False

def setup_account(num_tasks):
    username = generate_username()
    password = generate_password()

    session_id = create_account(username, password)
    if session_id:
        for _ in range(num_tasks):
            task_data = random.choice(tasks)
            if not create_task(session_id, task_data):
                print(f'Failed to create task: {task_data["title"]}')
    else:
        print(f'Failed to create account for username: {username}')

def special_setup_account(num_tasks, task_data_main):
    username = generate_username()
    password = generate_password()

    session_id = create_account(username, password)
    if session_id:
        if not create_task(session_id, task_data_main):
            raise Exception(f'Failed to create main task: {task_data_main["title"]}')
        for _ in range(num_tasks):
            task_data = random.choice(tasks)
            if not create_task(session_id, task_data):
                print(f'Failed to create task: {task_data["title"]}')
    else:
        raise Exception(f'Failed to create account for username: {username}')

def setup():
    try:
        amount = int(sys.argv[1])
    except:
        amount = 300

    threads = []
    for _ in range(amount):
        thread = threading.Thread(target=setup_account, args=(random.randint(1, 5),))
        threads.append(thread)
        thread.start()
        time.sleep(0.02)

    for thread in threads:
        thread.join()

    with open('setup/planets.json') as f:
        data = json.load(f)

    random_data = random.choice(data)
    random_base = random_data['plant']
    random_description = random_data['description']

    special_setup_account(random.randint(1, 3), {
        'title': 'Inspect Base',
        'description': random_description
    })
    special_setup_account(random.randint(1, 3), {
        'title': 'missing inspection report',
        'description': f"The following base have missing inspection report: {random_base}."
    })

    story(random_base)

def story(random_base):
    print("Proxy: http://127.0.0.1:3128")
    print("http://172.20.20.13:5000/tasks")
    print(
        """Your mission is to infiltrate the Imperial task management app.
The Empire has lost critical inspection reports from several bases, and they are believed to be hidden in the task management system.
The Rebellion has provided a proxy to bypass Imperial restrictions.
Your objective: find out which base has a missing inspection reports."""
    )
    input("Press Enter to continue...")
    print("We have provided you with the resources you will need in the Mission 3 document.")
    print("Good luck, and may the Force be with you!")
    input("When you get the information, press Enter...")
    print("Which bases had missing inspection reports?")
    if threeTriesInput(random_base):
        print("Good Job! You have retrieved the stolen inspection reports.")
    else:
        print("Incorrect information. The mission has failed.")
        return
    print(f"The stolen reports were related to the base: {random_base}.")
    print("Mission Success! The Rebellion celebrates your success.")