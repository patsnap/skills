# tech-report-skill 分发清单

本文档说明如何将 tech-report-skill 打包分享给其他用户。

## 当前状态检查

### ✅ 已完成的部分

1. **核心脚本**
   - ✅ `scripts/tag_relevant.py` - 专利标引脚本
   - ✅ `scripts/generate_report.py` - HTML生成脚本
   - ✅ `scripts/run.sh` - 主执行脚本

2. **文档**
   - ✅ `SKILL.md` - Claude Code Skill 定义文件
   - ✅ `README.md` - 快速入门文档
   - ✅ `IMPROVEMENTS.md` - 改进说明文档

3. **配置示例**
   - ✅ `config/BIPV_keywords.py` - BIPV关键词配置示例
   - ✅ `config/BIPV_content.py` - BIPV内容配置示例
   - ✅ `config/咖啡机_keywords.py` - 咖啡机关键词配置示��
   - ✅ `config/咖啡机_content.py` - 咖啡机内容配置示例

### ❌ 需要补充的部分

1. **缺少 LICENSE 文件**
   - 需要明确开源协议（建议 MIT License）

2. **缺少 requirements.txt**
   - 虽然 run.sh 会自动安装，但最好提供标准依赖清单

3. **缺少 .gitignore**
   - 避免分享时包含临时文件和测试数据

4. **缺少安装脚本**
   - 需要一键安装脚本，方便用户快速部署

5. **缺少示例数据**
   - 提供一个小型示例 Excel 文件，让用户可以快速测试

6. **templates/ 目录为空**
   - 要么删除，要么添加用途说明

7. **缺少版本号管理**
   - 需要在 SKILL.md 和 README.md 中统一版本号

8. **缺少贡献指南**
   - 如果希望其他人贡献，需要 CONTRIBUTING.md

## 分发前需要做的调整

### 1. 添加 LICENSE 文件

创建 MIT License（最常用的开源协议）：

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

### 2. 添加 requirements.txt

```txt
pandas>=2.0.0
openpyxl>=3.1.0
```

### 3. 添加 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# 测试和临时文件
*.xlsx
*.html
*_标引.xlsx
*_report_*.html
test_data/
output/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### 4. 添加一键安装脚本 (install.sh)

```bash
#!/bin/bash
# 一键安装 tech-report-skill

set -e

# 检测安装位置
INSTALL_DIR="${HOME}/.claude/skills/tech-report-skill"

echo "========================================="
echo "tech-report-skill 安装脚本"
echo "========================================="
echo ""

# 检查目标目录
if [ -d "$INSTALL_DIR" ]; then
    echo "警告：目标目录已存在: $INSTALL_DIR"
    read -p "是否覆盖安装？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 1
    fi
    rm -rf "$INSTALL_DIR"
fi

# 创建目录
mkdir -p "$(dirname "$INSTALL_DIR")"

# 复制文件
echo "正在安装文件..."
cp -r "$(dirname "$0")" "$INSTALL_DIR"

# 设置执行权限
chmod +x "$INSTALL_DIR/scripts/"*.sh
chmod +x "$INSTALL_DIR/scripts/"*.py

# 检查Python环境
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "错误：未找到Python环境"
    exit 1
fi

# 安装依赖
echo "正在安装Python依赖..."
$PYTHON_CMD -m pip install -r "$INSTALL_DIR/requirements.txt" --quiet

echo ""
echo "========================================="
echo "✓ 安装完成！"
echo "========================================="
echo ""
echo "安装位置: $INSTALL_DIR"
echo ""
echo "快速开始："
echo "  1. 创建配置文件: config/{技术主题}_keywords.py"
echo "  2. 运行生成命令："
echo "     cd $INSTALL_DIR"
echo "     bash scripts/run.sh <Excel路径> <技术主题> <开始日期> <结束日期>"
echo ""
echo "或在Claude Code中直接使用："
echo "  \"请用XX技术主题生成研发简报\""
echo ""
```

### 5. 创建示例数据模板

创建 `examples/sample_template.xlsx` 的说明文档：

```markdown
# 示例数据说明

由于专利数据受版权保护，本 skill 不提供真实专利数据。

## 创建测试数据

你需要准备一个包含以下列的 Excel 文件：

**必需列：**
- 公开(公告)号
- 标题
- [标]当前申请(专利权)人
- 简单法律状态

**可选列：**
- Patsnap专利标题
- 技术问题
- 技术手段
- 技术功效

## 数据来源

推荐从 Patsnap 专利数据库导出 Excel 数据。
```

### 6. 处理 templates/ 目录

两种选择：
- **删除空目录**：`rm -rf templates/`
- **添加说明**：在 templates/ 中创建 README.md 说明该目录预留给未来的模板功能

