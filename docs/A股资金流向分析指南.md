# A股资金流向分析指南

## 1. 概述

资金流向分析是技术分析和量化投资的重要组成部分，通过追踪资金的流入流出情况，可以判断市场主力行为，预判股价走势。

### 1.1 核心逻辑
- **资金净流入**：买入金额 > 卖出金额
- **资金净流出**：卖出金额 > 买入金额
- **主力资金**：大单、超大单的净买入
- **散户资金**：小单、中单的净买入

### 1.2 分析价值
- 识别机构建仓/出货信号
- 判断市场情绪变化
- 捕捉板块轮动机会
- 预警个股风险

---

## 2. 资金流向指标体系

### 2.1 核心指标定义

| 指标名称 | 含义 | 计算方法 | TuShare API | 优先级 |
|---------|------|---------|-------------|--------|
| 主力净流入 | 大单+超大单净买入金额 | buy_lg_amt + buy_elg_amt - sell_lg_amt - sell_elg_amt | moneyflow | P0 |
| 散户净流入 | 小单+中单净买入金额 | buy_sm_amt + buy_md_amt - sell_sm_amt - sell_md_amt | moneyflow | P0 |
| 资金集中度 | 主力净流入占总净流入比例 | 主力净流入 / 总净流入 * 100% | moneyflow | P1 |
| 资金连续性 | N日内净流入为正的天数 | count(net_amount > 0) | moneyflow | P1 |
| 净流入率 | 净流入额/流通市值 | net_amount / market_cap | moneyflow | P2 |
| 主力占比 | 主力成交占总成交比例 | (buy_lg_vol + sell_lg_vol) / total_vol | moneyflow | P1 |

### 2.2 资金规模分类

| 规模类型 | 单笔成交额 | TuShare 字段 |
|---------|-----------|-------------|
| 超大单 | ≥50万元 | buy_elg_amt / sell_elg_amt |
| 大单 | 10-50万元 | buy_lg_amt / sell_lg_amt |
| 中单 | 4-10万元 | buy_md_amt / sell_md_amt |
| 小单 | <4万元 | buy_sm_amt / sell_sm_amt |

---

## 3. 数据获取

### 3.1 环境配置
```python
import tushare as ts
import pandas as pd
import numpy as np
import os

# 设置 Token
TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()
```

### 3.2 获取资金流向数据
```python
def get_moneyflow_data(ts_code, start_date, end_date):
    """
    获取个股资金流向数据

    参数:
        ts_code: 股票代码，如 '000001.SZ'
        start_date: 开始日期，格式 YYYYMMDD
        end_date: 结束日期，格式 YYYYMMDD

    返回:
        DataFrame: 资金流向数据
    """
    df = pro.moneyflow(
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date
    )
    return df

# 示例
if __name__ == "__main__":
    df = get_moneyflow_data('000001.SZ', '20240101', '20240131')
    print(df.head())
```

### 3.3 获取多股票资金流向
```python
def get_batch_moneyflow(stock_list, start_date, end_date, delay=0.1):
    """
    批量获取多只股票的资金流向

    参数:
        stock_list: 股票代码列表
        start_date: 开始日期
        end_date: 结束日期
        delay: 请求间隔（秒），避免频繁调用

    返回:
        dict: {ts_code: DataFrame}
    """
    import time
    result = {}

    for code in stock_list:
        try:
            df = pro.moneyflow(
                ts_code=code,
                start_date=start_date,
                end_date=end_date
            )
            result[code] = df
            time.sleep(delay)
        except Exception as e:
            print(f"Error fetching {code}: {e}")
            result[code] = None

    return result
```

---

## 4. 指标计算

### 4.1 主力净流入/净流出
```python
def calculate_main_net_flow(df):
    """
    计算主力净流入

    主力 = 大单 + 超大单

    参数:
        df: 资金流向 DataFrame

    返回:
        DataFrame: 添加主力净流入列
    """
    df = df.copy()

    # 主力买入金额
    df['main_buy'] = df['buy_lg_amt'] + df['buy_elg_amt']

    # 主力卖出金额
    df['main_sell'] = df['sell_lg_amt'] + df['sell_elg_amt']

    # 主力净流入
    df['main_net_flow'] = df['main_buy'] - df['main_sell']

    # 分类：流入/流出/持平
    df['main_flow_type'] = pd.cut(
        df['main_net_flow'],
        bins=[-np.inf, 0, np.inf],
        labels=['净流出', '净流入']
    )

    return df
```

