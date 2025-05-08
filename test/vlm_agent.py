#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Filename         :uitars_agent.py
Description      :
Time             :2025/03/10 15:13:07
Author           :@huasheng
Version          :1.0
'''

import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../..')))

from pipeline.mm_agents.prompts import ASSOCIATING_LOW_LEVEL_TASKS_CH, GENERATE_PARAMETERS_CH
from utils.tools import  image2base64
from openai import OpenAI
import json

class VLMAgent:
    def __init__(self, model_name, max_tokens=100, temperature=0.7, top_p=0.9):
        self.prompt_template = ASSOCIATING_LOW_LEVEL_TASKS_CH
        self.prompt_parameter = GENERATE_PARAMETERS_CH
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.model_name = model_name
        # qwen
        self.vlm = OpenAI(
            base_url= "http://223.109.239.12:8008/v1",
            api_key="EMPTY"
        )
        # tars
        # self.vlm = OpenAI(
        #     base_url="http://223.109.239.12:15997/v1",
        #     api_key="empty",
        # )

    def generate_instructions(self, current_action, 
                              pre_website_address,  
                              pre_website_intro, 
                              cur_website_address,  
                              cur_website_intro, 
                              screenshot_1_base64, 
                              screenshot_2_base64
                              ):
        # 构建系统提示
        system_prompt = self.prompt_template.format(
            current_action = current_action,
            pre_website_address = pre_website_address,
            pre_website_intro = pre_website_intro,
            cur_website_address = cur_website_address,
            cur_website_intro = cur_website_intro
        )

        print(system_prompt)
        # 构建messages结构（符合DashScope多模态格式）
        messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt}
                ]
            },
            {
                "role": "user",
                "content": [
                    # 添加操作前截图
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_1_base64}"
                        }
                    },
                    {"type": "text", "text": "操作前截图,操作红色框框住的元素"},

                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_2_base64}"
                        }
                    },
                    {"type": "text", "text": "操作后截图，包含操作后的界面状态"},
                    # 用户指令
                    {"type": "text", "text": "请生成子指令和分析。"}
                ]
            }
        ]

        # 调用API（注意参数名和结构需要匹配DashScope要求）
        response = self.vlm.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        
        response_content = response.choices[0].message.content
        try:
            cleaned_response_content = response_content.strip().replace('```json', '').replace('\n', '').replace('```', '')
            parsed_response = json.loads(cleaned_response_content)
            print(parsed_response)
            return parsed_response
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None


    def generate_parameter(self, screenshot_base64, element_type):
        """
        使用多模态，自动生成输入文本内容
        """
        # 构建系统提示
        system_prompt = self.prompt_parameter.format(
            element_type=element_type,
            screenshot_base64=screenshot_base64
        )
        
        # 构建messages结构（符合DashScope多模态格式）
        messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt}
                ]
            },
            {
                "role": "user",
                "content": [
                    # 添加截图
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_base64}"
                        }
                    },
                    {"type": "text", "text": "请生成适当的输入内容。"}
                ]
            }
        ]
        
        # 调用API（注意参数名和结构需要匹配DashScope要求）
        response = self.vlm.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        
        response_content = response.choices[0].message.content

        try:
            # 预处理JSON字符串，去除多余的换行符和空格
            cleaned_response_content = response_content.strip().replace('```json', '').replace('\n', '').replace('```', '')
            parsed_response = json.loads(cleaned_response_content)
            print(parsed_response)
            return parsed_response
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        
     
     
    def generate_height_instructions(self, current_action, 
                              pre_website_address,  
                              pre_website_intro, 
                              cur_website_address,  
                              cur_website_intro, 
                              screenshot_1_base64, 
                              screenshot_2_base64
                              ):
        
        """
        生成高阶指令
        
        """
        # 构建系统提示
        system_prompt = self.prompt_template.format(
            current_action = current_action,
            pre_website_address = pre_website_address,
            pre_website_intro = pre_website_intro,
            cur_website_address = cur_website_address,
            cur_website_intro = cur_website_intro
        )

        print(system_prompt)
        # 构建messages结构（符合DashScope多模态格式）
        messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": system_prompt}
                ]
            },
            {
                "role": "user",
                "content": [
                    # 添加操作前截图
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_1_base64}"
                        }
                    },
                    {"type": "text", "text": "操作前截图,操作红色框框住的元素"},

                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_2_base64}"
                        }
                    },
                    {"type": "text", "text": "操作后截图，包含操作后的界面状态"},
                    # 用户指令
                    {"type": "text", "text": "请生成子指令和分析。"}
                ]
            }
        ]

        # 调用API（注意参数名和结构需要匹配DashScope要求）
        response = self.vlm.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        
        response_content = response.choices[0].message.content
        try:
            cleaned_response_content = response_content.strip().replace('```json', '').replace('\n', '').replace('```', '')
            parsed_response = json.loads(cleaned_response_content)
            print(parsed_response)
            return parsed_response
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
  


def test_task():
    agent = VLMAgent("/dataAll/liweier/Qwen2.5-VL-72B-Instruct-bnb-4bit")

    # 示例输入数据
    pre_website_address = "https://ebooking.ctrip.com/login/index"
    pre_website_intro = "携程酒店商家管理后台——让酒店生意更简单。携程eBooking是一个开放、透明的酒店服务平台，以数据为基础，为酒店提供收益管理；在线实时管控房态、房价；处理订单；参加营销活动；点评管卖酒店附加产品等服务。旨在实现酒店与携程双方共赢，更好地为客人提供服务。"
    current_action = "点击"
    cur_website_address = "https://www.ctrip.com/"
    cur_website_intro = "携程旅行网，酒店预订，机票预定"
    
    screenshot_1_base64 = image2base64(r"pipeline\mm_agents\demo_image\src.png")  # 替换为实际的Base64编码截图数据
    screenshot_2_base64 = image2base64(r"pipeline\mm_agents\demo_image\dst.png")  # 替换为实际的Base64编码截图数据

    # 生成指令和分析
    result = agent.generate_instructions( current_action, 
                                            pre_website_address,  
                                            pre_website_intro, 
                                            cur_website_address,  
                                            cur_website_intro, 
                                            screenshot_1_base64, 
                                            screenshot_2_base64
                                            )

def test_parameter():
 
    agent = VLMAgent("/dataAll/liweier/Qwen2.5-VL-72B-Instruct-bnb-4bit")
    element_type = "输入栏"
    screenshot_base64 = image2base64(r"pipeline\mm_agents\demo_image\screenshot_2025-03-24_11-01-31.png")  # 替换为实际的Base64编码截图数据
    # 生成指令和分析
    result = agent.generate_parameter( screenshot_base64, element_type)
    
    
def test_instructions():
    """
    测试生成高阶指令
    """

    agent = VLMAgent("/dataAll/liweier/Qwen2.5-VL-72B-Instruct-bnb-4bit")
    
    
# 示例使用
if __name__ == "__main__":
    # test_task()
    # test_parameter()
    # 测试生成高阶指令
    test_instructions()