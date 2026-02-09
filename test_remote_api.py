import requests

url = 'https://sheethal0703-fruith-quality-classifier.hf.space/predict'
try:
    with open('dummy.jpg', 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
except Exception as e:
    print(f"Request failed: {e}")
