#!/usr/bin/env python3
"""
A股行业资金流向分析系统 v2.0
使用 5000 积分 TuShare API
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import json

# 配置
TOKEN = "18427aa0a10e23a2bf2bf2de0b240aa0005db0629feea9fa2a3bd6a8"
ts.set_token(TOKEN)
pro = ts.pro_api()

def get_industry_money_flow(days=5):
    """获取行业资金流向"""
    
    # 1. 获取所有股票列表
    print("📋 获取A股股票列表...")
    stocks = pro.stock_basic(
        exchange='',
        list_status='L',
        fields='ts_code,name,industry'
    )
    
    print(f"   获取到 {len(stocks)} 只股票")
    
    # 2. 定义重点行业
    target_industries = [
        '半导体', '元件', '电子', '计算机', '通信', '互联网',
        '新能源', '电力设备', '汽车', '医药生物', '食品饮料',
        '银行', '非银金融', '房地产', '传媒', '机械设备'
    ]
    
    # 筛选目标行业
    target_stocks = stocks[stocks['industry'].isin(target_industries)]
    print(f"   目标行业股票: {len(target_stocks)} 只")
    
    # 3. 获取资金流向
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    print(f"\n📈 获取资金流向数据 ({start_date} ~ {end_date})...")
    
    results = []
    
    # 限制数量，避免 API 调用过多
    sample_stocks = target_stocks.head(50)
    
    for idx, row in sample_stocks.iterrows():
        try:
            df = pro.moneyflow(
                symbol=row['ts_code'],
                start_date=start_date
            )
            
            if len(df) > 0:
                # 计算指标
                net_inflow = df['net_inflow'].sum() if 'net_inflow' in df.columns else 0
                main_net = df['main_net_inflow'].sum() if 'main_net_inflow' in df.columns else 0
                retail_net = df['retail_net_inflow'].sum() if 'retail_net_inflow' in df.columns else 0
                
                results.append({
                    '股票代码': row['ts_code'],
                    '股票名称': row['name'],
                    '行业': row['industry'],
                    '净流入': net_inflow,
                    '主力净流入': main_net,
                    '散户净流入': retail_net,
                    '数据条数': len(df)
                })
                
                print(f"   ✅ {row['ts_code']} {row['name']}: {net_inflow:,.0f}")
                
        except Exception as e:
            print(f"   ❌ {row['ts_code']} {row['name']}: {str(e)[:50]}")
            continue
        
        # 避免请求过快
        # time.sleep(0.1)
    
    return pd.DataFrame(results)

def analyze_by_industry(df):
    """按行业汇总分析"""
    
    if df.empty:
        return pd.DataFrame()
    
    # 按行业分组
    industry_summary = df.groupby('行业').agg({
        '净流入': 'sum',
        '主力净流入': 'sum',
        '散户净流入': 'sum',
        '股票代码': 'count'
    }).reset_index()
    
    industry_summary.columns = ['行业', '净流入', '主力净流入', '散户净流入', '股票数']
    
    # 计算主力占比
    industry_summary['主力占比'] = industry_summary['主力净流入'] / (industry_summary['净流入'] + 0.01) * 100
    
    # 按净流入排序
    industry_summary = industry_summary.sort_values('净流入', ascending=False)
    
    return industry_summary

def generate_report(df, industry_summary, days=5):
    """生成报告"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""
================================================================================
                      A股行业资金流向分析报告
================================================================================
报告日期: {today}
分析周期: 最近 {days} 个交易日
================================================================================

【整体概览】
分析样本: {len(df)} 只股票
覆盖行业: {industry_summary['行业'].nunique()} 个

【资金流向汇总】
"""
    
    print(report)
    
    # 打印行业汇总
    print("-" * 80)
    print(f"{'行业':<15} {'净流入(万)':>15} {'主力占比':>10} {'股票数':>8}")
    print("-" * 80)
    
    for _, row in industry_summary.iterrows():
        net = row['净流入'] / 10000  # 转换为亿
        main_pct = row['主力占比'] if row['主力占比'] > 0 else 0
        print(f"{row['行业']:<15} {net:>12.2f}亿 {main_pct:>8.1f}% {int(row['股票数']):>8}")
    
    print("-" * 80)
    
    # 识别资金正在流入的行业
    inflow_industries = industry_summary[industry_summary['净流入'] > 0]
    outflow_industries = industry_summary[industry_summary['净流入'] < 0]
    
    report2 = f"""

【刚开始吸引资金的行业】
"""
    print(report2)
    
    for _, row in inflow_industries.head(5).iterrows():
        net = row['净流入'] / 10000
        print(f"  🔵 {row['行业']}: +{net:.2f}亿 ({row['股票数']}只)")
    
    report3 = f"""

【资金流出的行业】
"""
    print(report3)
    
    for _, row in outflow_industries.head(5).iterrows():
        net = row['净流入'] / 10000
        print(f"  🔴 {row['行业']}: {net:.2f}亿 ({row['股票数']}只)")
    
    # 个股资金排行榜
    top_stocks = df.nlargest(10, '净流入')
    bottom_stocks = df.nsmallest(10, '净流入')
    
    report4 = f"""

【资金流入最多的股票 TOP 10】
"""
    print(report4)
    
    for idx, row in top_stocks.iterrows():
        net = row['净流入'] / 10000
        print(f"  📈 {row['股票代码']} {row['股票名称']}: +{net:.2f}亿")
    
    report5 = f"""

【资金流出最多的股票 TOP 10】
"""
    print(report5)
    
    for idx, row in bottom_stocks.iterrows():
        net = row['净流入'] / 10000
        print(f"  📉 {row['股票代码']} {row['股票名称']}: {net:.2f}亿")
    
    print("\n" + "=" * 80)
    print("报告生成时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 80)
    
    return industry_summary

def main():
    """主函数"""
    
    print("\n" + "=" * 80)
    print("              A股行业资金流向分析系统 v2.0")
    print("=" * 80)
    print()
    
    # 获取数据
    df = get_industry_money_flow(days=5)
    
    if df.empty:
        print("\n❌ 无法获取资金流向数据")
        return
    
    # 按行业汇总
    industry_summary = analyze_by_industry(df)
    
    # 生成报告
    generate_report(df, industry_summary, days=5)
    
    # 保存数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    df.to_csv(f'/Users/dave/clawd/data/money_flow/stock_flow_{timestamp}.csv', index=False)
    industry_summary.to_csv(f'/Users/dave/clawd/data/money_flow/industry_flow_{timestamp}.csv', index=False)
    
    print(f"\n✅ 数据已保存:")
    print(f"   - /Users/dave/clawd/data/money_flow/stock_flow_{timestamp}.csv")
    print(f"   - /Users/dave/clawd/data/money_flow/industry_flow_{timestamp}.csv")

if __name__ == '__main__':
    main()
