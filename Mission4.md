# Mission 4: Cracking Encrypted Tasks – A Guided Python Hacking Adventure 🚀🕵️‍♀️

---

## 🧩 Encryption in Python: The Good, the Bad, and the Sneaky

Encryption and encoding are everywhere! Sometimes they're used to protect secrets, sometimes just to make things look mysterious. Here are some ways you might see data hidden in the wild:

### 🚫 Insecure Methods (For Learning Only!)

#### 1. Base64 Encoding (Just Obfuscation!)
```python
import base64
data = "Secret message".encode("utf-8")
encoded = base64.b64encode(data).decode("utf-8")
print("Encoded:", encoded)
decoded = base64.b64decode(encoded).decode("utf-8")
print("Decoded:", decoded)
```

#### 2. Weak Hashing (MD5 is Old News)
```python
import hashlib
password = "password123".encode("utf-8")
hash_md5 = hashlib.md5(password).hexdigest()
print("MD5 Hash:", hash_md5)
```

#### 3. XOR Cipher (Super Basic)
```python
def xor_encrypt(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
key = b"key"
plaintext = b"Secret message"
ciphertext = xor_encrypt(plaintext, key)
print("XOR Encrypted:", ciphertext.hex())
```

#### 4. AES in ECB Mode (Not Recommended)
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
key = b"1234567890123456"
cipher = AES.new(key, AES.MODE_ECB)
data = b"Secret data"
ciphertext = cipher.encrypt(pad(data, AES.block_size))
print("ECB Encrypted:", ciphertext.hex())
```

### 🛡️ Secure Encryption Example

#### AES-CBC with PBKDF2 (Much Better!)
```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2

password = b"SecurePassword123!"
salt = get_random_bytes(16)
key = PBKDF2(password, salt, dkLen=32, count=1000000)
iv = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
data = b"Top secret message!"
ciphertext = cipher.encrypt(pad(data, AES.block_size))
print("AES-CBC Encrypted:", ciphertext.hex())
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
print("Decrypted:", decrypted.decode("utf-8"))
```

---

## 🐍 Python Requests & Cookies 🍪

Automating data retrieval is a superpower! Many systems use cookies to keep track of users or sessions. Here’s how you can experiment with sending requests and cookies:

### 🍪 Sending Requests with Cookies
```python
import requests
url = "http://localhost:4333/tasks"
headers = {"Cookie": f"sessionID=YOUR_SESSION_ID"}
response = requests.get(url, headers=headers)
print(response.text)
```
*Tip: You can often find session tokens or IDs in your browser’s developer tools!*

### 📦 Handling JSON Responses
```python
if response.status_code == 200:
    data = response.json()
    print(data)
```

### 🔄 Looping Through IDs or Tokens
Try different values to see what you can discover!
```python
for sid in range(1, 500):
    headers = {"Cookie": f"sessionID={sid}"}
    response = requests.get(url, headers=headers)
    # ...check for your phrase...
```

### ⚡ Multithreading for Speed
```python
import threading
def check_sid(sid):
    # ...send request and check...
threads = []
for sid in range(1, 100):
    t = threading.Thread(target=check_sid, args=(sid,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
```

---

## 🕵️‍♂️ Finding Hidden APIs & JSON Data

Ever wondered how apps get their data? Many use APIs that return JSON! Here’s how to play detective:

**Try this:**
- Open your browser’s Developer Tools (`F12`) 🖥️.
- Visit pages and watch the **Network** tab for interesting requests.
- Look for responses with `{ ... }` or `[ ... ]` — that’s usually JSON!
- Check the **Cookies** and **Headers** tabs for clues.

*🖼️ Image idea: Screenshot of a network request returning JSON, and the cookies panel.*

---

## 🧬 Decoding Base64 in Data Fields

If you see strings like `U29tZSBzZWNyZXQgdGV4dA==`, you’ve probably found base64! Try decoding it:

```python
import base64
encoded = "U29tZSBzZWNyZXQgdGV4dA=="
decoded = base64.b64decode(encoded).decode("utf-8")
print(decoded)
```

---

## 🔍 Searching for Secret Phrases

Your challenge: Find a hidden phrase (like "Troops" or "Secret") in some encoded or encrypted data. You might need to:
- Loop through possible tokens or IDs 🔄
- Fetch and decode data 🧩
- Search for your phrase in the results 🔑

---

## 🛡️ Secure Password Hashing (For Reference) 🧂

If you want to see how passwords *should* be protected:
```python
import bcrypt
password = b"SecurePassword123!"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print("Bcrypt Hash:", hashed)
if bcrypt.checkpw(password, hashed):
    print("Password matches!")
```

---

## 🎯 Your Challenge

Combine your skills:
- Use cookies or tokens to fetch data 🍪
- Parse JSON and decode fields 🧬
- Search for the secret phrase 🔍
- Use threads for speed ⚡
- Handle errors and avoid rate limits 🚦

Once you find the answer, celebrate your hacking victory! 🎉🦸‍♂️
