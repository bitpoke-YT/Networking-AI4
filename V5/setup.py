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

def special_setup_account(num_tasks, task_data):
    # Generate random username and password
    username = generate_username()
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

    print("Working on special setup...")

    with open('setup/going.json') as f:
        going = json.load(f)

    random_task = random.choice(going)
    random_title

    special_threads.append(threading.Thread(target=special_setup_account, args=(random.randint(1, 3), {
        'title': random_planet_encoded,
        'description': random_description_encoded
    })))

    # Start all special threads
    for t in special_threads:
        t.start()
        time.sleep(0.01)  # Optional: slight delay to avoid server overload

    # Wait for all special threads to complete
    for t in special_threads:
        t.join()

    story(random_planet, random_troop)
    

# Story
def story(random_planet, random_troop):
    print("http://localhost:4333")
    print(f"""
Your mission: Hack into the Empire's task management software.
Our sources say that the troop data might be encrypted.
The Rebellion needs you to break through the encryption and discover the exact number of Imperial troops stationed on {random_planet}.
This intel is critical to launching a ground assault on the weapon supply depot on {random_planet}.
""")
    input("Press Enter to continue...")
    print("We have provided you with the resources you will need in the Mission 4 document.")
    print("May the Force be with you!")
    input_with_hints(
        "When you breach the encryption, press Enter...", 600, [
            "Hint: Try exploring how data is transferred and stored in modern web apps.",
            "Hint: Look for patterns or keywords in encoded or obfuscated data fields.",
            "Hint: Sometimes, what looks like gibberish is just encoded—think about common encoding schemes.",
            "Hint: Automation and parallel processing can help you search faster!",
            "Hint: The Empire Might be using base64 encoding for their data.",  
        ]
    )
    print(f"What is the TROOP COUNT on the surface of {random_planet}?")
    
    Troop = input("Troop Count: ")
    if Troop.strip() == str(random_troop):
        print("Decryption Success: The troop count is confirmed. You now have the intel needed for the ground assault.")
    else:
        print("Security Alert: Wrong decryption key! Imperial countermeasures have detected your intrusion. Abort mission!")
        return
    print("\n--- Rebel Ground Assault Channel ---")
    time.sleep(1)
    print("Squad Leader: Intel received. All units, prepare to breach the Imperial perimeter!")
    time.sleep(1.5)
    print("Demo Team: Charges set. Ready on your mark, Commander.")
    time.sleep(1.5)
    print("You: All teams, go! Take the depot and secure the weapon supplies!")
    time.sleep(2)
    # 0.5% chance of failure
    if random.random() < 0.005:
        print("Heavy Blaster Fire: The Empire was ready. Our assault is repelled. We must fall back and regroup.")
        print("Mission failed. The Empire holds the depot for now.")
        return
    print("Blaster Fire Erupts! The Rebels storm the facility, overwhelming the surprised Imperial garrison!")
    time.sleep(1)
    print("Squad Leader: Depot secured! We've captured the weapon supplies and vital schematics!")
    print("\n--- Transmission Secure ---")
    print("Your hacking and leadership have delivered a decisive victory for the Rebellion.")
    print("Congratulations! You have successfully completed the mission.")


if __name__ == "__main__":
    setup()