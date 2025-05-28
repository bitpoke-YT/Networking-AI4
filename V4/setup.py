import requests
import json
import random
import string
import sys
import time
import threading
import base64

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
    url = 'http://localhost:4333/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data, allow_redirects=False)
    if response.status_code in [201, 200, 302]:
        return response.cookies['sessionID']
    else:
        return None

# Function to create a new task
def create_task(session_id, task_data):
    url = 'http://localhost:4333/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    data = {'title': task_data['title'], 'description': task_data['description'], 'dueDate': (int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))))}
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [201, 200, 302]:
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

def special_setup_account(num_tasks, task_data_main):
    # Generate random username and password
    username = generate_username()
    password = generate_password()

    session_id = create_account(username, password)

    print(session_id)

    if session_id != None:
        if create_task(session_id, task_data_main):
            ...
        else:
            raise Exception(f'Failed to create main task: {task_data_main["title"]}')
        for i in range(num_tasks):
            task_data = random.choice(tasks)
            if create_task(session_id, task_data):
                ...
            else:
                print(f'Failed to create task: {task_data["title"]}')
    else:
        raise Exception(f'Failed to create account for username: {username}')

def setup():
    try:
        amount = int(sys.argv[1])
    except:
        amount = 300

    # Create threads for each account setup
    threads = []

    for i in range(amount):
        thread = threading.Thread(target=setup_account, args=(random.randint(1, 5),))
        threads.append(thread)
        thread.start()
        time.sleep(0.02)  # Slight delay to avoid overwhelming the server

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    with open('setup/planets.json') as f:
        data = json.load(f)

    random_data = random.choice(data)
    random_planet = random_data['plant']
    random_description = random_data['description']

    special_setup_account(random.randint(1, 3), {
        'title': 'Inspect Base',
        'description': random_description
    })

    with open('setup/KyberCrystal.json') as f:
        data = json.load(f)

    random_data = random.choice(data)
    random_planet = random_data['plant']
    random_description = random_data['description']

    special_setup_account(random.randint(1, 3), {
        'title': 'Get Kyber crystal update',
        'description': random_description
    })
    plumming = []
    for i in range(random.randint(1, 5)):
        plumming.append(random.choice(data)['plant'])
    plumming.append(random_planet)
    special_setup_account(random.randint(1, 3), {
        'title': 'Fix plumming',
        'description': f"The plumming is broken on {plumming}."
    })
    fooddrop = []
    for i in range(random.randint(1, 10)):
        fooddrop.append(random.choice(data)['plant'])
    for i in fooddrop:
        special_setup_account(random.randint(1, 3), {
            'title': 'Food drop',
            'description': f"Deliver food to {i}."
        })
    medicine = []
    for i in range(random.randint(1, 10)):
        medicine.append(random.choice(data)['plant'])
    for i in medicine:
        special_setup_account(random.randint(1, 3), {
            'title': 'Deliver medicine',
            'description': f"Deliver medicine to {i}."
        })
    random_coordinates = f"[{round(random.uniform(-1000, 1000), 3)}, {round(random.uniform(-1000, 1000), 3)}, {round(random.uniform(-3, 3), 3)}]"

    special_setup_account(random.randint(1, 3), {
        'title': 'EMERGANCY Medevac',
        'description': f"Get to {random_planet} and pick up the admiral. Coordinates: {random_coordinates}"
    })

    with open('setup/Troop.json') as f:
        data = json.load(f)

    for n in range(1, 30):
        random_data = random.choice(data)
        random_title = random_data['title']
        random_description = random_data['description']
        random_planet = random_data['planet']
        random_troop = random_data['troopamount']

        special_setup_account(random.randint(1, 3), {
            'title': base64.b64encode(random_title),
            'description': base64.b64encode(random_description)
        })
    

    random_data = random.choice(data)
    random_title = random_data['title']
    random_description = random_data['description']
    random_planet = random_data['planet']
    random_troop = random_data['troopamount']

    special_setup_account(random.randint(1, 3), {
        'title': base64.b64encode(random_title),
        'description': base64.b64encode(random_description)
    })
    

# Story
def story():
    print("http://localhost:4333")
    print(
        f"""Your mission is to hack into this task management app used by the Galactic Empire.
We would like to get the amount of troops on {random_planet} we know that te data in encrypted"""
    )
    input("Press Enter to continue...")
    print("We have provided you with the resources you will need in the Mission 4 document.")
    print("Good luck, and may the Force be with you!")
    input("When you get the information, press Enter...")
    print("On which planet is the Kyber crystal hidden?")
    Troop = input("troop: ")
    if Troop.lower() == random_troop.lower():
        print("Good Job you have found the planet where the Kyber crystal is hidden.")
    else:
        print("Incorrect planet. The Kyber crystal remains hidden... for now.")
        return

story()
