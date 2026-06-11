#!/usr/bin/env python3
"""
AIwork 每日数据更新脚本
- 爬取/汇总最新 AI 工具资讯
- 汇总各平台免费 Token 资源
- 更新 data/tools.json 与 data/tokens.json
- 由 GitHub Actions 在每天早上 7 点自动执行
"""

import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser


# ---------- 路径处理 ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TOOLS_FILE = os.path.join(DATA_DIR, "tools.json")
TOKENS_FILE = os.path.join(DATA_DIR, "tokens.json")


# ---------- 工具函数 ----------
def now_beijing():
    """返回北京时间字符串"""
    tz_beijing = timezone(timedelta(hours=8))
    return datetime.now(tz_beijing).strftime("%Y-%m-%d %H:%M:%S")


def fetch_url(url, timeout=15):
    """简单 HTTP GET，返回 HTML 文本；失败返回 None"""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36 AIwork-Bot/1.0"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            # 尝试多种编码
            for enc in ("utf-8", "gbk", "latin-1"):
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    continue
            return raw.decode("utf-8", errors="ignore")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        print(f"  ⚠️  抓取失败 {url}: {e}")
        return None


class TextExtractor(HTMLParser):
    """轻量 HTML -> 纯文本提取器（丢弃脚本/样式等）"""

    SKIP = {"script", "style", "nav", "footer", "header", "noscript"}

    def __init__(self):
        super().__init__()
        self._buf = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip == 0:
            t = data.strip()
            if t:
                self._buf.append(t)

    def text(self, sep=" "):
        return sep.join(self._buf)


def html_to_text(html):
    if not html:
        return ""
    p = TextExtractor()
    p.feed(html)
    return p.text()


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  ⚠️  读取 {os.path.basename(path)} 失败: {e}，使用默认值")
    return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


# ---------- AI 工具抓取 ----------
def try_scrape_aitools():
    """
    尝试从几个公开的 AI 工具聚合站抓取简要文本信息。
    这些站点经常调整结构，因此这里仅做 "尽力而为" 的抓取，
    真正的新增条目依赖于下方的 curated 列表。
    """
    sources = [
        "https://alternativeto.net/category/artificial-intelligence/",
        "https://www.producthunt.com/categories/artificial-intelligence",
        "https://www.futurepedia.io",
    ]
    results = []
    for url in sources:
        print(f"  · 尝试 {url} ...")
        html = fetch_url(url)
        if html:
            text = html_to_text(html)
            results.append((url, text[:500]))
    return results


