#!/usr/bin/env python3
"""AIwork 自动更新脚本。

功能:
  1. 从多个公开的 RSS / JSON 源抓取最新 AI 工具与技术新闻
  2. 基于关键词匹配生成新条目,写入 data/tools.json 与 data/tokens.json
  3. 使用 Git 提交并推送到主分支,触发 GitHub Pages 自动部署

设计原则:
  - 只使用 Python 标准库,无需 pip 安装依赖(便于 GitHub Actions 直接运行)
  - 任何数据源失败都不影响整体流程 (fail-soft)
  - 通过 id / platform 做去重,避免重复写入
"""

import json
import os
import re
import subprocess
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_FILE = os.path.join(BASE_DIR, 'data', 'tools.json')
TOKENS_FILE = os.path.join(BASE_DIR, 'data', 'tokens.json')

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
)

# ---- RSS / JSON 数据源 ---------------------------------------------------
# 这些源均可公开访问,无需 API key。若某源暂时不可用会被跳过。
RSS_SOURCES = [
    {
        'name': 'Hacker News (AI 相关)',
        'url': 'https://hnrss.org/newest?q=ai+OR+llm+OR+machine+learning',
    },
    {
        'name': 'MIT Technology Review - AI',
        'url': 'https://www.technologyreview.com/feed/',
    },
    {
        'name': 'Ars Technica - AI / Tech',
        'url': 'https://feeds.arstechnica.com/arstechnica/technology-lab',
    },
]

JSON_SOURCES = [
    {
        'name': 'dev.to (AI tag)',
        'url': 'https://dev.to/api/articles?tag=ai&per_page=20',
    },
]

AI_KEYWORDS = [
    'AI', 'LLM', 'GPT', 'Claude', 'Gemini', 'Llama', 'DeepSeek', 'Qwen',
    'Model', 'Assistant', 'Copilot', 'Chatbot', 'Agent',
    'Image', 'Video', 'Audio', '3D', 'Generate', 'Diffusion',
    '代码', '编程', '图像', '视频', '语音', '写作', '搜索', '3D',
]

TOKEN_KEYWORDS = [
    'token', 'credit', 'free', 'API', 'quota', '额度', '免费', '赠送',
]

TOKEN_PLATFORMS = {
    'deepseek': {
        'platform': 'DeepSeek',
        'tokenAmount': 'R1/V3: 免费API调用',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://platform.deepseek.com',
        'tutorialUrl': 'https://platform.deepseek.com/docs',
    },
    'groq': {
        'platform': 'Groq',
        'tokenAmount': 'Llama 3.3 70B: ~500K tokens/天',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://console.groq.com',
        'tutorialUrl': 'https://console.groq.com/docs',
    },
    'google': {
        'platform': 'Google Gemini',
        'tokenAmount': '2.5 Pro: 100 req/day',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://aistudio.google.com',
        'tutorialUrl': 'https://ai.google.dev/tutorials/rest_quickstart',
    },
    'anthropic': {
        'platform': 'Anthropic Claude',
        'tokenAmount': '免费额度',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://console.anthropic.com',
        'tutorialUrl': 'https://docs.anthropic.com/zh-CN/docs/get-started',
    },
    'openai': {
        'platform': 'OpenAI GPT',
        'tokenAmount': '$5新用户',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://platform.openai.com/signup',
        'tutorialUrl': 'https://platform.openai.com/docs/quickstart',
    },
    'huggingface': {
        'platform': 'Hugging Face',
        'tokenAmount': '免费GPU推理',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://huggingface.co',
        'tutorialUrl': 'https://huggingface.co/docs/hub快速入门',
    },
    'mistral': {
        'platform': 'Mistral AI',
        'tokenAmount': 'Mistral Small 3.1 免费额度',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://console.mistral.ai',
        'tutorialUrl': 'https://docs.mistral.ai',
    },
    'cerebras': {
        'platform': 'Cerebras',
        'tokenAmount': 'Llama 3.3 70B: 快速推理',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://inference.cerebras.ai',
        'tutorialUrl': 'https://docs.cerebras.ai',
    },
    'openrouter': {
        'platform': 'OpenRouter',
        'tokenAmount': '300+模型(含免费)',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://openrouter.ai',
        'tutorialUrl': 'https://openrouter.ai/docs',
    },
    'nvidia': {
        'platform': 'NVIDIA NIM',
        'tokenAmount': 'Llama 3.3 70B, Phi-4: 1000 req/月',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://build.nvidia.com/nim',
        'tutorialUrl': 'https://docs.nvidia.com/nim',
    },
    'sambanova': {
        'platform': 'SambaNova Cloud',
        'tokenAmount': 'Llama 3.3 70B 免费高速推理',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://cloud.sambanova.ai',
        'tutorialUrl': 'https://docs.sambanova.ai',
    },
    'together': {
        'platform': 'Together AI',
        'tokenAmount': '$100注册赠送 credits',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://together.ai',
        'tutorialUrl': 'https://docs.together.ai',
    },
    'cohere': {
        'platform': 'Cohere',
        'tokenAmount': 'Command R+: 1000 calls/月',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://cohere.com',
        'tutorialUrl': 'https://docs.cohere.com/docs/quick-start',
    },
    'cloudflare': {
        'platform': 'Cloudflare Workers AI',
        'tokenAmount': 'Llama 3.3 70B, Flux: 10K neurons/天',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://developers.cloudflare.com/workers-ai',
        'tutorialUrl': 'https://developers.cloudflare.com/workers-ai',
    },
    'github': {
        'platform': 'GitHub Models',
        'tokenAmount': 'GPT-4o, Llama 3.3 70B (开发测试)',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://github.com/marketplace/models',
        'tutorialUrl': 'https://docs.github.com/en/github-models',
    },
    'bailian': {
        'platform': '阿里云百炼',
        'tokenAmount': 'Qwen-Max, QwQ-32B: ~2M tokens',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://bailian.console.aliyun.com',
        'tutorialUrl': 'https://help.aliyun.com/zh/model-studio/getting-started',
    },
    'doubao': {
        'platform': '火山引擎豆包',
        'tokenAmount': '免费API调用',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://www.volcengine.com/product/doubao',
        'tutorialUrl': 'https://www.volcengine.com/docs/82379',
    },
    'xai': {
        'platform': 'xAI Grok',
        'tokenAmount': '$25注册 + 每月$150',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://x.ai/api',
        'tutorialUrl': 'https://docs.x.ai',
    },
}


