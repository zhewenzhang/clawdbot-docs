#!/usr/bin/env python3
"""
Token 使用情况追踪脚本
- 记录每日 Token 消耗
- 生成累计统计
- 支持多模型分账
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 配置
TOKEN_STATS_FILE = Path.home() / "clawd/memory/token_stats.json"

def load_stats():
    """加载现有统计数据"""
    if TOKEN_STATS_FILE.exists():
        with open(TOKEN_STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "meta": {
            "version": 2,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "notes": "Token usage tracking for daily reports - 支持多模型分账"
        },
        "current_baseline": None,
        "daily_history": []
    }

def save_stats(stats):
    """保存统计数据"""
    stats["meta"]["updated_at"] = datetime.now().isoformat()
    with open(TOKEN_STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

def update_daily_token(current_in, current_out, model="minimax/MiniMax-M2.1"):
    """更新每日 Token 消耗"""
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 查找今日记录
    today_record = None
    for day in stats["daily_history"]:
        if day["date"] == today:
            today_record = day
            break
    
    total_today = current_in + current_out
    
    if today_record:
        # 今日已有记录，检查是否需要更新
        if today_record["total"] < total_today:
            # 更新为最新值
            today_record["total_in"] = current_in
            today_record["total_out"] = current_out
            today_record["total"] = total_today
            today_record["by_model"][model] = {
                "in": current_in,
                "out": current_out,
                "total": total_today
            }
    else:
        # 新增今日记录
        today_record = {
            "date": today,
            "total_in": current_in,
            "total_out": current_out,
            "total": total_today,
            "by_model": {
                model: {
                    "in": current_in,
                    "out": current_out,
                    "total": total_today
                }
            }
        }
        stats["daily_history"].append(today_record)
    
    # 更新 Baseline
    stats["current_baseline"] = {
        "timestamp": datetime.now().isoformat(),
        "total_in": current_in,
        "total_out": current_out,
        "total": total_today,
        "by_model": {
            model: {
                "in": current_in,
                "out": current_out,
                "total": total_today
            }
        },
        "model": model
    }
    
    save_stats(stats)
    return stats

def get_monthly_total():
    """获取本月累计 Token（实际消耗，而非累计值叠加）"""
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    month_prefix = today[:7]  # YYYY-MM
    
    monthly_total = 0
    prev_total = 0
    
    for day in stats["daily_history"]:
        if day["date"].startswith(month_prefix):
            # 计算每日实际消耗
            if prev_total > 0:
                daily_consumption = max(0, day["total"] - prev_total)
            else:
                daily_consumption = day["total"]  # 第一天用绝对值
            monthly_total += daily_consumption
            prev_total = day["total"]
    
    return monthly_total

def get_daily_report(current_in, current_out, model="minimax/MiniMax-M2.1"):
    """生成每日报告"""
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 找昨日数据
    yesterday_total = None
    for day in reversed(stats["daily_history"]):
        if day["date"] < today:
            yesterday_total = day["total"]
            break
    
    # 计算今日消耗
    today_total = current_in + current_out
    
    if yesterday_total and yesterday_total > 0:
        daily_consumption = today_total - yesterday_total
    else:
        # 如果没有昨日数据，用最近一次记录计算
        if stats["current_baseline"]:
            baseline = stats["current_baseline"]["total"]
            daily_consumption = max(0, today_total - baseline)
        else:
            daily_consumption = today_total
    
    monthly_total = get_monthly_total()
    
    return {
        "date": today,
        "daily_consumption": daily_consumption,
        "daily_in": current_in,
        "daily_out": current_out,
        "monthly_total": monthly_total,
        "model": model
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: token_tracker.py <current_in> <current_out> [model]")
        sys.exit(1)
    
    current_in = int(sys.argv[1])
    current_out = int(sys.argv[2])
    model = sys.argv[3] if len(sys.argv) > 3 else "minimax/MiniMax-M2.1"
    
    update_daily_token(current_in, current_out, model)
    report = get_daily_report(current_in, current_out, model)
    
    print(f"✅ Token 统计已更新")
    print(f"📅 日期: {report['date']}")
    print(f"📊 今日消耗: {report['daily_consumption']:,} (In: {report['daily_in']:,} / Out: {report['daily_out']:,})")
    print(f"📈 本月累计: {report['monthly_total']:,}")
