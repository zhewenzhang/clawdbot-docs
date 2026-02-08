#!/usr/bin/env python3
"""
华为昇腾芯片信息验证脚本
功能: 检查昇腾芯片Roadmap信息的准确性
频率: 每日运行 / 华为大会后触发
"""

import re
import sys
import json
from datetime import datetime
from pathlib import Path

# 正确的昇腾 Roadmap
CORRECT_ROADMAP = {
    "910": {"year": 2019, "status": "已发布"},
    "910B": {"year": 2023, "status": "已发布"},
    "910C": {"year": 2024, "status": "已发布"},
    "950": {"year": 2026, "status": "规划中"},
    "960": {"year": 2027, "status": "规划中"},
    "970": {"year": 2028, "status": "规划中"},
}

# 错误的演进路径（不应出现）
INVALID_PATTERNS = [
    r"昇腾\s*9[23]0",      # 920, 930
    r"Ascend\s*9[23]0",    # Ascend 920, 930
    r"910.*->.*920",
    r"910.*->.*930",
    r"910.*->.*940",
    r"910C.*->.*920",
    r"910C.*->.*930",
    r"910C.*->.*940",
]

def check_file(file_path: str) -> dict:
    """检查单个文件"""
    result = {
        "file": file_path,
        "errors": [],
        "warnings": [],
        "status": "OK"
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result["errors"].append(f"读取文件失败: {e}")
        result["status"] = "ERROR"
        return result
    
    # 检查错误模式
    for pattern in INVALID_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                result["errors"].append(f"发现错误模式: {match}")
            result["status"] = "ERROR"
    
    # 检查昇腾系列完整性
    ascend_pattern = r"昇腾\s*(\d+)"
    found_chips = re.findall(ascend_pattern, content)
    
    for chip in found_chips:
        if chip in CORRECT_ROADMAP:
            continue  # 正确的芯片型号
        elif chip in ["920", "930", "940"]:
            result["errors"].append(f"发现无效芯片型号: 昇腾{chip}")
            result["status"] = "ERROR"
    
    return result

def check_all_files(base_path: str) -> dict:
    """检查所有相关文件"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_files": 0,
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    # 搜索所有md和txt文件
    patterns = ["**/*.md", "**/*.txt"]
    
    for pattern in patterns:
        for file_path in Path(base_path).glob(pattern):
            if "node_modules" in str(file_path):
                continue
            if ".git" in str(file_path):
                continue
                
            results["total_files"] += 1
            result = check_file(str(file_path))
            results["details"].append(result)
            
            if result["status"] == "OK":
                results["passed"] += 1
            else:
                results["failed"] += 1
    
    return results

def generate_report(results: dict) -> str:
    """生成验证报告"""
    report = []
    report.append("=" * 60)
    report.append("华为昇腾芯片信息验证报告")
    report.append(f"验证时间: {results['timestamp']}")
    report.append("=" * 60)
    report.append(f"总计检查文件: {results['total_files']}")
    report.append(f"✅ 通过: {results['passed']}")
    report.append(f"❌ 失败: {results['failed']}")
    report.append("")
    
    for detail in results["details"]:
        if detail["status"] == "ERROR":
            report.append(f"📄 文件: {detail['file']}")
            for error in detail["errors"]:
                report.append(f"   ❌ {error}")
            report.append("")
    
    if results["failed"] == 0:
        report.append("✅ 验证通过！所有文件未发现错误信息。")
    else:
        report.append(f"⚠️ 发现 {results['failed']} 个文件存在问题，请检查！")
    
    report.append("=" * 60)
    
    return "\n".join(report)

def main():
    """主函数"""
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/dave/clawd"
    
    print(f"🔍 开始验证华为昇腾芯片信息...")
    print(f"📁 检查目录: {base_path}")
    print("")
    
    results = check_all_files(base_path)
    report = generate_report(results)
    
    print(report)
    
    # 保存报告
    report_file = f"/Users/dave/clawd/memory/semiconductor_roadmaps/verification_report_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📄 报告已保存: {report_file}")
    
    # 返回退出码
    sys.exit(0 if results["failed"] == 0 else 1)

if __name__ == "__main__":
    main()
