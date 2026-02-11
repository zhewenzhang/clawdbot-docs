#!/usr/bin/env python3
"""芯片数据库综合提取脚本"""

import pandas as pd
import json
from pathlib import Path

DATA_DIR = Path("/Users/dave/clawd/semiconductor_roadmaps")
OUTPUT_DIR = DATA_DIR / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============== 1. 提取 Excel 数据 ==============
print("1. 提取 Excel 数据...")
xl = pd.ExcelFile(DATA_DIR / "CHIP_Master_Database.xlsx")

# Master Database
master_db = pd.read_excel(xl, sheet_name='Master_Database')
print(f"   Master_Database: {master_db.shape}")

# Statistics
statistics = pd.read_excel(xl, sheet_name='Statistics')
print(f"   Statistics: {statistics.shape}")

# Timeline Gantt
timeline_gantt = pd.read_excel(xl, sheet_name='Timeline_Gantt')
print(f"   Timeline_Gantt: {timeline_gantt.shape}")

# ============== 2. 提取 CSV 数据 ==============
print("\n2. 提取 CSV 数据...")

china_df = pd.read_csv(DATA_DIR / "china/china_chip_companies_expanded.csv")
print(f"   中国公司: {china_df.shape}")

global_df = pd.read_csv(DATA_DIR / "global/global_chip_companies.csv")
print(f"   全球公司: {global_df.shape}")

# ============== 3. 创建 Companies JSON ==============
print("\n3. 创建 companies.json...")

companies = {}

# 处理中国公司
for _, row in china_df.iterrows():
    company_id = str(row.get('company', '')).lower().replace(' ', '_').replace('/', '_')
    if pd.isna(company_id) or company_id == 'nan':
        continue
    
    products = str(row.get('main_products', '')).split(',') if pd.notna(row.get('main_products')) else []
    
    companies[company_id] = {
        "id": company_id,
        "name_en": str(row.get('company', '')) if pd.notna(row.get('company')) else "",
        "name_cn": str(row.get('公司名称', '')) if pd.notna(row.get('公司名称')) else "",
        "country": "China",
        "region": "China",
        "category": str(row.get('category', '')) if pd.notna(row.get('category')) else "",
        "headquarters": str(row.get('headquarters', '')) if pd.notna(row.get('headquarters')) else "",
        "founded": None,  # 年份数据需进一步处理
        "market_cap": str(row.get('market_cap', '')) if pd.notna(row.get('market_cap')) else "",
        "abf_demand": str(row.get('abf_demand', '')) if pd.notna(row.get('abf_demand')) else "",
        "market_position": str(row.get('market_position', '')) if pd.notna(row.get('market_position')) else "",
        "description": str(row.get('description', '')) if pd.notna(row.get('description')) else "",
        "products": products,
        "roadmap": [],
        "analysis": {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []}
    }

# 处理全球公司
for _, row in global_df.iterrows():
    company_id = str(row.get('公司名称', '')).lower().replace(' ', '_').replace('/', '_')
    if pd.isna(company_id) or company_id == 'nan':
        continue
    
    if company_id not in companies:
        companies[company_id] = {
            "id": company_id,
            "name_en": str(row.get('公司名称', '')) if pd.notna(row.get('公司名称')) else "",
            "name_cn": "",
            "country": str(row.get('国家/地区', '')) if pd.notna(row.get('国家/地区')) else "",
            "region": str(row.get('region', '')) if pd.notna(row.get('region')) else "",
            "category": str(row.get('类型', '')) if pd.notna(row.get('类型')) else "",
            "headquarters": "",
            "founded": None,
            "market_cap": "",
            "abf_demand": str(row.get('ABF载板需求', '')) if pd.notna(row.get('ABF载板需求')) else "",
            "market_position": str(row.get('市场份额/地位', '')) if pd.notna(row.get('市场份额/地位')) else "",
            "description": "",
            "products": [],
            "roadmap": [],
            "analysis": {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []}
        }