### 7. 统一版本号

在所有文档中统一版本号为 v1.1.0：
- SKILL.md
- README.md
- package 元数据（如果有）

### 8. 添加 CONTRIBUTING.md（可选）

```markdown
# 贡献指南

感谢你对 tech-report-skill 的关注！

## 如何贡献

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 报告问题

如果发现 bug 或有功能建议，请在 Issues 中提交。

## 代码规范

- Python 代码遵循 PEP 8
- 脚本文件使用 UTF-8 编码
- 提交信息使用中文或英文，清晰描述改动
```

## 最终文件结构

```
tech-report-skill/
├── LICENSE                       # ⚠️ 需要添加
├── README.md                     # ✅ 已有
├── SKILL.md                      # ✅ 已有
├── IMPROVEMENTS.md               # ✅ 已有
├── DISTRIBUTION.md               # 本文件
├── CONTRIBUTING.md               # ⚠️ 可选，建议添加
├── requirements.txt              # ⚠️ 需要添加
├── .gitignore                    # ⚠️ 需要添加
├── install.sh                    # ⚠️ 需要添加
├── scripts/
│   ├── run.sh                    # ✅ 已有
│   ├── tag_relevant.py           # ✅ 已有
│   └── generate_report.py        # ✅ 已有
├── config/
│   ├── README.md                 # ⚠️ 建议添加配置文件说明
│   ├── BIPV_keywords.py          # ✅ 已有（示例）
│   ├── BIPV_content.py           # ✅ 已有（示例）
│   ├── 咖啡机_keywords.py         # ✅ 已有（示例）
│   └── 咖啡机_content.py          # ✅ 已有（示例）
├── examples/
│   └── SAMPLE_DATA.md            # ⚠️ 需要添加（数据格式说明）
└── templates/                    # ⚠️ 删除或添加 README.md
```

## 打包分发方式

### 方式1：GitHub 仓库（推荐）

1. 创建 GitHub 仓库
2. 推送所有文件
3. 添加 Release 版本标签
4. 用户通过 `git clone` 安装

**安装命令：**
```bash
git clone https://github.com/yourusername/tech-report-skill.git ~/.claude/skills/tech-report-skill
cd ~/.claude/skills/tech-report-skill
bash install.sh
```

### 方式2：压缩包分发

```bash
# 打包
cd ~/.claude/skills
tar -czf tech-report-skill-v1.1.0.tar.gz tech-report-skill/

# 或使用 zip
zip -r tech-report-skill-v1.1.0.zip tech-report-skill/
```

**用户安装：**
```bash
cd ~/.claude/skills
tar -xzf tech-report-skill-v1.1.0.tar.gz
cd tech-report-skill
bash install.sh
```

### 方式3：Claude Code Skill 市场（未来）

等待 Claude Code 官方 Skill 市场上线后，可以提交到市场供其他用户一键安装。

## 分发前检查清单

- [ ] 添加 LICENSE 文件
- [ ] 添加 requirements.txt
- [ ] 添加 .gitignore
- [ ] 添加 install.sh 安装脚本
- [ ] 创建 examples/SAMPLE_DATA.md 说明
- [ ] 处理空的 templates/ 目录
- [ ] 在 config/ 中添加 README.md
- [ ] 统一版本号为 v1.1.0
- [ ] 添加 CONTRIBUTING.md（可选）
- [ ] 测试在全新环境中安装和运行
- [ ] 更新 README.md 添加安装章节
- [ ] 检查所有文档中的路径和命令是否正确

## 用户安装后的使用流程

1. **安装 skill**
   ```bash
   bash install.sh
   ```

2. **创建配置文件**
   - 复制 `config/BIPV_keywords.py` 作为模板
   - 修改为自己的技术主题关键词

3. **准备 Excel 数据**
   - 从 Patsnap 导出专利清单

4. **在 Claude Code 中使用**
   ```
   请用{技术主题}生成研发简报，Excel文件是{路径}，时间范围是{开始日期}到{结束日期}
   ```

5. **查看生成的 HTML 简报**

## 注意事项

1. **隐私保护**
   - 不要在分发包中包含真实的专利数据
   - 示例配置文件中不要包含敏感信息

2. **跨平台兼容性**
   - 测试 Windows（Git Bash）、macOS、Linux 环境
   - 路径使用通用格式

3. **版本管理**
   - 使用语义化版本号（Semantic Versioning）
   - 在 CHANGELOG.md 中记录每个版本的改动

4. **文档完整性**
   - 确保所有示例命令都能正常运行
   - 提供清晰的错误排查指南

## 后续维护

- 定期更新依赖版本
- 收集用户反馈，持续改进
- 添加更多技术主题的配置示例
- 考虑添加单元测试
