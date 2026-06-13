#!/usr/bin/env python3
"""AIwork 自动更新脚本 - 每日更新 AI 工具和免费 Token 资源。"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from html.parser import HTMLParser


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_FILE = os.path.join(BASE_DIR, 'data', 'tools.json')
TOKENS_FILE = os.path.join(BASE_DIR, 'data', 'tokens.json')

USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'
)


# ============================================================
# HTML 解析工具
# ============================================================
class TextExtractor(HTMLParser):
    """提取 HTML 中的纯文本内容。"""

    def __init__(self):
        super().__init__()
        self.texts = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self._skip_level = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self._skip_level += 1

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self._skip_level > 0:
            self._skip_level -= 1

    def handle_data(self, data):
        if self._skip_level > 0:
            return
        text = data.strip()
        if text:
            self.texts.append(text)

    def get_text(self, separator=' '):
        return separator.join(self.texts)


def fetch_url(url, timeout=15):
    """获取网页内容，失败返回 None。"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            raw = response.read()
            try:
                return raw.decode(charset, errors='ignore')
            except LookupError:
                return raw.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  [WARN] 获取失败 {url}: {e}")
        return None


def fetch_json(url, timeout=15):
    """获取 JSON API 内容。"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': USER_AGENT,
                'Accept': 'application/json',
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read().decode('utf-8', errors='ignore')
            return json.loads(data)
    except Exception as e:
        print(f"  [WARN] JSON 获取失败 {url}: {e}")
        return None


# ============================================================
# AI 工具数据源
# ============================================================
def get_latest_tools_candidates():
    """从多个公开源获取候选 AI 工具信息。

    注意：由于公开 API 通常不稳定或需要鉴权，本函数采用"尽量采集 + 回退
    预设数据"的策略，确保在数据源失败时依然能得到合理的更新结果。
    """
    candidates = []

    # 来源1：尝试从 Alternativeto 的 AI 分类页面解析工具名
    url1 = 'https://alternativeto.net/category/artificial-intelligence/'
    content = fetch_url(url1)
    if content:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()
        ai_keywords = re.findall(
            r'\b([A-Z][a-zA-Z0-9\-]{2,}(?:\s[A-Z][a-zA-Z0-9\-]+){0,2})\b',
            text,
        )
        for kw in list(dict.fromkeys(ai_keywords))[:20]:
            candidates.append({'name': kw, 'source': 'alternativeto'})

    # 来源2：Product Hunt 的 AI 分类
    url2 = 'https://www.producthunt.com/categories/artificial-intelligence'
    content = fetch_url(url2)
    if content:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()
        ph_keywords = re.findall(
            r'\b([A-Z][a-zA-Z0-9\-]{2,}(?:\s[A-Z][a-zA-Z0-9\-]+){0,2})\b',
            text,
        )
        for kw in list(dict.fromkeys(ph_keywords))[:20]:
            candidates.append({'name': kw, 'source': 'producthunt'})

    # 来源3：GitHub Trending（基于趋势判断热度）
    url3 = 'https://github.com/trending?since=daily'
    content = fetch_url(url3)
    if content:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()
        gh_keywords = re.findall(
            r'\b([A-Za-z][a-zA-Z0-9\-]{2,}(?:\s[A-Z][a-zA-Z0-9\-]+){0,2})\b',
            text,
        )
        for kw in list(dict.fromkeys(gh_keywords))[:20]:
            candidates.append({'name': kw, 'source': 'github-trending'})

    print(f"  从网络源共采集到 {len(candidates)} 个候选名称")
    return candidates


# 预设的"最新 AI 工具"候选（作为网络源失败时的回退）
FALLBACK_TOOLS = [
    {
        'id': 'searchgpt',
        'name': 'SearchGPT',
        'category': '搜索',
        'description': 'OpenAI 推出的实时 AI 搜索引擎，提供透明引用和高质量答案。',
        'tags': ['搜索', '实时', '引用'],
        'url': 'https://searchgpt.ai',
        'pricing': '免费/付费',
        'features': ['实时搜索', '源引用', '深度研究', '对话模式'],
    },
    {
        'id': 'grok-3',
        'name': 'Grok 3',
        'category': '聊天',
        'description': 'xAI 第三代大模型，支持实时 X 平台数据检索和深度推理。',
        'tags': ['对话', '实时搜索', '推理'],
        'url': 'https://x.ai',
        'pricing': '免费/付费',
        'features': ['实时搜索', '高速推理', 'X 平台集成', '多模态'],
    },
    {
        'id': 'gemini-2-5',
        'name': 'Gemini 2.5',
        'category': '聊天',
        'description': 'Google 新一代多模态大模型，具备超长上下文和代码生成能力。',
        'tags': ['对话', '多模态', '代码', 'Google'],
        'url': 'https://gemini.google.com',
        'pricing': '免费/付费',
        'features': ['1M 上下文', '多模态理解', '代码生成', 'Agent 能力'],
    },
    {
        'id': 'sora-2',
        'name': 'Sora 2',
        'category': '视频',
        'description': 'OpenAI 第二代视频生成模型，支持更长时长和更高质量视频。',
        'tags': ['视频生成', '文本转视频', 'OpenAI'],
        'url': 'https://openai.com/sora',
        'pricing': '付费',
        'features': ['高清长视频', '物理一致性', '多镜头', '角色保持'],
    },
    {
        'id': 'veo-3',
        'name': 'Google Veo 3',
        'category': '视频',
        'description': 'Google 最新 AI 视频生成模型，支持高质量长视频和可编辑时间轴。',
        'tags': ['视频生成', '国产', '高质量'],
        'url': 'https://deepmind.google/technologies/veo/',
        'pricing': '免费/付费',
        'features': ['长视频生成', '高质量', '可编辑时间轴', '多模态'],
    },
    {
        'id': 'cursor-ai',
        'name': 'Cursor',
        'category': '代码',
        'description': '基于 VS Code 的 AI 代码编辑器，具备强大的代码理解和重构能力。',
        'tags': ['编程', 'AI 代码编辑器', '代码补全'],
        'url': 'https://cursor.sh',
        'pricing': '免费/付费',
        'features': ['AI 代码生成', '智能重构', '项目级理解', '智能 Tab'],
    },
    {
        'id': 'claude-4',
        'name': 'Claude 4',
        'category': '聊天',
        'description': 'Anthropic 最新一代 AI 助手，具备卓越的推理能力和安全对齐。',
        'tags': ['对话', '推理', '安全对齐'],
        'url': 'https://claude.ai',
        'pricing': '免费/付费',
        'features': ['高级推理', '超长上下文', '多模态', '企业安全'],
    },
    {
        'id': 'qwen-3',
        'name': '通义千问 Qwen3',
        'category': '聊天',
        'description': '阿里云通义千问最新一代开源大模型，推理能力媲美顶级闭源模型。',
        'tags': ['对话', '开源', '推理'],
        'url': 'https://tongyi.aliyun.com',
        'pricing': '免费/付费',
        'features': ['强推理', '开源免费', '长上下文', '多语言'],
    },
    {
        'id': 'perplexity-sonar',
        'name': 'Perplexity Sonar',
        'category': '搜索',
        'description': 'Perplexity 新一代实时搜索 AI 模型，提供更深度的研究辅助。',
        'tags': ['搜索', 'AI 问答', '研究'],
        'url': 'https://www.perplexity.ai',
        'pricing': '免费/付费',
        'features': ['深度研究', '实时信息', '源引用', '学术搜索'],
    },
    {
        'id': 'llama-4',
        'name': 'Meta Llama 4',
        'category': '聊天',
        'description': 'Meta 最新开源多模态大模型，具备强大推理和本地部署能力。',
        'tags': ['对话', '开源', '多模态'],
        'url': 'https://llama.meta.com',
        'pricing': '开源免费',
        'features': ['开源', '多模态', '强推理', '本地部署'],
    },
]


def get_aitools_news():
    """综合网络源 + 预设数据，得到最新 AI 工具列表。"""
    candidates = get_latest_tools_candidates()

    # 将候选中的名称规范化并映射到预设库
    matched_ids = set()
    lower_to_id = {
        tool['name'].lower().replace(' ', ''): tool['id']
        for tool in FALLBACK_TOOLS
    }
    for c in candidates:
        key = c['name'].lower().replace(' ', '')
        if key in lower_to_id:
            matched_ids.add(lower_to_id[key])

    # 首先加入网络源匹配到的工具
    result = []
    for tool in FALLBACK_TOOLS:
        if tool['id'] in matched_ids:
            result.append(tool)

    # 如果网络源给出的工具数量不足，则补齐回退数据
    fallback_extra = [t for t in FALLBACK_TOOLS if t['id'] not in matched_ids]
    result.extend(fallback_extra)

    print(f"  最终返回 {len(result)} 个 AI 工具候选")
    return result


# ============================================================
# Token 资源数据源
# ============================================================
def get_tokens_from_network():
    """从网络源尝试获取最新的免费 Token 资源（作为参考信息补充）。

    由于 Token 资源通常需要登录才能获取具体数值，这里主要通过抓取各平台
    首页相关关键词的出现情况来确认平台是否仍然活跃。
    """
    platforms = [
        ('Google Gemini', 'https://aistudio.google.com'),
        ('Groq', 'https://console.groq.com'),
        ('DeepSeek', 'https://platform.deepseek.com'),
        ('Anthropic Claude', 'https://console.anthropic.com'),
        ('OpenAI GPT', 'https://platform.openai.com'),
        ('Mistral AI', 'https://console.mistral.ai'),
        ('Cerebras', 'https://inference.cerebras.ai'),
        ('Hugging Face', 'https://huggingface.co'),
        ('xAI Grok', 'https://x.ai/api'),
        ('NVIDIA NIM', 'https://build.nvidia.com/nim'),
        ('Cloudflare Workers AI', 'https://developers.cloudflare.com/workers-ai'),
        ('GitHub Models', 'https://github.com/marketplace/models'),
        ('阿里云百炼', 'https://bailian.console.aliyun.com'),
        ('火山引擎豆包', 'https://www.volcengine.com/product/doubao'),
        ('SambaNova Cloud', 'https://cloud.sambanova.ai'),
        ('Together AI', 'https://together.ai'),
        ('OpenRouter', 'https://openrouter.ai'),
        ('Cohere', 'https://cohere.com'),
    ]

    active = set()
    for name, url in platforms:
        content = fetch_url(url, timeout=8)
        if content and len(content) > 500:
            active.add(name)
            print(f"    ✓ {name} 在线")
        else:
            print(f"    ⚠ {name} 无法访问")

    return active


FALLBACK_TOKENS = [
    {
        'platform': 'Google Gemini',
        'tokenAmount': '2.5 Pro: 100 req/day, 1M 上下文',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://aistudio.google.com',
        'tutorialUrl': 'https://ai.google.dev/tutorials/rest_quickstart',
    },
    {
        'platform': 'Groq',
        'tokenAmount': 'Llama 3.3 70B: ~500K tokens/天',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://console.groq.com',
        'tutorialUrl': 'https://console.groq.com/docs',
    },
    {
        'platform': 'DeepSeek',
        'tokenAmount': 'R1/V3: ~1M tokens/月',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://platform.deepseek.com',
        'tutorialUrl': 'https://platform.deepseek.com/docs',
    },
    {
        'platform': 'Cerebras',
        'tokenAmount': 'Llama 3.3 70B: ~100K tokens/分钟',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://inference.cerebras.ai',
        'tutorialUrl': 'https://docs.cerebras.ai',
    },
    {
        'platform': 'Mistral AI',
        'tokenAmount': 'Mistral Small 3.1: ~1B tokens/月',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://console.mistral.ai',
        'tutorialUrl': 'https://docs.mistral.ai',
    },
    {
        'platform': 'OpenRouter',
        'tokenAmount': '300+ 模型（含免费层级）',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://openrouter.ai',
        'tutorialUrl': 'https://openrouter.ai/docs',
    },
    {
        'platform': 'Cloudflare Workers AI',
        'tokenAmount': 'Llama 3.3 70B, Flux: 10K neurons/天',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://developers.cloudflare.com/workers-ai',
        'tutorialUrl': 'https://developers.cloudflare.com/workers-ai',
    },
    {
        'platform': 'GitHub Models',
        'tokenAmount': 'GPT-4o, Llama 3.3 70B（开发测试）',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://github.com/marketplace/models',
        'tutorialUrl': 'https://docs.github.com/en/github-models',
    },
    {
        'platform': 'NVIDIA NIM',
        'tokenAmount': 'Llama 3.3 70B, Phi-4: 1000 req/月',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://build.nvidia.com/nim',
        'tutorialUrl': 'https://docs.nvidia.com/nim',
    },
    {
        'platform': '阿里云百炼',
        'tokenAmount': 'Qwen-Max, QwQ-32B: ~2M tokens',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://bailian.console.aliyun.com',
        'tutorialUrl': 'https://help.aliyun.com/zh/model-studio/getting-started',
    },
    {
        'platform': 'SambaNova Cloud',
        'tokenAmount': 'Llama 3.3 70B: 1000 tokens/秒',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://cloud.sambanova.ai',
        'tutorialUrl': 'https://docs.sambanova.ai',
    },
    {
        'platform': 'Cohere',
        'tokenAmount': 'Command R+: 1000 calls/月',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://cohere.com',
        'tutorialUrl': 'https://docs.cohere.com/docs/quick-start',
    },
    {
        'platform': 'Together AI',
        'tokenAmount': '$100 注册赠送 credits',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://together.ai',
        'tutorialUrl': 'https://docs.together.ai',
    },
    {
        'platform': '火山引擎豆包',
        'tokenAmount': '免费 API 调用额度',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://www.volcengine.com/product/doubao',
        'tutorialUrl': 'https://www.volcengine.com/docs/82379',
    },
    {
        'platform': 'xAI Grok',
        'tokenAmount': '$25 注册 + 每月 $150',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://x.ai/api',
        'tutorialUrl': 'https://docs.x.ai',
    },
    {
        'platform': 'Anthropic Claude',
        'tokenAmount': '免费额度',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://console.anthropic.com',
        'tutorialUrl': 'https://docs.anthropic.com/zh-CN/docs/get-started',
    },
    {
        'platform': 'OpenAI GPT',
        'tokenAmount': '$5 新用户',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://platform.openai.com/signup',
        'tutorialUrl': 'https://platform.openai.com/docs/quickstart',
    },
    {
        'platform': 'Hugging Face',
        'tokenAmount': '免费 GPU 推理额度',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://huggingface.co',
        'tutorialUrl': 'https://huggingface.co/docs/hub/quick-start',
    },
]


def get_freetokens():
    """综合网络源在线检测 + 预设数据，返回 Token 列表。"""
    print("  开始检测各 Token 平台在线状态...")
    active = get_tokens_from_network()

    tokens = []
    for t in FALLBACK_TOKENS:
        status = 'active' if t['platform'] in active else 'limited'
        t_copy = dict(t)
        t_copy['status'] = status
        tokens.append(t_copy)

    return tokens


# ============================================================
# JSON 文件读写与更新
# ============================================================
def load_json(filepath, default):
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  [WARN] 读取 {filepath} 失败: {e}")
        return default


def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_tools():
    """更新工具数据文件。"""
    print("\n[1/2] 开始更新 AI 工具数据...")
    data = load_json(TOOLS_FILE, {'lastUpdated': '', 'tools': []})

    new_tools = get_aitools_news()
    existing_ids = {tool['id'] for tool in data.get('tools', [])}

    added = 0
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            added += 1
            existing_ids.add(tool['id'])

    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['totalCount'] = len(data.get('tools', []))
    save_json(TOOLS_FILE, data)

    print(f"  ✅ 工具数据已更新：新增 {added} 个，总计 {data['totalCount']} 个")


def update_tokens():
    """更新 Token 数据文件。"""
    print("\n[2/2] 开始更新免费 Token 数据...")
    data = load_json(TOKENS_FILE, {'lastUpdated': '', 'tokens': []})

    new_tokens = get_freetokens()
    existing_platforms = {token['platform'] for token in data.get('tokens', [])}

    added = 0
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
            added += 1
            existing_platforms.add(token['platform'])

    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['totalCount'] = len(data.get('tokens', []))
    save_json(TOKENS_FILE, data)

    print(f"  ✅ Token 数据已更新：新增 {added} 个，总计 {data['totalCount']} 个")


# ============================================================
# Git 提交与推送
# ============================================================
def git_commit_and_push():
    """将更改提交并推送到远程仓库（如果在 git 仓库中）。"""
    print("\n[Git] 检查是否需要提交更改...")

    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("  [INFO] 未检测到 git，跳过提交步骤")
        return

    if result.returncode != 0 or not result.stdout.strip():
        print("  [INFO] 没有需要提交的更改")
        return

    try:
        subprocess.run(
            ['git', 'config', 'user.name', 'AIwork Bot'],
            cwd=BASE_DIR,
            check=False,
        )
        subprocess.run(
            ['git', 'config', 'user.email', 'aiwork-bot@users.noreply.github.com'],
            cwd=BASE_DIR,
            check=False,
        )
        subprocess.run(
            ['git', 'add', 'data/tools.json', 'data/tokens.json'],
            cwd=BASE_DIR,
            check=True,
        )
        commit_message = (
            f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        )
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=BASE_DIR,
            check=True,
        )
        push_result = subprocess.run(
            ['git', 'push'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )
        if push_result.returncode == 0:
            print("  ✅ 更改已提交并推送到 GitHub")
        else:
            print(f"  [WARN] Git push 返回非零：{push_result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"  [WARN] Git 操作失败: {e}")


# ============================================================
# 主入口
# ============================================================
def main():
    print("=" * 60)
    print("🚀 AIwork 数据自动更新脚本")
    print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        update_tools()
        update_tokens()
        print()
        git_commit_and_push()
        print("\n✨ 数据更新完成！GitHub Pages 将在几分钟内自动重新部署。")
        return 0
    except Exception as e:
        print(f"\n❌ 脚本异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
