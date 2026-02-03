#!/usr/bin/env python3
"""
Markdown 转 PDF 工具
用于将半导体分析报告转换为 PDF 格式

使用方法:
    python3 md2pdf.py <markdown_file>
    
示例:
    python3 md2pdf.py ethernet_switch_market.md
"""

import sys
import os
import subprocess
from datetime import datetime

def md_to_html(md_file):
    """读取并转换 Markdown 为简单 HTML"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    lines = md_content.split('\n')
    html_content = ""
    in_table = False
    
    for i, line in enumerate(lines):
        if line.startswith('# '):
            if in_table:
                html_content += '</table>'
                in_table = False
            html_content += f'<h1>{line[2:]}</h1>\n'
        elif line.startswith('## '):
            if in_table:
                html_content += '</table>'
                in_table = False
            html_content += f'<h2>{line[3:]}</h2>\n'
        elif line.startswith('### '):
            if in_table:
                html_content += '</table>'
                in_table = False
            html_content += f'<h3>{line[4:]}</h3>\n'
        elif line.startswith('---'):
            if in_table:
                html_content += '</table>'
                in_table = False
            html_content += '<hr>\n'
        elif '| ---' in line or '|---|' in line:
            # 表格标题行后的分隔线
            if not in_table and i > 0 and lines[i-1].startswith('|'):
                in_table = True
                html_content += '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">\n'
        elif line.startswith('| ') and in_table:
            cells = [c.strip() for c in line.split('|')[1:-1]]
            html_content += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n'
        elif line.startswith('- '):
            if in_table:
                html_content += '</table>'
                in_table = False
            html_content += f'<li>{line[2:]}</li>\n'
        elif line.strip() == '':
            if in_table:
                pass  # 表格中保留空行
            else:
                html_content += '<br>\n'
        else:
            if in_table:
                pass  # 跳过表格中的其他行
            else:
                # 处理粗体
                processed = line
                if '**' in line:
                    processed = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                # 处理行内代码
                if '`' in line:
                    processed = processed.replace('`', '<code>', 1).replace('</code>', '</code>', 1) if processed.count('`') >= 2 else processed
                html_content += f'<p>{processed}</p>\n'
    
    if in_table:
        html_content += '</table>'
    
    return html_content

def generate_html(md_file, html_body):
    """生成完整 HTML 文档"""
    filename = os.path.basename(md_file).replace('.md', '')
    title = filename.replace('_', ' ').title()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            font-size: 24px;
            color: #1a1a1a;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 15px;
            margin-top: 30px;
        }}
        h2 {{
            font-size: 20px;
            color: #0066cc;
            margin-top: 25px;
        }}
        h3 {{
            font-size: 16px;
            color: #333;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 13px;
        }}
        th {{
            background-color: #0066cc;
            color: white;
            padding: 12px 8px;
            text-align: left;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 10px 8px;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        strong {{
            color: #0066cc;
        }}
        li {{
            margin: 8px 0;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'SF Mono', Monaco, monospace;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}
        @media print {{
            body {{
                font-size: 12px;
            }}
            h1 {{
                font-size: 20px;
            }}
            h2 {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <h1>📊 {title}</h1>
    
    <p><strong>生成时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M')}
    <br><strong>文档来源：</strong>{md_file}</p>
    
    <hr>
    
    {html_body}
    
    <hr>
    
    <p style="font-size: 12px; color: #666;">
        <strong>阅读说明：</strong>本文档可在浏览器中打开，按 <code>Cmd+P</code> (Mac) 或 <code>Ctrl+P</code> (Windows) 打印为 PDF。
    </p>
</body>
</html>
"""
    return html

def main():
    if len(sys.argv) < 2:
        print("用法: python3 md2pdf.py <markdown_file>")
        print("示例: python3 md2pdf.py ethernet_switch_market.md")
        sys.exit(1)
    
    md_file = sys.argv[1]
    
    if not os.path.exists(md_file):
        print(f"❌ 文件不存在: {md_file}")
        sys.exit(1)
    
    print("=" * 60)
    print("📄 Markdown 转 PDF 工具")
    print("=" * 60)
    
    # 转换
    html_body = md_to_html(md_file)
    full_html = generate_html(md_file, html_body)
    
    # 保存 HTML
    output_html = md_file.replace('.md', '_printable.html')
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ HTML 已生成: {output_html}")
    print()
    print("📖 使用方法:")
    print("  1. 在浏览器中打开 HTML 文件")
    print("  2. 按 Cmd+P (Mac) 或 Ctrl+P (Windows)")
    print("  3. 选择 '保存为 PDF'")
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()
