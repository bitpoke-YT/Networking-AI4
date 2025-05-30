

# Mission 5.2: Advanced Web Interaction with Python 🚀

This mission builds on the concepts from Mission 2 but dives deeper into advanced Python scripting for web interaction. We'll explore new techniques while maintaining the same style and format as previous missions.

---

## 📬 Sending PUT Requests for Task Creation
PUT requests are commonly used to create or update resources on a server. In our script, we use PUT requests to create new tasks with specific properties.

### Example:
```python
def create_task(session_id, task_data):
    url = 'http://localhost:4553/tasks'
    headers = {'Cookie': f'sessionID={session_id}'}
    data = {
        'title': task_data['title'],
        'description': task_data['description'],
        'dueDate': int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))
    }
    response = requests.put(url, headers=headers, json=data, allow_redirects=False)
```

### 🔍 Breakdown:
1. **URL Endpoint**: The endpoint `/tasks` indicates we're interacting with the tasks resource
2. **Session Cookie**: We're using a session cookie for authentication, similar to what we learned in Mission 2
3. **Custom Data**: We're sending:
   - Title and description from our predefined list
   - A dynamically generated due date (more on this later)

4. **`requests.put()`**: This sends a PUT request instead of a GET or POST. The difference:
   - GET: Retrieve data
   - POST: Submit data to be processed
   - PUT: Replace an existing resource or create one if it doesn't exist

5. **`allow_redirects=False`**: This prevents automatic following of redirects, giving us more control over the response handling

---

## ⏱️ Dynamic Timestamp Generation

A unique aspect of this script is the dynamic timestamp generation for task due dates.

### Code Snippet:
```python
dueDate = int((int(time.time() * 100) + ((random.randint(0, 400) * 8640000)))
```

### 🔍 Breakdown:
1. **`time.time()`**: Gets the current timestamp in seconds since epoch (e.g., 1712345678.123456)
2. **`* 100`**: Converts to a value resembling hundredths of seconds (171234567812)
3. **`random.randint(0, 400)`**: Generates a random number between 0 and 400 days
4. **`* 8640000`**: Converts days to milliseconds (86,400 seconds/day × 100 for our hundredths)
5. **`int()`**: Ensures we have an integer value for the date

### 🧮 Example Calculation:
If today is 2024-04-05 12:00:00 (timestamp: 1712347200):
1. `time.time() * 100` = 171234720000
2. `random.randint(0, 400)` = 137 (randomly chosen)
3. `137 * 8640000` = 1183680000 (137 days in milliseconds)
4. Final due date: 171234720000 + 1183680000 = 172418400000 (which is 2024-08-20)

---

## 🔍 Case-Insensitive String Matching

The script uses case-insensitive matching to find planets in task responses.

### Code Snippet:
```python
def check_task(session_id, phrase):
    headers = {'Cookie': f'sessionID={session_id}'}
    response = requests.get(url, headers=headers)
    respond = []
    for elem in phrase:
        if elem in response.text.lower():
            respond.append(elem)
    return respond if respond else None
```

### 🔍 Breakdown:
1. **`response.text`**: Gets the raw text of the response
2. **`.lower()`**: Converts everything to lowercase for comparison
3. **Loop Through Phrases**: Checks each phrase in our planets list
4. **Build Response List**: Only adds phrases that were found

### 🧪 Example:
If the response contains "Hoth is a frozen planet" and our search list includes "hoth":
1. Response becomes "hoth is a frozen planet" after lower()
2. "hoth" is found in the response text
3. "hoth" is added to the respond list

This is particularly useful when dealing with APIs that might return mixed-case data.

---

## 🧵 Thread-Safe Result Collection

The script uses multithreading to check multiple IDs simultaneously, and collects results in a shared list.

### Code Snippet:
```python
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
```

### 🔍 Breakdown:
1. **Batched Processing**: The ID range is divided into manageable chunks
2. **Thread Creation**: Each batch gets its own thread
3. **Shared Results List**: All threads append to the same list
4. **Thread Coordination**: `thread.join()` ensures we wait for all threads to finish

---

## 🚨 Error Handling in Network Requests

The script includes robust error handling for network requests.

### Code Snippet:
```python
try:
    response = check_task(id, phrase)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### 🔍 Breakdown:
1. **`try-except` Block**: Catches any request-related exceptions
2. **`requests.exceptions.RequestException`**: The base class for all requests exceptions
   - Includes timeouts, connection errors, HTTP errors, etc.
3. **Error Reporting**: Provides clear feedback about what went wrong

### 🧠 Best Practice:
This is an improvement over simple `response.status_code` checks because it handles:
- Connection errors (server down)
- Timeouts
- SSL errors
- Too many redirects

---

## 🔄 Nested List Processing in Results

The script processes complex nested data structures in its results.

### Code Snippet:
```python
for planet in found:
    for i in planet:
        if type(i) == type(""):
            print(i)
            print(planet[0])
            compleate(planet[0], i)
            create_task(planet[0], {
                'title': random.choice(save),
                'description': random.choice(save)
            })
```

### 🔍 Breakdown:
1. **Outer Loop**: Iterates through each result (each found task)
2. **Inner Loop**: Iterates through elements of each result
3. **Type Check**: Identifies string elements (our planet names)
4. **ID Extraction**: Uses `planet[0]` to get the task ID
5. **Action Execution**: Completes the task and creates a new one

### 🧪 Example:
If `found = [[17, "sullust"], [83, "hoth"], [155, "lothal"]]`:
1. First iteration: `planet = [17, "sullust"]`
   - `i = 17` → Not a string, skip
   - `i = "sullust"` → Process task 17
2. Second iteration: `planet = [83, "hoth"]`
   - `i = 83` → Not a string, skip
   - `i = "hoth"` → Process task 83

---

## 📦 Conditional JSON Parsing with Fallback

The script includes safe handling of JSON responses.

### Code Snippet:
```python
try:
    tasks = response.json().get('tasks', [])
except Exception:
    return None
```

### 🔍 Breakdown:
1. **`try` Block**: Attempts to parse JSON and extract the 'tasks' field
2. **`.get('tasks', [])`**: Safely accesses the 'tasks' key, defaulting to an empty list
3. **`except` Block**: Catches any exceptions during parsing
   - Could be invalid JSON
   - Could be a missing 'tasks' field
   - Could be a non-JSON response (like HTML error pages)

### 🧠 Best Practice:
This pattern prevents the script from crashing if:
- The server returns an error page (HTML instead of JSON)
- The JSON structure changes unexpectedly
- The network request fails midway

---

