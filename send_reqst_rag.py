import requests

url = "http://localhost:5005/test_process"
data = {
    "query": "D2 类制造策略路线"
}

response = requests.post(url, json=data)
print("状态码:", response.status_code)
print("响应内容:", response.json())