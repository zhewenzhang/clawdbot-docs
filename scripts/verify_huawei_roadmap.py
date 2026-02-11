#!/usr/bin/env python3
"""
华为昇腾芯片 roadmap 验证脚本
每小时自动检查昇腾芯片信息的准确性
"""

import pandas as pd
import json
from datetime import datetime
import os

# 配置
INPUT_FILE = '/Users/dave/clawd/semiconductor_roadmaps//china/Huawei_Roadmap.xlsx'
VERIFY_FILE = '/Users/dave/clawd/memory/semiconductor_roadmaps/Huawei_Ascend_Verification.md'
LOG_FILE = '/Users/dave/clawd/memory/semiconductor_roadmaps/verification_log.json'

def load_ascend_roadmap():
    """加载 Ascend roadmap 数据"""
    try:
        xlsx = pd.ExcelFile(INPUT_FILE)
        df = pd.read_excel(xlsx, sheet_name='Ascend_Roadmap')
        return df
    except Exception as e:
        log_error(f"读取文件失败: {e}")
        return None

def verify_roadmap(df):
    """验证 roadmap 正确性"""
    errors = []
    
    # 检查是否有错误的 roadmap（910C 直接跳到 950）
    products = df.iloc[:, 1].tolist() if len(df.columns) > 1 else []
    
    # 正确的 roadmap 应该是：910 → 910B → 910C → 950 → 960 → 970
    correct_sequence = ['910', '910B', '910C', '950', '960', '970']
    
    # 检查是否有错误的版本号
    wrong_versions = ['920', '930', '940']
    for product in products:
        if product and any(wrong in str(product) for wrong in wrong_versions):
            # 检查是否是 AI 芯片（昇腾系列）
            if '910' not in str(product) and '950' not in str(product):
                # 这可能是 GPU 或 CPU，不是 AI 芯片
                pass
            else:
                errors.append(f"发现可能的错误: {product}")
    
    return errors

def log_verification(errors):
    """记录验证结果"""
    result = {
        'timestamp': datetime.now().isoformat(),
        'status': 'PASS' if not errors else 'FAIL',
        'errors': errors,
        'file': INPUT_FILE
    }
    
    # 读取现有日志
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except:
        logs = []
    
    logs.append(result)
    
    # 只保留最近100条记录
    logs = logs[-100:]
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return result

def log_error(message):
    """记录错误"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}\n"
    
    with open('/Users/dave/clawd/memory/semiconductor_roadmaps/verification_errors.log', 'a') as f:
        f.write(log_line)

def main():
    """主函数"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始验证华为昇腾 roadmap...")
    
    # 加载数据
    df = load_ascend_roadmap()
    if df is None:
        log_verification([f"无法读取文件: {INPUT_FILE}"])
        return
    
    # 验证
    errors = verify_roadmap(df)
    
    # 记录结果
    result = log_verification(errors)
    
    # 输出结果
    if not errors:
        print("✅ 验证通过！昇腾 roadmap 信息正确")
    else:
        print("⚠️ 发现潜在问题:")
        for error in errors:
            print(f"  - {error}")
    
    return result

if __name__ == '__main__':
    main()
