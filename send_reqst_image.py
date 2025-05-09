import requests

url = 'http://localhost:5005/image_recognition'
files = {'file': open('/Users/oliver/Desktop/yunjian_poc/组网图.jpg', 'rb')}
response = requests.post(url, files=files)

print(response.text)