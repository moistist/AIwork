#!/usr/bin/env python3
import json
import os
import subprocess
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """提取HTML中的文本内容"""
    def __init__(self):
        super().__init__()
        self.texts = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.texts.append(text)

    def get_text(self, separator=' '):
        return separator.join(self.texts)

def fetch_url(url, timeout=10):
    """获取网页内容"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"获取 {url} 失败: {e}")
        return None

def get_aitools_news():
    """获取AI工具最新资讯"""
    tools = []

    # 来源1: AI工具导航网站 - AlternativeTo
    alt_url = "https://alternativeto.net/category/artificial-intelligence/"
    content = fetch_url(alt_url)
    if content:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()[:2000]
        # 从文本中提取相关AI工具名称
        ai_keywords = ['ChatGPT', 'Claude', 'Midjourney', 'Stable Diffusion', 'Gemini',
                       'Perplexity', 'Cursor', 'Copilot', 'Sora', 'Runway', 'Luma',
                       'DALL-E', 'Stable Video', 'Kling', 'Vidu', 'Pixverse']

    # 来源2: Product Hunt AI分类
    ph_url = "https://www.producthunt.com/categories/artificial-intelligence"
    content = fetch_url(ph_url)
    if content:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()[:2000]

    # 返回预设的最新AI工具列表（实际项目中可接入更多数据源）
    new_tools = [
        {
            "id": "gemini",
            "name": "Google Gemini",
            "category": "聊天",
            "description": "Google推出的多模态AI模型，支持文本、图像、音频和视频理解。",
            "tags": ["对话", "多模态", "Google"],
            "url": "https://gemini.google.com",
            "pricing": "免费/付费",
            "features": ["多模态理解", "代码生成", "长上下文", "Google集成"]
        },
        {
            "id": "claude-3",
            "name": "Claude 3",
            "category": "聊天",
            "description": "Anthropic最新一代AI助手，配备卓越的推理能力和超长上下文窗口。",
            "tags": ["对话", "推理", "长文本"],
            "url": "https://claude.ai",
            "pricing": "免费/付费",
            "features": ["200K上下文", "多模态", "编程能力", "安全对齐"]
        },
        {
            "id": "grok",
            "name": "Grok",
            "category": "聊天",
            "description": "xAI推出的AI助手，具有实时知识获取和独特的幽默风格。",
            "tags": ["对话", "实时知识", "幽默"],
            "url": "https://x.ai/grok",
            "pricing": "免费/付费",
            "features": ["实时搜索", "幽默对话", "开源模型", "X平台集成"]
        },
        {
            "id": "stable-video",
            "name": "Stable Video",
            "category": "视频",
            "description": "Stability AI推出的文本生成视频工具，支持多种风格和时长。",
            "tags": ["视频生成", "文本到视频", "AI视频"],
            "url": "https://www.stability.ai/stable-video",
            "pricing": "免费/付费",
            "features": ["4秒视频生成", "多风格", "图像到视频", "API支持"]
        },
        {
            "id": "pika",
            "name": "Pika",
            "category": "视频",
            "description": "AI视频生成平台，支持图像动画化和文本生成视频功能。",
            "tags": ["视频生成", "图像动画", "AI视频"],
            "url": "https://pika.art",
            "pricing": "免费/付费",
            "features": ["图像动画化", "文本生成视频", "视频编辑", "社区模型"]
        },
        {
            "id": "kling-video",
            "name": "Kling AI",
            "category": "视频",
            "description": "快手可灵AI视频生成模型，支持高质量长视频生成。",
            "tags": ["视频生成", "国产", "长视频"],
            "url": "https://klingai.com",
            "pricing": "免费/付费",
            "features": ["3秒视频生成", "长视频支持", "电影级效果", "运动笔刷"]
        },
        {
            "id": "vidu",
            "name": "Vidu",
            "category": "视频",
            "description": "生数科技推出的AI视频生成工具，支持中文理解的视频创作。",
            "tags": ["视频生成", "国产", "中文理解"],
            "url": "https://www.vidu.studio",
            "pricing": "免费/付费",
            "features": ["文生视频", "图生视频", "角色一致性", "中文优化"]
        },
        {
            "id": "pixverse",
            "name": "PixVerse",
            "category": "视频",
            "description": "AI视频生成平台，支持多种风格和快速视频生成。",
            "tags": ["视频生成", "快速生成", "多风格"],
            "url": "https://pixverse.ai",
            "pricing": "免费/付费",
            "features": ["快速生成", "多种风格", "社区分享", "API支持"]
        }
    ]

    return new_tools

def get_freetokens():
    """获取免费Token资源"""
    tokens = [
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
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.groq.com",
            "tutorialUrl": "https://console.groq.com/docs"
        },
        {
            "platform": "Google Gemini",
            "tokenAmount": "免费使用",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://aistudio.google.com",
            "tutorialUrl": "https://ai.google.dev/tutorials/rest_quickstart"
        },
        {
            "platform": "Anthropic Claude",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.anthropic.com",
            "tutorialUrl": "https://docs.anthropic.com/zh-CN/docs/get-started"
        },
        {
            "platform": "OpenAI GPT",
            "tokenAmount": "$5新用户",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.openai.com/signup",
            "tutorialUrl": "https://platform.openai.com/docs/quickstart"
        },
        {
            "platform": "Hugging Face",
            "tokenAmount": "免费GPU",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://huggingface.co",
            "tutorialUrl": "https://huggingface.co/docs/hub快速入门"
        }
    ]
    return tokens

def update_tools():
    """更新工具数据"""
    tools_file = '/workspace/data/tools.json'

    with open(tools_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 确保 data 包含必要字段
    if 'tools' not in data or not isinstance(data['tools'], list):
        data['tools'] = []

    new_tools = get_aitools_news()
    existing_ids = {tool['id'] for tool in data['tools']}

    added_count = 0
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            added_count += 1

    # 动态更新 totalCount 和 lastUpdated 字段
    data['totalCount'] = len(data['tools'])
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(tools_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 工具数据已更新，新增 {added_count} 个工具，总计 {data['totalCount']} 个")

def update_tokens():
    """更新Token数据"""
    tokens_file = '/workspace/data/tokens.json'

    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 确保 data 包含必要字段
    if 'tokens' not in data or not isinstance(data['tokens'], list):
        data['tokens'] = []

    new_tokens = get_freetokens()
    existing_platforms = {token['platform'] for token in data['tokens']}

    added_count = 0
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
            added_count += 1

    # 动态更新 totalCount 和 lastUpdated 字段
    data['totalCount'] = len(data['tokens'])
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Token数据已更新，新增 {added_count} 个Token资源，总计 {data['totalCount']} 个")

def git_commit_and_push():
    """提交并推送更改"""
    try:
        # 检查是否有更改
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd='/workspace',
            capture_output=True,
            text=True
        )

        if not result.stdout.strip():
            print("📝 没有需要提交的更改")
            return

        subprocess.run(['git', 'add', 'data/tools.json', 'data/tokens.json'], cwd='/workspace', check=True)
        commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        subprocess.run(['git', 'commit', '-m', commit_message], cwd='/workspace', check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], cwd='/workspace', check=True)
        print("✅ 更改已提交并推送到GitHub")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        raise

def main():
    print("🚀 开始更新AIwork数据...")
    print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    update_tools()
    update_tokens()

    print("-" * 50)
    git_commit_and_push()
    print("✨ 更新完成!")

if __name__ == "__main__":
    main()
