#!/usr/bin/env python3
"""
Markdown 转纯文字工具
用于将 Markdown 文件转换为易读的纯文字格式
"""

import re
import json
import sys

def convert_markdown_to_text(md_content):
    """将 Markdown 转换为纯文字"""
    text = md_content
    
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # 处理标题
    text = re.sub(r'^### (.+)$', r'=== \1 ===', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'=== \1 ===', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'=== \1 ===', text, flags=re.MULTILINE)
    
    # 处理粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    
    # 处理斜体
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    
    # 处理行内代码
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    # 处理链接 [text](url) -> text (url)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # 处理图片 ![alt](url) -> [图片]
    text = re.sub(r'!\[.*?\]\(.+?\)', r'[图片]', text)
    
    # 处理无序列表
    text = re.sub(r'^[\-\*] (.+)$', r'• \1', text, flags=re.MULTILINE)
    
    # 处理有序列表
    text = re.sub(r'^\d+\. (.+)$', r'◦ \1', text, flags=re.MULTILINE)
    
    # 处理引用块
    text = re.sub(r'^> (.+)$', r'  「\1」', text, flags=re.MULTILINE)
    
    # 处理水平线
    text = re.sub(r'^[\-\*]{3,}$', '', text, flags=re.MULTILINE)
    
    # 移除多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 清理首尾空行
    text = text.strip()
    
    return text

def main():
    if len(sys.argv) < 2:
        print("请提供 Markdown 文件路径")
        return
    
    md_file = sys.argv[1]
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    text = convert_markdown_to_text(md_content)
    
    print(text)

if __name__ == "__main__":
    main()
