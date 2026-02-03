#!/usr/bin/env python3
"""
文件快速查找与发送工具

用法:
- 发送文件编号 → 快速发送到 Telegram
  例如: 01-01, 02-03, 03-01

- 列出分类 → 显示该分类下所有文件
  例如: 列出 01, 列出 02

- 全部列表 → 显示完整编号清单
"""

import json
import sys
from pathlib import Path

def load_index():
    with open('/Users/dave/clawd/file_index.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_file(index, file_id):
    for f in index['files']:
        if f['id'] == file_id:
            return f
    return None

def list_category(index, cat_id):
    files = [f for f in index['files'] if f['id'].startswith(cat_id)]
    return files

def main():
    if len(sys.argv) < 2:
        print("请提供文件编号或指令")
        return
    
    cmd = sys.argv[1]
    index = load_index()
    
    if cmd == "全部列表":
        # 显示完整清单
        for f in index['files']:
            print(f"[{f['id']}] {f['name']}")
            
    elif cmd.startswith("列出"):
        # 列出分类
        cat_id = cmd.split()[1].zfill(2)
        files = list_category(index, cat_id)
        if files:
            cat_name = index['categories'].get(cat_id, "未知分类")
            print(f"\n【{cat_name}】")
            for f in files:
                print(f"  [{f['id']}] {f['name']}")
        else:
            print(f"未找到分类: {cat_id}")
            
    else:
        # 查找单个文件
        file_id = cmd.zfill(4)  # 确保格式为 01-01
        f = find_file(index, file_id)
        if f:
            print(f"找到文件: {f['path']}")
            # 读取内容
            with open(f['path'], 'r', encoding='utf-8') as file:
                content = file.read()
            # 保存到临时文件供发送
            output = f"{f['path']}.temp"
            with open(output, 'w', encoding='utf-8') as out:
                out.write(content)
            print(f"内容已保存到: {output}")
        else:
            print(f"未找到文件: {file_id}")

if __name__ == "__main__":
    main()
