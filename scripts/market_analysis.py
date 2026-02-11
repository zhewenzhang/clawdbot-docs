#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贵金属与A股市场多周期分析
分析日期：2026-02-04
"""

import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta

def get_commodity_data():
    """获取贵金属数据"""
    print("\n" + "=" * 80)
    print("📊 贵金属价格分析")
    print("=" * 80)
    
    # 贵金属 ticker
    tickers = ['GC=F', 'SI=F', 'HG=F', 'PL=F', 'PA=F']
    names = {
        'GC=F': '黄金(COMEX)',
        'SI=F': '白银(COMEX)',
        'HG=F': '铜(LME)',
        'PL=F': '铂金(NYMEX)',
        'PA=F': '钯金(NYMEX)'
    }
    
    # 批量获取
    data = yf.download(tickers, period="6mo", progress=False)['Close']
    
    results = []
    
    for ticker in tickers:
        name = names[ticker]
        df = data[ticker].dropna()
        
        if len(df) >= 60:
            latest = float(df.iloc[-1])
            week_ago = float(df.iloc[-5]) if len(df) >= 5 else latest
            month_ago = float(df.iloc[-20]) if len(df) >= 20 else latest
            quarter_ago = float(df.iloc[-60]) if len(df) >= 60 else latest
            
            week_change = (latest - week_ago) / week_ago * 100
            month_change = (latest - month_ago) / month_ago * 100
            quarter_change = (latest - quarter_ago) / quarter_ago * 100
            
            results.append({
                'name': name,
                'latest': round(latest, 2),
                'week_change': round(week_change, 2),
                'month_change': round(month_change, 2),
                'quarter_change': round(quarter_change, 2)
            })
            
            print(f"\n{name}:")
            print(f"  最新价: {latest:.2f}")
            print(f"  周涨跌: {week_change:+.2f}%")
            print(f"  月涨跌: {month_change:+.2f}%")
            print(f"  季涨跌: {quarter_change:+.2f}%")
    
    return results

def get_a_stock_data():
    """获取A股指数数据"""
    print("\n" + "=" * 80)
    print("📈 A股市场表现分析")
    print("=" * 80)
    
    # A股指数
    indices = {
        '000001.SS': '上证指数',
        '399001.SZ': '深证成指',
        '399006.SZ': '创业板指',
        '000688.SH': '科创50'
    }
    
    results = []
    
    for ticker, name in indices.items():
        try:
            df = yf.download(ticker, period="6mo", progress=False)['Close'].dropna()
            
            if len(df) >= 60:
                latest = float(df.iloc[-1])
                week_ago = float(df.iloc[-5]) if len(df) >= 5 else latest
                month_ago = float(df.iloc[-20]) if len(df) >= 20 else latest
                quarter_ago = float(df.iloc[-60]) if len(df) >= 60 else latest
                
                week_change = (latest - week_ago) / week_ago * 100
                month_change = (latest - month_ago) / month_ago * 100
                quarter_change = (latest - quarter_ago) / quarter_ago * 100
                
                results.append({
                    'name': name,
                    'latest': round(latest, 2),
                    'week_change': round(week_change, 2),
                    'month_change': round(month_change, 2),
                    'quarter_change': round(quarter_change, 2)
                })
                
                print(f"\n{name}:")
                print(f"  最新点位: {latest:.2f}")
                print(f"  周涨跌: {week_change:+.2f}%")
                print(f"  月涨跌: {month_change:+.2f}%")
                print(f"  季涨跌: {quarter_change:+.2f}%")
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    return results

if __name__ == "__main__":
    # 贵金属数据
    commodities = get_commodity_data()
    
    # A股指数
    indices = get_a_stock_data()
    
    # 保存JSON
    data = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'commodities': commodities,
        'indices': indices
    }
    
    with open('/Users/dave/clawd/data/market_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 数据已保存到: /Users/dave/clawd/data/market_analysis.json")