### 4.2 散户净流入
```python
def calculate_retail_net_flow(df):
    """
    计算散户净流入

    散户 = 小单 + 中单

    参数:
        df: 资金流向 DataFrame

    返回:
        DataFrame: 添加散户净流入列
    """
    df = df.copy()

    # 散户买入金额
    df['retail_buy'] = df['buy_sm_amt'] + df['buy_md_amt']

    # 散户卖出金额
    df['retail_sell'] = df['sell_sm_amt'] + df['sell_md_amt']

    # 散户净流入
    df['retail_net_flow'] = df['retail_buy'] - df['retail_sell']

    return df
```

### 4.3 资金集中度
```python
def calculate_concentration(df, window=5):
    """
    计算资金集中度

    集中度 = 主力净流入 / 总净流入 * 100%

    参数:
        df: 资金流向 DataFrame
        window: 移动平均窗口

    返回:
        DataFrame: 添加资金集中度列
    """
    df = df.copy()

    # 总净流入
    df['total_net_flow'] = df['main_net_flow'] + df['retail_net_flow']

    # 资金集中度
    df['concentration'] = np.where(
        df['total_net_flow'] != 0,
        df['main_net_flow'] / df['total_net_flow'] * 100,
        0
    )

    # 5日移动平均集中度
    df['concentration_ma5'] = df['concentration'].rolling(window=window).mean()

    return df
```

### 4.4 资金连续性
```python
def calculate_flow_continuous(df, window=10):
    """
    计算资金连续性

    连续性 = N日内净流入为正的天数

    参数:
        df: 资金流向 DataFrame
        window: 统计窗口

    返回:
        DataFrame: 添加连续性列
    """
    df = df.copy()

    # 净流入标志（1为正，0为负或0）
    df['net_positive'] = (df['net_mf_amt'] > 0).astype(int)

    # N日连续净流入天数
    df['continuous_days'] = df['net_positive'].rolling(window=window).sum()

    # 连续流入比例
    df['continuous_ratio'] = df['continuous_days'] / window * 100

    return df
```

### 4.5 综合指标计算
```python
def calculate_all_indicators(df):
    """
    计算所有资金流向指标

    参数:
        df: 原始资金流向数据

    返回:
        DataFrame: 包含所有指标的完整数据
    """
    # 主力净流入
    df = calculate_main_net_flow(df)

    # 散户净流入
    df = calculate_retail_net_flow(df)

    # 资金集中度
    df = calculate_concentration(df)

    # 资金连续性
    df = calculate_flow_continuous(df)

    # 净流入率（需要流通市值）
    # df['net_flow_rate'] = df['main_net_flow'] / df['market_cap'] * 100

    return df
```

---

## 5. 信号生成

### 5.1 资金流向信号规则

```python
def generate_flow_signals(df, threshold_inflow=1000, threshold_outflow=-1000):
    """
    生成资金流向信号

    参数:
        df: 包含计算指标的 DataFrame
        threshold_inflow: 主力净流入阈值（万元）
        threshold_outflow: 主力净流出阈值（万元）

    返回:
        DataFrame: 添加信号列
    """
    df = df.copy()

    # 单日信号
    df['signal'] = '持有'
    df.loc[df['main_net_flow'] > threshold_inflow, 'signal'] = '买入信号'
    df.loc[df['main_net_flow'] < threshold_outflow, 'signal'] = '卖出信号'

    # 连续流入信号
    df['continuous_signal'] = '无'
    df.loc[df['continuous_days'] >= 5, 'continuous_signal'] = '5日连流入'
    df.loc[df['continuous_days'] >= 10, 'continuous_signal'] = '10日连流入'

    # 集中度信号
    df['concentration_signal'] = '正常'
    df.loc[df['concentration'] > 80, 'concentration_signal'] = '高度集中'
    df.loc[df['concentration'] > 90, 'concentration_signal'] = '极度集中'

    return df
```

