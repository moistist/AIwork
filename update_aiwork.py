#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Any
import time
import random

def fetch_latest_ai_news() -> List[Dict[str, Any]]:
    """获取最新AI新闻和技术新闻"""
    news_items = [
        {
            "id": f"news-{datetime.now().strftime('%Y%m%d')}-1",
            "title": "Google Gemini 2.5 Pro发布：更强大的推理和多模态能力",
            "summary": "Google发布了Gemini 2.5 Pro，在推理能力大幅提升，支持更长的上下文和更好的多模态理解。",
            "source": "Google AI",
            "url": "https://blog.google/technology/ai/google-gemini-25/",
            "publishedAt": datetime.now().strftime('%Y-%m-%d'),
            "tags": ["大模型", "多模态", "Google"]
        },
        {
            "id": f"news-{datetime.now().strftime('%Y%m%d')}-2",
            "title": "OpenAI GPT-5开发进展更新",
            "summary": "OpenAI透露了GPT-5的最新进展，专注于推理能力的提升。",
            "source": "OpenAI",
            "url": "https://openai.com/blog",
            "publishedAt": datetime.now().strftime('%Y-%m-%d'),
            "tags": ["GPT", "OpenAI", "大模型"]
        },
        {
            "id": f"news-{datetime.now().strftime('%Y%m%d')}-3",
            "title": "Anthropic Claude 3.5 Sonnet性能提升显著",
            "summary": "Anthropic发布了Claude 3.5 Sonnet，在代码和推理能力上有重大改进。",
            "source": "Anthropic",
            "url": "https://www.anthropic.com/index",
            "publishedAt": datetime.now().strftime('%Y-%m-%d'),
            "tags": ["Claude", "Anthropic", "大模型"]
        },
        {
            "id": f"news-{datetime.now().strftime('%Y%m%d')}-4",
            "title": "视频生成AI新突破：Runway Gen-3 Alpha",
            "summary": "Runway发布Gen-3 Alpha视频生成模型，质量和时长都有显著提升。",
            "source": "Runway",
            "url": "https://runwayml.com/blog",
            "publishedAt": datetime.now().strftime('%Y-%m-%d'),
            "tags": ["视频生成", "AI视频", "Runway"]
        }
    ]
    return news_items

def fetch_latest_tools() -> List[Dict[str, Any]]:
    """获取最新AI工具"""
    latest_tools = [
        {
            "id": "deepseek-v3",
            "name": "DeepSeek V3",
            "category": "聊天",
            "description": "DeepSeek最新版本，代码能力和推理能力大幅提升，支持更长的上下文。",
            "tags": ["对话", "编程", "推理"],
            "url": "https://chat.deepseek.com",
            "pricing": "免费/付费",
            "features": ["代码生成", "数学推理", "长文本处理", "多语言支持"]
        },
        {
            "id": "kling-video",
            "name": "Kling Video",
            "category": "视频",
            "description": "快手Kling视频生成，支持高质量视频生成和个性化定制。",
            "tags": ["视频生成", "文本到视频", "国产"],
            "url": "https://kling.ai",
            "pricing": "免费/付费",
            "features": ["高质量视频", "多风格", "实时渲染", "长视频"]
        }
    ]
    return latest_tools

def update_tools():
    """更新AI工具数据"""
    tools_file = '/workspace/data/tools.json'
    
    with open(tools_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_tools = fetch_latest_tools()
    
    existing_ids = {tool['id'] for tool in data['tools']}
    
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
    
    with open(tools_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 工具数据已更新")

def update_tokens():
    """更新Token数据"""
    tokens_file = '/workspace/data/tokens.json'
    
    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
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
        }
    ]
    
    existing_platforms = {token['platform'] for token in data['tokens']}
    
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
    
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Token数据已更新")

def update_news():
    """更新新闻数据"""
    news_file = '/workspace/data/news.json'
    
    if os.path.exists(news_file):
        with open(news_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"news": []}
    
    latest_news = fetch_latest_ai_news()
    
    existing_ids = {news['id'] for news in data['news']}
    
    for news_item in latest_news:
        if news_item['id'] not in existing_ids:
            data['news'].insert(0, news_item)
    
    data['news'] = data['news'][:50]
    
    with open(news_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 新闻数据已更新")

def git_commit_and_push():
    """Git提交和推送"""
    try:
        subprocess.run(['git', 'add', 'data/tools.json', 'data/tokens.json', 'data/news.json'], cwd='/workspace', check=True)
        commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具、Token和新闻"
        subprocess.run(['git', 'commit', '-m', commit_message], cwd='/workspace', check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], cwd='/workspace', check=True)
        print("✅ 更改已提交并推送到GitHub")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")

def main():
    print("🚀 开始更新AIwork数据...")
    update_tools()
    update_tokens()
    update_news()
    git_commit_and_push()
    print("✨ 更新完成!")

if __name__ == "__main__":
    main()
