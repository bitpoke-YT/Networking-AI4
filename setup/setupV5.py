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

domain = "http://172.20.20.15:5000"

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
    response = requests.put(url, headers=headers, json=data, allow_redirects=False, proxies=proxies)
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

def special_setup_account(num_tasks, task_data, session_list=None):
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
        if session_list is not None:
            session_list.append(session_id)
    else:
        raise Exception(f'Failed to create account for username: {username}')

def check_user(session_id, compleatedlist, newlist):
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

def check_all(rebelbase, other, planets, sessionID):
    rebelbaseNum = len(rebelbase)
    otherNum = len(other)
    planetsNum = len(rebelbase)
    for id in sessionID:
        # Check rebel bases
        url = f'{domain}/tasks?completed=true'
        headers = {'Cookie': f'sessionID={id}'}
        response = requests.get(url, headers=headers, proxies=proxies)
        try:
            tasks = response.json().get('tasks', [])
        except Exception:
            return None
        for task in tasks:
            description = task.get('description')
            if any(elem in description.lower() for elem in rebelbase):
                rebelbaseNum -= 1
                # Check replacment
                url = f'{domain}/tasks?completed=false'
                response = requests.get(url, headers=headers, proxies=proxies)
                try:
                    tasks = response.json().get('tasks', [])
                except Exception:
                    return None
                for task in tasks:
                    description = task.get('description')
                    if any(elem in description.lower() for elem in planets):
                        planetsNum -= 1
        # Check others have not changed
        url = f'{domain}/tasks?completed=false'
        response = requests.get(url, headers=headers, proxies=proxies)
        try:
            tasks = response.json().get('tasks', [])
            if tasks == []:
                raise Exception ("NONE")
        except Exception:
            return None
        for task in tasks:
            description = task.get('description')
            title = task.get('title')
            if any(elem.lower() in description.lower() for elem in other):
                print(description)
                otherNum -= 1
            elif any(elem.lower() in title.lower() for elem in other):
                otherNum -= 1
        time.sleep(0.002)


    # Returns 1 if not success or faild
    # 2 for all success
    # 3 for first part success
    # 4 Fail
    # print(otherNum)
    # print(rebelbaseNum)
    # print(planetsNum)

    if not otherNum <= 0:
        return 4
    elif (not planetsNum <= 0) and rebelbaseNum <= 0:
        return 3
    elif planetsNum <= 0 and rebelbaseNum <= 0:
        return 2
    return 1


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

    with open('setup/rebel.json') as f:
        data = json.load(f)

    with open('setup/planet.json') as file:
        planets = json.load(file)

    rebelbase = []
    other = []
    sessionID = []

    currentTasks = []

    random.shuffle(data)

    for task in data:
        task_title = task['title']
        task_description = task['description']

        currentTasks.append({
                'title': task_title,
                'description': task_description
            })
        
        if random.random() < 0.35 and len(rebelbase) < len(planets):
            rebelbase.append(task['planet'])
        elif random.random() < 0.5: 
            other.append(task['planet'])
        
        
        if random.random() < 0.65 and currentTasks != []:
            threads.append(threading.Thread(target=special_setup_account, args=(0, currentTasks, sessionID)))
            currentTasks = []

    random.shuffle(threads)

    # Start all special threads
    for thread in threads:
        thread.start()
        time.sleep(0.02)  # Optional: slight delay to avoid server overload

    rebelbase = [base.lower() for base in rebelbase]
    planets = [elem.lower() for elem in planets]
    other = [elem.lower() for elem in other]

    # Wait for all special threads to complete
    for thread in threads:
        thread.join()

    story(rebelbase, other, planets, sessionID)



def story(rebelbase, other, planets, sessionID):
    # Debuging 
    print(other)
    # 
    print(len(sessionID))
    """Mission briefing function for eliminating child-related tasks in the Empire."""
    print("Proxy: http://127.0.0.1:3128")
    print(domain)
    
    print(f"""
Your mission: Use your access in the Imperial Task Management System to compleate
task where we have rebel bases. Here is a list of rebel base for you to use. 
{rebelbase}
Make sure that you don't remove non rebel bases and add back the task closes to them
but relating to these planets.
{planets}
    """)
    
    input("Press Enter to continue...")
    print("We have provided the necessary resources in the Mission 5 document.")
    print("May the Force be with you!")
    print("We'll notify you upon mission completion.")

    checked = 1
    while(checked == 1):
        checked = check_all(rebelbase, other, planets, sessionID)
        time.sleep(random.uniform(1,5))
    if checked == 3:
        print("Well done on compleating thoughs task now make fake ones with the planets we provied.")
        while(checked == 1 or checked == 3):
            checked = check_all(rebelbase, other, planets, sessionID)
            time.sleep(random.uniform(1,5))
    if checked == 2:
        print("""
Well Done on keeping our bases Secret.
              """)
        return
    if checked == 4:
        print("""
        Failed! Make sure you only complete the ones where the rebel bases are.
        """)
    else:
        print(checked)
        print(f""" {checked}
        Failed! Make sure you only complete the ones where the rebel bases are.
        """)
    time.sleep(1)
    return True



if __name__ == "__main__":
    setup()