### 5.2 资金流向评级
```python
def rate_moneyflow_quality(df, lookback=5):
    """
    资金流向质量评级

    评分维度：
    1. 净流入幅度
    2. 连续性
    3. 集中度
    4. 稳定性

    参数:
        df: 包含计算指标的 DataFrame
        lookback: 回顾天数

    返回:
        Series: 每日评级
    """
    df = df.tail(lookback).copy()

    # 评分
    scores = pd.DataFrame(index=df.index)

    # 净流入评分
    avg_flow = df['main_net_flow'].mean()
    if avg_flow > 5000:
        scores['flow_score'] = 5
    elif avg_flow > 1000:
        scores['flow_score'] = 4
    elif avg_flow > 0:
        scores['flow_score'] = 3
    elif avg_flow > -1000:
        scores['flow_score'] = 2
    else:
        scores['flow_score'] = 1

    # 连续性评分
    avg_continuous = df['continuous_days'].mean()
    if avg_continuous >= lookback:
        scores['continuous_score'] = 5
    elif avg_continuous >= lookback * 0.7:
        scores['continuous_score'] = 4
    elif avg_continuous >= lookback * 0.5:
        scores['continuous_score'] = 3
    else:
        scores['continuous_score'] = 2

    # 综合评分
    scores['total_score'] = (scores['flow_score'] * 2 + scores['continuous_score']) / 3

    # 评级
    if scores['total_score'] >= 4.5:
        df['quality_rating'] = 'A'
    elif scores['total_score'] >= 4:
        df['quality_rating'] = 'B+'
    elif scores['total_score'] >= 3.5:
        df['quality_rating'] = 'B'
    elif scores['total_score'] >= 3:
        df['quality_rating'] = 'C'
    else:
        df['quality_rating'] = 'D'

    return df['quality_rating']
```

---

## 6. 可视化

### 6.1 资金流向时间序列图
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_moneyflow_time_series(df, title='资金流向分析'):
    """
    绘制资金流向时间序列图

    参数:
        df: 包含主力净流入、散户净流入的 DataFrame
        title: 图表标题
    """
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    # 转换日期格式
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
    df = df.sort_values('trade_date')

    # 图1：主力 vs 散户净流入
    ax1 = axes[0]
    ax1.bar(df['trade_date'], df['main_net_flow'], color='red', alpha=0.7, label='主力净流入')
    ax1.bar(df['trade_date'], df['retail_net_flow'], color='blue', alpha=0.5, label='散户净流入')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax1.set_ylabel('净流入（万元）')
    ax1.set_title('主力 vs 散户资金流向')
    ax1.legend()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    # 图2：资金集中度
    ax2 = axes[1]
    ax2.plot(df['trade_date'], df['concentration'], color='purple', linewidth=2)
    ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.7, label='50%基准线')
    ax2.fill_between(df['trade_date'], 50, df['concentration'],
                     where=df['concentration'] > 50, color='green', alpha=0.3)
    ax2.set_ylabel('集中度（%）')
    ax2.set_title('资金集中度')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    # 图3：净流入柱状图
    ax3 = axes[2]
    colors = ['green' if x > 0 else 'red' for x in df['main_net_flow']]
    ax3.bar(df['trade_date'], df['main_net_flow'], color=colors, alpha=0.7)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax3.set_ylabel('主力净流入（万元）')
    ax3.set_title('主力净流入')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    plt.tight_layout()
    plt.savefig(f'{title}.png', dpi=150, bbox_inches='tight')
    plt.show()

# 使用示例
if __name__ == "__main__":
    df = get_moneyflow_data('000001.SZ', '20240101', '20240131')
    df = calculate_all_indicators(df)
    plot_moneyflow_time_series(df)
```

### 6.2 资金流向热力图
```python
def plot_moneyflow_heatmap(stocks_data, title='资金流向热力图'):
    """
    绘制多股票资金流向热力图

    参数:
        stocks_data: dict, {ts_code: DataFrame}
        title: 图表标题
    """
    # 汇总数据
    summary = []
    for code, df in stocks_data.items():
        if df is not None and len(df) > 0:
            last_row = df.iloc[-1]
            summary.append({
                'code': code,
                'main_net_flow': last_row['main_net_flow'],
                'retail_net_flow': last_row['retail_net_flow'],
                'concentration': last_row['concentration']
            })

    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.set_index('code')

    # 绘制热力图
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(summary_df.values, cmap='RdYlGn', aspect='auto')

    # 设置标签
    ax.set_xticks(range(len(summary_df.columns)))
    ax.set_xticklabels(['主力净流入', '散户净流入', '集中度'])
    ax.set_yticks(range(len(summary_df.index)))
    ax.set_yticklabels(summary_df.index)

    # 添加数值标注
    for i in range(len(summary_df.index)):
        for j in range(len(summary_df.columns)):
            text = ax.text(j, i, f'{summary_df.values[i, j]:.1f}',
                          ha="center", va="center", color="black")

    ax.set_title(title)
    plt.colorbar(im)
    plt.tight_layout()
    plt.savefig(f'{title}.png', dpi=150, bbox_inches='tight')
    plt.show()
