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

domain = "http://172.20.20.16:5000"

proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}

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
    data = {'title': task_data['title'], 'description': task_data['description'], 'dueDate': (int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))))}
    response = requests.put(url, headers=headers, json=data, proxies=proxies)
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

def special_setup_account(num_tasks, task_data, return_session=False, session_list=None, lock=None):
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
        if return_session and session_list is not None and lock is not None:
            with lock:
                session_list.append(session_id)
        return session_id if return_session else None
    else:
        raise Exception(f'Failed to create account for username: {username}')

def check_darth_vader(session_id):
    url = f'{domain}/tasks?completed=false'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers, proxies=proxies)
    try:
        tasks = response.json().get('tasks', [])
    except Exception:
        return None

    for task in tasks:
        description = task.get('description', '')
        if 'kids' in description.lower():
            return True
    url = f'{domain}/tasks?completed=false'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers, proxies=proxies)
    return False

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

    special_threads = []

    with open('setup/going.json') as f:
        going = json.load(f)

    for n in range(1, 30):
        # Multi Thread
        random_task = random.choice(going)
        random_title = random_task['title']
        random_description = random_task['description']

        special_JSON = [
            {
                'title': random_title,
                'description': random_description
            }
        ]

        special_threads.append(threading.Thread(target=special_setup_account, args=(random.randint(1, 2), special_JSON)))

    random_task = random.choice(going)
    random_title = random_task['title']
    random_description = random_task['description']
    random_planet = random_task['planet']

    # Darth Vader
    special_JSON = [
        {
            'title': random_title,
            'description': random_description
        },
        {
            'title': 'Do Reaserch on if my kids where born and if so where he is',
            'description': 'I need to find out if my kids were born and if so where he is.'
        }
    ]

    vader_sessions = []
    vader_lock = threading.Lock()
    vader_thread = threading.Thread(
        target=special_setup_account,
        args=(random.randint(1, 2), special_JSON, True, vader_sessions, vader_lock)
    )

    special_JSON = [
        {
            'title': 'Do Reaserch on if my kids where born and if so where he is',
            'description': 'I need to find out if my kids were born and if so where he is.'
        }
    ]

    other_sessions = []
    other_lock = threading.Lock()
    other_thread = threading.Thread(
        target=special_setup_account,
        args=(random.randint(1, 2), special_JSON, True, other_sessions, other_lock)
    )
    special_threads.append(vader_thread)
    special_threads.append(other_thread)

    # Start all special threads
    for t in special_threads:
        t.start()
        time.sleep(0.01)  # Optional: slight delay to avoid server overload

    # Wait for all special threads to complete
    for t in special_threads:
        t.join()

    story(random_planet, vader_sessions[0] if vader_sessions else None, other_sessions[0] if other_sessions else None)



def story(random_planet, darth_vader_session=None, other_session=None):
    """Mission briefing function for eliminating child-related tasks in the Empire."""
    print("Proxy: http://127.0.0.1:3128")
    print(domain)
    
    print(f"""
Your mission: Use your access in the Imperial Task Management System to delete 
anything related to kids. If it is Darth Vader's account, we know he is going to 
{random_planet}, so you need to find the account he's using and delete any tasks 
related to children. We've been told by a spy there's a way to delete, but you'll 
need to find the right HTTP request to do so.
    """)
    
    input("Press Enter to continue...")
    print("We have provided the necessary resources in the Mission 6 document.")
    print("May the Force be with you!")
    print("We'll notify you upon mission completion.")
    
    timer = 1
    darth_vader_kid = True
    other_kid = True
    while darth_vader_kid and other_kid:
        if darth_vader_session is not None and other_session is not None:
            darth_vader_kid = check_darth_vader(darth_vader_session)
            other_kid = check_darth_vader(other_session)
        else:
            raise Exception("Darth Vader's session is not available. Please try again later.")
        time.sleep(1)
        timer += 1
        if timer == 600:
            print("The http request relates to /task")
    
    if not darth_vader_kid and other_kid:
        print("""
Congratulations! You've completed the mission by deleting all tasks related 
to Darth Vader's children. The kids are now safe from the Empire's reach.
        """)
    else:
        print("""
Failed! Make sure you only delete kid related things in darth vaders account.
""")




if __name__ == "__main__":
    setup()