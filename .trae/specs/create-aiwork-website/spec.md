# AIwork AI导航网站 Spec

## Why
用户需要一个科技风格（黑金暗色）的AI导航网站，用于展示最新AI工具和免费Token信息。网站通过GitHub Pages部署，内容通过对话更新。

## What Changes
- 创建多页面静态网站（首页、AI工具页、免费Token页、关于页）
- 实现星空/星云动态背景效果
- 实现AI工具列表+详情展开展示
- 实现免费Token表格展示
- 实现搜索和分类筛选功能
- 采用黑金暗色科技风格

## Impact
- 新增完整网站文件结构
- 新增CSS样式系统
- 新增JavaScript交互功能
- 新增数据JSON文件

## ADDED Requirements

### Requirement: 网站架构
The system SHALL provide a multi-page static website with the following pages:
- 首页 (index.html): Hero区域+精选工具预览+网站简介
- AI工具页 (tools.html): 完整工具列表+搜索筛选
- 免费Token页 (tokens.html): Token信息表格
- 关于页 (about.html): 网站介绍

#### Scenario: 页面导航
- **WHEN** 用户访问网站
- **THEN** 可以通过导航栏在不同页面间切换

### Requirement: 视觉风格
The system SHALL use a black-gold dark tech theme:
- 背景色: #0a0a0a (深黑)
- 主色: #d4af37 (金色)
- 辅助色: #1a1a1a (深灰), #f5f5f5 (浅灰文字)
- 强调色: #ffd700 (亮金)
- 字体: 现代无衬线字体

#### Scenario: 视觉呈现
- **WHEN** 用户浏览网站
- **THEN** 看到黑金暗色科技风格，非通用蓝紫色

### Requirement: 动态背景
The system SHALL provide a starfield/nebula animated background on the homepage hero section using Canvas.

#### Scenario: 首页加载
- **WHEN** 用户访问首页
- **THEN** 看到星空/星云动态背景效果，金色星光闪烁

### Requirement: AI工具展示
The system SHALL display AI tools in a list with expandable details:
- 列表显示: 名称、图标、简介、标签
- 点击展开: 功能介绍、官网链接、价格信息
- 分类: 聊天、图像、代码、写作、音频、视频等

#### Scenario: 查看工具详情
- **WHEN** 用户点击工具项
- **THEN** 展开显示该工具的详细信息

### Requirement: 搜索和筛选
The system SHALL provide search and filter functionality:
- 搜索框: 按名称/关键词搜索
- 分类筛选: 按类别标签筛选
- 实时过滤: 输入时即时过滤结果

#### Scenario: 筛选工具
- **WHEN** 用户输入关键词或选择分类
- **THEN** 列表实时显示匹配结果

### Requirement: 免费Token展示
The system SHALL display free token information in a table format:
- 列: 平台名称、Token数量、有效期、领取状态、领取链接
- 筛选: 按有效期筛选

#### Scenario: 查看Token信息
- **WHEN** 用户访问Token页面
- **THEN** 看到清晰的表格展示各平台免费Token信息

### Requirement: 响应式设计
The system SHALL be responsive and work on desktop and mobile devices.

#### Scenario: 移动端访问
- **WHEN** 用户通过手机访问
- **THEN** 网站布局自适应，内容可读

### Requirement: GitHub Pages部署
The system SHALL be deployable to GitHub Pages as a static site.

#### Scenario: 部署
- **WHEN** 代码推送到GitHub
- **THEN** GitHub Pages自动部署网站
