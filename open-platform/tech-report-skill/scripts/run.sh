#!/bin/bash
# 技术研发简报生成主脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -lt 4 ]; then
    echo -e "${RED}错误：参数不足${NC}"
    echo "用法: $0 <Excel文件路径> <技术主题> <开始日期> <结束日期>"
    echo ""
    echo "示例:"
    echo "  $0 \"/path/to/BIPV专利清单202604.XLSX\" \"BIPV\" \"20260201\" \"20260430\""
    echo "  $0 \"/path/to/固态电池专利.xlsx\" \"固态电池\" \"20260101\" \"20260331\""
    exit 1
fi

INPUT_XLSX="$1"
TECH_TOPIC="$2"
START_DATE="$3"
END_DATE="$4"

# 检查输入文件是否存在
if [ ! -f "$INPUT_XLSX" ]; then
    echo -e "${RED}错误：输入文件不存在: $INPUT_XLSX${NC}"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$SKILL_DIR/config"

# 检查配置文件
KEYWORDS_CONFIG="$CONFIG_DIR/${TECH_TOPIC}_keywords.py"
CONTENT_CONFIG="$CONFIG_DIR/${TECH_TOPIC}_content.py"

if [ ! -f "$KEYWORDS_CONFIG" ]; then
    echo -e "${YELLOW}警告：关键词配置文件不存在: $KEYWORDS_CONFIG${NC}"
    echo -e "${YELLOW}请先创建配置文件，或使用AI引导创建${NC}"
    exit 1
fi

if [ ! -f "$CONTENT_CONFIG" ]; then
    echo -e "${YELLOW}警告：内容配置文件不存在: $CONTENT_CONFIG${NC}"
    echo -e "${YELLOW}将使用默认配置生成简报（不包含行业动态和公司分析）${NC}"
fi

# 生成输出文件路径
INPUT_DIR="$(dirname "$INPUT_XLSX")"
INPUT_BASENAME="$(basename "$INPUT_XLSX" .XLSX)"
INPUT_BASENAME="$(basename "$INPUT_BASENAME" .xlsx)"

# 格式化日期范围
DATE_RANGE="${START_DATE:0:6}to${END_DATE:0:6}"

TAGGED_XLSX="$INPUT_DIR/${INPUT_BASENAME}_标引.xlsx"
OUTPUT_HTML="$INPUT_DIR/${TECH_TOPIC}_report_${DATE_RANGE}.html"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}技术研发简报生成工具${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "输入文件: $INPUT_XLSX"
echo "技术主题: $TECH_TOPIC"
echo "日期范围: $START_DATE - $END_DATE"
echo ""

# 检查Python环境
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误：未找到Python环境${NC}"
    exit 1
fi

echo -e "${GREEN}使用Python: $PYTHON_CMD${NC}"
echo ""

# 检查并安装依赖
echo -e "${YELLOW}[1/3] 检查依赖...${NC}"
$PYTHON_CMD -c "import pandas, openpyxl" 2>/dev/null || {
    echo -e "${YELLOW}安装依赖包...${NC}"
    $PYTHON_CMD -m pip install pandas openpyxl --quiet || {
        echo -e "${RED}错误：依赖安装失败${NC}"
        exit 1
    }
}
echo -e "${GREEN}✓ 依赖检查完成${NC}"
echo ""

# 步骤1：专利标引
echo -e "${YELLOW}[2/3] 执行专利标引...${NC}"
$PYTHON_CMD "$SCRIPT_DIR/tag_relevant.py" "$INPUT_XLSX" "$TAGGED_XLSX" "$TECH_TOPIC"
echo ""

# 步骤2：生成HTML简报
echo -e "${YELLOW}[3/3] 生成HTML简报...${NC}"
$PYTHON_CMD "$SCRIPT_DIR/generate_report.py" "$TAGGED_XLSX" "$OUTPUT_HTML" "$TECH_TOPIC" "$DATE_RANGE"
echo ""

# 完成
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ 简报生成完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "输出文件:"
echo "  - 标引Excel: $TAGGED_XLSX"
echo "  - HTML简报:  $OUTPUT_HTML"
echo ""
echo -e "${YELLOW}提示：在浏览器中打开HTML文件查看完整简报${NC}"
