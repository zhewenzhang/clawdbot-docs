#!/usr/bin/env python3
"""
Excel 文件索引生成器
扫描 clawd 目录下的所有 xlsx 文件，生成 JSON 索引
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path

# 配置
ROOT_DIR = "/Users/dave/clawd"
OUTPUT_FILE = "/Users/dave/clawd/docs/excel_index.json"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/zhewenzhang/clawdbot-docs/main"

def get_file_info(file_path):
    """获取文件详细信息"""
    stat = os.stat(file_path)
    return {
        "name": os.path.basename(file_path),
        "path": file_path,
        "size": stat.st_size,
        "size_kb": round(stat.st_size / 1024, 1),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "modified_timestamp": int(stat.st_mtime),
        "url": f"{GITHUB_RAW_URL}/{os.path.basename(file_path)}"
    }

def scan_xlsx_files():
    """扫描所有 xlsx 文件"""
    files = []
    
    # 扫描根目录
    root_files = glob.glob(os.path.join(ROOT_DIR, "*.xlsx"))
    for f in root_files:
        info = get_file_info(f)
        info["location"] = "root"
        info["description"] = get_description(info["name"])
        files.append(info)
    
    # 扫描子目录 (memory/semiconductor_roadmaps 等)
    for subdir in ["memory", "docs", "output"]:
        subdir_path = os.path.join(ROOT_DIR, subdir)
        if os.path.exists(subdir_path):
            sub_files = glob.glob(os.path.join(subdir_path, "**/*.xlsx"), recursive=True)
            for f in sub_files:
                info = get_file_info(f)
                info["location"] = subdir
                info["description"] = get_description(info["name"])
                files.append(info)
    
    return sorted(files, key=lambda x: (-x["size"], x["name"]))

def get_description(filename):
    """根据文件名生成描述"""
    descriptions = {
        "Roadmap_Summary": "半导体 Roadmap 汇总表",
        "China_Semiconductor_Fab_Map": "中国半导体晶圆厂分布图",
        "CoWoS_Capacity_2026": "2026年 CoWoS 产能预测",
        "Competitor_Roadmaps": "竞争对手路线图",
        "NVIDIA_Roadmap": "NVIDIA 产品路线图",
        "TPU_ASIC_Analysis": "TPU/ASIC 分析数据",
        "ABF_TAM_history": "ABF 市场历史数据",
        "ABF_supplier_capacity": "ABF 供应商产能",
        "ABF_customer_demand": "ABF 客户需求",
    }
    
    for key, desc in descriptions.items():
        if key.lower() in filename.lower():
            return desc
    
    return "Excel 数据文件"

def generate_index():
    """生成索引"""
    files = scan_xlsx_files()
    
    index = {
        "version": "1.0",
        "lastUpdate": datetime.now().isoformat(),
        "lastUpdateTimestamp": int(datetime.now().timestamp()),
        "totalFiles": len(files),
        "dashboardUrl": "https://zhewenzhang.github.io/clawdbot-docs/dashboard.html",
        "files": files
    }
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 写入 JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成索引: {OUTPUT_FILE}")
    print(f"   文件数量: {len(files)}")
    
    return index

if __name__ == "__main__":
    generate_index()
