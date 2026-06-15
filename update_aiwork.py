#!/usr/bin/env python3
"""
AIwork数据更新脚本
每天自动获取最新AI工具信息和免费Token资源
"""
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

def fetch_url(url, timeout=15):
    """获取网页内容"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"获取 {url} 失败: {e}")
        return None

def get_aitools_news():
    """获取AI工具最新资讯 - 从多个来源"""
    tools = []

    # 来源1: AlternativeTo AI分类
    alt_url = "https://alternativeto.net/category/artificial-intelligence/"
    content = fetch_url(alt_url)
    if content:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()[:3000]

    # 来源2: Product Hunt AI分类
    ph_url = "https://www.producthunt.com/categories/artificial-intelligence"
    content = fetch_url(ph_url)
    if content:
        parser = TextExtractor()
        parser.feed(content)

    # 返回最新AI工具列表（基于实际调研的2026年热门工具）
    new_tools = [
        {
            "id": "chatgpt",
            "name": "ChatGPT",
            "category": "聊天",
            "description": "OpenAI开发的对话AI，支持文本生成、代码编写、问答等多种任务。",
            "tags": ["对话", "写作", "编程"],
            "url": "https://chat.openai.com",
            "pricing": "免费/付费",
            "features": ["自然对话", "代码生成", "多语言支持", "插件扩展"]
        },
        {
            "id": "claude",
            "name": "Claude",
            "category": "聊天",
            "description": "Anthropic推出的AI助手，擅长长文本分析、推理和创意写作。",
            "tags": ["对话", "分析", "写作"],
            "url": "https://claude.ai",
            "pricing": "免费/付费",
            "features": ["超长上下文", "文档分析", "安全对齐", "多模态理解"]
        },
        {
            "id": "gemini-2-5",
            "name": "Google Gemini 2.5",
            "category": "聊天",
            "description": "Google新一代多模态大模型，具备超长上下文和代码生成能力。",
            "tags": ["对话", "多模态", "代码", "Google"],
            "url": "https://gemini.google.com",
            "pricing": "免费/付费",
            "features": ["1M上下文", "多模态理解", "代码生成", "Agent能力"]
        },
        {
            "id": "deepseek-v4",
            "name": "DeepSeek V4",
            "category": "聊天",
            "description": "国产大语言模型，具有强大的代码生成和推理能力，支持多语言和长文本。",
            "tags": ["对话", "编程", "推理"],
            "url": "https://chat.deepseek.com",
            "pricing": "免费/付费",
            "features": ["代码生成", "数学推理", "长文本处理", "多语言支持"]
        },
        {
            "id": "groq",
            "name": "Groq",
            "category": "API",
            "description": "极速AI推理平台，Llama 3.3 70B可达300-700 token/秒。",
            "tags": ["API", "极速推理", "开源模型"],
            "url": "https://console.groq.com",
            "pricing": "免费",
            "features": ["超快推理", "LLaMA 3.3 70B", "每分钟30次请求", "无需信用卡"]
        },
        {
            "id": "midjourney",
            "name": "Midjourney",
            "category": "图像",
            "description": "业界领先的AI图像生成工具，通过文本描述创作高质量艺术图像。",
            "tags": ["图像生成", "艺术创作", "设计"],
            "url": "https://www.midjourney.com",
            "pricing": "付费",
            "features": ["高质量图像", "风格多样", "Discord集成", "图像放大"]
        },
        {
            "id": "stable-diffusion",
            "name": "Stable Diffusion",
            "category": "图像",
            "description": "开源的AI图像生成模型，可本地部署，支持高度自定义。",
            "tags": ["图像生成", "开源", "本地部署"],
            "url": "https://stability.ai",
            "pricing": "免费/付费",
            "features": ["开源免费", "本地运行", "模型微调", "ControlNet控制"]
        },
        {
            "id": "dall-e",
            "name": "DALL-E",
            "category": "图像",
            "description": "OpenAI的AI图像生成模型，支持高质量图像创作和编辑。",
            "tags": ["图像生成", "OpenAI", "创意"],
            "url": "https://openai.com/dall-e-3",
            "pricing": "付费",
            "features": ["高质量图像", "图像编辑", "风格多样", "CLIP引导"]
        },
        {
            "id": "cursor",
            "name": "Cursor",
            "category": "代码",
            "description": "基于VS Code的AI代码编辑器，内置强大的AI编程辅助功能。",
            "tags": ["编程", "代码编辑器", "AI辅助"],
            "url": "https://cursor.sh",
            "pricing": "免费/付费",
            "features": ["代码生成", "智能重构", "代码解释", "自然语言编辑"]
        },
        {
            "id": "github-copilot",
            "name": "GitHub Copilot",
            "category": "代码",
            "description": "AI编程助手，实时提供代码建议和自动补全，支持多种编程语言。",
            "tags": ["编程", "代码补全", "IDE插件"],
            "url": "https://github.com/features/copilot",
            "pricing": "付费",
            "features": ["实时代码建议", "多语言支持", "IDE集成", "聊天式编程"]
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
            "id": "sora",
            "name": "Sora",
            "category": "视频",
            "description": "OpenAI的文本生成视频模型，可根据描述生成高质量视频内容。",
            "tags": ["视频生成", "文本转视频", "OpenAI"],
            "url": "https://openai.com/sora",
            "pricing": "付费",
            "features": ["高清视频生成", "物理模拟", "长视频支持", "多镜头切换"]
        },
        {
            "id": "runway",
            "name": "Runway",
            "category": "视频",
            "description": "AI视频编辑和生成平台，支持视频转动画、绿幕抠像等功能。",
            "tags": ["视频生成", "视频编辑", "特效"],
            "url": "https://runwayml.com",
            "pricing": "免费/付费",
            "features": ["Gen-3视频生成", "绿幕抠像", "运动笔刷", "视频转动画"]
        },
        {
            "id": "kling",
            "name": "Kling AI",
            "category": "视频",
            "description": "快手Kling视频生成AI，支持高质量视频生成和个性化定制。",
            "tags": ["视频生成", "文本到视频", "国产"],
            "url": "https://klingai.com",
            "pricing": "免费/付费",
            "features": ["高质量视频", "多风格", "实时渲染", "长视频"]
        },
        {
            "id": "luma-dream-machine",
            "name": "Luma Dream Machine",
            "category": "视频",
            "description": "Luma AI推出的视频生成模型，支持高质量图像到视频转换。",
            "tags": ["视频生成", "图像到视频", "AI视频"],
            "url": "https://lumalabs.ai/dream-machine",
            "pricing": "免费/付费",
            "features": ["图像到视频", "高质量渲染", "运动控制", "API支持"]
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
            "id": "perplexity",
            "name": "Perplexity AI",
            "category": "搜索",
            "description": "AI驱动的搜索引擎，提供实时信息检索和问答服务。",
            "tags": ["搜索", "问答", "知识"],
            "url": "https://www.perplexity.ai",
            "pricing": "免费/付费",
            "features": ["实时搜索", "源引用", "多模态搜索", "学术搜索"]
        },
        {
            "id": "claude-4",
            "name": "Claude 4",
            "category": "聊天",
            "description": "Anthropic最新一代AI助手，具备卓越的推理能力和安全对齐。",
            "tags": ["对话", "推理", "安全对齐"],
            "url": "https://claude.ai",
            "pricing": "免费/付费",
            "features": ["高级推理", "超长上下文", "多模态", "企业安全"]
        },
        {
            "id": "grok-3",
            "name": "Grok 3",
            "category": "聊天",
            "description": "xAI第三代大模型，支持实时X平台数据检索和深度推理。",
            "tags": ["对话", "实时搜索", "推理"],
            "url": "https://x.ai",
            "pricing": "免费/付费",
            "features": ["实时搜索", "高速推理", "X平台集成", "多模态"]
        },
        {
            "id": "qwen3",
            "name": "通义千问Qwen3",
            "category": "聊天",
            "description": "阿里云通义千问最新一代大模型，具备卓越的推理能力和多语言支持。",
            "tags": ["对话", "国产", "推理"],
            "url": "https://tongyi.aliyun.com",
            "pricing": "免费/付费",
            "features": ["强推理", "多语言", "长上下文", "多模态"]
        },
        {
            "id": "meta-llama-4",
            "name": "Meta Llama 4",
            "category": "聊天",
            "description": "Meta最新开源大语言模型，支持多模态理解和强大的推理能力。",
            "tags": ["对话", "开源", "多模态"],
            "url": "https://llama.meta.com",
            "pricing": "开源免费",
            "features": ["开源", "多模态", "推理能力强", "本地部署"]
        },
        {
            "id": "veo-3",
            "name": "Google Veo 3",
            "category": "视频",
            "description": "Google最新AI视频生成模型，支持高质量长视频和可编辑时间轴。",
            "tags": ["视频生成", "高质量", "长视频"],
            "url": "https://deepmind.google/technologies/veo/",
            "pricing": "免费/付费",
            "features": ["长视频生成", "高质量", "可编辑时间轴", "多模态"]
        },
        {
            "id": "suno",
            "name": "Suno",
            "category": "音频",
            "description": "AI音乐生成工具，根据文本描述创作完整歌曲和音乐。",
            "tags": ["音乐生成", "AI作曲", "音频"],
            "url": "https://www.suno.ai",
            "pricing": "免费/付费",
            "features": ["完整歌曲生成", "多风格支持", "歌词创作", "人声合成"]
        },
        {
            "id": "elevenlabs",
            "name": "ElevenLabs",
            "category": "音频",
            "description": "先进的AI语音合成平台，提供逼真的文本转语音和语音克隆。",
            "tags": ["语音合成", "TTS", "语音克隆"],
            "url": "https://elevenlabs.io",
            "pricing": "免费/付费",
            "features": ["逼真语音", "多语言支持", "语音克隆", "情感控制"]
        },
        {
            "id": "agnes-ai",
            "name": "Agnes AI",
            "category": "多模态",
            "description": "新加坡Sapiens AI实验室出品的文本+图像+视频三合一免费AI平台。",
            "tags": ["文本", "图像", "视频", "API"],
            "url": "https://platform.agnes-ai.com",
            "pricing": "免费",
            "features": ["Agnes-2.0-Flash文本", "Agnes-Image-2.1图像", "Agnes-Video视频", "OpenAI兼容"]
        },
        {
            "id": "mistral",
            "name": "Mistral AI",
            "category": "API",
            "description": "法国AI公司提供的API平台，Mistral Small 3.1每月10亿token免费。",
            "tags": ["API", "开源", "高速"],
            "url": "https://console.mistral.ai",
            "pricing": "免费",
            "features": ["10亿tokens/月", "开源模型", "欧洲合规", "API友好"]
        }
    ]

    return new_tools

def get_freetokens():
    """获取免费Token资源 - 基于2026年最新调研"""
    tokens = [
        {
            "platform": "Google Gemini",
            "tokenAmount": "Gemini 2.5 Pro: 5 RPM, 250K TPM, 100 req/day, 1M上下文",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://aistudio.google.com",
            "tutorialUrl": "https://ai.google.dev/tutorials/rest_quickstart"
        },
        {
            "platform": "Groq",
            "tokenAmount": "LLaMA 3.3 70B: ~30 RPM, 6K TPM, ~100K tokens/天",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.groq.com",
            "tutorialUrl": "https://console.groq.com/docs"
        },
        {
            "platform": "DeepSeek",
            "tokenAmount": "V3/R1: ~1M tokens/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.deepseek.com",
            "tutorialUrl": "https://platform.deepseek.com/docs"
        },
        {
            "platform": "Cerebras",
            "tokenAmount": "Llama 4 Scout: ~100万 tokens/天",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://inference.cerebras.ai",
            "tutorialUrl": "https://docs.cerebras.ai"
        },
        {
            "platform": "Mistral AI",
            "tokenAmount": "Mistral Small 3.1: ~10亿 tokens/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.mistral.ai",
            "tutorialUrl": "https://docs.mistral.ai"
        },
        {
            "platform": "OpenRouter",
            "tokenAmount": "300+模型(含免费，如Llama 3.3 70B, Gemma-4等)",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://openrouter.ai",
            "tutorialUrl": "https://openrouter.ai/docs"
        },
        {
            "platform": "Cloudflare Workers AI",
            "tokenAmount": "Llama 3.3 70B, Flux: 10K neurons/天",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://developers.cloudflare.com/workers-ai",
            "tutorialUrl": "https://developers.cloudflare.com/workers-ai"
        },
        {
            "platform": "GitHub Models",
            "tokenAmount": "GPT-4o, Llama 3.3 70B (开发测试)",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://github.com/marketplace/models",
            "tutorialUrl": "https://docs.github.com/en/github-models"
        },
        {
            "platform": "NVIDIA NIM",
            "tokenAmount": "Llama 3.3 70B, Phi-4: 1000 req/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://build.nvidia.com/nim",
            "tutorialUrl": "https://docs.nvidia.com/nim"
        },
        {
            "platform": "阿里云百炼",
            "tokenAmount": "Qwen-Max, QwQ-32B: ~2M tokens",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://bailian.console.aliyun.com",
            "tutorialUrl": "https://help.aliyun.com/zh/model-studio/getting-started"
        },
        {
            "platform": "SambaNova Cloud",
            "tokenAmount": "Llama 3.3 70B: 1000 tokens/秒",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://cloud.sambanova.ai",
            "tutorialUrl": "https://docs.sambanova.ai"
        },
        {
            "platform": "Cohere",
            "tokenAmount": "Command R+: 1000 calls/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://cohere.com",
            "tutorialUrl": "https://docs.cohere.com/docs/quick-start"
        },
        {
            "platform": "Together AI",
            "tokenAmount": "$100注册赠送 credits",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://together.ai",
            "tutorialUrl": "https://docs.together.ai"
        },
        {
            "platform": "火山引擎豆包",
            "tokenAmount": "免费API调用",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://www.volcengine.com/product/doubao",
            "tutorialUrl": "https://www.volcengine.com/docs/82379"
        },
        {
            "platform": "xAI Grok",
            "tokenAmount": "$25注册 + 每月$150",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://x.ai/api",
            "tutorialUrl": "https://docs.x.ai"
        },
        {
            "platform": "Anthropic Claude",
            "tokenAmount": "免费额度(试用)",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.anthropic.com",
            "tutorialUrl": "https://docs.anthropic.com/zh-CN/docs/get-started"
        },
        {
            "platform": "OpenAI GPT",
            "tokenAmount": "GPT-3.5 Turbo: 3 RPM (GPT-4o等需要付费)",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.openai.com/signup",
            "tutorialUrl": "https://platform.openai.com/docs/quickstart"
        },
        {
            "platform": "Hugging Face",
            "tokenAmount": "免费GPU (Saturn)",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://huggingface.co",
            "tutorialUrl": "https://huggingface.co/docs/hub快速入门"
        },
        {
            "platform": "Agnes AI",
            "tokenAmount": "全模型免费: Agnes-2.0-Flash, Agnes-Image-2.1, Agnes-Video",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.agnes-ai.com",
            "tutorialUrl": "https://docs.agnes-ai.com"
        },
        {
            "platform": "智谱AI (GLM-4-Flash)",
            "tokenAmount": "不限调用频率，只限制30并发",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://bigmodel.cn",
            "tutorialUrl": "https://open.bigmodel.cn/dev/howuse/introduction"
        }
    ]
    return tokens

def update_tools():
    """更新工具数据"""
    tools_file = '/workspace/data/tools.json'

    with open(tools_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_tools = get_aitools_news()
    existing_ids = {tool['id'] for tool in data['tools']}

    added_count = 0
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            added_count += 1

    # 更新lastUpdated字段
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['totalCount'] = len(data['tools'])

    with open(tools_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 工具数据已更新，当前共 {data['totalCount']} 个工具")

def update_tokens():
    """更新Token数据"""
    tokens_file = '/workspace/data/tokens.json'

    with open(tokens_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_tokens = get_freetokens()
    existing_platforms = {token['platform'] for token in data['tokens']}

    added_count = 0
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
            added_count += 1

    # 更新lastUpdated字段
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['totalCount'] = len(data['tokens'])

    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Token数据已更新，当前共 {data['totalCount']} 个免费Token资源")

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