def curated_ai_tools():
    """
    人工维护的高质量 AI 工具清单（作为爬虫失败时的可靠来源，
    同时也是站点首次数据填充的基准数据）。
    """
    return [
        {
            "id": "chatgpt",
            "name": "ChatGPT",
            "category": "聊天",
            "description": "OpenAI 开发的对话 AI，支持文本生成、代码编写、问答等多种任务。",
            "tags": ["对话", "写作", "编程"],
            "url": "https://chat.openai.com",
            "pricing": "免费/付费",
            "features": ["自然对话", "代码生成", "多语言支持", "插件扩展"],
        },
        {
            "id": "claude",
            "name": "Claude",
            "category": "聊天",
            "description": "Anthropic 推出的 AI 助手，擅长长文本分析、推理和创意写作。",
            "tags": ["对话", "分析", "写作"],
            "url": "https://claude.ai",
            "pricing": "免费/付费",
            "features": ["超长上下文", "文档分析", "安全对齐", "多模态理解"],
        },
        {
            "id": "gemini",
            "name": "Google Gemini",
            "category": "聊天",
            "description": "Google 推出的多模态 AI 模型，支持文本、图像、音频和视频理解。",
            "tags": ["对话", "多模态", "Google"],
            "url": "https://gemini.google.com",
            "pricing": "免费/付费",
            "features": ["多模态理解", "代码生成", "长上下文", "Google 集成"],
        },
        {
            "id": "deepseek",
            "name": "DeepSeek",
            "category": "聊天",
            "description": "国产大语言模型，具有强大的代码生成和推理能力，支持多语言和长文本。",
            "tags": ["对话", "编程", "推理"],
            "url": "https://chat.deepseek.com",
            "pricing": "免费/付费",
            "features": ["代码生成", "数学推理", "长文本处理", "多语言支持"],
        },
        {
            "id": "grok",
            "name": "Grok",
            "category": "聊天",
            "description": "xAI 推出的 AI 助手，具有实时知识获取和独特的幽默风格。",
            "tags": ["对话", "实时知识", "幽默"],
            "url": "https://x.ai/grok",
            "pricing": "免费/付费",
            "features": ["实时搜索", "幽默对话", "开源模型", "X 平台集成"],
        },
        {
            "id": "qwen3",
            "name": "通义千问 Qwen3",
            "category": "聊天",
            "description": "阿里云通义千问最新一代大模型，具备卓越的推理能力和多语言支持。",
            "tags": ["对话", "国产", "推理"],
            "url": "https://tongyi.aliyun.com",
            "pricing": "免费/付费",
            "features": ["强推理", "多语言", "长上下文", "多模态"],
        },
        {
            "id": "doubao",
            "name": "字节豆包",
            "category": "聊天",
            "description": "字节跳动推出的 AI 助手，支持对话、写作、编程等多种场景。",
            "tags": ["对话", "国产", "多模态"],
            "url": "https://www.doubao.com",
            "pricing": "免费/付费",
            "features": ["智能对话", "AI 搜索", "创作助手", "视频生成"],
        },
        {
            "id": "perplexity",
            "name": "Perplexity AI",
            "category": "搜索",
            "description": "AI 驱动的搜索引擎，提供实时信息检索和问答服务。",
            "tags": ["搜索", "问答", "知识"],
            "url": "https://www.perplexity.ai",
            "pricing": "免费/付费",
            "features": ["实时搜索", "源引用", "多模态搜索", "学术搜索"],
        },
        {
            "id": "cursor",
            "name": "Cursor",
            "category": "代码",
            "description": "基于 VS Code 的 AI 代码编辑器，内置强大的 AI 编程辅助功能。",
            "tags": ["编程", "代码编辑器", "AI 辅助"],
            "url": "https://cursor.sh",
            "pricing": "免费/付费",
            "features": ["代码生成", "智能重构", "代码解释", "自然语言编辑"],
        },
        {
            "id": "github-copilot",
            "name": "GitHub Copilot",
            "category": "代码",
            "description": "AI 编程助手，实时提供代码建议和自动补全。",
            "tags": ["编程", "代码补全", "IDE 插件"],
            "url": "https://github.com/features/copilot",
            "pricing": "付费",
            "features": ["实时代码建议", "多语言支持", "IDE 集成", "聊天式编程"],
        },
        {
            "id": "v0",
            "name": "V0.dev",
            "category": "代码",
            "description": "Vercel 的 AI 前端生成工具，从描述快速构建 UI 组件。",
            "tags": ["前端开发", "UI 生成", "AI 编程"],
            "url": "https://v0.dev",
            "pricing": "免费/付费",
            "features": ["UI 组件生成", "React 组件", "Tailwind CSS", "实时预览"],
        },
        {
            "id": "midjourney",
            "name": "Midjourney",
            "category": "图像",
            "description": "业界领先的 AI 图像生成工具。",
            "tags": ["图像生成", "艺术创作", "设计"],
            "url": "https://www.midjourney.com",
            "pricing": "付费",
            "features": ["高质量图像", "风格多样", "Discord 集成", "图像放大"],
        },
        {
            "id": "stable-diffusion",
            "name": "Stable Diffusion",
            "category": "图像",
            "description": "开源的 AI 图像生成模型，可本地部署。",
            "tags": ["图像生成", "开源", "本地部署"],
            "url": "https://stability.ai",
            "pricing": "免费/付费",
            "features": ["开源免费", "本地运行", "模型微调", "ControlNet 控制"],
        },
        {
            "id": "sora",
            "name": "Sora",
            "category": "视频",
            "description": "OpenAI 的文本生成视频模型。",
            "tags": ["视频生成", "文本到视频", "OpenAI"],
            "url": "https://openai.com/sora",
            "pricing": "付费",
            "features": ["高清视频生成", "物理模拟", "长视频支持", "多镜头切换"],
        },
        {
            "id": "runway",
            "name": "Runway",
            "category": "视频",
            "description": "AI 视频编辑和生成平台。",
            "tags": ["视频生成", "视频编辑", "特效"],
            "url": "https://runwayml.com",
            "pricing": "免费/付费",
            "features": ["视频生成", "绿幕抠像", "运动笔刷", "视频转动画"],
        },
        {
            "id": "luma-dream-machine",
            "name": "Luma Dream Machine",
            "category": "视频",
            "description": "Luma AI 推出的视频生成模型，支持高质量图像到视频转换。",
            "tags": ["视频生成", "图像到视频", "AI 视频"],
            "url": "https://lumalabs.ai/dream-machine",
            "pricing": "免费/付费",
            "features": ["图像到视频", "高质量渲染", "运动控制", "API 支持"],
        },
        {
            "id": "kling",
            "name": "Kling AI",
            "category": "视频",
            "description": "快手 Kling 视频生成 AI，支持高质量视频生成。",
            "tags": ["视频生成", "文本到视频", "国产"],
            "url": "https://kling.ai",
            "pricing": "免费/付费",
            "features": ["高质量视频", "多风格", "实时渲染", "长视频"],
        },
        {
            "id": "pika",
            "name": "Pika",
            "category": "视频",
            "description": "AI 视频生成平台，支持图像动画化。",
            "tags": ["视频生成", "图像动画", "AI 视频"],
            "url": "https://pika.art",
            "pricing": "免费/付费",
            "features": ["图像动画化", "文本生成视频", "视频编辑", "社区模型"],
        },
        {
            "id": "vidu",
            "name": "Vidu",
            "category": "视频",
            "description": "生数科技推出的 AI 视频生成工具，支持中文理解的视频创作。",
            "tags": ["视频生成", "国产", "中文理解"],
            "url": "https://www.vidu.studio",
            "pricing": "免费/付费",
            "features": ["文生视频", "图生视频", "角色一致性", "中文优化"],
        },
        {
            "id": "pixverse",
            "name": "PixVerse",
            "category": "视频",
            "description": "AI 视频生成平台，支持多种风格。",
            "tags": ["视频生成", "快速生成", "多风格"],
            "url": "https://pixverse.ai",
            "pricing": "免费/付费",
            "features": ["快速生成", "多种风格", "社区分享", "API 支持"],
        },
        {
            "id": "elevenlabs",
            "name": "ElevenLabs",
            "category": "音频",
            "description": "先进的 AI 语音合成平台。",
            "tags": ["语音合成", "TTS", "语音克隆"],
            "url": "https://elevenlabs.io",
            "pricing": "免费/付费",
            "features": ["逼真语音", "多语言支持", "语音克隆", "情感控制"],
        },
        {
            "id": "suno",
            "name": "Suno",
            "category": "音频",
            "description": "AI 音乐生成工具。",
            "tags": ["音乐生成", "AI 作曲", "音频"],
            "url": "https://www.suno.ai",
            "pricing": "免费/付费",
            "features": ["完整歌曲生成", "多风格支持", "歌词创作", "人声合成"],
        },
        {
            "id": "meta-llama4",
            "name": "Meta Llama 4",
            "category": "聊天",
            "description": "Meta 最新开源大语言模型。",
            "tags": ["对话", "开源", "多模态"],
            "url": "https://llama.meta.com",
            "pricing": "开源免费",
            "features": ["开源", "多模态", "推理能力强", "本地部署"],
        },
        {
            "id": "imagine-3d",
            "name": "Imagine 3D",
            "category": "3D",
            "description": "AI 驱动的 3D 模型生成工具。",
            "tags": ["3D 生成", "文本到 3D", "游戏开发"],
            "url": "https://www.imagine.art",
            "pricing": "免费/付费",
            "features": ["文本到 3D", "高质量模型", "多种格式", "游戏资产"],
        },
    ]


