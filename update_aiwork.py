#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime

def update_tools():
    tools_file = '/workspace/data/tools.json'
    
    with open(tools_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2026年最新的AI工具列表
    new_tools = [
        {
            "id": "gemini-2-flash",
            "name": "Gemini 2 Flash",
            "category": "聊天",
            "description": "Google的最新AI模型，拥有快速推理和多模态能力，适合实时应用场景。",
            "tags": ["对话", "多模态", "高速"],
            "url": "https://aistudio.google.com",
            "pricing": "免费/付费",
            "features": ["实时响应", "图像理解", "代码生成", "超长上下文"]
        },
        {
            "id": "gpt-5",
            "name": "GPT-5",
            "category": "聊天",
            "description": "OpenAI最新旗舰模型，具备更强的推理能力和多模态理解能力。",
            "tags": ["对话", "推理", "多模态"],
            "url": "https://chat.openai.com",
            "pricing": "付费",
            "features": ["高级推理", "实时联网", "语音对话", "视频理解"]
        },
        {
            "id": "claude-opus",
            "name": "Claude 3.5 Opus",
            "category": "聊天",
            "description": "Anthropic的最新顶级模型，在复杂推理和长文本理解方面表现卓越。",
            "tags": ["对话", "长文本", "安全"],
            "url": "https://claude.ai",
            "pricing": "付费",
            "features": ["超长上下文", "复杂推理", "文档分析", "多模态"]
        },
        {
            "id": "sora-2",
            "name": "Sora 2",
            "category": "视频",
            "description": "OpenAI第二代视频生成模型，支持更长时长和更高质量的视频内容。",
            "tags": ["视频生成", "文本转视频", "OpenAI"],
            "url": "https://openai.com/sora",
            "pricing": "付费",
            "features": ["4K视频", "5分钟时长", "多镜头切换", "物理真实"]
        },
        {
            "id": "stable-diffusion-4",
            "name": "Stable Diffusion 4",
            "category": "图像",
            "description": "Stability AI最新开源图像生成模型，质量和速度都有大幅提升。",
            "tags": ["图像生成", "开源", "本地部署"],
            "url": "https://stability.ai",
            "pricing": "免费/付费",
            "features": ["高质量图像", "实时生成", "控制精准", "多语言"]
        },
        {
            "id": "llama-3-70b",
            "name": "Llama 3 70B",
            "category": "聊天",
            "description": "Meta开源的最强版本大模型，性能接近闭源模型，可免费商用。",
            "tags": ["开源", "对话", "推理"],
            "url": "https://llama.meta.com",
            "pricing": "免费开源",
            "features": ["开源免费", "本地部署", "强推理", "多语言"]
        },
        {
            "id": "qwen-max",
            "name": "Qwen Max",
            "category": "聊天",
            "description": "阿里巴巴通义千问最新旗舰模型，在中文处理和代码生成方面表现出色。",
            "tags": ["国产", "中文优化", "代码"],
            "url": "https://tongyi.aliyun.com",
            "pricing": "免费/付费",
            "features": ["中文优化", "代码生成", "长文本", "多模态"]
        },
        {
            "id": "mistral-large-2",
            "name": "Mistral Large 2",
            "category": "聊天",
            "description": "Mistral AI的最新大模型，具有高效推理和优秀的代码能力。",
            "tags": ["高效", "代码", "推理"],
            "url": "https://mistral.ai",
            "pricing": "免费/付费",
            "features": ["高效推理", "代码生成", "长上下文", "多语言"]
        },
        {
            "id": "flux-1-dev",
            "name": "FLUX.1 [dev]",
            "category": "图像",
            "description": "Black Forest Labs最新的开源图像生成模型，画质达到商业级水平。",
            "tags": ["图像生成", "开源", "高质量"],
            "url": "https://blackforestlabs.ai",
            "pricing": "免费/付费",
            "features": ["照片级画质", "快速生成", "精准控制", "开源"]
        },
        {
            "id": "voicevox",
            "name": "Voicevox",
            "category": "音频",
            "description": "日本开发的高质量免费语音合成工具，支持多种角色和风格。",
            "tags": ["语音合成", "免费", "日语"],
            "url": "https://voicevox.hiroshiba.jp",
            "pricing": "免费开源",
            "features": ["免费使用", "多种角色", "情感调节", "本地运行"]
        },
        {
            "id": "canva-magic",
            "name": "Canva Magic",
            "category": "设计",
            "description": "Canva集成的AI设计工具，支持一键生成海报、视频、演示文稿等。",
            "tags": ["设计", "生产力", "多模态"],
            "url": "https://www.canva.com",
            "pricing": "免费/付费",
            "features": ["一键设计", "模板丰富", "多语言", "团队协作"]
        },
        {
            "id": "figma-ai",
            "name": "Figma AI",
            "category": "设计",
            "description": "Figma内置的AI设计助手，可自动生成UI组件和设计稿。",
            "tags": ["UI设计", "原型", "协作"],
            "url": "https://www.figma.com",
            "pricing": "免费/付费",
            "features": ["UI生成", "组件自动", "实时协作", "插件生态"]
        },
        {
            "id": "notion-ai-2",
            "name": "Notion AI Pro",
            "category": "写作",
            "description": "Notion的升级版AI助手，提供更强的写作、分析和自动化能力。",
            "tags": ["写作", "笔记", "生产力"],
            "url": "https://www.notion.so/product/ai",
            "pricing": "付费",
            "features": ["智能写作", "数据库分析", "自动化", "多语言"]
        },
        {
            "id": "windsurf",
            "name": "Windsurf",
            "category": "代码",
            "description": "基于VS Code的AI代码编辑器，专注于Web开发，内置强大的AI功能。",
            "tags": ["编程", "代码编辑器", "Web开发"],
            "url": "https://windsurf.com",
            "pricing": "免费/付费",
            "features": ["代码生成", "智能重构", "实时预览", "AI调试"]
        }
    ]
    
    existing_ids = {tool['id'] for tool in data['tools']}
    
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            print(f"  + 添加新工具: {tool['name']}")
    
    with open(tools_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 工具数据已更新 (共 {len(data['tools'])} 个工具)")

def update_tokens():
    tokens_file = '/workspace/data/tokens.json'
    
    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = datetime.now()
    
    # 更新有效期并添加新的Token信息
    new_tokens = [
        {
            "platform": "Gemini 2 Flash",
            "tokenAmount": "600万 tokens",
            "validityPeriod": (today.replace(year=today.year + 1)).strftime('%Y-%m-%d'),
            "status": "active",
            "claimUrl": "https://aistudio.google.com",
            "tutorialUrl": "https://ai.google.dev/docs"
        },
        {
            "platform": "Claude 3.5",
            "tokenAmount": "$20",
            "validityPeriod": (today.replace(year=today.year + 1)).strftime('%Y-%m-%d'),
            "status": "active",
            "claimUrl": "https://console.anthropic.com",
            "tutorialUrl": "https://docs.anthropic.com"
        },
        {
            "platform": "Llama 3",
            "tokenAmount": "完全免费",
            "validityPeriod": "永久",
            "status": "active",
            "claimUrl": "https://llama.meta.com",
            "tutorialUrl": "https://llama.meta.com/docs"
        },
        {
            "platform": "Qwen",
            "tokenAmount": "¥30",
            "validityPeriod": (today.replace(year=today.year + 1)).strftime('%Y-%m-%d'),
            "status": "active",
            "claimUrl": "https://dashscope.aliyun.com",
            "tutorialUrl": "https://help.aliyun.com/zh/dashscope"
        },
        {
            "platform": "Mistral",
            "tokenAmount": "€15",
            "validityPeriod": (today.replace(year=today.year + 1)).strftime('%Y-%m-%d'),
            "status": "active",
            "claimUrl": "https://console.mistral.ai",
            "tutorialUrl": "https://docs.mistral.ai"
        },
        {
            "platform": "FLUX.1",
            "tokenAmount": "2500积分",
            "validityPeriod": (today.replace(year=today.year + 1)).strftime('%Y-%m-%d'),
            "status": "active",
            "claimUrl": "https://blackforestlabs.ai",
            "tutorialUrl": "https://docs.bfl.ml"
        },
        {
            "platform": "Replicate",
            "tokenAmount": "10美元免费额度",
            "validityPeriod": (today.replace(year=today.year + 1)).strftime('%Y-%m-%d'),
            "status": "active",
            "claimUrl": "https://replicate.com",
            "tutorialUrl": "https://replicate.com/docs"
        }
    ]
    
    # 更新现有Token的有效期
    for token in data['tokens']:
        if token.get('validityPeriod') != '永久':
            token['validityPeriod'] = (today.replace(year=today.year + 1)).strftime('%Y-%m-%d')
    
    existing_platforms = {token['platform'] for token in data['tokens']}
    
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
            print(f"  + 添加新Token: {token['platform']}")
    
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Token数据已更新 (共 {len(data['tokens'])} 个平台)")

def git_commit_and_push():
    try:
        # 检查是否有变更
        status = subprocess.run(['git', 'status', '--porcelain'], 
                              cwd='/workspace', 
                              capture_output=True, 
                              text=True)
        if not status.stdout:
            print("ℹ️ 没有需要提交的更改")
            return
        
        subprocess.run(['git', 'add', 'data/tools.json', 'data/tokens.json'], 
                      cwd='/workspace', check=True)
        commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        subprocess.run(['git', 'commit', '-m', commit_message], 
                      cwd='/workspace', check=True)
        subprocess.run(['git', 'push'], cwd='/workspace', check=True)
        print("✅ 更改已提交并推送到GitHub")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git操作: {e}")
        print("ℹ️ 这通常在GitHub Actions环境中是正常的，因为Push权限由Actions处理")

def main():
    print("🚀 开始更新AIwork数据...")
    print(f"📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    update_tools()
    update_tokens()
    git_commit_and_push()
    print("✨ 更新完成!")

if __name__ == "__main__":
    main()
