from flask import Flask, request, jsonify
import base64
from PIL import Image
import io
from mimetypes import guess_type
from openai import OpenAI
import json
import logging
from utils import analyze_with_qwen_vl
import requests


logging.basicConfig(level=logging.INFO)
API_KEY = "app-3lSIEZYFnGR4bTWUpt32E4xs"
BASE_URL = "http://10.4.2.47/v1/chat-messages"
app = Flask(__name__)

@app.route('/image_recognition', methods=['POST'])
def image_recognition():
    app.logger.info("收到/image_recognition请求")

    # 检查请求中是否包含文件部分
    if 'file' not in request.files:
        app.logger.error('请求中不包含文件部分')
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']

    # 检查是否有文件被上传
    if file.filename == '':
        app.logger.error('未选择任何文件')
        return jsonify({'error': 'No selected file'}), 400

    # 获取 query 参数
    query = request.form.get('query', '')

    if file:
        try:
            # 读取图片二进制数据
            img_bytes = file.read()
            app.logger.info(f"成功接收到文件 {file.filename}，大小: {len(img_bytes)} 字节")

            # 调用图像分析模型，同时传递 query 参数
            answer = analyze_with_qwen_vl(img_bytes, query=query)

            if answer is None:
                return jsonify({'error': '图像分析失败，请检查输入或模型服务'}), 500

            # 返回分析结果
            return jsonify({
                "answer": answer
            }), 200

        except Exception as e:
            app.logger.error(f"处理文件时发生异常: {str(e)}", exc_info=True)
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500



@app.route('/test_process', methods=['POST'])
def test_process():
    app.logger.info("收到 /test_process 请求")

    data = request.get_json()
    if not data or 'query' not in data:
        app.logger.error("请求中缺少 'query' 字段")
        return jsonify({'error': 'Missing "query" field in the request'}), 400

    query = data['query']
    app.logger.info(f"接收到的问题: {query}")

    # 构造请求体
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "abc-123"
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 发起远程请求
        response = requests.post(BASE_URL, json=payload, headers=headers)
        app.logger.info(f"知识库服务返回状态码: {response.status_code}")

        if response.status_code != 200:
            return jsonify({
                'error': '知识库服务调用失败',
                'status_code': response.status_code,
                'response_text': response.text
            }), response.status_code

        # 解析知识库服务的结果
        answer = response.json()['answer']

        clean_answer=answer.strip().replace('```json', '').replace('\n', '').replace('```', '')
        # 处理企业大脑知识库检索后返回的内容
        print(clean_answer)


        # 返回知识库服务的结果
        return jsonify({
            "answer": clean_answer
        }), 200

    except Exception as e:
        app.logger.error(f"调用知识库服务时发生异常: {str(e)}", exc_info=True)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)