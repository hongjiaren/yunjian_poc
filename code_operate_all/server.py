# 模块一 ：rpa完成（目前不用做）
# 模块二 ：调用智能体的生成结果
# 模块三 ：调用vl大模型（gpt4o+qwenvl）

import os
import base64
from mimetypes import guess_type
import requests
from docx import Document
from docx.oxml.ns import qn
from lxml import etree
import re
from tool import extract_images_and_find_target
from dashscope import MultiModalConversation
from http import HTTPStatus
from openai import OpenAI
import json
from prompt import HARDWARE_ANALYSIS_PROMPT


# ================== 配置区域 ==================
DOC_PATH = "file/0507【输出-生产测试方案-案例-推荐】产品生产测试方案.docx"
TARGET_TITLE = "整机测试系统框图"

# 配置项（请替换为你自己的 Azure 配置）
OPENAI_API_KEY = "你的AzureOpenAIAPIKey"
RESOURCE_NAME = "你的资源名称"   # 如 my-openai-resource
DEPLOYMENT_NAME = "你的部署名称" # 如 gpt-4o-vision
API_VERSION = "2024-02-15-preview"




def encode_image(image_data):
    """将图片二进制数据编码为 base64"""
    return base64.b64encode(image_data).decode("utf-8")


def image_to_data_url(image_data, mime_type=None):
    """
    将图片二进制数据转换为 data URI 格式。
    可自动识别类型或手动指定（如 'image/png'）
    """
    if not mime_type:
        # 自动猜测 MIME 类型，默认使用 jpeg
        mime_type = guess_type('image.jpg')[0] or 'image/jpeg'
    encoded = encode_image(image_data)
    return f"data:{mime_type};base64,{encoded}"


def analyze_with_azure_gpt4v(image_data, prompt="请描述这张图片的内容。", detail_level="auto"):

    print("🧠 正在调用 Azure 上的 GPT-4 Vision 进行图像分析...")

    # 将图片转为 data:image;base64,...
    image_url = image_to_data_url(image_data)

    # 请求头
    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY
    }

    # 请求体
    payload = {
        "model": DEPLOYMENT_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": detail_level
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500,
        "stream": False
    }

    # 构建请求 URL
    endpoint = f"https://{RESOURCE_NAME}.openai.azure.com/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"

    # 发送请求
    response = requests.post(endpoint, headers=headers, json=payload)

    # 处理响应
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "❌ 响应中没有内容：" + str(result)
    else:
        return f"❌ 请求失败，状态码 {response.status_code}：{response.text}"


def analyze_with_qwen_vl(image_data, prompt):

    # Set OpenAI's API key and API base to use vLLM's API server.
    print("🧠 正在调用本地的qwen2.5vl进行图像分析...")

    # 将图片转为 data:image;base64,...
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

    # 直接获取模型输出的文本内容
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


# # 
# 测试调用
# ================================================

if __name__ == "__main__":
    # Step 1: 查找标题并提取图片（返回的是图片的二进制数据）
    image_data = extract_images_and_find_target(DOC_PATH, TARGET_TITLE)

    if image_data:
        # Step 2: 使用 GPT-4o 分析图片（直接传入图片二进制数据）
        # gpt4o_result = analyze_with_azure_gpt4v(image_data)
        # print("\n🟢【GPT-4o】分析结果：\n")
        # print(gpt4o_result)

        # Step 3: 使用 Qwen2.5-VL 分析图片（直接传入图片二进制数据）
        prompt = HARDWARE_ANALYSIS_PROMPT
        qwen_result = analyze_with_qwen_vl(image_data, prompt)
        print("\n🔵【Qwen2.5-VL】分析结果处理后：\n")
        print(qwen_result)
    else:
        print("⚠️ 未找到图片，无法进行视觉分析。")