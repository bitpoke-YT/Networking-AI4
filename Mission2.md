# Using Cookies with Python Requests
=====================================

## Introduction
The `requests` library in Python makes it easy to send HTTP requests and handle cookies 🍪. This is useful for automating tasks, testing web applications, or interacting with websites that require cookies for authentication or personalization 🤖. In this tutorial, you'll learn how to use cookies with `requests` and write scripts to modify cookies and check for specific phrases in server responses.

## What is the Requests Library? 🐍
The `requests` library is a popular Python package for making HTTP requests. It allows you to send GET, POST, and other types of requests easily, handle responses, and manage cookies and sessions.

To install it, run:
```bash
pip install requests
```

## Sending Requests with Cookies 🍪
You can send cookies with your HTTP requests by passing a `cookies` dictionary to the `requests.get()` or `requests.post()` functions.

Example:
```python
import requests

url = "https://example.com"
cookies = {"sessionid": "123456", "user": "micah"}

response = requests.get(url, cookies=cookies)
print(response.text)
```
This sends a GET request to the server with the specified cookies.

## Checking for a Phrase in the Response 🔍
After sending a request, you can check if a certain phrase appears in the response content.

Example:
```python
if "Welcome back" in response.text:
    print("Phrase found!")
else:
    print("Phrase not found.")
```

## Looping Through Different Cookies 🔄
You might want to try different cookie values to see how the server responds. You can do this by looping through a list of cookie values.

Example:
```python
import requests

url = "https://example.com"
cookie_values = ["abc123", "def456", "ghi789"]

for value in cookie_values:
    cookies = {"sessionid": value}
    response = requests.get(url, cookies=cookies)
    if "Welcome back" in response.text:
        print(f"Phrase found with cookie {value}!")
    else:
        print(f"Phrase not found with cookie {value}.")
```

## Using Sessions for Persistent Cookies 🗂️
If you want to persist cookies across multiple requests, use a `requests.Session()` object.

Example:
```python
import requests

session = requests.Session()
url = "https://example.com"
cookies = {"sessionid": "persistent123"}

response = session.get(url, cookies=cookies)
print(response.text)
```

## Multithreading for Faster Requests ⚡
If you have many cookies to try, you can use multithreading to send requests faster. Python's `threading` module lets you run multiple requests at the same time.

Example:
```python
import requests
import threading

url = "https://example.com"
cookie_values = ["abc123", "def456", "ghi789", "jkl012", "mno345"]

def check_cookie(value):
    cookies = {"sessionid": value}
    response = requests.get(url, cookies=cookies)
    if "Welcome back" in response.text:
        print(f"✅ Phrase found with cookie {value}!")
    else:
        print(f"❌ Phrase not found with cookie {value}.")

threads = []
for value in cookie_values:
    t = threading.Thread(target=check_cookie, args=(value,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```
This script will try all the cookie values at the same time, making your script much faster when dealing with many requests.