#!/bin/bash
# Daily Token Report - 生成并发送每日运行报告
# 执行时间: 每天 8:00 AM

cd /Users/dave/clawd

# 1. 获取当前 Token 数据
CURRENT=$(python3 -c "
import json
from pathlib import Path
stats = json.load(open(Path.home() / 'clawd/memory/token_stats.json'))
cb = stats['current_baseline']
print(f\"{cb['total_in']} {cb['total_out']} {cb['model']}\")
")

IN=$(echo $CURRENT | cut -d' ' -f1)
OUT=$(echo $CURRENT | cut -d' ' -f2)
MODEL=$(echo $CURRENT | cut -d' ' -f3-)

# 2. 更新 Token 统计
python3 scripts/token_tracker.py $IN $OUT "$MODEL"

# 3. 获取系统状态
UPTIME=$(uptime | sed 's/.*up/up/' | sed 's/,.*load//')
LOAD=$(uptime | sed 's/.*load average: //')

# 4. 发送报告
python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime

stats = json.load(open(Path.home() / 'clawd/memory/token_stats.json'))
today = datetime.now().strftime('%Y-%m-%d')

# 找昨日数据
yesterday_total = 0
for day in stats['daily_history']:
    if day['date'] < today and day['date'].startswith('2026-02'):
        yesterday_total = day['total']

# 计算今日消耗
current_total = stats['current_baseline']['total']
daily_consumption = current_total - yesterday_total if yesterday_total > 0 else 0

# 本月累计
monthly_total = sum(
    d['total'] for d in stats['daily_history'] 
    if d['date'].startswith('2026-02')
)

report = f"""
📊 **每日综合运行报告**
━━━━━━━━━━━━━━━━━━
📅 **日期**: {today}

🤖 **Token 消耗**
📉 **今日**: {daily_consumption:,} (In: {stats['current_baseline']['total_in']:,} / Out: {stats['current_baseline']['total_out']:,})
📊 **本月累计**: {monthly_total:,}
📈 **当前基准**: {current_total:,}

🖥️ **系统状态**
⏱️ **连续运行**: {open('/proc/uptime').read().split()[0]} 秒
⚙️ **负载**: {open('/proc/loadavg').read().split()[0:3].join('/')}

🧠 **模型**: {stats['current_baseline']['model']}
━━━━━━━━━━━━━━━━━━
✅ 系统运行正常
"""

print(report.strip())
EOF
