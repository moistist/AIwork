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
            "id": "mistral",
            "name": "Mistral AI",
            "category": "聊天",
            "description": "法国AI公司开发的高效大语言模型，以速度和性能著称。",
            "tags": ["对话", "高效", "开源"],
            "url": "https://mistral.ai",
            "pricing": "免费/付费",
            "features": ["高效推理", "开源模型", "多语言", "代码生成"]
        },
        {
            "id": "gemini",
            "name": "Google Gemini",
            "category": "聊天",
            "description": "Google开发的多模态AI模型，支持文本、图像、视频和音频处理。",
            "tags": ["多模态", "对话", "Google"],
            "url": "https://gemini.google.com",
            "pricing": "免费/付费",
            "features": ["多模态理解", "实时信息", "代码生成", "多语言"]
        },
        {
            "id": "flux",
            "name": "FLUX",
            "category": "图像",
            "description": "Black Forest Labs开发的高质量图像生成模型，具有出色的真实感和细节。",
            "tags": ["图像生成", "高质量", "开源"],
            "url": "https://blackforestlabs.ai",
            "pricing": "免费/付费",
            "features": ["超高质量", "真实感强", "精细细节", "快速生成"]
        },
        {
            "id": "leptonai",
            "name": "Lepton AI",
            "category": "代码",
            "description": "AI驱动的云原生开发平台，简化AI应用部署和开发流程。",
            "tags": ["开发平台", "云原生", "AI部署"],
            "url": "https://www.lepton.ai",
            "pricing": "免费/付费",
            "features": ["一键部署", "模型托管", "API开发", "自动扩展"]
        },
        {
            "id": "togetherai",
            "name": "Together AI",
            "category": "代码",
            "description": "AI推理和微调平台，支持多种开源模型的快速部署和定制。",
            "tags": ["AI平台", "模型微调", "推理"],
            "url": "https://www.together.ai",
            "pricing": "免费/付费",
            "features": ["快速推理", "模型微调", "多模型支持", "低延迟"]
        },
        {
            "id": "ideogram",
            "name": "Ideogram",
            "category": "图像",
            "description": "AI图像生成工具，特别擅长生成带有文字的图像和设计。",
            "tags": ["图像生成", "文字生成", "设计"],
            "url": "https://ideogram.ai",
            "pricing": "免费/付费",
            "features": ["文字图像", "精准生成", "多种风格", "快速迭代"]
        },
        {
            "id": "hailuo",
            "name": "HeyGen (Hailuo)",
            "category": "视频",
            "description": "AI视频生成平台，支持数字人、口型同步和多语言视频创作。",
            "tags": ["视频生成", "数字人", "口型同步"],
            "url": "https://www.heygen.com",
            "pricing": "免费/付费",
            "features": ["数字人主播", "口型同步", "多语言", "模板丰富"]
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
            "platform": "Mistral AI",
            "tokenAmount": "$5 免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.mistral.ai",
            "tutorialUrl": "https://docs.mistral.ai"
        },
        {
            "platform": "Replicate",
            "tokenAmount": "免费运行模型",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://replicate.com",
            "tutorialUrl": "https://replicate.com/docs"
        },
        {
            "platform": "Together AI",
            "tokenAmount": "$25 免费额度",
            "validityPeriod": "2027-09-01",
            "status": "active",
            "claimUrl": "https://api.together.ai",
            "tutorialUrl": "https://docs.together.ai"
        },
        {
            "platform": "Fireworks AI",
            "tokenAmount": "$30 免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://fireworks.ai",
            "tutorialUrl": "https://readme.fireworks.ai"
        },
        {
            "platform": "Lepton AI",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://www.lepton.ai",
            "tutorialUrl": "https://www.lepton.ai/docs"
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
