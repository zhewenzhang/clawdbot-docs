#!/usr/bin/env python3
"""
贵金属价格和A股市场多周期分析 - 增强版
执行日期: 2026-02-04
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============ 配置 ============
TODAY = datetime.now()
ANALYSIS_DAYS = {
    '本周': 5,
    '本月': 20,
    '本季': 60,
    '半年': 120
}

# ============ 贵金属配置 ============
PRECIOUS_METALS = {
    'COMEX黄金': 'GC=F',
    'COMEX白银': 'SI=F',
    'LME铜': 'HG=F',
    'NYMEX铂金': 'PL=F',
    'NYMEX钯金': 'PA=F',
}

# ============ A股指数配置 ============
CHINA_INDICES = {
    '上证指数': '000001.SS',
    '深证成指': '399001.SZ',
    '创业板指': '399006.SZ',
    '科创50': '000688.SS',
    '沪深300': '000300.SS',
}

# ============ A股行业板块配置 ============
SECTORS = {
    '中证银行': '399986.SZ',
    '证券公司': '399905.SZ',
    '中证白酒': '399997.SZ',
    '中证医药': '399300.SZ',
    '新能源': '000941.SS',
    '中证半导体': '399811.SZ',
    '中证人工智能': '931071.CS',
    '先进制造': '931126.CS',
}

# ============ 数据获取函数 ============
def get_data(ticker, days=120):
    """获取历史数据"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            end_date = TODAY
            start_date = end_date - timedelta(days=days + 30)
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, timeout=10)
            if data.empty:
                continue
            
            # 处理多级列索引
            if isinstance(data.columns, pd.MultiIndex):
                if 'Close' in data.columns.get_level_values(0):
                    close_prices = data['Close']
                    if isinstance(close_prices, pd.DataFrame):
                        close_prices = close_prices.iloc[:, 0]
                else:
                    close_prices = data.iloc[:, 0]
            else:
                close_prices = data['Close'] if 'Close' in data.columns else data.iloc[:, 0]
            
            return close_prices
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"获取 {ticker} 数据失败: {e}")
            continue
    return None

def calculate_returns(prices, days):
    """计算指定周期的涨跌幅"""
    if prices is None or len(prices) < days:
        return None
    recent_prices = prices.tail(days)
    if len(recent_prices) < 2:
        return None
    
    try:
        start_price = float(recent_prices.iloc[0])
        end_price = float(recent_prices.iloc[-1])
    except:
        return None
    
    if start_price == 0 or np.isnan(start_price) or np.isnan(end_price):
        return None
    return ((end_price - start_price) / start_price) * 100

def get_latest_price(prices):
    """获取最新价格"""
    if prices is None or len(prices) == 0:
        return None
    try:
        latest = prices.iloc[-1]
        if isinstance(latest, (pd.Series, np.ndarray)):
            latest = latest.iloc[0] if len(latest) > 0 else None
        return float(latest) if latest is not None else None
    except:
        return None

# ============ 主分析流程 ============
def analyze_precious_metals():
    """分析贵金属"""
    results = {}
    print("=" * 60)
    print("【贵金属价格分析】")
    print("=" * 60)
    
    for name, ticker in PRECIOUS_METALS.items():
        prices = get_data(ticker)
        if prices is not None:
            latest = get_latest_price(prices)
            returns = {
                period: calculate_returns(prices, days) 
                for period, days in ANALYSIS_DAYS.items()
            }
            results[name] = {
                'ticker': ticker,
                'latest_price': latest,
                'returns': returns
            }
            print(f"\n{name} ({ticker}):")
            print(f"  最新价: {latest:.4f}" if latest else "  最新价: N/A")
            for period, ret in returns.items():
                if ret is not None:
                    trend = "↑" if ret > 0 else "↓"
                    print(f"  {period}涨跌: {trend} {ret:.2f}%")
                else:
                    print(f"  {period}涨跌: N/A")
    
    return results

def analyze_china_indices():
    """分析A股指数"""
    results = {}
    print("\n" + "=" * 60)
    print("【A股市场表现分析】")
    print("=" * 60)
    
    for name, ticker in CHINA_INDICES.items():
        prices = get_data(ticker)
        if prices is not None:
            latest = get_latest_price(prices)
            returns = {
                period: calculate_returns(prices, days) 
                for period, days in ANALYSIS_DAYS.items()
            }
            results[name] = {
                'ticker': ticker,
                'latest_price': latest,
                'returns': returns
            }
            print(f"\n{name} ({ticker}):")
            print(f"  最新价: {latest:.4f}" if latest else "  最新价: N/A")
            for period, ret in returns.items():
                if ret is not None:
                    trend = "↑" if ret > 0 else "↓"
                    print(f"  {period}涨跌: {trend} {ret:.2f}%")
                else:
                    print(f"  {period}涨跌: N/A")
    
    return results

