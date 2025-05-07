# 智能测试文档生成系统

[![License: MIT](https://img.shields.io/github/license/hongjiaren/test-doc-generator.svg)](https://github.com/hongjiaren/test-doc-generator/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Issues](https://img.shields.io/github/issues/hongjiaren/test-doc-generator.svg)](https://github.com/hongjiaren/test-doc-generator/issues)
[![Stars](https://img.shields.io/github/stars/hongjiaren/test-doc-generator.svg?style=social)](https://github.com/hongjiaren/test-doc-generator/stargazers)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)]()
[![Downloads](https://img.shields.io/badge/downloads-100%2B-lightgrey.svg)]()
[![CI](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)]()

---
# 智能测试文档生成系统

## 📖 项目简介

智能测试文档生成系统是一个基于人工智能的自动化测试文档生成工具，专注于文档内容提取、智能填写、文档理解和图像识别等功能。该系统能够自动分析测试需求，生成标准化的测试文档，并提供智能化的文档管理解决方案。

## 🎯 功能概览

目前系统内置以下核心功能模块：

- **文档内容提取**：自动从各种格式的文档中提取关键信息
- **智能填写**：基于上下文自动填写测试用例和测试步骤
- **文档理解**：深度理解文档内容，提取测试要点和关键信息
- **图像识别**：支持测试界面截图分析，自动生成测试步骤
- **文档生成**：自动生成标准格式的测试文档

## 📦 系统架构

- 支持多种文档格式（Word、PDF、Excel等）
- 集成OCR和图像识别技术
- 内置NLP处理模块，支持文档智能分析
- 支持自定义文档模板
- 提供API接口，支持与其他系统集成
- 支持批量处理和实时处理模式

## 📂 项目结构
.
├── server.py                  # 主程序
├── config.py                  # 配置文件
├── .env                       # 环境变量
├── modules/                   # 核心模块目录
│   ├── __init__.py
│   ├── document_extractor.py  # 文档提取模块
│   ├── content_filler.py      # 内容填写模块
│   ├── doc_analyzer.py        # 文档分析模块
│   └── image_processor.py     # 图像处理模块
├── templates/                 # 文档模板目录
└── requirements.txt           # 依赖包列表

## 🚀 快速启动

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入必要的配置信息
   ```

3. 启动服务：
   ```bash
   python server.py
   ```

## 📡 API接口示例

1. 文档处理请求：
```json
{
  "file_path": "path/to/document.pdf",
  "template_type": "test_case",
  "options": {
    "extract_content": true,
    "generate_steps": true,
    "analyze_images": true
  }
}
```

2. 返回格式：
```json
{
  "status": "success",
  "document": {
    "title": "测试文档标题",
    "content": "生成的测试文档内容",
    "test_cases": [...],
    "images": [...]
  }
}
```

## 🔧 配置说明

系统通过`.env`文件进行配置，主要配置项包括：

- `OCR_API_KEY`: OCR服务API密钥
- `NLP_MODEL_PATH`: NLP模型路径
- `TEMPLATE_DIR`: 文档模板目录
- `OUTPUT_DIR`: 输出文档目录
- `MAX_FILE_SIZE`: 最大文件大小限制

## 📌 未来规划

- 支持更多文档格式和模板
- 增强图像识别准确度
- 添加文档版本控制功能
- 集成测试用例管理系统
- 提供Web界面
- 支持多语言文档处理
- 优化文档生成性能

## 📄 License

MIT License
