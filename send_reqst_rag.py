import requests

url = "http://localhost:5005/test_process"
headers = {
    "Content-Type": "application/json"
}
data = {
    "question": "D2 类制造策略路线"
}

response = requests.post(url, json=data, headers=headers)
print("状态码:", response.status_code)
print("响应内容:", response.json())