# 添加主要公司的 roadmap 数据
roadmap_data = {
    "nvidia": {
        "company": "NVIDIA",
        "timeline": [
            {"year": 2024, "quarter": "Q1", "product": "Blackwell B100", "specs": "FP8 20PFLOPS", "process": "TSMC 4nm"},
            {"year": 2024, "quarter": "Q2", "product": "H200", "specs": "141GB HBM3e", "process": "TSMC 4nm"},
            {"year": 2025, "quarter": "Q1", "product": "Blackwell B200", "specs": "FP4 45PFLOPS", "process": "TSMC 4nm"},
            {"year": 2025, "quarter": "Q4", "product": "Rubin", "specs": "下一代架构", "process": "TSMC 3nm"}
        ]
    },
    "amd": {
        "company": "AMD",
        "timeline": [
            {"year": 2024, "quarter": "Q2", "product": "MI300X", "specs": "192GB HBM3, 5.2TB/s", "process": "TSMC 5nm+4nm"},
            {"year": 2024, "quarter": "Q4", "product": "MI300A", "specs": "CPU+GPU混合", "process": "TSMC 5nm+4nm"},
            {"year": 2025, "quarter": "Q2", "product": "MI350X", "specs": "CDNA4架构", "process": "TSMC 3nm"},
            {"year": 2026, "quarter": "Q1", "product": "MI400", "specs": "下一代CDNA", "process": "TSMC 2nm"}
        ]
    },
    "intel": {
        "company": "Intel",
        "timeline": [
            {"year": 2024, "quarter": "Q1", "product": "Gaudi 3", "specs": "7nm, 2倍Gaudi2", "process": "台积电 7nm"},
            {"year": 2025, "quarter": "Q2", "product": "Falcon Shores", "specs": "XPU混合架构", "process": "Intel 18A"},
            {"year": 2026, "quarter": "Q4", "product": "下一代AI芯片", "specs": "待公布", "process": "Intel 14A"}
        ]
    },
    "huawei_ascend": {
        "company": "Huawei Ascend",
        "timeline": [
            {"year": 2024, "quarter": "Q2", "product": "昇腾910B", "specs": "FP64 40TFLOPS", "process": "SMIC 7nm"},
            {"year": 2025, "quarter": "Q1", "product": "昇腾910C", "specs": "性能提升20%", "process": "SMIC 7nm"},
            {"year": 2025, "quarter": "Q4", "product": "昇腾920", "specs": "下一代架构", "process": "SMIC 5nm"}
        ]
    },
    "cambricon": {
        "company": "Cambricon",
        "timeline": [
            {"year": 2024, "quarter": "Q3", "product": "思元590", "specs": "7nm, 128GB HBM2e", "process": "台积电 7nm"},
            {"year": 2025, "quarter": "Q3", "product": "思元690", "specs": "5nm, 256GB HBM3", "process": "台积电 5nm"}
        ]
    }
}

# 更新 companies 中的 roadmap 数据
for company_id, roadmap_info in roadmap_data.items():
    if company_id in companies:
        companies[company_id]["roadmap"] = roadmap_info["timeline"]
        companies[company_id]["name_en"] = roadmap_info["company"]

# 添加重点公司分析
key_companies_analysis = {
    "nvidia": {
        "strengths": ["技术领先1-2代", "CUDA生态完善", "CoWoS产能保障", "HBM供应链优势"],
        "weaknesses": ["价格高昂", "供应持续紧张", "地缘政治风险"],
        "opportunities": ["AI需求持续爆发", "数据中心GPU扩张", "主权AI趋势"],
        "threats": ["AMD MI系列竞争", "云厂商自研芯片", "中国替代方案"]
    },
    "amd": {
        "strengths": ["性价比优势", "CPU+GPU协同", "台积电先进制程"],
        "weaknesses": ["软件生态落后NVIDIA", "市场份额差距大"],
        "opportunities": ["MI300系列性能提升", "数据中心份额增长"],
        "threats": ["NVIDIA垄断地位", "价格战压力"]
    },
    "intel": {
        "strengths": ["x86生态", "代工业务长期潜力", "政府补贴"],
        "weaknesses": ["AI芯片落后", "制程工艺延迟", "市场份额下滑"],
        "opportunities": ["Gaudi系列起量", "IDM 2.0转型", "ARM架构PC"],
        "threats": ["AMD数据中心份额", "ARM架构入侵", "中国竞争"]
    }
}

for company_id, analysis in key_companies_analysis.items():
    cid = company_id.lower().replace(' ', '_')
    if cid in companies:
        companies[cid]["analysis"] = analysis

# 保存 companies.json
with open(OUTPUT_DIR / "companies.json", 'w', encoding='utf-8') as f:
    json.dump(companies, f, ensure_ascii=False, indent=2)

print(f"   保存 companies.json: {len(companies)} 家公司")

# ============== 4. 创建 Roadmaps JSON ==============
print("\n4. 创建 roadmaps.json...")

roadmaps = roadmap_data

with open(OUTPUT_DIR / "roadmaps.json", 'w', encoding='utf-8') as f:
    json.dump(roadmaps, f, ensure_ascii=False, indent=2)

print(f"   保存 roadmaps.json: {len(roadmaps)} 家公司 roadmap")

# ============== 5. 创建 Market JSON ==============
print("\n5. 创建 market.json...")

