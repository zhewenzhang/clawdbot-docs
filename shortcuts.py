#!/usr/bin/env python3
"""
快捷命令处理器
支持: /*今日总结, /*金价, /*分析, /*邮件, /*日历
"""

import sys
import os
from datetime import datetime

# 添加 clawd 路径
CLAWD_DIR = os.path.expanduser("~/clawd")
sys.path.insert(0, CLAWD_DIR)

def cmd_summary():
    """/*今日总结 - 显示今天任务和进度"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = os.path.join(CLAWD_DIR, "memory", f"{today}.md")
    
    print(f"\n📋 今日总结 - {today}")
    print("="*50)
    
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            content = f.read()
            # 显示完成事项
            if "完成事项" in content or "✅ 完成" in content:
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('## ') or line.startswith('### '):
                        print(f"\n{line}")
                    elif '✅' in line or '完成' in line:
                        print(f"  {line.strip()}")
            else:
                print("  暂无记录")
    else:
        print("  今日暂无记录")
    
    print("\n" + "="*50)

def cmd_gold_price():
    """/*金价 - 查询黄金价格"""
    print("\n💰 黄金价格查询")
    print("="*50)
    print("  请稍候，正在查询...")
    print("  (可集成天气查询 skill)")
    print("="*50)

def cmd_analyze():
    """/*分析 - 执行分析脚本"""
    print("\n📊 执行分析")
    print("="*50)
    print("  请输入分析类型：")
    print("  1. 行业分析")
    print("  2. 数据分析")
    print("  3. 报告生成")
    print("="*50)

def cmd_email():
    """/*邮件 - 检查邮箱"""
    print("\n📧 邮箱检查")
    print("="*50)
    print("  账户: davezhangus@gmail.com")
    print("  状态: 待集成邮件 API")
    print("="*50)

def cmd_calendar():
    """/*日历 - 查看日程"""
    print("\n📅 日历 - " + datetime.now().strftime("%Y-%m-%d %A"))
    print("="*50)
    print("  今日暂无日程记录")
    print("  (待集成日历 API)")
    print("="*50)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 shortcuts.py <命令>")
        print("可用命令: 今日总结, 金价, 分析, 邮件, 日历")
        return
    
    cmd = sys.argv[1].lower()
    
    commands = {
        '今日总结': cmd_summary,
        '金价': cmd_gold_price,
        '分析': cmd_analyze,
        '邮件': cmd_email,
        '日历': cmd_calendar
    }
    
    if cmd in commands:
        commands[cmd]()
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: 今日总结, 金价, 分析, 邮件, 日历")

if __name__ == "__main__":
    main()
