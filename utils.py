from flask import Flask, request, jsonify
import base64
from mimetypes import guess_type
from openai import OpenAI
import json
from prompt import HARDWARE_ANALYSIS_PROMPT


def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')


def image_to_data_url(image_data, mime_type=None):
    if not mime_type:
        mime_type = guess_type('image.jpg')[0] or 'image/jpeg'
    encoded = encode_image(image_data)
    return f"data:{mime_type};base64,{encoded}"

def analyze_with_qwen_vl(image_data, query):
    print("🧠 正在调用本地的qwen2.5vl进行图像分析...")
    
    # 定义固定的提示信息或根据需求动态生成
    prompt = HARDWARE_ANALYSIS_PROMPT.format(query=query)
    
    image_url = image_to_data_url(image_data)
    openai_api_key = "EMPTY"
    openai_api_base = "http://223.109.239.12:8008/v1"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    chat_response = client.chat.completions.create(
        model="/dataAll/liweier/Qwen2.5-VL-72B-Instruct-bnb-4bit",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            },
        ],
    )
    response_content = chat_response.choices[0].message.content
    print("📝 模型输出内容如下：")
    print(response_content)

    try:
        cleaned_response_content = response_content.strip().replace('```json', '').replace('\n', '').replace('```', '')
        parsed_response = json.loads(cleaned_response_content)
        print(parsed_response)
        return parsed_response
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None


