import requests
import threading
import base64
import time
import random

url = 'http://localhost:4333/tasks'

def check_task(session_id, phrase):
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    if phrase.lower() in response.text.lower():
        return response.text
    else:
        return None


def decode_if_base64(s):
    try:
        return base64.b64decode(s).decode("utf-8")
    except Exception:
        return s

def check_task_encoded(session_id, phrase):
    import json
    url = 'http://localhost:4333/tasks?completed=false'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    try:
        tasks = response.json().get('tasks', [])
    except Exception:
        return None

    for task in tasks:
        description = decode_if_base64(task.get('description', ''))
        if phrase.lower() in description.lower():
            return f"ID: {task.get('taskid', '')}\n Description: {description}\n"
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
                result_holder['result'] = f"Found task with phrase in ID: {id}\n"
            if stop_event:
                stop_event.set()
            return
        id += 1
        # time.sleep(random.uniform(0.001, 0.1))  # Sleep to avoid overwhelming the server

    print(f"[Thread {start}-{end-1}] Finished without finding phrase.")

def multThreadedFindTask(phrase, max_id=500, batch_size=20):
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
        # time.sleep(random.uniform(0.01, 0.4))  # Sleep to avoid overwhelming the server
    for thread in threads:
        thread.join()
    return result_holder.get('result', "Phrase not found in any task.")

print("What phrase do you want to search for?")
phrase = input()
print("Searching for tasks with phrase:", phrase)
print(multThreadedFindTask(phrase))