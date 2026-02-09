import requests

url = 'http://localhost:7860/predict'
files = {'file': open('dummy.jpg', 'rb')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Request failed: {e}")
