import requests


response = requests.get("http://deleonautoglass.com")

print(response.status_code)