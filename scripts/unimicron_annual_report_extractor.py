#!/usr/bin/env python3
"""
欣兴电子年报下载与信息提取工具
功能：
1. 系统性搜索年报PDF
2. 下载并提取关键信息
3. 定位"大陆子公司信息披露"页面
4. 截图保存关键页面
"""

import requests
import re
import os
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def search_unimicron_annual_reports():
    """搜索欣兴电子历年财报"""
    
    # 可能的年报URL模式
    url_patterns = [
        # 台湾公开资讯观测站
        'https://mops.twse.com.tw/mops/web/ajax_t164sb04_e?firstin=true&year={year}&co_id=3037',
        # 欣兴官网
        'https://www.unimicron.com/files/money/Shareholders_Meeting/{year}-annual_en.pdf',
        # 雪球
        'https://stockn.xueqiu.com/00631/{yyyymmdd}.pdf',
    ]
    
    # 搜索关键词
    search_queries = [
        '欣興電子 2024 年報 PDF',
        'Unimicron 2024 annual report Taiwan',
        '3037 年報 PDF 下載',
    ]
    
    print("📊 搜索欣兴电子历年财报...")
    
    # 尝试直接访问可能的URL
    for year in [2024, 2023, 2022, 2021]:
        yyyy = str(year)
        yyyymmdd = f"{year}1231" if year <= 2024 else f"{year-1}1231"
        
        for pattern in url_patterns:
            url = pattern.format(year=year, yyyy=yyyy, yyyymmdd=yyyymmdd)
            try:
                r = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
                if r.status_code == 200:
                    print(f"✅ 可能存在: {url[:80]}")
                    return url  # 返回找到的URL
            except:
                pass
    
    return None

def extract_china_subsidiary_info(pdf_path):
    """
    从PDF中提取"大陆子公司信息披露"
    关键章节通常在：
    - 非合併財務報告之子公司財務資訊
    - 大陸子公司資訊揭露
    - 主要往來銀行授信額度
    """
    
    import subprocess
    
    # 使用 pdftotext 提取文本
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', pdf_path, '-'],
            capture_output=True,
            text=True
        )
        text = result.stdout
        
        # 搜索关键章节
        keywords = [
            '大陸子公司',
            '非合併財務報告之子公司',
            '大陸子公司資訊揭露',
            '子公司',
            '附屬公司'
        ]
        
        found_sections = []
        for keyword in keywords:
            if keyword in text:
                # 提取关键词附近的文本
                pattern = rf'{keyword}[^\n]{{0,500}}'
                matches = re.findall(pattern, text)
                if matches:
                    for match in matches[:5]:  # 最多提取5条
                        found_sections.append(match.strip())
        
        return found_sections[:10]  # 返回最多10条
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        return []

def extract_last_pages(pdf_path, num_pages=5):
    """提取PDF最后几页"""
    
    import subprocess
    
    total_pages = subprocess.run(
        ['pdfinfo', pdf_path],
        capture_output=True,
        text=True
    )
    
    # 解析总页数
    for line in total_pages.stdout.split('\n'):
        if line.startswith('Pages:'):
            total = int(line.split(':')[1].strip())
            print(f"📄 PDF总页数: {total}")
            break
    
    # 使用 pdftotext 提取最后几页
    last_pages_text = []
    for i in range(num_pages, 0, -1):
        page_num = total - i + 1
        try:
            result = subprocess.run(
                ['pdftotext', '-f', str(page_num), '-l', str(page_num), pdf_path, '-'],
                capture_output=True,
                text=True
            )
            content = result.stdout.strip()
            if content:
                last_pages_text.append(f"--- 第 {page_num} 页 ---")
                last_pages_text.append(content[:3000])  # 每页最多3000字符
        except Exception as e:
            print(f"❌ 提取第{page_num}页失败: {e}")
    
    return '\n\n'.join(last_pages_text)

if __name__ == '__main__':
    # 测试：使用2020年年报
    pdf_path = '/tmp/unimicron_annual_2020.pdf'
    
    if os.path.exists(pdf_path):
        print("=" * 60)
        print("📊 测试：提取2020年年报最后几页")
        print("=" * 60)
        
        # 提取最后几页
        last_pages = extract_last_pages(pdf_path, num_pages=5)
        
        if last_pages:
            print(f"\n📄 最后5页内容预览:")
            print("-" * 60)
            print(last_pages[:5000])
            print("-" * 60)
            
            # 搜索大陆子公司信息
            china_info = extract_china_subsidiary_info(pdf_path)
            
            if china_info:
                print(f"\n✅ 找到 {len(china_info)} 条相关信息:")
                for i, info in enumerate(china_info[:5], 1):
                    print(f"\n{i}. {info[:500]}")
            else:
                print("\n❌ 未找到大陆子公司信息披露")
    else:
        print(f"❌ PDF不存在: {pdf_path}")
