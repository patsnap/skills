#!/bin/bash
# tech-report-skill 一键安装脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检测安装位置
INSTALL_DIR="${HOME}/.claude/skills/tech-report-skill"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}tech-report-skill 安装脚本${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo "版本: v1.1.0"
echo "源目录: $SCRIPT_DIR"
echo "目标目录: $INSTALL_DIR"
echo ""

# 检查目标目录
if [ -d "$INSTALL_DIR" ] && [ "$SCRIPT_DIR" != "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}警告：目标目录已存在: $INSTALL_DIR${NC}"
    read -p "是否覆盖安装？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}安装已取消${NC}"
        exit 1
    fi
    echo -e "${YELLOW}正在备份现有安装...${NC}"
    mv "$INSTALL_DIR" "${INSTALL_DIR}.backup.$(date +%Y%m%d%H%M%S)"
fi

# 如果已经在目标位置，跳过复制
if [ "$SCRIPT_DIR" = "$INSTALL_DIR" ]; then
    echo -e "${GREEN}✓ 已在安装位置，跳过文件复制${NC}"
else
    # 创建目录
    mkdir -p "$(dirname "$INSTALL_DIR")"

    # 复制文件
    echo -e "${YELLOW}正在安装文件...${NC}"
    cp -r "$SCRIPT_DIR" "$INSTALL_DIR"
    echo -e "${GREEN}✓ 文件复制完成${NC}"
fi

# 设置执行权限
echo -e "${YELLOW}正在设置执行权限...${NC}"
chmod +x "$INSTALL_DIR/scripts/"*.sh 2>/dev/null || true
chmod +x "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true
echo -e "${GREEN}✓ 权限设置完成${NC}"

# 检查Python环境
echo -e "${YELLOW}正在检查Python环境...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误：未找到Python环境${NC}"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ 找到 Python: $PYTHON_VERSION${NC}"

# 安装依赖
echo -e "${YELLOW}正在安装Python依赖...${NC}"
$PYTHON_CMD -m pip install -q -r "$INSTALL_DIR/requirements.txt" || {
    echo -e "${RED}错误：依赖安装失败${NC}"
    echo "请手动运行: $PYTHON_CMD -m pip install pandas openpyxl"
    exit 1
}
echo -e "${GREEN}✓ 依赖安装完成${NC}"

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✓ 安装成功！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${BLUE}安装位置:${NC} $INSTALL_DIR"
echo ""
echo -e "${BLUE}快速开始：${NC}"
echo ""
echo "1. 创建配置文件（参考示例）："
echo "   - config/BIPV_keywords.py (BIPV技术关键词)"
echo "   - config/BIPV_content.py (BIPV技术内容)"
echo "   - config/咖啡机_keywords.py (咖啡机技术关键词)"
echo "   - config/咖啡机_content.py (咖啡机技术内容)"
echo ""
echo "2. 命令行运行："
echo "   cd $INSTALL_DIR"
echo "   bash scripts/run.sh <Excel路径> <技术主题> <开始日期> <结束日期>"
echo ""
echo "3. 或在 Claude Code 中直接使用："
echo "   \"请用XX技术主题生成研发简报\""
echo ""
echo -e "${YELLOW}查看完整文档：${NC}"
echo "   - README.md: 快速入门指南"
echo "   - SKILL.md: 详细使用说明"
echo "   - IMPROVEMENTS.md: 技术改进说明"
echo ""
