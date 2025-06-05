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

# Load tasks from data.json
with open('setup/data.json') as f:
    data = json.load(f)
    tasks = data['tasks']

def threeTriesInput(requements):
    i = 0
    while i is not 3:
        put = input()
        if put.lower == requements.lower():
            return True
        else:
            print("Wrong anwer")
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
    url = 'http://127.0.0.1:5002/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data, allow_redirects=False)
    if response.status_code in [201, 200, 302]:
        return response.cookies['sessionID']
    else:
        return None

# Function to create a new task
def create_task(session_id, task_data):
    url = 'http://127.0.0.1:5002/tasks'
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
    story(random_planet, random_coordinates)

def story(random_planet, random_coordinates):
    import webbrowser
    print("http://127.0.0.1:5000")
    webbrowser.open_new('http://127.0.0.1:5000')
    print(
        """Your mission is to hack into this task management app used by the Galactic Empire.
Intelligence reports indicate that a hidden Kyber crystal, crucial for the Empire's next superweapon, is being tracked in the app.
We don't know which account has the information, so you'll need to figure out a way to automate the process of hacking into accounts, retrieving, and checking the information.
Your objective: hack into the right account and discover the planet where the Kyber crystal is hidden."""
    )
    input("Press Enter to continue...")
    print("We have provided you with the resources you will need in the Mission 2 document.")
    print("Good luck, and may the Force be with you!")
    input("When you get the information, press Enter...")
    print("On which planet is the Kyber crystal hidden?")
    if threeTriesInput(random_planet):
        print("Good Job you have found the planet where the Kyber crystal is hidden.")
    else:
        print("Incorrect planet. The Kyber crystal remains hidden... for now.")
        return
    print(f"We are unable to find the coordinates of {random_planet}.")
    input("Press Enter to continue...")
    print(f"We need you to find the galactic coordinates of {random_planet} where the Kyber crystal is located.")
    print("You should be able to use the tool you coded to find the coordinates.")
    input("When you get the information, press Enter...")
    print("What are the coordinates of the Kyber crystal?")
    print("Make sure to incude the square brakes")
    if threeTriesInput(random_coordinates):
        print("\nMission Success!\n")
        print(f"You have located the Kyber crystal on {random_planet} at coordinates {random_coordinates}.")
        print("You quickly transmit the coordinates to the Rebel fleet. The strike team is scrambled and bombers are dispatched.")
        print("\n--- Rebel Bomber Channel ---")
        time.sleep(random.uniform(0.1, 1))
        print("Cobalt Leader: All wings report in.")
        time.sleep(random.uniform(0.1, 1))
        print("Cobalt Two: Cobalt Two standing by.")
        time.sleep(random.uniform(0.1, 1))
        print("Cobalt Three: Cobalt Three standing by.")
        time.sleep(random.uniform(1, 2))
        print("Cobalt Leader: Target locked. Beginning attack run on Imperial facility.")
        time.sleep(random.uniform(1, 3))
        print("Cobalt Two: Anti-air batteries are active, evasive maneuvers!")
        time.sleep(random.uniform(0.1, 1))
        print("Cobalt Leader: Stay on target...")
        time.sleep(random.uniform(1, 3))
        print("Cobalt Three: Bombs away!")
        time.sleep(random.uniform(0.1, 1))
        # 0.5% chance of failure
        if random.random() < 0.005:
            print("Cobalt Leader: Direct hit... wait, the Kyber crystal is still intact! The Empire's shields held. We'll have to try again another day.")
            print("Mission failed. The Kyber crystal remains in Imperial hands... for now.")
            return
        print("Cobalt Leader: Direct hit! The Kyber crystal is shattering—massive energy surge detected!")
        time.sleep(random.uniform(0.1, 1))
        print("Cobalt Two: The entire facility is going up! That's one less superweapon for the Empire.")
        time.sleep(random.uniform(0.1, 1))
        print("Cobalt Leader: Mission accomplished. Returning to base. The galaxy owes you one, agent.")
        print("\n--- Transmission Ended ---\n")
        print("The Rebellion celebrates your victory! The Empire's plans are in ruins, and the galaxy is safer thanks to your skill and courage.")
        print("\nCongratulations! You have successfully completed the Kyber crystal mission and struck a major blow against the Empire.")
    else:
        print("Incorrect coordinates. The Kyber crystal remains hidden... for now.")
        return