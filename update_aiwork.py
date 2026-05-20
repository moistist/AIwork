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
            "id": "gemini",
            "name": "Google Gemini",
            "category": "聊天",
            "description": "Google开发的多模态AI模型，支持文本、图像、视频和代码理解。",
            "tags": ["对话", "多模态", "编程"],
            "url": "https://gemini.google.com",
            "pricing": "免费/付费",
            "features": ["多模态", "代码生成", "数学推理", "长文本处理"]
        },
        {
            "id": "mistral",
            "name": "Mistral AI",
            "category": "聊天",
            "description": "高效开源的大语言模型，提供快速响应和出色的推理能力。",
            "tags": ["对话", "开源", "推理"],
            "url": "https://chat.mistral.ai",
            "pricing": "免费/付费",
            "features": ["快速响应", "开源模型", "代码生成", "多语言支持"]
        },
        {
            "id": "heygen",
            "name": "HeyGen",
            "category": "视频",
            "description": "AI数字人视频生成平台，支持文本驱动的虚拟人视频制作。",
            "tags": ["数字人", "视频生成", "AIGC"],
            "url": "https://www.heygen.com",
            "pricing": "免费/付费",
            "features": ["数字人视频", "文本到视频", "多语言支持", "实时渲染"]
        },
        {
            "id": "d-id",
            "name": "D-ID",
            "category": "视频",
            "description": "AI视频生成平台，专注于人脸动画和实时数字人创建。",
            "tags": ["人脸动画", "数字人", "视频生成"],
            "url": "https://d-id.com",
            "pricing": "免费/付费",
            "features": ["人脸动画", "文本驱动", "多语言", "实时处理"]
        },
        {
            "id": "ideogram",
            "name": "Ideogram",
            "category": "图像",
            "description": "AI图像生成工具，擅长文字渲染和创意设计。",
            "tags": ["图像生成", "文字渲染", "设计"],
            "url": "https://ideogram.ai",
            "pricing": "免费/付费",
            "features": ["文字渲染", "高质量图像", "创意设计", "风格多样"]
        },
        {
            "id": "leptonai",
            "name": "Lepton AI",
            "category": "代码",
            "description": "AI应用开发平台，提供快速部署和托管AI模型的服务。",
            "tags": ["AI部署", "云服务", "开发"],
            "url": "https://www.lepton.ai",
            "pricing": "免费/付费",
            "features": ["一键部署", "多模型支持", "API托管", "低代码开发"]
        },
        {
            "id": "replicate",
            "name": "Replicate",
            "category": "代码",
            "description": "开源AI模型托管和运行平台，支持各种机器学习模型。",
            "tags": ["AI托管", "开源模型", "API"],
            "url": "https://replicate.com",
            "pricing": "免费/付费",
            "features": ["模型托管", "API访问", "开源模型", "按需付费"]
        },
        {
            "id": "huggingface",
            "name": "Hugging Face",
            "category": "代码",
            "description": "AI模型社区和平台，提供丰富的预训练模型和工具。",
            "tags": ["模型库", "社区", "开源"],
            "url": "https://huggingface.co",
            "pricing": "免费/付费",
            "features": ["预训练模型", "开源社区", "Transformers库", "模型推理"]
        },
        {
            "id": "udio",
            "name": "Udio",
            "category": "音频",
            "description": "AI音乐生成工具，根据文本描述生成各种风格的音乐。",
            "tags": ["音乐生成", "AI作曲", "音频"],
            "url": "https://www.udio.com",
            "pricing": "免费/付费",
            "features": ["音乐生成", "多风格支持", "人声合成", "音乐编辑"]
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
    
    new_tokens = [
        {
            "platform": "Google Gemini",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://aistudio.google.com",
            "tutorialUrl": "https://ai.google.dev/docs"
        },
        {
            "platform": "Mistral AI",
            "tokenAmount": "免费试用",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://console.mistral.ai",
            "tutorialUrl": "https://docs.mistral.ai"
        },
        {
            "platform": "Ideogram",
            "tokenAmount": "免费生成",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://ideogram.ai",
            "tutorialUrl": "https://help.ideogram.ai"
        },
        {
            "platform": "Lepton AI",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://www.lepton.ai",
            "tutorialUrl": "https://www.lepton.ai/docs"
        },
        {
            "platform": "Replicate",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-06-01",
            "status": "active",
            "claimUrl": "https://replicate.com",
            "tutorialUrl": "https://replicate.com/docs"
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
        status_result = subprocess.run(['git', 'status', '--porcelain'], cwd='/workspace', capture_output=True, text=True)
        if status_result.stdout.strip():
            commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd='/workspace', check=True)
            # 使用GitHub Actions提供的token进行推送
            github_token = os.getenv('GITHUB_TOKEN')
            if github_token:
                # 修改remote URL以包含token
                subprocess.run(['git', 'remote', 'set-url', 'origin', f'https://x-access-token:{github_token}@github.com/{os.getenv("GITHUB_REPOSITORY", "")}.git'], cwd='/workspace', check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], cwd='/workspace', check=True)
            print("✅ 更改已提交并推送到GitHub")
        else:
            print("ℹ️ 没有新的更改需要提交")
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
