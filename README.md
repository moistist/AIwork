# AIwork

AI 工具导航网站，收录最新 AI 工具、免费 Token/API 额度信息。

## 网站链接

https://yourusername.github.io/AIwork

## 功能特点

- **AI 工具库**：分类收录全球主流 AI 工具（聊天、代码、图像、视频、音频、搜索、3D 等）
- **免费 Token**：汇总各平台免费 API Token 与额度信息
- **每日自动更新**：每天早上 7 点（北京时间）由 GitHub Actions 自动运行 `update_aiwork.py` 抓取最新数据并更新 `data/tools.json` / `data/tokens.json`
- **响应式设计**：适配桌面端与移动端

## 技术栈

- HTML5 / CSS3 / JavaScript（原生 ES6+）
- Python 3（数据更新脚本，仅使用标准库，零依赖）
- GitHub Actions（每日调度 + GitHub Pages 自动部署）

## 目录结构

```
.
├── index.html            # 首页
├── tools.html            # 工具导航页
├── tokens.html           # 免费 Token 页
├── about.html            # 关于页
├── css/                  # 样式
├── js/                   # 前端脚本
├── data/
│   ├── tools.json        # 工具数据
│   └── tokens.json       # Token 数据
├── update_aiwork.py      # 每日数据更新脚本
└── .github/workflows/
    └── update-aiwork.yml # 自动化 workflow（每天 07:00 北京时间）
```

## 自动化更新说明

**触发时间**：每天北京时间 07:00（UTC 23:00），或在 push 到 `main`/`master` 分支时，或通过 Actions 页面手动点击 *Run workflow*。

**执行流程**：
1. 运行 `update_aiwork.py` 抓取/汇总 AI 工具与 Token 信息；
2. 自动 commit 数据变更并推送回仓库；
3. 使用 `actions/deploy-pages` 将仓库根目录部署到 GitHub Pages。

**本地手动运行**：
```bash
python3 update_aiwork.py
```
脚本会更新 `data/tools.json` 与 `data/tokens.json` 的 `lastUpdated` 时间戳，并在本地尝试 git 提交推送。

## 部署方式

1. Fork 或克隆本仓库
2. 在仓库 **Settings → Pages** 中，将 *Source* 设置为 **GitHub Actions**
3. 推送到 `main` 分支，或在 Actions 页面手动触发 *Update AIwork Data Daily* 工作流
4. 网站将自动部署到 `https://<your-username>.github.io/AIwork`
