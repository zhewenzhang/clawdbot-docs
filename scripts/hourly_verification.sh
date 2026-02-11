#!/bin/bash
# 每小时验证华为昇腾 roadmap

echo "[$(date)] 开始验证华为昇腾 roadmap..."

# 运行 Python 验证脚本
python3 /Users/dave/clawd/scripts/verify_huawei_roadmap.py

# 如果发现错误，发送通知
if grep -q "FAIL" /Users/dave/clawd/memory/semiconductor_roadmaps/verification_log.json 2>/dev/null; then
    echo "⚠️ 发现错误！请检查验证日志"
    # 可以添加邮件或 Telegram 通知
fi

echo "[$(date)] 验证完成"