# ---- 辅助函数 --------------------------------------------------------------

def fetch_url(url, timeout=15):
    """抓取 URL 内容,失败返回 None 而不中断主流程。"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        print(f"  ⚠️  抓取失败 [{url}]: {exc}")
        return None


def slugify(text):
    """生成英文/数字的简单 slug,用于 id 字段。"""
    text = (text or '').lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:60] or 'item'


def contains_any(text, keywords):
    if not text:
        return False
    lowered = text.lower()
    return any(kw.lower() in lowered for kw in keywords)


def detect_category(title_or_text):
    """根据关键词粗略判断工具类别。"""
    text = (title_or_text or '').lower()
    if any(k in text for k in ('video', '视频', 'pika', 'sora', 'kling', 'vidu', 'runway', 'luma')):
        return '视频'
    if any(k in text for k in ('image', '图像', '图片', 'diffusion', 'midjourney', 'flux')):
        return '图像'
    if any(k in text for k in ('audio', '语音', 'tts', 'suno', 'eleven', '音乐')):
        return '音频'
    if any(k in text for k in ('code', '代码', '编程', 'copilot', 'cursor', '编程助手')):
        return '代码'
    if any(k in text for k in ('search', '搜索', 'perplexity')):
        return '搜索'
    if any(k in text for k in ('3d', 'three')):
        return '3D'
    if any(k in text for k in ('write', '写作', '笔记', 'notion')):
        return '写作'
    return '聊天'


def parse_rss(xml_text):
    """解析 RSS 2.0 / Atom,返回 [{title, link, description, pubDate}]"""
    items = []
    if not xml_text:
        return items
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    # RSS 2.0: <rss><channel><item>
    for item in root.iter('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        desc = (item.findtext('description') or '').strip()
        pub = item.findtext('pubDate') or ''
        if title:
            items.append({'title': title, 'link': link, 'description': desc, 'pubDate': pub})

    # Atom: <feed xmlns="..."><entry>
    atom_ns = 'http://www.w3.org/2005/Atom'
    if not items:
        for entry in root.findall(f'{{{atom_ns}}}entry'):
            title = (entry.findtext(f'{{{atom_ns}}}title') or '').strip()
            link_el = entry.find(f'{{{atom_ns}}}link')
            link = link_el.get('href') if link_el is not None else ''
            desc = (entry.findtext(f'{{{atom_ns}}}summary')
                    or entry.findtext(f'{{{atom_ns}}}content') or '').strip()
            pub = entry.findtext(f'{{{atom_ns}}}updated') or ''
            if title:
                items.append({'title': title, 'link': link, 'description': desc, 'pubDate': pub})
    return items


def parse_devto(json_text):
    items = []
    if not json_text:
        return items
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return items
    for article in data:
        if not isinstance(article, dict):
            continue
        title = article.get('title') or ''
        link = article.get('url') or ''
        desc = article.get('description') or ''
        pub = article.get('published_at') or ''
        if title:
            items.append({'title': title, 'link': link, 'description': desc, 'pubDate': pub})
    return items


# ---- 数据收集 --------------------------------------------------------------

def collect_news_items():
    """抓取所有源并返回统一格式的 items 列表。"""
    items = []
    print(f"[1/3] 正在抓取 RSS/JSON 数据源 (共 {len(RSS_SOURCES) + len(JSON_SOURCES)} 个)...")
    for source in RSS_SOURCES:
        print(f"  - {source['name']}: {source['url']}")
        xml = fetch_url(source['url'])
        parsed = parse_rss(xml)
        print(f"    ✓ 得到 {len(parsed)} 条")
        items.extend(parsed)
        time.sleep(0.5)

    for source in JSON_SOURCES:
        print(f"  - {source['name']}: {source['url']}")
        raw = fetch_url(source['url'])
        parsed = parse_devto(raw)
        print(f"    ✓ 得到 {len(parsed)} 条")
        items.extend(parsed)
        time.sleep(0.5)

    return items


def items_to_tools(items):
    """把新闻条目筛选后转换成 tools.json 的结构。"""
    tools = []
    seen_ids = set()
    for item in items:
        title = item['title']
        text = f"{title} {item.get('description', '')}"
        if not contains_any(text, AI_KEYWORDS):
            continue
        tool_id = slugify(title)
        if tool_id in seen_ids or len(tool_id) < 4:
            continue
        seen_ids.add(tool_id)
        desc = (item.get('description') or title)[:200]
        tools.append({
            'id': tool_id,
            'name': title[:80],
            'category': detect_category(text),
            'description': desc,
            'tags': [detect_category(text)],
            'url': item.get('link', '') or '#',
            'pricing': '免费/付费',
            'features': [title[:50], '来自RSS/JSON聚合', '实时更新'],
        })
    return tools


def items_to_tokens(items):
    """基于新闻中出现的平台关键词,决定是否补充 TOKEN_PLATFORMS 中已知条目。"""
    mentioned_keys = set()
    for item in items:
        text = f"{item['title']} {item.get('description', '')}".lower()
        for key in TOKEN_PLATFORMS:
            if key in text or any(k in text for k in key.split()):
                mentioned_keys.add(key)
    return [TOKEN_PLATFORMS[k] for k in mentioned_keys]


# ---- 读写 JSON ------------------------------------------------------------

def read_json(path):
    if not os.path.exists(path):
        return {'lastUpdated': '', 'tools': []} if 'tools' in path else {'lastUpdated': '', 'tokens': []}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_tools(new_tools):
    data = read_json(TOOLS_FILE)
    data.setdefault('tools', [])
    existing_ids = {t.get('id') for t in data['tools']}
    added = 0
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            existing_ids.add(tool['id'])
            added += 1
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_json(TOOLS_FILE, data)
    print(f"✅ tools.json 已更新,新增 {added} 条 (总计 {len(data['tools'])})")
    return added


def update_tokens(new_tokens):
    data = read_json(TOKENS_FILE)
    data.setdefault('tokens', [])
    existing = {t.get('platform') for t in data['tokens']}
    added = 0
    for token in new_tokens:
        if token['platform'] not in existing:
            data['tokens'].append(token)
            existing.add(token['platform'])
            added += 1
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_json(TOKENS_FILE, data)
    print(f"✅ tokens.json 已更新,新增 {added} 条 (总计 {len(data['tokens'])})")
    return added


# ---- Git 提交推送 ----------------------------------------------------------

def git_commit_and_push():
    """检测 data/*.json 是否有变更,若有则提交到 main 分支并 push。"""
    print('[3/3] Git 提交与推送...')
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain', 'data/tools.json', 'data/tokens.json'],
            cwd=BASE_DIR, capture_output=True, text=True,
        )
        if not result.stdout.strip():
            print('  📝 没有需要提交的更改,跳过推送。')
            return
        subprocess.run(['git', 'add', 'data/tools.json', 'data/tokens.json'],
                       cwd=BASE_DIR, check=True)
        msg = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        subprocess.run(['git', 'commit', '-m', msg], cwd=BASE_DIR, check=True)
        # 兼容分支名: 先尝试 main,再尝试 master
        push_result = subprocess.run(
            ['git', 'push', 'origin', 'main'], cwd=BASE_DIR,
            capture_output=True, text=True,
        )
        if push_result.returncode != 0:
            print('  main 分支推送失败,回退到 master:')
            subprocess.run(['git', 'push', 'origin', 'master'], cwd=BASE_DIR, check=True)
        print('✅ 更改已推送到 GitHub,将触发 GitHub Pages 自动部署。')
    except subprocess.CalledProcessError as exc:
        print(f'❌ Git 操作失败: {exc}')


# ---- 主流程 ---------------------------------------------------------------

def main():
    print('🚀 开始更新 AIwork 数据...')
    print(f'⏰ 当前时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('-' * 60)

    items = collect_news_items()
    print(f'[2/3] 共获取 {len(items)} 条原始条目,开始筛选/写入 JSON...')

    new_tools = items_to_tools(items)
    added_tools = update_tools(new_tools)

    new_tokens = items_to_tokens(items)
    added_tokens = update_tokens(new_tokens)

    print('-' * 60)
    git_commit_and_push()
    print(f'✨ 本轮结束 (tools +{added_tools}, tokens +{added_tokens})')


if __name__ == '__main__':
    main()
