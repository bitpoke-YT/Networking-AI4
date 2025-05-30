

# Mission 6: Mastering Advanced HTTP Methods and Thread Coordination 🚀

## Introduction  
This mission explores advanced techniques in HTTP communication and thread coordination using Python's `requests` library. We'll focus on different HTTP methods, efficient thread synchronization, and robust error handling while maintaining the practical, hands-on style of previous missions.

---

## 🧩 HTTP Methods: The Full Toolkit  

### Overview of Common HTTP Methods
| Method | Purpose | Example Use Case |
|-------|---------|------------------|
| **GET** | Retrieve data | Fetching task lists |
| **POST** | Submit data | Creating new tasks |
| **PUT** | Update resources | Modifying task details |
| **DELETE** | Remove resources | Deleting completed tasks |
| **PATCH** | Partial updates | Updating specific task fields |

---

## 🧵 Thread Coordination with `threading.Event`

### Why Coordination Matters
When multiple threads are searching for a result, we need to stop all threads once one finds it. This is where `threading.Event` comes in.

### Example Implementation:
```python
def findTask(...):
    while not stop_event.is_set() and id < end:
        if found_match:
            stop_event.set()  # Signal all threads to stop

def multThreadedFindTask(...):
    stop_event = threading.Event()
    # Pass stop_event to threads
```

### 🔍 Breakdown:
1. **`threading.Event()`** creates a shared signal flag
2. **`is_set()`** checks if the flag has been raised
3. **`set()`** raises the flag to signal all threads to stop
4. **Each thread checks this flag in its loop** to determine whether to continue

### 🧪 Analogy:
Think of this like a relay race where all runners stop immediately if the first one crosses the finish line.

---

## 🧮 Dynamic URL Construction

### Why We Build URLs Programmatically
APIs often require dynamic parameters in URLs (like query strings or path segments).

### Example in Our Script:
```python
url = f'http://localhost:4633/tasks?taskID={taskid}'
```

### 🧠 Key Concepts:
1. **Query Parameters** (`?key=value`): Used for filtering or configuring requests
2. **Path Segments** (`/tasks/123`): Used to identify specific resources
3. **URL Encoding**: Always ensure special characters are properly encoded

### Example with `urlencode`:
```python
from urllib.parse import urlencode
params = {'taskID': '123', 'type': 'urgent'}
encoded_params = urlencode(params)  # taskID=123&type=urgent
url = f'http://localhost:4633/tasks?{encoded_params}'
```

---

## 🛡️ Robust JSON Handling

### Why Safe JSON Parsing Matters
Not all server responses will be valid JSON, especially when errors occur.

### Example in Our Script:
```python
try:
    tasks = response.json().get('tasks', [])
except Exception:
    return None
```

### 🔍 Breakdown:
1. **`try-except` block** catches JSON parsing errors
2. **`get('tasks', [])`** safely accesses nested data with a default
3. **Error recovery** returns `None` instead of crashing

### 🧪 Common Failure Scenarios:
- Server returns HTML error page (not JSON)
- Network interruption cuts off response
- Malformed JSON from server bug

---

## 🔁 Recursive Search with Memory

### Why Track Previous Attempts
Avoiding redundant checks improves efficiency and prevents infinite loops.

### Example in Our Script:
```python
tested = [found,]
while(deletedKid is None):
    found = multThreadedFindTask(phrase, 500, 20, tested)
    tested.append(found)
```

### 🔍 Breakdown:
1. **`tested` list** stores previously checked IDs
2. **Recursive search** continues until task is found
3. **Avoids redundant searches** by passing `tested` to function

### 🧠 Best Practices:
- Use sets instead of lists for faster lookups: `if id not in tested`
- Implement maximum attempt limits to prevent infinite loops
- Consider using LRU (Least Recently Used) caching for large search spaces

---

## 📊 HTTP Status Code Handling

### Why Status Codes Matter
They provide precise information about request success or failure.

### Example in Our Script:
```python
if response.status_code == 200:
    return "Done"
else:
    return response.text
```

### 🧩 Common HTTP Status Codes:
| Code | Meaning | Use in Our Script |
|------|--------|-------------------|
| 200  | OK | Task successfully deleted |
| 201  | Created | Task creation |
| 204  | No Content | Successful deletion with no response body |
| 400  | Bad Request | Invalid parameters |
| 401  | Unauthorized | Authentication needed |
| 403  | Forbidden | Permission denied |
| 404  | Not Found | Task ID not found |
| 500  | Server Error | Internal server problems |

### 🧠 Advanced Handling:
```python
if 200 <= response.status_code < 300:
    print("Request successful")
elif 400 <= response.status_code < 500:
    print(f"Client error: {response.status_code}")
elif 500 <= response.status_code < 600:
    print(f"Server error: {response.status_code}")
```

---

## 🛠️ Challenge: Thread Coordination Race Condition Fix

### Problem
Our current implementation might have a race condition where multiple threads find a match at the same time.

### Your Task
1. Modify the script to:
   - Ensure only the lowest ID match is used
   - Track all found matches but process only the best one
   - Add a timeout for thread completion

2. Add a shared result holder that stores:
   - All found IDs
   - Timestamps of discoveries
   - Thread numbers that found them

Example structure:
```python
result_holder = {
    'results': [],      # List of all found IDs
    'first': None,      # Lowest ID
    'timestamp': None,  # When first match found
    'thread': None      # Which thread found it
}
```