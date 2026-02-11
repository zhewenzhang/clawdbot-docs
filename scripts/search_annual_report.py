#!/usr/bin/env python3
"""
系统性搜索欣兴电子2024年年报
"""
import requests
import re
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def search_annual_report():
    """搜索欣兴电子年报"""

    # 已知可能的年报来源
    sources = [
        {
            'name': '鉅亨網-年报下载',
            'url': 'https://invest.cnyes.com/twstock/3037/financials/annual',
            'pdf_pattern': r'href=[\'"]([^\'"]*\.pdf[^\'"]*)[\'"]'
        },
        {
            'name': '旺年财经网-年报',
            'url': 'https://www.wantgoo.com/stock/3037/annual-report',
            'pdf_pattern': r'href=[\'"]([^\'"]*annual[^\'"]*\.pdf[^\'"]*)[\'"]'
        },
        {
            'name': 'MoneyDJ-年报中心',
            'url': 'https://www.moneydj.com/StockInfo/StockInfo3.aspx?a=STK3037&c=0000&d=0019',
            'pdf_pattern': r'href=[\'"]([^\'"]*\.pdf[^\'"]*)[\'"]'
        },
        {
            'name': '公开资讯观测站-年报',
            'url': 'https://mops.twse.com.tw/mops/web/t164sb04_e?firstin=true&year=113&co_id=3037',
            'pdf_pattern': r'href=[\'"](t164sb04_e[^\'"]*\.pdf[^\'"]*)[\'"]'
        }
    ]

    found_pdfs = []

    for source in sources:
        try:
            print(f"正在搜索: {source['name']}...")
            r = requests.get(source['url'], headers=headers, timeout=5, allow_redirects=True)

            # 查找PDF链接
            pdf_links = re.findall(source['pdf_pattern'], r.text, re.I)

            if pdf_links:
                for link in pdf_links[:5]:
                    full_url = link if link.startswith('http') else f"https://mops.twse.com.tw/mops/web/{link}"
                    print(f"  📄 找到: {full_url[:80]}")
                    found_pdfs.append({'source': source['name'], 'url': full_url})

        except Exception as e:
            print(f"  ❌ 错误: {str(e)[:50]}")

        time.sleep(0.5)

    return found_pdfs

if __name__ == '__main__':
    results = search_annual_report()
    print(f"\n找到 {len(results)} 个PDF链接")
