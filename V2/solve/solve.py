import requests
import threading

url = 'http://127.0.0.1:5002/tasks'

def check_task(session_id, phrase):
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    if phrase.lower() in response.text.lower():
        return response.text
    else:
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
            response = check_task(id, phrase)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        if response is not None:
            print(f"[Thread {start}-{end-1}] Found phrase in ID: {id}")
            if result_holder is not None:
                result_holder.append(f"Found task with phrase in ID: {id}\n")
            # if stop_event:
            #     stop_event.set()
            return
        id += 1
    print(f"[Thread {start}-{end-1}] Finished without finding phrase.")

def multThreadedFindTask(phrase, max_id=1000, batch_size=20):
    threads = []
    stop_event = threading.Event()
    result_holder = []
    for start in range(1, max_id + 1, batch_size):
        end = min(start + batch_size, max_id + 1)
        thread = threading.Thread(
            target=findTask,
            args=(phrase, end, start, stop_event, result_holder)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return result_holder

print("What phrase do you want to search for?")
phrase = input()
print("Searching for tasks with phrase:", phrase)
print(multThreadedFindTask(phrase))