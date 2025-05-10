import requests
url = 'http://localhost:5005/image_recognition'
files = {'file': open('/Users/oliver/Desktop/yunjian_poc/组网图.jpg', 'rb')}
data = {
    "query": """1、图中标注为SD6881的模块为被测设备。
        2、需要用到1个USB，图中未画出。
        3、需要配置5个风扇模块，图中未画出，对应编码为0231K2ET。
        4、2个AC电源模块，图中以PWRX表示，对应编码为0231K2EN/0231K2EP。
        5、需要配置48个SFP28 25G工具光模块，图中未画出。
        6、需要配置8个QSFP28 100G工具光模块，图中未画出。"""
}
response = requests.post(url, files=files, data=data)

print("状态码:", response.status_code)
print("响应内容:", response.json())