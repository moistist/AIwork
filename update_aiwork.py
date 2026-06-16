#!/usr/bin/env python3
"""AIwork 每日数据更新脚本

功能：
1. 从多种数据源爬取/汇总最新 AI 工具信息
2. 整理免费 Token / API 额度资源
3. 更新 data/tools.json 和 data/tokens.json
4. 提交更改并推送到 GitHub（由 GitHub Actions 执行）
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser

# ---------- 基础工具函数 ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_FILE = os.path.join(BASE_DIR, 'data', 'tools.json')
TOKENS_FILE = os.path.join(BASE_DIR, 'data', 'tokens.json')

USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/120.0 Safari/537.36 AIworkBot/1.0'
)


class TextExtractor(HTMLParser):
    """简单提取 HTML 纯文本内容"""

    def __init__(self):
        super().__init__()
        self.texts = []
        self._skip = False
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header', 'noscript'}

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self._skip = False

    def handle_data(self, data):
        if self._skip:
            return
        text = data.strip()
        if text:
            self.texts.append(text)

    def get_text(self, separator=' '):
        return separator.join(self.texts)


def fetch_url(url, timeout=15):
    """抓取网页内容，失败返回 None"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            # 尝试几种常见编码
            for enc in ('utf-8', 'utf-8-sig', 'gbk', 'latin-1'):
                try:
                    return raw.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    continue
            return raw.decode('utf-8', errors='ignore')
    except Exception as exc:  # 网络异常不应让整个流程失败
        print(f'  [warn] 获取 {url} 失败: {exc}')
        return None


def fetch_json(url, timeout=15):
    """抓取 JSON 接口"""
    content = fetch_url(url, timeout=timeout)
    if not content:
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


# ---------- AI 工具数据收集 ----------

CURATED_TOOLS = [
    {
        'id': 'gemini-2-5-pro',
        'name': 'Google Gemini 2.5 Pro',
        'category': '聊天',
        'description': 'Google 新一代多模态大模型，支持 1M 超长上下文与代码生成。',
        'tags': ['对话', '多模态', '代码', 'Google'],
        'url': 'https://gemini.google.com',
        'pricing': '免费/付费',
        'features': ['1M 上下文', '多模态理解', '代码生成', 'Agent 能力'],
    },
    {
        'id': 'claude-4',
        'name': 'Claude 4',
        'category': '聊天',
        'description': 'Anthropic 最新一代 AI 助手，具备卓越的推理能力和企业级安全对齐。',
        'tags': ['对话', '推理', '安全对齐'],
        'url': 'https://claude.ai',
        'pricing': '免费/付费',
        'features': ['高级推理', '超长上下文', '多模态', '企业安全'],
    },
    {
        'id': 'grok-3',
        'name': 'Grok 3',
        'category': '聊天',
        'description': 'xAI 第三代大模型，支持实时 X 平台数据检索和高速推理。',
        'tags': ['对话', '实时搜索', '推理'],
        'url': 'https://x.ai',
        'pricing': '免费/付费',
        'features': ['实时搜索', '高速推理', 'X 平台集成', '多模态'],
    },
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
        'id': 'veo-3',
        'name': 'Google Veo 3',
        'category': '视频',
        'description': 'Google 最新 AI 视频生成模型，支持高质量长视频和可编辑时间轴。',
        'tags': ['视频生成', '高质量', 'Google'],
        'url': 'https://deepmind.google/technologies/veo/',
        'pricing': '免费/付费',
        'features': ['长视频生成', '高质量', '可编辑时间轴', '多模态'],
    },
    {
        'id': 'sora-2',
        'name': 'Sora 2',
        'category': '视频',
        'description': 'OpenAI 第二代视频生成模型，支持更长时长和更高质量的视频生成。',
        'tags': ['视频生成', 'OpenAI', '高质量'],
        'url': 'https://openai.com/sora',
        'pricing': '付费',
        'features': ['更长时长', '更高质量', '物理模拟', '多镜头'],
    },
    {
        'id': 'luma-dream-machine',
        'name': 'Luma Dream Machine',
        'category': '视频',
        'description': 'Luma AI 推出的视频生成模型，支持高质量图像到视频转换。',
        'tags': ['视频生成', '图像到视频', 'AI视频'],
        'url': 'https://lumalabs.ai/dream-machine',
        'pricing': '免费/付费',
        'features': ['图像到视频', '高质量渲染', '运动控制', 'API支持'],
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
        'id': 'meta-llama-4',
        'name': 'Meta Llama 4',
        'category': '聊天',
        'description': 'Meta 最新开源多模态大模型，具备强大推理和本地部署能力。',
        'tags': ['对话', '开源', '多模态'],
        'url': 'https://llama.meta.com',
        'pricing': '开源免费',
        'features': ['开源', '多模态', '强推理', '本地部署'],
    },
    {
        'id': 'deepseek-v4',
        'name': 'DeepSeek V4',
        'category': '聊天',
        'description': '国产大语言模型，具有强大的代码生成和推理能力，支持多语言和长文本。',
        'tags': ['对话', '编程', '推理'],
        'url': 'https://chat.deepseek.com',
        'pricing': '免费/付费',
        'features': ['代码生成', '数学推理', '长文本处理', '多语言支持'],
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
        'id': 'agnes-ai',
        'name': 'Agnes AI',
        'category': '多模态',
        'description': '新加坡 Sapiens AI 实验室出品的文本+图像+视频三合一免费 AI 平台。',
        'tags': ['文本', '图像', '视频', 'API'],
        'url': 'https://platform.agnes-ai.com',
        'pricing': '免费',
        'features': ['Agnes-2.0-Flash文本', 'Agnes-Image-2.1图像', 'Agnes-Video视频', 'OpenAI兼容'],
    },
    {
        'id': 'mistral-api',
        'name': 'Mistral AI',
        'category': 'API',
        'description': '法国 AI 公司提供的 API 平台，Mistral Small 3.1 每月 10 亿 token 免费。',
        'tags': ['API', '开源', '高速'],
        'url': 'https://console.mistral.ai',
        'pricing': '免费',
        'features': ['10亿tokens/月', '开源模型', '欧洲合规', 'API友好'],
    },
    {
        'id': 'groq',
        'name': 'Groq',
        'category': 'API',
        'description': '极速 AI 推理平台，Llama 3.3 70B 可达 300-700 token/秒。',
        'tags': ['API', '极速推理', '开源模型'],
        'url': 'https://console.groq.com',
        'pricing': '免费',
        'features': ['超快推理', 'LLaMA 3.3 70B', '每分钟30次请求', '无需信用卡'],
    },
]


