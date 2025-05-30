

# Mission 5: Advanced Python Scripting for Task Automation 🚀

---

## 📨 Sending PUT Requests  
The `create_task()` function uses a **PUT request** to create a new task with a custom `dueDate`. PUT is often used to update resources on a server.  

### Example:
```python
def create_task(session_id, task_data):
    url = 'http://localhost:4553/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    data = {
        'title': task_data['title'],
        'description': task_data['description'],
        'dueDate': (int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))))  # Dynamic timestamp
    }
    response = requests.put(url, headers=headers, json=data, allow_redirects=False)
```
- **`requests.put()`**: Sends a PUT request to update or create a resource.  
- **`allow_redirects=False`**: Prevents automatic redirection.  

---

## 📬 Sending POST Requests with JSON Data  
The `compleate()` function sends a **POST request** to mark a task as completed.  

### Example:
```python
def compleate(session_id, planet):
    url = 'http://localhost:4553/tasks?completed=false'
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    try:
        tasks = response.json().get('tasks', [])
    except Exception:
        return None
    for task in tasks:
        description = task.get('description', '')
        if any(elem in planet for elem in description.lower()):
            taskid = task.get('taskid', '')
            url = 'http://127.0.0.1:4553/task'
            headers = {'Content-Type': 'application/json'}
            data = {"taskid": f'{taskid}'}
            response = requests.post(url, json=data, headers=headers, allow_redirects=False)
```
- **`requests.post()`**: Sends JSON data to the server.  
- **`Content-Type: application/json`**: Specifies the payload format.  

---

## ⏱️ Using `time` and `random` for Dynamic Timestamps  
The `create_task()` function generates a timestamp with a random offset (up to 400 days).  

### Example:
```python
dueDate = int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000))))
```
- **`time.time()`**: Gets the current timestamp in seconds.  
- **`random.randint(0, 400)`**: Adds a random number of days (converted to milliseconds with `8640000`).  

---

## 🔍 Case-Insensitive String Matching  
The `check_task()` function checks if a phrase exists in the response text, ignoring case.  

### Example:
```python
def check_task(session_id, phrase):
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    respond = []
    for elem in phrase:
        if elem in response.text.lower():  # Case-insensitive check
            respond.append(elem)
    return respond if respond else None
```
- **`response.text.lower()`**: Converts the entire response to lowercase for comparison.  

---

## 🧵 Shared Results in Multithreading  
The `multThreadedFindTask()` function uses a shared list (`results`) to collect findings from multiple threads.  

### Example:
```python
def multThreadedFindTask(phrase, max_id=1000, batch_size=20, checked=None):
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
```
- **Shared `results` list**: Threads append matches to this list.  
- **`threading.Thread`**: Creates and starts threads for batched ID ranges.  

---

## 🚨 Error Handling for Requests  
The `findTask()` function includes error handling for failed HTTP requests.  

### Example:
```python
try:
    response = check_task(id, phrase)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```
- **`try-except` block**: Catches exceptions like connection errors or timeouts.  

---

## 📊 Batched Threaded Requests  
The script divides ID ranges into batches to avoid overwhelming the server.  

### Example:
```python
for start in range(1, max_id + 1, batch_size):
    end = min(start + batch_size, max_id + 1)
    thread = threading.Thread(
        target=findTask,
        args=(phrase, end, start, results, checked)
    )
    threads.append(thread)
    thread.start()
```
- **Batch size**: Controls how many IDs each thread checks.  

---

## 📦 Parsing JSON Responses and Extracting Data  
The `compleate()` function parses JSON to extract tasks and their descriptions.  

### Example:
```python
try:
    tasks = response.json().get('tasks', [])
except Exception:
    return None
for task in tasks:
    description = task.get('description', '')
```
- **`response.json()`**: Converts the response to a Python dictionary.  
- **`get('tasks', [])`**: Safely accesses nested data.  