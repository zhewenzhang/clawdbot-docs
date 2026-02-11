#!/usr/bin/env python3
"""
手动创建提醒 - 不依赖 Calendar API
使用 cron 定时任务提醒
"""

import os
import json
from datetime import datetime, timedelta

def create_manual_reminders():
    """手动创建提醒"""
    
    reminders = [
        {
            "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "time": "08:00",
            "title": "⏰ 提醒：10086 鸿蒙手机套餐申请延期",
            "description": "需要拨打 10086 申请鸿蒙手机套餐延期",
            "priority": "high"
        },
        {
            "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "time": "14:00",
            "title": "⏰ 提醒：知乎保存 CPO 知识文档",
            "description": "需要在知乎保存 CPO 相关知识文档",
            "priority": "medium"
        }
    ]
    
    # 保存到文件
    reminder_file = '/Users/dave/clawd/data/reminders.json'
    
    # 读取现有提醒
    existing = []
    if os.path.exists(reminder_file):
        with open(reminder_file, 'r') as f:
            existing = json.load(f)
    
    # 添加新提醒
    existing.extend(reminders)
    
    # 保存
    with open(reminder_file, 'w') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print("✅ 提醒已创建！")
    print("=" * 60)
    
    for r in reminders:
        print(f"\n📅 {r['date']} {r['time']}")
        print(f"   标题: {r['title']}")
        print(f"   说明: {r['description']}")
    
    print("\n" + "=" * 60)
    print("📋 提醒管理命令：")
    print("   - 查看提醒: cat /Users/dave/clawd/data/reminders.json")
    print("   - 删除提醒: rm /Users/dave/clawd/data/reminders.json")
    print("=" * 60)

def check_reminders():
    """检查今日提醒"""
    reminder_file = '/Users/dave/clawd/data/reminders.json'
    
    if not os.path.exists(reminder_file):
        print("无提醒")
        return
    
    with open(reminder_file, 'r') as f:
        reminders = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    today_reminders = [r for r in reminders if r['date'] == today]
    
    if today_reminders:
        print(f"\n📅 今日提醒 ({today}):")
        for r in today_reminders:
            print(f"\n  ⏰ {r['time']}")
            print(f"     {r['title']}")
            print(f"     {r['description']}")
    else:
        print(f"\n✅ 今日 ({today}) 无提醒")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        check_reminders()
    else:
        create_manual_reminders()
