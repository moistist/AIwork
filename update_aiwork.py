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
            "id": "gpt-5",
            "name": "GPT-5",
            "category": "聊天",
            "description": "OpenAI最新的大语言模型，具有更强的推理能力、多模态理解和代码生成能力。",
            "tags": ["对话", "推理", "多模态", "编程"],
            "url": "https://chat.openai.com",
            "pricing": "免费/付费",
            "features": ["高级推理", "多模态理解", "代码生成", "长上下文"]
        },
        {
            "id": "claude-opus",
            "name": "Claude 4 Opus",
            "category": "聊天",
            "description": "Anthropic的旗舰模型，具有超强的长文本分析、推理和创意写作能力。",
            "tags": ["对话", "分析", "写作", "长文本"],
            "url": "https://claude.ai",
            "pricing": "付费",
            "features": ["超长上下文", "深度推理", "文档分析", "安全对齐"]
        },
        {
            "id": "sora-2",
            "name": "Sora 2",
            "category": "视频",
            "description": "OpenAI的第二代文本生成视频模型，支持更长时长、更高质量的视频生成。",
            "tags": ["视频生成", "文本转视频", "OpenAI"],
            "url": "https://openai.com/sora",
            "pricing": "付费",
            "features": ["4K视频", "10分钟时长", "物理模拟", "多镜头"]
        },
        {
            "id": "ideogram-3",
            "name": "Ideogram 3.0",
            "category": "图像",
            "description": "文字嵌入专家，生成带有完美文字的图像，支持多种艺术风格。",
            "tags": ["图像生成", "文字嵌入", "艺术创作"],
            "url": "https://ideogram.ai",
            "pricing": "免费/付费",
            "features": ["完美文字", "高分辨率", "风格多样", "快速生成"]
        },
        {
            "id": "replit-ai",
            "name": "Replit AI",
            "category": "代码",
            "description": "在线编程平台的AI助手，支持协作编程、实时调试和代码生成。",
            "tags": ["编程", "在线IDE", "协作"],
            "url": "https://replit.com",
            "pricing": "免费/付费",
            "features": ["在线IDE", "协作编程", "AI辅助", "实时调试"]
        },
        {
            "id": "whisper-v4",
            "name": "Whisper V4",
            "category": "音频",
            "description": "OpenAI最新版语音识别模型，支持更多语言和更低的错误率。",
            "tags": ["语音识别", "ASR", "音频"],
            "url": "https://openai.com/research/whisper",
            "pricing": "免费/付费",
            "features": ["多语言", "高准确率", "实时转写", "方言支持"]
        },
        {
            "id": "fal-ai",
            "name": "Fal AI",
            "category": "视频",
            "description": "高性能视频生成API，提供实时视频生成和编辑能力。",
            "tags": ["视频生成", "API", "实时"],
            "url": "https://fal.ai",
            "pricing": "免费/付费",
            "features": ["实时生成", "API集成", "高质量", "低延迟"]
        },
        {
            "id": "cognition-ai",
            "name": "Cognition AI",
            "category": "代码",
            "description": "AI编程助手，能够自主完成复杂的编程任务和项目。",
            "tags": ["编程", "自主", "AI代理"],
            "url": "https://cognition.ai",
            "pricing": "付费",
            "features": ["自主编程", "任务规划", "代码测试", "文档生成"]
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
        token['validityPeriod'] = "2027-06-01"
    
    new_tokens = [
        {
            "platform": "OpenAI GPT-5",
            "tokenAmount": "$10",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.openai.com/signup",
            "tutorialUrl": "https://platform.openai.com/docs"
        },
        {
            "platform": "Anthropic Claude 4",
            "tokenAmount": "$20",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.anthropic.com",
            "tutorialUrl": "https://docs.anthropic.com"
        },
        {
            "platform": "Fal AI",
            "tokenAmount": "5000积分",
            "validityPeriod": "2027-09-01",
            "status": "active",
            "claimUrl": "https://fal.ai",
            "tutorialUrl": "https://fal.ai/docs"
        },
        {
            "platform": "Cohere Coral",
            "tokenAmount": "$15",
            "validityPeriod": "2027-08-01",
            "status": "active",
            "claimUrl": "https://cohere.com",
            "tutorialUrl": "https://docs.cohere.com"
        },
        {
            "platform": "Replit AI",
            "tokenAmount": "Pro订阅30天",
            "validityPeriod": "2027-07-01",
            "status": "active",
            "claimUrl": "https://replit.com/pricing",
            "tutorialUrl": "https://docs.replit.com"
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
