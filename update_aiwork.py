#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent.resolve()

def update_tools():
    tools_file = get_project_root() / 'data' / 'tools.json'
    
    with open(tools_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 这里可以添加获取最新AI工具的逻辑（比如爬取网站或API）
    # 目前保持示例数据
    new_tools = [
        {
            "id": "deepseek",
            "name": "DeepSeek",
            "category": "聊天",
            "description": "国产大语言模型，具有强大的代码生成和推理能力，支持多语言和长文本。",
            "tags": ["对话", "编程", "推理"],
            "url": "https://chat.deepseek.com",
            "pricing": "免费/付费",
            "features": ["代码生成", "数学推理", "长文本处理", "多语言支持"]
        },
        {
            "id": "perplexity",
            "name": "Perplexity AI",
            "category": "搜索",
            "description": "AI驱动的搜索引擎，提供实时信息检索和问答服务，支持多种搜索模式。",
            "tags": ["搜索", "问答", "知识"],
            "url": "https://www.perplexity.ai",
            "pricing": "免费/付费",
            "features": ["实时搜索", "源引用", "多模态搜索", "学术搜索"]
        },
        {
            "id": "luma",
            "name": "Luma AI",
            "category": "视频",
            "description": "3D场景和视频生成AI工具，支持从文本生成3D模型和视频内容。",
            "tags": ["3D生成", "视频生成", "文本到3D"],
            "url": "https://lumalabs.ai",
            "pricing": "免费/付费",
            "features": ["文本到3D", "视频生成", "3D场景", "AR预览"]
        },
        {
            "id": "ollama",
            "name": "Ollama",
            "category": "模型",
            "description": "本地运行大语言模型的工具，支持多种开源模型，简单易用。",
            "tags": ["本地部署", "开源", "LLM"],
            "url": "https://ollama.com",
            "pricing": "免费",
            "features": ["本地运行", "开源模型", "命令行工具", "API支持"]
        }
    ]
    
    existing_ids = {tool['id'] for tool in data['tools']}
    added_count = 0
    
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            added_count += 1
    
    with open(tools_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 工具数据已更新，新增 {added_count} 个工具")

def update_tokens():
    tokens_file = get_project_root() / 'data' / 'tokens.json'
    
    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 这里可以添加获取最新免费Token的逻辑
    new_tokens = [
        {
            "platform": "DeepSeek",
            "tokenAmount": "¥18",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.deepseek.com",
            "tutorialUrl": "https://platform.deepseek.com/docs"
        },
        {
            "platform": "Groq",
            "tokenAmount": "免费高速API",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://console.groq.com",
            "tutorialUrl": "https://console.groq.com/docs"
        },
        {
            "platform": "Ollama",
            "tokenAmount": "完全免费",
            "validityPeriod": "永久",
            "status": "active",
            "claimUrl": "https://ollama.com/download",
            "tutorialUrl": "https://github.com/ollama/ollama"
        }
    ]
    
    existing_platforms = {token['platform'] for token in data['tokens']}
    added_count = 0
    
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
            added_count += 1
    
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Token数据已更新，新增 {added_count} 个Token")

def main():
    print("🚀 开始更新AIwork数据...")
    
    # 更新数据
    update_tools()
    update_tokens()
    
    # 检查是否有变更
    project_root = get_project_root()
    
    print("✨ 更新完成!")

if __name__ == "__main__":
    main()
