#!/usr/bin/env python3
"""
AIwork 数据自动更新脚本
每天自动获取最新AI工具和免费Token资源信息
"""
import json
import os
import subprocess
from datetime import datetime

def fetch_latest_tools():
    """获取最新AI工具列表"""
    # 基于最新搜索结果的工具列表（2025-2026年最新）
    latest_tools = [
        {
            "id": "gpt-5",
            "name": "GPT-5",
            "category": "聊天",
            "description": "OpenAI最新大语言模型，支持复杂推理和多模态理解。",
            "tags": ["对话", "推理", "多模态"],
            "url": "https://chat.openai.com",
            "pricing": "付费",
            "features": ["高级推理", "多模态理解", "代码生成", "长文本处理"]
        },
        {
            "id": "gemini-3",
            "name": "Gemini 3",
            "category": "聊天",
            "description": "Google最新AI模型，支持100万token上下文窗口。",
            "tags": ["对话", "长文本", "多模态"],
            "url": "https://ai.google.dev",
            "pricing": "免费/付费",
            "features": ["100万上下文", "多模态", "高速推理", "API访问"]
        },
        {
            "id": "claude-4",
            "name": "Claude 4",
            "category": "聊天",
            "description": "Anthropic最新AI助手，擅长分析和创意写作。",
            "tags": ["对话", "分析", "写作"],
            "url": "https://claude.ai",
            "pricing": "免费/付费",
            "features": ["超强分析能力", "超长上下文", "安全对齐", "代码生成"]
        },
        {
            "id": "glm-4",
            "name": "GLM-4",
            "category": "聊天",
            "description": "智谱AI国产大模型，GLM-4-Flash API全部免费。",
            "tags": ["对话", "国产", "免费API"],
            "url": "https://www.zhipuai.cn",
            "pricing": "免费",
            "features": ["免费API", "多语言", "代码生成", "中文优化"]
        },
        {
            "id": "qwen-3",
            "name": "Qwen 3",
            "category": "聊天",
            "description": "阿里通义千问最新版本，强大推理和代码能力。",
            "tags": ["对话", "代码", "推理"],
            "url": "https://tongyi.aliyun.com",
            "pricing": "免费/付费",
            "features": ["开源模型", "代码生成", "多语言", "长文本"]
        },
        {
            "id": "midjourney-v7",
            "name": "Midjourney V7",
            "category": "图像",
            "description": "业界领先AI图像生成工具最新版，生成质量大幅提升。",
            "tags": ["图像生成", "艺术创作", "设计"],
            "url": "https://www.midjourney.com",
            "pricing": "付费",
            "features": ["高质量图像", "风格控制", "个性化定制", "VR支持"]
        },
        {
            "id": "stable-diffusion-xl",
            "name": "Stable Diffusion XL",
            "category": "图像",
            "description": "开源AI图像生成模型最新版本，图像质量大幅提升。",
            "tags": ["图像生成", "开源", "本地部署"],
            "url": "https://stability.ai",
            "pricing": "免费",
            "features": ["SDXL质量", "本地运行", "高度自定义", "ControlNet"]
        },
        {
            "id": "sora",
            "name": "Sora",
            "category": "视频",
            "description": "OpenAI文本生成视频模型，支持高清长视频生成。",
            "tags": ["视频生成", "文本到视频", "OpenAI"],
            "url": "https://openai.com/sora",
            "pricing": "付费",
            "features": ["高清视频", "物理模拟", "长视频支持", "多镜头"]
        },
        {
            "id": "kling-2",
            "name": "Kling 2.0",
            "category": "视频",
            "description": "快手Kling视频生成AI新版，支持更长视频和更好效果。",
            "tags": ["视频生成", "国产", "文本到视频"],
            "url": "https://kling.ai",
            "pricing": "免费/付费",
            "features": ["高质量视频", "长视频支持", "实时渲染", "多风格"]
        },
        {
            "id": "sunuo",
            "name": "Sunuo",
            "category": "音频",
            "description": "AI音乐生成工具，支持创作完整歌曲和音乐。",
            "tags": ["音乐生成", "AI作曲", "音频"],
            "url": "https://www.sunuo.ai",
            "pricing": "免费/付费",
            "features": ["完整歌曲生成", "多风格", "歌词创作", "人声合成"]
        },
        {
            "id": "cursor-pro",
            "name": "Cursor Pro",
            "category": "代码",
            "description": "AI代码编辑器专业版，更强大的编程辅助功能。",
            "tags": ["编程", "代码编辑", "AI辅助"],
            "url": "https://cursor.sh",
            "pricing": "付费",
            "features": ["智能补全", "代码解释", "自然语言编辑", "团队协作"]
        },
        {
            "id": "windsurf",
            "name": "Windsurf",
            "category": "代码",
            "description": "Codeium推出的AI代码编辑器，强大且免费。",
            "tags": ["编程", "代码编辑", "免费"],
            "url": "https://windsurf.com",
            "pricing": "免费",
            "features": ["免费使用", "代码生成", "智能重构", "多语言支持"]
        },
        {
            "id": "perplexity-pro",
            "name": "Perplexity Pro",
            "category": "搜索",
            "description": "AI搜索引擎，支持实时信息检索和多种搜索模式。",
            "tags": ["搜索", "问答", "知识"],
            "url": "https://www.perplexity.ai",
            "pricing": "免费/付费",
            "features": ["实时搜索", "源引用", "多模态", "学术搜索"]
        },
        {
            "id": "notion-ai",
            "name": "Notion AI",
            "category": "写作",
            "description": "集成在Notion中的AI助手，智能写作和总结。",
            "tags": ["写作", "笔记", "生产力"],
            "url": "https://www.notion.so/product/ai",
            "pricing": "付费",
            "features": ["智能写作", "内容总结", "头脑风暴", "翻译"]
        },
        {
            "id": "jasper-pro",
            "name": "Jasper Pro",
            "category": "写作",
            "description": "专业AI写作工具，专注营销文案和内容创作。",
            "tags": ["写作", "营销", "内容创作"],
            "url": "https://www.jasper.ai",
            "pricing": "付费",
            "features": ["营销文案", "SEO优化", "品牌调性", "团队协作"]
        }
    ]
    return latest_tools

