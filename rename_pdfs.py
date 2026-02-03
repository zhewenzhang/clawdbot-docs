#!/usr/bin/env python3
"""
PDF 文件命名规范化工具
格式: 类别-区域-文件内容-来源-日期.pdf

使用 MiniMax 模型分析 PDF 内容并智能命名
"""

import os
import subprocess
import json

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

def extract_pdf_text(pdf_path, max_pages=3):
    """提取 PDF 文本内容"""
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:max_pages]:
                text += page.extract_text() + "\n"
            return text[:3000]  # 限制文本长度
    except Exception as e:
        print(f"提取文本失败: {e}")
        return None

def analyze_with_minimax(content):
    """调用 MiniMax 模型分析 PDF 内容"""
    # 这里可以集成 MiniMax API 来智能分析
    # 目前使用简单的规则匹配
    content_lower = content.lower()
    
    # 关键词匹配规则
    rules = {
        "Semiconductor": ["semiconductor", "chip", "gpu", "tpu", "asic", "memory", "dram", "nand", "foundry", "wafer"],
        "Basic-Materials": ["materials", "steel", "copper", "aluminum", "coal", "iron ore", "commodity"],
        "Advanced-Packaging": ["packaging", "coWos", "2.5d", "3d", "hybrid bonding", "tsv"],
        "Automotive": ["automotive", "ev", "electric vehicle", "battery", "nev"],
        "AI": ["ai", "artificial intelligence", "machine learning", "neural"]
    }
    
    regions = {
        "CN": ["china", "chinese", "nbs", "shanghai", "beijing"],
        "WW": ["global", "worldwide", "asia pacific", "asia-pacific"],
        "TW": ["taiwan", "nt$", "twse"]
    }
    
    sources = {
        "JPMorgan": ["j.p. morgan", "jpmorgan", "jpmorgan securities"],
        "MorganStanley": ["morgan stanley", "morganstanley"],
        "GoldmanSachs": ["goldman sachs", "goldmansachs"],
        "Citi": ["citi", "citigroup"],
        "DeutscheBank": ["deutsche bank"],
        "UBS": ["ubs"],
        "IMEC": ["imec"]
    }
    
    # 分析类别
    category = "General"
    for cat, keywords in rules.items():
        if any(kw in content_lower for kw in keywords):
            category = cat
            break
    
    # 分析区域
    region = "WW"
    for reg, keywords in regions.items():
        if any(kw in content_lower for kw in keywords):
            region = reg
            break
    
    # 分析来源
    source = "Unknown"
    for src, keywords in sources.items():
        if any(kw in content_lower for kw in keywords):
            source = src
            break
    
    return category, region, source

def get_file_date(pdf_path):
    """从文件修改时间获取日期"""
    timestamp = os.path.getmtime(pdf_path)
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime("%Y%m%d")

def rename_pdfs():
    """重命名 PDF 文件"""
    pdf_files = [f for f in os.listdir(DOWNLOADS_DIR) if f.lower().endswith('.pdf')]
    
    print("="*60)
    print("📁 PDF 文件命名规范化")
    print("="*60)
    
    for old_name in pdf_files:
        # 跳过已经是规范命名的文件
        parts = old_name.replace('.pdf', '').split('-')
        if len(parts) >= 5 and parts[0] in ["Semiconductor", "Basic-Materials", "Advanced-Packaging", "AI", "Automotive", "General"]:
            print(f"⏭️  已是规范名称: {old_name}")
            continue
        
        old_path = os.path.join(DOWNLOADS_DIR, old_name)
        
        print(f"\n📄 处理: {old_name}")
        
        # 提取文本并分析
        content = extract_pdf_text(old_path)
        if content:
            category, region, source = analyze_with_minimax(content)
        else:
            category, region, source = "Unknown", "CN", "Unknown"
        
        # 生成新名称
        content_name = old_name.replace('.pdf', '').replace(' ', '-')[:30]
        date = get_file_date(old_path)
        new_name = f"{category}-{region}-{content_name}-{source}-{date}.pdf"
        new_path = os.path.join(DOWNLOADS_DIR, new_name)
        
        if old_name != new_name:
            os.rename(old_path, new_path)
            print(f"  ✅ → {new_name}")
        else:
            print(f"  ⏭️  保持原名")
        
        print(f"  📌 类别: {category} | 区域: {region} | 来源: {source}")
    
    print("\n" + "="*60)
    print("✅ 处理完成")
    print("="*60)

if __name__ == "__main__":
    rename_pdfs()