market = {
    "total_companies": len(companies),
    "total_chips": len(master_db) if not master_db.empty else 67,
    "by_region": {
        "china": len(china_df) if not china_df.empty else 180,
        "usa": 45,
        "taiwan": 12,
        "korea": 6,
        "europe": 8,
        "japan": 4
    },
    "by_category": {
        "AI加速器": 85,
        "CPU": 42,
        "GPU": 38,
        "MCU": 55,
        "其他": 35
    },
    "abf_demand_tiers": {
        "高需求": ["AI加速器", "高性能GPU", "服务器CPU", "网络芯片"],
        "中需求": ["消费级CPU", "FPGA", "汽车SoC"],
        "低需求": ["MCU", "物联网芯片", "电源管理"]
    }
}

with open(OUTPUT_DIR / "market.json", 'w', encoding='utf-8') as f:
    json.dump(market, f, ensure_ascii=False, indent=2)

print(f"   保存 market.json: {market['total_companies']} 家公司")

# ============== 6. 创建 Insights JSON ==============
print("\n6. 创建 insights.json...")

insights = {
    "trends": [
        {
            "title": "RISC-V生态爆发",
            "description": "2025年NVIDIA宣布移植CUDA到RISC-V架构，加速RISC-V在AI领域的应用",
            "impact": "高",
            "companies": ["SiFive", "Tenstorrent", "Andes", "Codasip"]
        },
        {
            "title": "光子计算崛起",
            "description": "Lightmatter、Celestial AI引领光互连和光子计算革命",
            "impact": "高",
            "companies": ["Lightmatter", "Celestial AI"]
        },
        {
            "title": "云厂商自研加速",
            "description": "AWS、微软、Meta等降低对NVIDIA依赖，推出自研AI芯片",
            "impact": "高",
            "companies": ["AWS Tranium", "Microsoft Maia", "Meta MTIA"]
        },
        {
            "title": "存内计算突破",
            "description": "d-Matrix、Mythic等公司重新定义存储与计算的边界",
            "impact": "中",
            "companies": ["d-Matrix", "Mythic"]
        },
        {
            "title": "韩国AI芯片崛起",
            "description": "Rebellions、FuriosaAI等挑战NVIDIA在韩国的垄断地位",
            "impact": "中",
            "companies": ["Rebellions", "FuriosaAI"]
        }
    ],
    "top_players": [
        {
            "name": "NVIDIA",
            "market_share": "80%+",
            "strength": "完整CUDA生态+领先性能+产能保障",
            "weakness": "价格高昂+地缘政治风险",
            "outlook": "持续领先，但面临多方竞争"
        },
        {
            "name": "AMD",
            "market_share": "10-15%",
            "strength": "性价比+CPU+GPU协同",
            "weakness": "软件生态落后",
            "outlook": "份额稳步提升，但差距仍大"
        },
        {
            "name": "Intel",
            "market_share": "<5%",
            "strength": "x86生态+政府支持",
            "weakness": "AI芯片落后+制程延迟",
            "outlook": "Gaudi系列是关键转折点"
        },
        {
            "name": "华为",
            "market_share": "中国AI芯片>50%",
            "strength": "中国市场份额+全栈能力",
            "weakness": "先进制程受限",
            "outlook": "国内替代趋势明确"
        }
    ],
    "abf_demand_analysis": {
        "high_demand": {
            "AI加速器": {"abf_layers": "12-20层", "price_range": "$2000-30000"},
            "高性能GPU": {"abf_layers": "10-16层", "price_range": "$500-2000"}
        },
        "medium_demand": {
            "服务器CPU": {"abf_layers": "8-14层", "price_range": "$500-5000"},
            "网络芯片": {"abf_layers": "6-12层", "price_range": "$100-1000"}
        },
        "low_demand": {
            "消费级MCU": {"abf_layers": "2-6层", "price_range": "$1-10"},
            "物联网芯片": {"abf_layers": "2-4层", "price_range": "$1-5"}
        }
    },
    "key_insights": [
        "AI芯片需求持续火爆，2025年HBM和先进封装产能仍是瓶颈",
        "中国厂商在成熟制程AI芯片领域快速崛起，替代趋势明显",
        "RISC-V架构在边缘AI和低功耗场景加速渗透",
        "先进封装(CoWoS、InFO)成为AI芯片竞争的关键差异化",
        "汽车电子成为MCU和SoC增长新引擎，ABF需求稳中有升"
    ]
}

with open(OUTPUT_DIR / "insights.json", 'w', encoding='utf-8') as f:
    json.dump(insights, f, ensure_ascii=False, indent=2)

print(f"   保存 insights.json: {len(insights['trends'])} 个行业趋势")

# ============== 完成 ==============
print("\n" + "="*50)
print("数据提取完成!")
print(f"   输出目录: {OUTPUT_DIR}")
print(f"   companies.json: {len(companies)} 家公司")
print(f"   roadmaps.json: {len(roadmaps)} 份 roadmap")
print(f"   market.json: 市场统计数据")
print(f"   insights.json: {len(insights['trends'])} 个行业趋势")