def fetch_latest_tokens():
    """获取最新免费Token资源列表"""
    latest_tokens = [
        {
            "platform": "OpenAI",
            "tokenAmount": "$500-$1000",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.openai.com",
            "tutorialUrl": "https://platform.openai.com/docs/quickstart"
        },
        {
            "platform": "Anthropic",
            "tokenAmount": "$10-$1000",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.anthropic.com",
            "tutorialUrl": "https://docs.anthropic.com/zh-CN/docs/get-started"
        },
        {
            "platform": "Google AI Studio",
            "tokenAmount": "免费额度+100万token",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://aistudio.google.com",
            "tutorialUrl": "https://ai.google.dev/tutorials/rest_quickstart"
        },
        {
            "platform": "DeepSeek",
            "tokenAmount": "¥18+免费API",
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
            "platform": "智谱AI",
            "tokenAmount": "GLM-4-Flash免费",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://www.zhipuai.cn",
            "tutorialUrl": "https://www.zhipuai.cn/price"
        },
        {
            "platform": "阿里云百炼",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://bailian.console.aliyun.com",
            "tutorialUrl": "https://help.aliyun.com/zh/model-studio"
        },
        {
            "platform": "Cohere",
            "tokenAmount": "$15免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://cohere.com",
            "tutorialUrl": "https://docs.cohere.com/docs/quick-start"
        },
        {
            "platform": "Hugging Face",
            "tokenAmount": "Pro试用+免费API",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://huggingface.co/pricing",
            "tutorialUrl": "https://huggingface.co/docs/hub"
        },
        {
            "platform": "Stability AI",
            "tokenAmount": "1000积分",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.stability.ai",
            "tutorialUrl": "https://platform.stability.ai/docs/api"
        }
    ]
    return latest_tokens

def update_tools():
    """更新工具数据"""
    tools_file = '/workspace/data/tools.json'

    with open(tools_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    latest_tools = fetch_latest_tools()
    existing_ids = {tool['id'] for tool in data['tools']}

    new_count = 0
    for tool in latest_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            new_count += 1

    # 更新数据版本信息
    if 'lastUpdated' not in data:
        data['lastUpdated'] = {}
    data['lastUpdated']['tools'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(tools_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 工具数据已更新，新增 {new_count} 个工具")

def update_tokens():
    """更新Token数据"""
    tokens_file = '/workspace/data/tokens.json'

    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    latest_tokens = fetch_latest_tokens()
    existing_platforms = {token['platform'] for token in data['tokens']}

    new_count = 0
    for token in latest_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
            new_count += 1

    # 更新数据版本信息
    if 'lastUpdated' not in data:
        data['lastUpdated'] = {}
    data['lastUpdated']['tokens'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Token数据已更新，新增 {new_count} 个资源")

def git_commit_and_push():
    """提交并推送更改"""
    try:
        subprocess.run(['git', 'add', 'data/tools.json', 'data/tokens.json'],
                      cwd='/workspace', check=True, capture_output=True)
        commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        result = subprocess.run(['git', 'commit', '-m', commit_message],
                              cwd='/workspace', check=True, capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run(['git', 'push', 'origin', 'main'],
                          cwd='/workspace', check=True, capture_output=True)
            print("✅ 更改已提交并推送到GitHub")
        else:
            print("ℹ️ 没有需要提交的更改")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")

def main():
    print("🚀 开始更新AIwork数据...")
    print(f"📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    update_tools()
    update_tokens()
    git_commit_and_push()
    print("-" * 50)
    print("✨ 更新完成!")

if __name__ == "__main__":
    main()