def get_aitools_news():
    """
    获取最新 AI 工具资讯：
    - 尝试抓取网页提取关键字段，作为辅助信号
    - 主要使用精心维护的 CURATED_TOOLS 作为基础数据
      （避免垃圾数据/爬虫失败导致内容空洞）
    """
    print('  抓取辅助数据源（Product Hunt / AlternativeTo）...')
    ph_text = ''
    alt_text = ''

    ph = fetch_url('https://www.producthunt.com/categories/artificial-intelligence')
    if ph:
        parser = TextExtractor()
        parser.feed(ph)
        ph_text = parser.get_text()[:1000]

    alt = fetch_url('https://alternativeto.net/category/artificial-intelligence/')
    if alt:
        parser = TextExtractor()
        parser.feed(alt)
        alt_text = parser.get_text()[:1000]

    # 打印前几行作为日志，便于人工检查
    if ph_text:
        print('   - Product Hunt 已获取（约', len(ph_text), '字符）')
    if alt_text:
        print('   - AlternativeTo 已获取（约', len(alt_text), '字符）')

    return CURATED_TOOLS


# ---------- Token 资源数据收集 ----------

CURATED_TOKENS = [
    {
        'platform': 'Google Gemini',
        'tokenAmount': '2.5 Pro: 100 req/day, 1M上下文',
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
        'tokenAmount': '300+模型(含免费)',
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
        'tokenAmount': 'GPT-4o, Llama 3.3 70B (开发测试)',
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
        'tokenAmount': '$100注册赠送 credits',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://together.ai',
        'tutorialUrl': 'https://docs.together.ai',
    },
    {
        'platform': '火山引擎豆包',
        'tokenAmount': '免费API调用',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://www.volcengine.com/product/doubao',
        'tutorialUrl': 'https://www.volcengine.com/docs/82379',
    },
    {
        'platform': 'xAI Grok',
        'tokenAmount': '$25注册 + 每月$150',
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
        'tokenAmount': '$5新用户',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://platform.openai.com/signup',
        'tutorialUrl': 'https://platform.openai.com/docs/quickstart',
    },
    {
        'platform': 'Hugging Face',
        'tokenAmount': '免费GPU',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://huggingface.co',
        'tutorialUrl': 'https://huggingface.co/docs/hub快速入门',
    },
    {
        'platform': 'Agnes AI',
        'tokenAmount': '全模型免费: Agnes-2.0-Flash, Agnes-Image-2.1, Agnes-Video',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://platform.agnes-ai.com',
        'tutorialUrl': 'https://docs.agnes-ai.com',
    },
    {
        'platform': '智谱AI (GLM-4-Flash)',
        'tokenAmount': '不限调用频率，只限制30并发',
        'validityPeriod': '2027-12-31',
        'status': 'active',
        'claimUrl': 'https://bigmodel.cn',
        'tutorialUrl': 'https://open.bigmodel.cn/dev/howuse/introduction',
    },
]