def curated_tokens():
    """汇总各平台免费 Token/额度信息"""
    return [
        {
            "platform": "Google Gemini",
            "tokenAmount": "2.5 Pro: 100 req/day, 1M 上下文",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://aistudio.google.com",
            "tutorialUrl": "https://ai.google.dev/tutorials/rest_quickstart",
        },
        {
            "platform": "Groq",
            "tokenAmount": "Llama 3.3 70B: ~500K tokens/天",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.groq.com",
            "tutorialUrl": "https://console.groq.com/docs",
        },
        {
            "platform": "DeepSeek",
            "tokenAmount": "R1/V3: ~1M tokens/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.deepseek.com",
            "tutorialUrl": "https://platform.deepseek.com/docs",
        },
        {
            "platform": "Cerebras",
            "tokenAmount": "Llama 3.3 70B: ~100K tokens/分钟",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://inference.cerebras.ai",
            "tutorialUrl": "https://docs.cerebras.ai",
        },
        {
            "platform": "Mistral AI",
            "tokenAmount": "Mistral Small 3.1: ~1B tokens/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.mistral.ai",
            "tutorialUrl": "https://docs.mistral.ai",
        },
        {
            "platform": "OpenRouter",
            "tokenAmount": "300+ 模型(含免费)",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://openrouter.ai",
            "tutorialUrl": "https://openrouter.ai/docs",
        },
        {
            "platform": "Cloudflare Workers AI",
            "tokenAmount": "Llama 3.3 70B, Flux: 10K neurons/天",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://developers.cloudflare.com/workers-ai",
            "tutorialUrl": "https://developers.cloudflare.com/workers-ai",
        },
        {
            "platform": "GitHub Models",
            "tokenAmount": "GPT-4o, Llama 3.3 70B（开发测试）",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://github.com/marketplace/models",
            "tutorialUrl": "https://docs.github.com/en/github-models",
        },
        {
            "platform": "NVIDIA NIM",
            "tokenAmount": "Llama 3.3 70B, Phi-4: 1000 req/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://build.nvidia.com/nim",
            "tutorialUrl": "https://docs.nvidia.com/nim",
        },
        {
            "platform": "阿里云百炼",
            "tokenAmount": "Qwen-Max, QwQ-32B: ~2M tokens",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://bailian.console.aliyun.com",
            "tutorialUrl": "https://help.aliyun.com/zh/model-studio/getting-started",
        },
        {
            "platform": "SambaNova Cloud",
            "tokenAmount": "Llama 3.3 70B: 1000 tokens/秒",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://cloud.sambanova.ai",
            "tutorialUrl": "https://docs.sambanova.ai",
        },
        {
            "platform": "Cohere",
            "tokenAmount": "Command R+: 1000 calls/月",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://cohere.com",
            "tutorialUrl": "https://docs.cohere.com/docs/quick-start",
        },
        {
            "platform": "Together AI",
            "tokenAmount": "$100 注册赠送 credits",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://together.ai",
            "tutorialUrl": "https://docs.together.ai",
        },
        {
            "platform": "火山引擎豆包",
            "tokenAmount": "免费 API 调用",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://www.volcengine.com/product/doubao",
            "tutorialUrl": "https://www.volcengine.com/docs/82379",
        },
        {
            "platform": "xAI Grok",
            "tokenAmount": "$25 注册 + 每月 $150",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://x.ai/api",
            "tutorialUrl": "https://docs.x.ai",
        },
        {
            "platform": "Anthropic Claude",
            "tokenAmount": "免费额度",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://console.anthropic.com",
            "tutorialUrl": "https://docs.anthropic.com/zh-CN/docs/get-started",
        },
        {
            "platform": "OpenAI GPT",
            "tokenAmount": "$5 新用户",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://platform.openai.com/signup",
            "tutorialUrl": "https://platform.openai.com/docs/quickstart",
        },
        {
            "platform": "Hugging Face",
            "tokenAmount": "免费 GPU",
            "validityPeriod": "2027-12-31",
            "status": "active",
            "claimUrl": "https://huggingface.co",
            "tutorialUrl": "https://huggingface.co/docs/hub/quick-start",
        },
    ]