def analyze_sectors():
    """分析行业板块"""
    results = {}
    print("\n" + "=" * 60)
    print("【行业板块表现分析】")
    print("=" * 60)
    
    for name, ticker in SECTORS.items():
        prices = get_data(ticker)
        if prices is not None:
            latest = get_latest_price(prices)
            returns = {
                period: calculate_returns(prices, days) 
                for period, days in ANALYSIS_DAYS.items()
            }
            results[name] = {
                'ticker': ticker,
                'latest_price': latest,
                'returns': returns
            }
            print(f"\n{name} ({ticker}):")
            print(f"  最新价: {latest:.4f}" if latest else "  最新价: N/A")
            for period, ret in returns.items():
                if ret is not None:
                    trend = "↑" if ret > 0 else "↓"
                    print(f"  {period}涨跌: {trend} {ret:.2f}%")
                else:
                    print(f"  {period}涨跌: N/A")
    
    return results

def format_return(ret):
    """格式化涨跌幅"""
    if ret is None:
        return "N/A"
    return f"{ret:+.2f}%"

def generate_summary_report(metals_data, indices_data, sectors_data):
    """生成汇总报告"""
    report = []
    report.append("=" * 70)
    report.append("【贵金属与A股市场多周期分析报告】")
    report.append(f"生成时间: {TODAY.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    
    # 执行摘要
    report.append("\n【执行摘要】")
    report.append("-" * 50)
    
    # 找贵金属中表现最好的
    best_metal = None
    best_metal_ret = None
    for name, data in metals_data.items():
        if data['returns']['本月'] is not None:
            if best_metal_ret is None or data['returns']['本月'] > best_metal_ret:
                best_metal = name
                best_metal_ret = data['returns']['本月']
    
    # 找A股中表现最好的
    best_index = None
    best_index_ret = None
    for name, data in indices_data.items():
        if data['returns']['本月'] is not None:
            if best_index_ret is None or data['returns']['本月'] > best_index_ret:
                best_index = name
                best_index_ret = data['returns']['本月']
    
    if best_metal:
        report.append(f"贵金属焦点: {best_metal}本月表现最强 ({best_metal_ret:+.2f}%)")
    if best_index:
        report.append(f"A股焦点: {best_index}本月表现最好 ({best_index_ret:+.2f}%)")
    
    # 贵金属汇总
    report.append("\n\n【一、贵金属价格分析】")
    report.append("-" * 50)
    for name, data in metals_data.items():
        price = data['latest_price']
        report.append(f"\n{name}:")
        report.append(f"  最新价: {price:.4f}" if price else "  最新价: N/A")
        report.append(f"  本周涨跌: {format_return(data['returns']['本周'])}")
        report.append(f"  本月涨跌: {format_return(data['returns']['本月'])}")
        report.append(f"  本季涨跌: {format_return(data['returns']['本季'])}")
        report.append(f"  半年涨跌: {format_return(data['returns']['半年'])}")
    
    # A股指数汇总
    report.append("\n\n【二、A股市场表现】")
    report.append("-" * 50)
    for name, data in indices_data.items():
        price = data['latest_price']
        report.append(f"\n{name}:")
        report.append(f"  最新价: {price:.4f}" if price else "  最新价: N/A")
        report.append(f"  本周涨跌: {format_return(data['returns']['本周'])}")
        report.append(f"  本月涨跌: {format_return(data['returns']['本月'])}")
        report.append(f"  本季涨跌: {format_return(data['returns']['本季'])}")
        report.append(f"  半年涨跌: {format_return(data['returns']['半年'])}")
    
    # 行业板块汇总
    report.append("\n\n【三、行业板块表现】")
    report.append("-" * 50)
    for name, data in sectors_data.items():
        price = data['latest_price']
        report.append(f"\n{name}:")
        report.append(f"  最新价: {price:.4f}" if price else "  最新价: N/A")
        report.append(f"  本周涨跌: {format_return(data['returns']['本周'])}")
        report.append(f"  本月涨跌: {format_return(data['returns']['本月'])}")
        report.append(f"  本季涨跌: {format_return(data['returns']['本季'])}")
        report.append(f"  半年涨跌: {format_return(data['returns']['半年'])}")
    
    # 排名分析
    report.append("\n\n【四、板块轮动排名】")
    report.append("-" * 50)
    
    all_sectors = {**sectors_data}
    
    for period, days in ANALYSIS_DAYS.items():
        report.append(f"\n{period}涨幅排名:")
        
        all_data = {}
        for name, data in all_sectors.items():
            if data['returns'][period] is not None:
                all_data[name] = data['returns'][period]
        
        if all_data:
            sorted_data = sorted(all_data.items(), key=lambda x: x[1], reverse=True)
            
            report.append("  领涨:")
            top_count = 0
            for i, (name, ret) in enumerate(sorted_data, 1):
                if ret > 0 and top_count < 3:
                    trend = "↑"
                    report.append(f"    第{top_count+1}: {name} {trend} {ret:+.2f}%")
                    top_count += 1
            
            report.append("  领跌:")
            bottom_count = 0
            for name, ret in reversed(sorted_data):
                if ret < 0 and bottom_count < 3:
                    trend = "↓"
                    report.append(f"    第{bottom_count+1}: {name} {trend} {abs(ret):.2f}%")
                    bottom_count += 1
    
    # 关键指标解读
    report.append("\n\n【五、关键指标解读】")
    report.append("-" * 50)
    
    # 计算市场情绪
    weekly_returns = []
    for name, data in indices_data.items():
        if data['returns']['本周'] is not None:
            weekly_returns.append(data['returns']['本周'])
    
    if weekly_returns:
        avg_weekly = sum(weekly_returns) / len(weekly_returns)
        if avg_weekly > 2:
            report.append(f"市场情绪: 偏热 (本周平均涨幅 {avg_weekly:.2f}%)")
        elif avg_weekly < -2:
            report.append(f"市场情绪: 偏冷 (本周平均跌幅 {abs(avg_weekly):.2f}%)")
        else:
            report.append(f"市场情绪: 震荡 (本周平均涨跌 {avg_weekly:+.2f}%)")
    
    # 资金流向判断
    report.append("\n资金流向判断:")
    if best_metal and metals_data.get(best_metal, {}).get('returns', {}).get('本季', 0) > 20:
        report.append("  - 贵金属: 资金持续流入避险资产")
    if best_index_ret and best_index_ret > 5:
        report.append("  - A股: 增量资金入场，结构性机会")
    else:
        report.append("  - A股: 存量博弈，板块轮动为主")
    
    # 估值水平
    report.append("\n估值水平参考:")
    sh_pe = indices_data.get('上证指数', {}).get('latest_price', 0)
    if sh_pe:
        report.append(f"  - 上证指数点位: {sh_pe:.2f} (历史区间中位约3000-3500)")
    
    # 投资建议
    report.append("\n\n【六、投资建议】")
    report.append("-" * 50)
    
    # 贵金属建议
    report.append("\n贵金属操作建议:")
    gold_monthly = metals_data.get('COMEX黄金', {}).get('returns', {}).get('本月', 0)
    silver_monthly = metals_data.get('COMEX白银', {}).get('returns', {}).get('本月', 0)
    
    if gold_monthly > 10:
        report.append("  - 黄金: 月涨幅超10%，短期超涨，建议减仓或观望")
    elif gold_monthly > 5:
        report.append("  - 黄金: 涨幅较大，谨慎追高")
    elif gold_monthly < -5:
        report.append("  - 黄金: 回调整理，可择机布局")
    else:
        report.append("  - 黄金: 震荡整理，观望为主")
    
    if silver_monthly > 15:
        report.append("  - 白银: 月涨幅超15%，波动较大，风险较高")
    elif silver_monthly > 0:
        report.append("  - 白银: 温和上涨，弹性较好")
    else:
        report.append("  - 白银: 回调整理，关注支撑位")
    
    # A股建议
    report.append("\nA股操作建议:")
    report.append("  - 半导体: 关注AI芯片和先进封装龙头")
    report.append("  - 新能源: 回调后可逢低布局")
    report.append("  - 银行: 防御配置，关注股息率")
    report.append("  - 白酒: 短期承压，等待基本面改善")
    
    # 仓位配置
    report.append("\n仓位配置建议:")
    report.append("  - 贵金属: 5-10% (黄金为主，白银为辅)")
    report.append("  - A股: 30-40% (科技+消费+金融)")
    report.append("  - 现金: 50-60% (保持流动性)")
    
    # 风险提示
    report.append("\n\n【七、风险提示】")
    report.append("-" * 50)
    report.append("  - 数据风险: 数据来源为公开市场数据，可能存在延迟")
    report.append("  - 市场风险: 贵金属波动较大，注意止损")
    report.append("  - 操作风险: A股板块轮动快，勿追涨杀跌")
    report.append("  - 政策风险: 关注国内外货币政策变化")
    
    return "\n".join(report)

# ============ 主程序 ============
if __name__ == "__main__":
    print("开始获取贵金属价格数据...")
    metals_data = analyze_precious_metals()
    
    print("\n开始获取A股指数数据...")
    indices_data = analyze_china_indices()
    
    print("\n开始获取行业板块数据...")
    sectors_data = analyze_sectors()
    
    print("\n生成汇总报告...")
    report = generate_summary_report(metals_data, indices_data, sectors_data)
    
    # 保存报告
    report_path = "/Users/dave/clawd/memory/2026-02-04-贵金属A股分析报告.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n报告已保存到: {report_path}")
    print("\n" + report)
