import requests
import json
import random
import string
import sys
import time
import threading

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
    response = requests.post(url, data=data, allow_redirects=False)
    if response.status_code in [201, 200, 302]:
        return response.cookies['sessionID']
    else:
        return None

# Function to create a new task
def create_task(session_id, task_data):
    url = 'http://localhost:1111/tasks'
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

try:
    amount = int(sys.argv[1])
except:
    amount = 30

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

create_task(random.randint(3,17), {'title': 'Inspect Secret Base', 'description': random_description})

print("http://localhost:1111")
print("""Your goal is to hack into this task management app used by the Galactic Empire.
Our sources say that Darth Vader was part of the first 20 users of the app.
We need you to hack into his account and get the location of a secret base.""")
input("Press Enter to continue...")
print("We have provided you with the resources you will need in the Mission 1 document.")
print("Good luck, and may the Force be with you!")
input("When you get the Planet with the Secret Base press enter...")
print("What planet is the secret base on?")
Planet = input("Planet: ")
if Planet.lower() == random_planet.lower():
    print("Congratulations! You have successfully completed the mission.")
else:
    print("Incorrect planet. we will get them next time.")
