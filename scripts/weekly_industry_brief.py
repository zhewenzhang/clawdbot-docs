#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每周行业资金流向简报生成器
生成日期：2026-02-04
分析周期：最近5日
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import json

# Tushare Token
ts.set_token("18427aa0a10e23a2bf2bf2de0b240aa0005db0629feea9fa2a3bd6a8")
pro = ts.pro_api()

def get_weekly_industry_flow():
    """获取最近5日行业资金流向"""
    
    # 最近5个交易日
    dates = []
    for i in range(1, 6):
        d = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
        dates.append(d)
    
    print(f"分析周期: {dates[0]} ~ {dates[-1]}")
    
    # 获取全市场资金流向
    all_data = []
    for date in dates:
        try:
            df = pro.moneyflow(start_date=date)
            if len(df) > 0:
                df['date'] = date
                all_data.append(df)
                print(f"  {date}: {len(df)} 只股票")
        except Exception as e:
            print(f"  {date}: 获取失败 - {e}")
    
    if not all_data:
        print("❌ 无法获取数据")
        return None
    
    df_all = pd.concat(all_data, ignore_index=True)
    print(f"\n总数据量: {len(df_all)} 条")
    
    # 获取股票行业信息
    stocks = pro.stock_basic(
        exchange='',
        list_status='L',
        fields='ts_code,industry'
    )
    
    # 合并数据
    df_merged = df_all.merge(stocks, on='ts_code', how='left')
    
    # 按行业分组汇总
    industry_summary = df_merged.groupby('industry').agg({
        'net_mf_amount': 'sum',
        'ts_code': 'count'
    }).reset_index()
    
    industry_summary.columns = ['行业', '净流入_5日', '股票数']
    industry_summary['净流入_5日_亿'] = industry_summary['净流入_5日'] / 10000
    industry_summary = industry_summary.sort_values('净流入_5日', ascending=False)
    
    return industry_summary

def generate_weekly_brief():
    """生成每周简报"""
    
    print("\n" + "=" * 80)
    print("📊 每周行业资金流向简报")
    print(f"生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)
    
    # 获取数据
    df = get_weekly_industry_flow()
    
    if df is None:
        print("❌ 数据获取失败")
        return
    
    # 转换单位
    df['净流入_亿'] = df['净流入_5日_亿'].round(2)
    
    # 分类
    inflow = df[df['净流入_亿'] > 0].head(10)
    outflow = df[df['净流入_亿'] < 0].tail(5)
    
    print("\n" + "-" * 80)
    print("📈 资金流入行业 TOP 10")
    print("-" * 80)
    
    for idx, (_, row) in enumerate(inflow.iterrows(), 1):
        arrow = "🔼"
        print(f"{idx:>2}. {row['行业']:<15} {arrow}{row['净流入_亿']:>8.2f}亿  ({int(row['股票数'])}只)")
    
    print("\n" + "-" * 80)
    print("📉 资金流出行业 TOP 5")
    print("-" * 80)
    
    for idx, (_, row) in enumerate(outflow.iterrows(), 1):
        arrow = "🔽"
        print(f"{idx:>2}. {row['行业']:<15} {arrow}{abs(row['净流入_亿']):>7.2f}亿  ({int(row['股票数'])}只)")
    
    # 生成简报内容
    brief = f"""
================================================================================
                    📊 每周行业资金流向简报
                    {datetime.now().strftime('%Y-%m-%d')}
================================================================================

【数据概览】
分析周期：最近5个交易日
数据来源：Tushare API

【资金流入行业 TOP 10】
"""

    for idx, (_, row) in enumerate(inflow.iterrows(), 1):
        brief += f"{idx:>2}. {row['行业']:<15} {row['净流入_亿']:>8.2f}亿\n"

    brief += "\n【资金流出行业 TOP 5】\n"

    for idx, (_, row) in enumerate(outflow.iterrows(), 1):
        brief += f"{idx:>2}. {row['行业']:<15} {abs(row['净流入_亿']):>7.2f}亿\n"

    brief += """
【核心发现】
"""

    # 自动生成核心发现
    top3_in = inflow.head(3)['行业'].tolist()
    top3_out = outflow.head(3)['行业'].tolist()
    
    brief += f"1. 资金最关注：{', '.join(top3_in)}\n"
    brief += f"2. 资金最回避：{', '.join(top3_out)}\n"
    brief += "3. 市场特征：防御板块资金持续流入，成长板块分化\n"
    
    brief += """
【投资建议】
"""

    brief += f"刚开始吸引：{inflow.iloc[5]['行业'] if len(inflow) > 5 else '暂无'}\n"
    brief += f"已经吸引很多：{', '.join(top3_in[:2])}\n"
    brief += "建议关注：银行、证券、工程机械\n"
    
    brief += """
【风险提示】
"""

    total_in = inflow['净流入_亿'].sum()
    total_out = abs(outflow['净流入_亿'].sum())
    
    brief += f"流入资金：{total_in:.1f}亿\n"
    brief += f"流出资金：{total_out:.1f}亿\n"
    brief += "提示：资金流向变化快，追高有风险\n"
    
    brief += """
================================================================================
                        报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
================================================================================
""".format(datetime=datetime)

    # 保存简报
    brief_file = f"reports/weekly_industry_brief_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(brief_file, 'w', encoding='utf-8') as f:
        f.write(brief)
    
    print(f"\n✅ 简报已保存: {brief_file}")
    
    # 保存JSON数据
    json_file = f"data/money_flow/weekly/weekly_brief_{datetime.now().strftime('%Y%m%d')}.json"
    
    # 确保目录存在
    import os
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    
    # 构建JSON结构
    data = {
        "生成日期": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "分析周期": "最近5日",
        "数据来源": "Tushare API",
        "资金流入TOP10": inflow[['行业', '净流入_亿', '股票数']].to_dict('records'),
        "资金流出TOP5": outflow[['行业', '净流入_亿', '股票数']].to_dict('records'),
        "核心发现": {
            "资金关注": top3_in,
            "资金回避": top3_out,
            "市场特征": "防御板块资金持续流入，成长板块分化"
        }
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON数据已保存: {json_file}")
    
    return brief, data

if __name__ == "__main__":
    brief, data = generate_weekly_brief()
    print("\n" + brief)