# ---------- 合并逻辑 ----------
def merge_tools(existing, incoming):
    """按 id 去重合并工具列表，新的追加在尾部"""
    seen = {t.get("id") for t in existing if t.get("id")}
    added = 0
    for t in incoming:
        if not t.get("id"):
            continue
        if t["id"] in seen:
            # 若已有同 id，则以新数据覆盖更新
            for i, old in enumerate(existing):
                if old.get("id") == t["id"]:
                    existing[i] = t
                    break
            continue
        existing.append(t)
        seen.add(t["id"])
        added += 1
    return added


def merge_tokens(existing, incoming):
    """按 platform 去重合并 Token 列表"""
    seen = {t.get("platform") for t in existing if t.get("platform")}
    added = 0
    for t in incoming:
        if not t.get("platform"):
            continue
        if t["platform"] in seen:
            for i, old in enumerate(existing):
                if old.get("platform") == t["platform"]:
                    existing[i] = t
                    break
            continue
        existing.append(t)
        seen.add(t["platform"])
        added += 1
    return added


# ---------- 主流程 ----------
def update_tools():
    print("🔍 采集 AI 工具数据 ...")
    try_scrape_aitools()  # 尽力而为，结果不直接落盘

    current = load_json(TOOLS_FILE, {"lastUpdated": "", "tools": []})
    current.setdefault("tools", [])
    added = merge_tools(current["tools"], curated_ai_tools())
    current["lastUpdated"] = now_beijing()
    save_json(TOOLS_FILE, current)
    print(f"   ✅ tools.json 已更新，新增/更新 {added} 项，共 {len(current['tools'])} 个工具")


