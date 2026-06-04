# GSAP 技能安装指南

本指南说明如何在 Trae AI 助手中安装和使用 GSAP（GreenSock Animation Platform）技能。

## 📦 技能列表

共包含 8 个技能：

1. **gsap-core** - 核心 API 技能
2. **gsap-timeline** - 时间线技能
3. **gsap-scrolltrigger** - ScrollTrigger 技能
4. **gsap-plugins** - 插件技能
5. **gsap-utils** - 工具函数技能
6. **gsap-react** - React 特定技能
7. **gsap-performance** - 性能优化技能
8. **gsap-frameworks** - 其他框架技能

---

## 🚀 安装方法

Trae 支持 3 种技能安装方式，推荐使用第一种。

### 方法 1：手动部署（最简单，推荐 ✅）

如果你已经在使用这个项目，技能已经自动安装好了！

**验证方法**：
1. 检查项目根目录是否存在 `.trae/skills/` 文件夹
2. 重启 Trae IDE
3. 在对话中输入 "使用 gsap 做一个动画" 来测试

**如果需要手动安装到其他项目**：
1. 复制 `.trae/skills/` 文件夹到你的项目根目录
2. 确保每个技能文件夹都包含 `SKILL.md` 文件
3. 重启 Trae

---

### 方法 2：ZIP 包导入（可视化界面）

1. **获取 ZIP 包**：从 `gsap_skills_zips/` 文件夹中获取所需的技能 ZIP 文件
2. **打开 Trae 设置**：
   - 打开 Trae → 设置 → 技能 → 创建技能
3. **选择压缩包**：
   - 点击"选择压缩包"
   - 选择你要安装的技能 ZIP 文件（如 `gsap-core.zip`）
4. **选择安装范围**：
   - 项目级：仅当前项目可用
   - 全局级：所有项目都可用（推荐）
5. **确认生效**：重启 Trae 后即可使用

---

### 方法 3：命令行安装（高级用户）

使用 `give-skill` 工具一键安装：

```bash
# 使用 npx 安装
npx give-skill greensock/gsap-skills
```

---

## 📁 文件说明

```
/workspace/
├── .trae/
│   └── skills/              # 已安装的技能（方法1使用）
│       ├── gsap-core/
│       ├── gsap-timeline/
│       └── ...
├── gsap_skills_zips/        # ZIP 压缩包（方法2使用）
│   ├── gsap-core.zip
│   ├── gsap-timeline.zip
│   └── ...
├── gsap-skills/             # 原始仓库
└── package_gsap_skills.py   # 打包脚本
```

---

## 💡 使用示例

安装成功后，你可以这样使用技能：

### 示例 1：基础动画
```
帮我用 GSAP 创建一个元素淡入并移动的动画
```

### 示例 2：时间线动画
```
使用 gsap timeline 创建一个多步骤的序列动画
```

### 示例 3：滚动动画
```
如何用 ScrollTrigger 实现滚动触发的动画效果？
```

### 示例 4：React 动画
```
在 React 项目中如何正确使用 GSAP？
```

---

## 🔍 验证安装

1. 打开 Trae 对话窗口
2. 输入 "你能使用 GSAP 技能吗？"
3. 如果 AI 能正确识别并开始提供 GSAP 相关的帮助，说明安装成功！

---

## ⚠️ 注意事项

- **确保根目录**：ZIP 包的根目录必须直接包含技能文件夹和 `SKILL.md`，不要有多余的嵌套层级
- **重启生效**：安装技能后需要重启 Trae
- **项目/全局**：根据需要选择安装范围
- **Trae 仅项目级**：Trae 目前只支持项目级技能安装

---

## 📚 更多资源

- [GSAP 官方文档](https://gsap.com/docs)
- [GSAP GitHub](https://github.com/greensock/gsap)
- [Agent Skills 规范](https://agentskills.io)

---

## 🆘 常见问题

**Q: 技能没生效怎么办？**
A: 首先确认 `.trae/skills/` 文件夹位置正确，然后重启 Trae。

**Q: 我可以只安装部分技能吗？**
A: 可以！只复制或导入你需要的技能文件夹/ZIP 包即可。

**Q: ZIP 包中的内容是什么？**
A: 每个 ZIP 包包含一个技能文件夹，里面有 `SKILL.md` 配置文件，这是技能的核心。

**Q: 如何更新技能？**
A: 删除旧技能文件夹，重新复制新版本或重新导入 ZIP 包。