```

---

## 7. 分析框架

### 7.1 选股筛选流程

```python
def screen_stocks_by_moneyflow(stocks, start_date, end_date, criteria):
    """
    基于资金流向筛选股票

    参数:
        stocks: 股票代码列表
        start_date: 开始日期
        end_date: 结束日期
        criteria: 筛选条件 dict

    返回:
        list: 符合条件的股票列表
    """
    qualified = []

    for code in stocks:
        df = get_moneyflow_data(code, start_date, end_date)
        if df is None or len(df) == 0:
            continue

        df = calculate_all_indicators(df)
        df = generate_flow_signals(df)

        # 检查条件
        last_row = df.iloc[-1]

        # 条件1：主力净流入
        if criteria.get('main_net_flow_min', 0):
            if last_row['main_net_flow'] < criteria['main_net_flow_min']:
                continue

        # 条件2：资金集中度
        if criteria.get('concentration_min', 0):
            if last_row['concentration'] < criteria['concentration_min']:
                continue

        # 条件3：连续流入天数
        if criteria.get('continuous_days_min', 0):
            if last_row['continuous_days'] < criteria['continuous_days_min']:
                continue

        qualified.append({
            'code': code,
            'main_net_flow': last_row['main_net_flow'],
            'concentration': last_row['concentration'],
            'continuous_days': last_row['continuous_days'],
            'signal': last_row['signal']
        })

    return sorted(qualified, key=lambda x: x['main_net_flow'], reverse=True)

# 使用示例
if __name__ == "__main__":
    criteria = {
        'main_net_flow_min': 1000,      # 主力净流入 > 1000万
        'concentration_min': 60,        # 集中度 > 60%
        'continuous_days_min': 5        # 连续流入 >= 5天
    }

    stock_list = ['000001.SZ', '000002.SZ', '600000.SH']
    result = screen_stocks_by_moneyflow(stock_list, '20240101', '20240131', criteria)
    print(result)
```

### 7.2 板块资金流向分析

```python
def analyze_industry_moneyflow(date, top_n=10):
    """
    分析板块资金流向

    参数:
        date: 交易日期
        top_n: 返回前N名

    返回:
        DataFrame: 板块资金流向排名
    """
    # 获取所有股票的资金流向
    stocks = pro.stock_basic(
        exchange='',
        list_status='L',
        fields='ts_code,industry'
    )

    industry_flow = {}

    for idx, row in stocks.iterrows():
        try:
            df = pro.moneyflow(
                ts_code=row['ts_code'],
                trade_date=date
            )
            if df is not None and len(df) > 0:
                industry = row['industry']
                main_net = df.iloc[0]['main_net_flow'] if 'main_net_flow' in df.columns else \
                           df.iloc[0]['buy_lg_amt'] + df.iloc[0]['buy_elg_amt'] - \
                           df.iloc[0]['sell_lg_amt'] - df.iloc[0]['sell_elg_amt']

                if industry in industry_flow:
                    industry_flow[industry] += main_net
                else:
                    industry_flow[industry] = main_net
        except:
            continue

    # 排序
    result = pd.DataFrame([
        {'industry': k, 'net_flow': v}
        for k, v in industry_flow.items()
    ])
    result = result.sort_values('net_flow', ascending=False).head(top_n)

    return result
```

---

## 8. 注意事项

### 8.1 数据局限性
- **单笔划分标准**：不同券商可能有不同标准
- **时滞性**：资金流向数据为收盘后统计
- **覆盖范围**：仅统计已上报的券商数据

### 8.2 分析建议
- **多日验证**：不要依赖单日数据
- **结合价格**：资金流向需与价格走势结合
- **关注异常**：警惕集中度过高的信号
- **分散投资**：不要集中单只股票

### 8.3 风险提示
- 历史数据不代表未来表现
- 资金流向仅供参考，不构成投资建议
- 需结合基本面和技术分析综合判断

---

## 9. 参考资源

- TuShare 官方文档：https://tushare.pro/document
- 资金流向指标说明：https://tushare.pro/document/2?doc_id=170
- 量化投资相关书籍和课程
