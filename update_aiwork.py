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
            "id": "kling",
            "name": "Kling AI",
            "category": "视频",
            "description": "快手Kling视频生成AI，支持高质量视频生成和个性化定制。",
            "tags": ["视频生成", "文本到视频", "国产"],
            "url": "https://kling.ai",
            "pricing": "免费/付费",
            "features": ["高质量视频", "多风格", "实时渲染", "长视频"]
        },
        {
            "id": "v0",
            "name": "V0.dev",
            "category": "代码",
            "description": "Vercel的AI前端生成工具，从描述快速构建UI组件。",
            "tags": ["前端开发", "UI生成", "AI编程"],
            "url": "https://v0.dev",
            "pricing": "免费/付费",
            "features": ["UI组件生成", "React组件", "Tailwind CSS", "实时预览"]
        },
        {
            "id": "sora-text-to-video",
            "name": "Sora-like Tools",
            "category": "视频",
            "description": "类似Sora的文本生成视频工具，提供多种平台的视频生成能力。",
            "tags": ["视频生成", "文本转视频", "AI视频"],
            "url": "https://sora.com",
            "pricing": "免费/付费",
            "features": ["高清视频", "长时长", "多镜头", "真实场景"]
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
            "platform": "Claude.ai",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://claude.ai",
            "tutorialUrl": "https://docs.anthropic.com"
        },
        {
            "platform": "Kling AI",
            "tokenAmount": "免费视频生成",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://kling.ai",
            "tutorialUrl": "https://kling.ai/docs"
        }
    ]
    
    existing_platforms = {token['platform'] for token in data['tokens']}
    
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
    
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Token数据已更新")

def git_commit_and_push():
    try:
        subprocess.run(['git', 'add', 'data/tools.json', 'data/tokens.json'], cwd='/workspace', check=True)
        commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        subprocess.run(['git', 'commit', '-m', commit_message], cwd='/workspace', check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], cwd='/workspace', check=True)
        print("✅ 更改已提交并推送到GitHub")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")

def main():
    print("🚀 开始更新AIwork数据...")
    update_tools()
    update_tokens()
    git_commit_and_push()
    print("✨ 更新完成!")

if __name__ == "__main__":
    main()
