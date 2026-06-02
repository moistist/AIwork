#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime

def update_tools():
    tools_file = '/workspace/data/tools.json'
    
    with open(tools_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_tools = [
        {
            "id": "o1-preview",
            "name": "OpenAI o1",
            "category": "推理",
            "description": "OpenAI的推理大模型，擅长复杂问题解决、数学和编程。",
            "tags": ["推理", "编程", "数学"],
            "url": "https://openai.com/index/introducing-openai-o1/",
            "pricing": "付费",
            "features": ["复杂推理", "思维链", "数学解题", "代码优化"]
        },
        {
            "id": "dall-e-3",
            "name": "DALL·E 3",
            "category": "图像",
            "description": "OpenAI最新图像生成模型，更高质量、更准确的文本到图像转换。",
            "tags": ["图像生成", "OpenAI", "高质量"],
            "url": "https://openai.com/dall-e-3",
            "pricing": "免费/付费",
            "features": ["高质量图像", "文本准确", "多风格", "详细提示"]
        },
        {
            "id": "gemini-2",
            "name": "Google Gemini 2",
            "category": "多模态",
            "description": "Google最新多模态大模型，支持文本、图像、视频、音频。",
            "tags": ["多模态", "Gemini", "Google"],
            "url": "https://gemini.google.com",
            "pricing": "免费/付费",
            "features": ["多模态理解", "实时搜索", "编程", "创意生成"]
        },
        {
            "id": "coze",
            "name": "字节跳动Coze",
            "category": "应用开发",
            "description": "一站式AI应用开发平台，快速构建聊天机器人和AI工作流。",
            "tags": ["应用开发", "工作流", "机器人"],
            "url": "https://www.coze.cn",
            "pricing": "免费/付费",
            "features": ["智能体开发", "插件集成", "工作流编排", "多平台部署"]
        }
    ]
    
    existing_ids = {tool['id'] for tool in data['tools']}
    
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
    
    with open(tools_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 工具数据已更新")

def update_tokens():
    tokens_file = '/workspace/data/tokens.json'
    
    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for token in data['tokens']:
        token['validityPeriod'] = "2027-12-31"
    
    new_tokens = [
        {
            "platform": "字节跳动豆包",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://www.doubao.com",
            "tutorialUrl": "https://www.doubao.com/docs"
        },
        {
            "platform": "阿里云百炼",
            "tokenAmount": "免费试用",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://bailian.console.aliyun.com",
            "tutorialUrl": "https://help.aliyun.com/zh/bailian"
        },
        {
            "platform": "腾讯混元",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://hunyuan.tencent.com",
            "tutorialUrl": "https://cloud.tencent.com/document/product/1729"
        }
    ]
    
    existing_platforms = {token['platform'] for token in data['tokens']}
    
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
    
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Token数据已更新")

def main():
    print("🚀 开始更新AIwork数据...")
    update_tools()
    update_tokens()
    print("✨ 更新完成!")

if __name__ == "__main__":
    main()
