#!/usr/bin/env python3
"""
定时提醒检查脚本
每天 7:55 和 13:55 检查提醒并发送通知
"""

import os
import sys
import json
from datetime import datetime

def send_reminder_notification():
    """发送提醒通知"""
    reminder_file = '/Users/dave/clawd/data/reminders.json'
    
    if not os.path.exists(reminder_file):
        return
    
    with open(reminder_file, 'r') as f:
        reminders = json.load(f)
    
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_hour = now.strftime("%H:%M")
    
    # 检查今日提醒
    for r in reminders[:]:
        if r['date'] != today:
            continue
        
        # 早上 7:55 检查 8:00 的提醒
        if current_hour >= "07:55" and current_hour <= "08:05" and r['time'] == "08:00":
            send_telegram(r)
            reminders.remove(r)
        
        # 下午 13:55 检查 14:00 的提醒
        elif current_hour >= "13:55" and current_hour <= "14:05" and r['time'] == "14:00":
            send_telegram(r)
            reminders.remove(r)
    
    # 保存更新后的提醒
    with open(reminder_file, 'w') as f:
        json.dump(reminders, f, indent=2, ensure_ascii=False)

def send_telegram(reminder):
    """发送 Telegram 通知"""
    # 这里需要集成 OpenClaw 的 message 功能
    # 目前先打印到控制台
    print("\n" + "=" * 60)
    print("🔔 提醒时间到！")
    print("=" * 60)
    print(f"\n📅 {reminder['date']} {reminder['time']}")
    print(f"   {reminder['title']}")
    print(f"   {reminder['description']}")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    send_reminder_notification()