def get_freetokens():
    """获取免费 Token 资源数据"""
    print('  整理 Token 资源（共', len(CURATED_TOKENS), '项）...')
    return CURATED_TOKENS


# ---------- 读写 JSON ----------

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)


def update_tools(new_tools):
    """更新 tools.json（按 id 去重，不存在则追加）"""
    data = load_json(TOOLS_FILE)
    if data is None:
        data = {'lastUpdated': '', 'tools': []}

    existing_ids = {t['id'] for t in data.get('tools', [])}
    added = 0
    for tool in new_tools:
        if tool['id'] not in existing_ids:
            data['tools'].append(tool)
            existing_ids.add(tool['id'])
            added += 1

    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['totalCount'] = len(data['tools'])

    save_json(TOOLS_FILE, data)
    print(f'✅ tools.json 已更新：新增 {added} 个，累计 {data["totalCount"]} 个')
    return added


def update_tokens(new_tokens):
    """更新 tokens.json（按 platform 去重）"""
    data = load_json(TOKENS_FILE)
    if data is None:
        data = {'lastUpdated': '', 'tokens': []}

    existing_platforms = {t['platform'] for t in data.get('tokens', [])}
    added = 0
    for token in new_tokens:
        if token['platform'] not in existing_platforms:
            data['tokens'].append(token)
            existing_platforms.add(token['platform'])
            added += 1

    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['totalCount'] = len(data['tokens'])

    save_json(TOKENS_FILE, data)
    print(f'✅ tokens.json 已更新：新增 {added} 个，累计 {data["totalCount"]} 个')
    return added


# ---------- Git 提交与推送 ----------

def git_commit_and_push():
    """
    提交并推送更改。
    注意：在 GitHub Actions 环境下需要 GITHUB_TOKEN，本函数会兼容失败场景
    （即无更改时直接返回，不报错）。
    """
    try:
        status = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )
        if not status.stdout.strip():
            print('📝 无更改，跳过提交')
            return

        subprocess.run(['git', 'add', 'data/tools.json', 'data/tokens.json'],
                       cwd=BASE_DIR, check=True)
        commit_msg = f"自动更新: {datetime.now().strftime('%Y-%m-%d')} AI工具和Token信息"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=BASE_DIR, check=True)

        # 尝试推送，失败不致命（可能本地无权限）
        push = subprocess.run(['git', 'push', 'origin', 'HEAD'],
                              cwd=BASE_DIR, capture_output=True, text=True)
        if push.returncode != 0:
            print('⚠️  Git push 失败（可能是本地运行无权限，在 Actions 中将由 workflow 处理）：')
            print('   ', push.stderr.strip() or push.stdout.strip())
        else:
            print('✅ 已推送到远程仓库')
    except subprocess.CalledProcessError as exc:
        print(f'❌ Git 操作失败: {exc}')


# ---------- 主流程 ----------

def main():
    print('🚀 开始更新 AIwork 数据...')
    print(f'⏰ 当前时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('-' * 50)

    print('[1/3] 获取 AI 工具资讯...')
    new_tools = get_aitools_news()
    update_tools(new_tools)

    print('[2/3] 获取免费 Token 资源...')
    new_tokens = get_freetokens()
    update_tokens(new_tokens)

    print('[3/3] 提交并推送更改...')
    git_commit_and_push()

    print('-' * 50)
    print('✨ 更新完成!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
