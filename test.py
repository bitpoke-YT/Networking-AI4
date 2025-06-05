import requests

url = "http://172.20.20.13:5000"
proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}
response = requests.get(url, proxies=proxies)
print(response.status_code)