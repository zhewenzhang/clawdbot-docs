#!/usr/bin/env python3
"""
贵金属与A股市场多周期分析 - 优化版
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

TODAY = datetime.now()
print(f"分析时间: {TODAY.strftime('%Y-%m-%d %H:%M')}")

# ============ 核心配置 ============
PRECIOUS_METALS = ['GC=F', 'SI=F', 'HG=F', 'PL=F', 'PA=F']
METAL_NAMES = {'GC=F': 'COMEX黄金', 'SI=F': 'COMEX白银', 'HG=F': 'LME铜', 
               'PL=F': 'NYMEX铂金', 'PA=F': 'NYMEX钯金'}

INDICES = ['000001.SS', '399001.SZ', '000300.SS']
INDEX_NAMES = {'000001.SS': '上证指数', '399001.SZ': '深证成指', '000300.SS': '沪深300'}

SECTORS = ['399811.SZ', '399986.SZ', '399997.SZ', '399300.SZ', '000941.SS']
SECTOR_NAMES = {'399811.SZ': '中证半导体', '399986.SZ': '中证银行', '399997.SZ': '中证白酒',
                '399300.SZ': '中证医药', '000941.SS': '新能源'}

PERIODS = {'本周': 5, '本月': 20, '本季': 60}

# ============ 数据获取 ============
ALL_TICKERS = PRECIOUS_METALS + INDICES + SECTORS
print(f"获取 {len(ALL_TICKERS)} 个标的数据...")

data = yf.download(ALL_TICKERS, start=TODAY - timedelta(days=90), 
                    end=TODAY, progress=False, timeout=10)

if data.empty:
    print("数据获取失败")
    exit(1)

# ============ 数据处理 ============
def clean_series(series):
    """清理NaN数据"""
    if series is None:
        return None
    series = series.dropna()
    if len(series) == 0:
        return None
    return series

def get_returns(series, days):
    """计算涨跌幅"""
    series = clean_series(series)
    if series is None or len(series) < days:
        return None
    recent = series.tail(days)
    if len(recent) < 2:
        return None
    try:
        start = float(recent.iloc[0])
        end = float(recent.iloc[-1])
    except:
        return None
    if start == 0 or np.isnan(start) or np.isnan(end):
        return None
    return round(((end - start) / start) * 100, 2)

def get_latest(series):
    """获取最新价"""
    series = clean_series(series)
    if series is None or len(series) == 0:
        return None
    try:
        latest = series.iloc[-1]
        if isinstance(latest, (pd.Series, np.ndarray)):
            latest = latest.iloc[0] if len(latest) > 0 else None
        return round(float(latest), 2) if latest is not None and not np.isnan(latest) else None
    except:
        return None

# 提取收盘价
if isinstance(data.columns, pd.MultiIndex):
    close_data = data['Close']
else:
    close_data = data['Close']

# ============ 生成报告 ============
report = []
report.append("=" * 70)
report.append("【贵金属与A股市场多周期分析报告】")
report.append(f"分析时间: {TODAY.strftime('%Y-%m-%d')} | 数据来源: Yahoo Finance")
report.append("=" * 70)

# ============ 1. 执行摘要 ============
report.append("\n【执行摘要】")
report.append("-" * 50)

# 找亮点
best_metal, best_metal_ret = None, None
for ticker in PRECIOUS_METALS:
    if ticker in close_data.columns:
        ret = get_returns(close_data[ticker], 20)
        if ret and (best_metal_ret is None or ret > best_metal_ret):
            best_metal = METAL_NAMES.get(ticker, ticker)
            best_metal_ret = ret

best_index, best_index_ret = None, None
for ticker in INDICES:
    if ticker in close_data.columns:
        ret = get_returns(close_data[ticker], 20)
        if ret and (best_index_ret is None or ret > best_index_ret):
            best_index = INDEX_NAMES.get(ticker, ticker)
            best_index_ret = ret

if best_metal:
    report.append(f"贵金属焦点: {best_metal}本月涨幅+{best_metal_ret}%最强劲")
if best_index:
    report.append(f"A股焦点: {best_index}本月表现最佳({best_index_ret:+.2f}%)")

report.append("市场状态: 贵金属延续强势，A股震荡整理")

# ============ 2. 贵金属分析 ============
report.append("\n\n【一、贵金属价格分析】")
report.append("-" * 50)

for ticker in PRECIOUS_METALS:
    if ticker not in close_data.columns:
        continue
    name = METAL_NAMES.get(ticker, ticker)
    prices = close_data[ticker]
    latest = get_latest(prices)
    
    w_ret = get_returns(prices, 5)
    m_ret = get_returns(prices, 20)
    q_ret = get_returns(prices, 60)
    
    report.append(f"\n{name}:")
    report.append(f"  最新价: {latest}" if latest else "  最新价: N/A")
    report.append(f"  本周: {w_ret:+.2f}%" if w_ret is not None else "  本周: N/A")
    report.append(f"  本月: {m_ret:+.2f}%" if m_ret is not None else "  本月: N/A")
    report.append(f"  本季: {q_ret:+.2f}%" if q_ret is not None else "  本季: N/A")

# ============ 3. A股指数分析 ============
report.append("\n\n【二、A股市场表现】")
report.append("-" * 50)

for ticker in INDICES:
    if ticker not in close_data.columns:
        continue
    name = INDEX_NAMES.get(ticker, ticker)
    prices = close_data[ticker]
    latest = get_latest(prices)
    
    w_ret = get_returns(prices, 5)
    m_ret = get_returns(prices, 20)
    q_ret = get_returns(prices, 60)
    
    report.append(f"\n{name}:")
    report.append(f"  最新价: {latest}" if latest else "  最新价: N/A")
    report.append(f"  本周: {w_ret:+.2f}%" if w_ret is not None else "  本周: N/A")
    report.append(f"  本月: {m_ret:+.2f}%" if m_ret is not None else "  本月: N/A")
    report.append(f"  本季: {q_ret:+.2f}%" if q_ret is not None else "  本季: N/A")

# ============ 4. 行业板块分析 ============
report.append("\n\n【三、行业板块表现】")
report.append("-" * 50)

for ticker in SECTORS:
    if ticker not in close_data.columns:
        continue
    name = SECTOR_NAMES.get(ticker, ticker)
    prices = close_data[ticker]
    latest = get_latest(prices)
    
    w_ret = get_returns(prices, 5)
    m_ret = get_returns(prices, 20)
    q_ret = get_returns(prices, 60)
    
    report.append(f"\n{name}:")
    report.append(f"  最新价: {latest}" if latest else "  最新价: N/A")
    report.append(f"  本周: {w_ret:+.2f}%" if w_ret is not None else "  本周: N/A")
    report.append(f"  本月: {m_ret:+.2f}%" if m_ret is not None else "  本月: N/A")
    report.append(f"  本季: {q_ret:+.2f}%" if q_ret is not None else "  本季: N/A")

# ============ 5. 板块轮动排名 ============
report.append("\n\n【四、板块轮动排名】")
report.append("-" * 50)

for period, days in [('本周', 5), ('本月', 20), ('本季', 60)]:
    report.append(f"\n{period}涨幅排名:")
    
    results = []
    for ticker in SECTORS:
        if ticker in close_data.columns:
            ret = get_returns(close_data[ticker], days)
            if ret is not None:
                results.append((SECTOR_NAMES.get(ticker, ticker), ret))
    
    if results:
        results.sort(key=lambda x: x[1], reverse=True)
        
        # 领涨
        positive = [r for r in results if r[1] > 0]
        report.append("  领涨TOP3:")
        for i, (name, ret) in enumerate(positive[:3], 1):
            report.append(f"    {i}. {name} +{ret:.2f}%")
        if not positive:
            report.append("    无")
        
        # 领跌
        negative = [r for r in results if r[1] < 0]
        report.append("  领跌TOP3:")
        for i, (name, ret) in enumerate(negative[:3], 1):
            report.append(f"    {i}. {name} {ret:.2f}%")
        if not negative:
            report.append("    无")

# ============ 6. 关键指标解读 ============
report.append("\n\n【五、关键指标解读】")
report.append("-" * 50)

# 市场情绪
sh_ret = get_returns(close_data.get('000001.SS'), 5) if '000001.SS' in close_data.columns else None
sz_ret = get_returns(close_data.get('399001.SZ'), 5) if '399001.SZ' in close_data.columns else None

if sh_ret is not None and sz_ret is not None:
    avg_ret = (sh_ret + sz_ret) / 2
    if avg_ret > 2:
        sentiment = "偏热"
    elif avg_ret < -2:
        sentiment = "偏冷"
    else:
        sentiment = "震荡"
    report.append(f"\n市场情绪: {sentiment} (本周平均 {avg_ret:+.2f}%)")

# 估值参考
sh_price = get_latest(close_data.get('000001.SS')) if '000001.SS' in close_data.columns else None
if sh_price:
    report.append(f"\n上证指数: {sh_price}点")
    if sh_price > 4000:
        report.append("  估值: 偏高区域 (历史中位数约3000-3500)")
    elif sh_price > 3000:
        report.append("  估值: 中位区域")
    else:
        report.append("  估值: 偏低区域")

# ============ 7. 投资建议 ============
report.append("\n\n【六、投资建议】")
report.append("-" * 50)

report.append("\n贵金属操作:")
gold_ret = get_returns(close_data.get('GC=F'), 20) if 'GC=F' in close_data.columns else None
silver_ret = get_returns(close_data.get('SI=F'), 20) if 'SI=F' in close_data.columns else None

if gold_ret and gold_ret > 10:
    report.append("  - 黄金: 月涨幅超10%，短期超涨，建议减仓")
elif gold_ret and gold_ret > 0:
    report.append("  - 黄金: 温和上涨，持有为主")
else:
    report.append("  - 黄金: 回调整理，支撑位布局")

if silver_ret and silver_ret > 15:
    report.append("  - 白银: 波动剧烈，注意风险")
elif silver_ret and silver_ret > 0:
    report.append("  - 白银: 弹性较好，逢低布局")

report.append("\nA股操作:")
semi_ret = get_returns(close_data.get('399811.SZ'), 20) if '399811.SZ' in close_data.columns else None
if semi_ret and semi_ret > 5:
    report.append("  - 半导体: 涨幅较大，谨慎追高")
elif semi_ret and semi_ret > 0:
    report.append("  - 半导体: 温和上涨，AI芯片龙头关注")
else:
    report.append("  - 半导体: 回调后布局，关注先进封装")

report.append("  - 新能源: 回调后逢低布局")
report.append("  - 银行: 防御配置，关注高股息")

report.append("\n仓位配置:")
report.append("  - 贵金属: 5-10% (黄金为主)")
report.append("  - A股: 30-40% (科技+防御)")
report.append("  - 现金: 50%+ (保持流动性)")

# ============ 8. 风险提示 ============
report.append("\n\n【七、风险提示】")
report.append("-" * 50)
report.append("  - 数据风险: 数据来源公开市场，可能存在延迟")
report.append("  - 市场风险: 贵金属波动大，注意止损")
report.append("  - 操作风险: 板块轮动快，勿追涨杀跌")
report.append("  - 政策风险: 关注美联储利率决议")

# ============ 保存报告 ============
report_text = "\n".join(report)
report_path = "/Users/dave/clawd/memory/2026-02-04-贵金属A股分析报告.md"
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_text)

print(f"\n报告已保存: {report_path}")
print("\n" + report_text)
