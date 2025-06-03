import requests
import webbrowser
import json
import random
import string
import sys
import time
import threading
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from package.hintInput import three_input_with_hints

# Example
import requests
import json

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
    url = 'http://localhost:4553/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data, allow_redirects=False)
    if response.status_code in [201, 200, 302]:
        return response.cookies['session']
    else:
        return None

# Function to create a new task
def create_task(session_id, task_data):
    url = 'http://localhost:4553/tasks'
    headers = {'Cookie': f'session={session_id}'}
    data = {'title': task_data['title'], 'description': task_data['description'], 'dueDate': (int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))))}
    response = requests.put(url, headers=headers, json=data, allow_redirects=False)
    if response.status_code in [201, 200]:
        return True
    else:
        return False


def setup_account(num_tasks):
    # Generate random username and password
    username = generate_username()
    password = generate_password()

    session_id = create_account(username, password)

    if session_id != None:
        for i in range(num_tasks):
            task_data = random.choice(tasks)
            if create_task(session_id, task_data):
                ...
            else:
                print(f'Failed to create task: {task_data["title"]}')
    else:
        print(f'Failed to create account for username: {username}')

def special_setup_account(num_tasks, task_data, session_list=None, password=None, username=None):
    # Generate random username and password
    if username == None:
        username = generate_username()
    if password == None:
        password = generate_password()

    session_id = create_account(username, password)

    if session_id != None:
        for task in task_data:
            if create_task(session_id, task):
                ...
            else:
                raise Exception(f'Failed to create main task: {task["title"]}')
        for i in range(num_tasks):
            task_data = random.choice(tasks)
            if create_task(session_id, task_data):
                ...
            else:
                print(f'Failed to create task: {task_data["title"]}')
        if session_list != None:
            session_list.append(session_id)
    else:
        raise Exception(f'Failed to create account for username: {username}')


def setup():
    try:
        amount = int(sys.argv[1])
    except:
        amount = 300

    # # Create threads for each account setup
    threads = []

    for i in range(amount):
        thread = threading.Thread(target=setup_account, args=(random.randint(1, 5),))
        threads.append(thread)

    task_data = [
        {
            'title': 'Project Star Dust Report',
            'description': 'Get the report about point defences. there should be at at leset 10 turrets per square meter.'
        },
    ]

    threads.append(threading.Thread(target=special_setup_account, args=(random.randint(1,3), task_data,)))

    for thread in threads:
        thread.start()
        time.sleep(random.uniform(0.000, 0.1))

    # Wait for all special threads to complete
    for thread in threads:
        thread.join()
    story()

# UnlimitedPower

def story():
    """Mission briefing Access the imperial task management software and get info on Project Stardust."""
    webbrowser.open_new('http://localhost:8980')
    print("http://localhost:4553")
    
    print(f"""
Your mission: Access the Imperial Task Managemente System to find info Project Star Dust and how many turrets per square meter.
To do this we have a spy which has gotten the secret key "UnlimitedPower".
Use this to gain acces and find out this information.
    """)
    
    input("Press Enter to continue...")
    print("We have provided the necessary resources in the Mission 8 document.")
    print("May the Force be with you!")
    if(three_input_with_hints("How many turrets per square meter", "10", 600, ["",])):
        print("Well done, we have more information ")
    else:
        print("You will need to get them next time")


if __name__ == "__main__":
    setup()