def update_tokens():
    print("🔑 采集免费 Token 数据 ...")
    current = load_json(TOKENS_FILE, {"lastUpdated": "", "tokens": []})
    current.setdefault("tokens", [])
    added = merge_tokens(current["tokens"], curated_tokens())
    current["lastUpdated"] = now_beijing()
    save_json(TOKENS_FILE, current)
    print(f"   ✅ tokens.json 已更新，新增/更新 {added} 项，共 {len(current['tokens'])} 个平台")


def git_commit_and_push():
    """本地 git 提交推送（仅在本地手动运行时使用；GitHub Actions 中由 workflow 负责）"""
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )
        if not res.stdout.strip():
            print("📝 没有需要提交的更改")
            return
        subprocess.run(["git", "add", "data/tools.json", "data/tokens.json"], cwd=BASE_DIR, check=True)
        msg = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        subprocess.run(["git", "commit", "-m", msg], cwd=BASE_DIR, check=True)
        # 尝试常见的分支名
        for branch in ("main", "master"):
            r = subprocess.run(["git", "push", "origin", branch], cwd=BASE_DIR,
                               capture_output=True, text=True)
            if r.returncode == 0:
                print(f"✅ 更改已推送到 origin/{branch}")
                return
        print("⚠️  Git push 失败（可能未配置仓库或权限）")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        # 不抛异常，保证脚本在 Actions 中仍能正常结束


def main():
    print("🚀 开始更新 AIwork 数据 ...")
    print(f"⏰ 北京时间: {now_beijing()}")
    print(f"📁 工作目录: {BASE_DIR}")
    print("-" * 60)

    try:
        update_tools()
        update_tokens()
    except Exception as e:  # noqa: BLE001
        print(f"❌ 更新过程中出错: {e}")
        sys.exit(1)

    print("-" * 60)

    # 本地手动运行（非 GitHub Actions 环境）时，顺便尝试提交推送
    if not os.environ.get("GITHUB_ACTIONS"):
        git_commit_and_push()

    print("✨ 更新完成!")


if __name__ == "__main__":
    main()
