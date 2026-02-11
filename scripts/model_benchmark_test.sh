#!/bin/bash
# 模型基准测试脚本

echo "========================================"
echo "MiniMax vs Kimi 模型基准测试"
echo "测试时间: $(date)"
echo "========================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：测试场景
test_scenario() {
    local model=$1
    local scenario=$2
    local prompt=$3
    
    echo ""
    echo -e "${YELLOW}测试: $model - $scenario${NC}"
    echo "提示词: $prompt"
    echo "----------------------------------------"
    
    # 记录开始时间
    start_time=$(date +%s)
    
    # 执行测试（这里应该调用实际的模型）
    # 由于无法直接调用，我们记录测试意图
    echo "测试意图: $prompt"
    
    # 记录结束时间
    end_time=$(date +%s)
    duration=$(($end_time - $start_time))
    
    echo "耗时: ${duration}秒"
    echo ""
}

# 当前模型配置
echo "当前默认模型: minimax/MiniMax-M2.1"

# 场景1: 工具调用能力
test_scenario "MiniMax" "工具调用能力" \
    "请调用 exec 工具执行 'echo \"测试 MiniMax 工具调用能力\"' 并说明整个调用过程。"

# 场景2: 代码生成能力
test_scenario "MiniMax" "代码生成能力" \
    "请用 Python 写一个简单的 Web 服务器代码（使用 Flask），包含路由、错误处理、日志记录。"

# 场景3: 中文理解与写作
test_scenario "MiniMax" "中文理解与写作" \
    "请用中文写一段关于半导体行业发展的分析（200字），包含行业趋势、挑战、机遇三个部分。"

# 场景4: 深度思考能力
test_scenario "MiniMax" "深度思考能力" \
    "请分析：为什么 AI 芯片需求在 2025-2026 年爆发？从技术、市场、应用三个维度分析。"

# 场景5: 多轮对话记忆
echo ""
echo -e "${YELLOW}测试: MiniMax - 多轮对话记忆${NC}"
echo "----------------------------------------"
echo "第1轮: 请告诉我你的名字。"
echo "第2轮: 请重复我上一轮问的问题。"
echo "第3轮: 我刚才告诉你我的名字了吗？如果有，是什么？"
echo "注意: 此测试需要在同一会话中连续执行"
echo ""

# 场景6: 系统提示词遵循
test_scenario "MiniMax" "系统提示词遵循" \
    "请用英文回答这个问题：What is artificial intelligence?"

echo ""
echo "========================================"
echo "MiniMax 测试完成"
echo "========================================"

echo ""
echo "切换到 Kimi 模型..."
# 切换模型命令
# openclaw models set kimi/Kimi-K2.5

echo ""
echo "========================================"
echo "准备测试 Kimi K2.5"
echo "请执行以下命令切换模型:"
echo "  openclaw models set kimi/Kimi-K2.5"
echo "========================================"
