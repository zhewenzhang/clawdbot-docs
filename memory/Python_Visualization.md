# Python 可视化实战：matplotlib/plotly 绑图
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、可视化概述

### 1.1 Python 可视化库

```
Python 可视化库

├── 基础库
│   ├── matplotlib（最常用）
│   ├── pandas.plot()
│   └── seaborn（统计图表）
│
├── 交互库
│   ├── plotly（交互图表）
│   ├── bokeh（交互图表）
│   └── altair（声明式）
│
└── 专用库
    ├── pyecharts（中国地图）
    ├── mplfinance（金融图表）
    └── networkx（网络图）
```

### 1.2 图表类型

| 图表类型 | 用途 | 库 |
|----------|------|-----|
| **折线图** | 时间序列 | matplotlib |
| **K 线图** | 金融行情 | mplfinance |
| **柱状图** | 类别比较 | matplotlib |
| **散点图** | 相关性 | matplotlib |
| **热力图** | 矩阵数据 | seaborn |
| **饼图** | 占比 | matplotlib |
| **箱线图** | 分布 | seaborn |

---

## 二、matplotlib 实战

### 2.1 基础用法

```python
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 简单折线图
x = [1, 2, 3, 4, 5]
y = [2, 4, 3, 5, 4]

plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linewidth=2, color='blue')
plt.title('简单折线图', fontsize=14)
plt.xlabel('X 轴', fontsize=12)
plt.ylabel('Y 轴', fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()
```

### 2.2 股票行情可视化

```python
import matplotlib.pyplot as plt
import pandas as pd
import akshare as ak

# 获取股票数据
df = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                         start_date="20230101", end_date="20231231")

# 处理日期
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# 绘制收盘价
plt.figure(figsize=(14, 6))
plt.plot(df['日期'], df['收盘'], linewidth=1.5, color='blue')
plt.title('平安银行 2023 年收盘价走势', fontsize=14)
plt.xlabel('日期', fontsize=12)
plt.ylabel('收盘价 (元)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 2.3 多图对比

```python
import matplotlib.pyplot as plt
import pandas as pd
import akshare as ak

# 获取多只股票
stocks = ['000001', '600519', '000002']
stock_names = ['平安银行', '贵州茅台', '万 科Ａ']

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

for i, (code, name) in enumerate(zip(stocks, stock_names)):
    df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                            start_date="20230101", end_date="20231231")
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values('日期')
    
    axes[i].plot(df['日期'], df['收盘'], linewidth=1.5)
    axes[i].set_title(f'{name} 2023 年收盘价走势', fontsize=12)
    axes[i].set_ylabel('收盘价 (元)', fontsize=10)
    axes[i].grid(True, alpha=0.3)

plt.xlabel('日期', fontsize=12)
plt.tight_layout()
plt.show()
```

### 2.4 成交量可视化

```python
import matplotlib.pyplot as plt
import pandas as pd
import akshare as ak

# 获取数据
df = ak.stock_zh_a_hist(symbol="600519", period="daily", 
                         start_date="20230101", end_date="20231231")
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# 设置颜色：上涨红色，下跌绿色
colors = ['red' if df['涨跌幅'].iloc[i] >= 0 else 'green' for i in range(len(df))]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])

# 收盘价
ax1.plot(df['日期'], df['收盘'], linewidth=1.5, color='blue')
ax1.set_title('贵州茅台 2023 年行情', fontsize=14)
ax1.set_ylabel('收盘价 (元)', fontsize=12)
ax1.grid(True, alpha=0.3)

# 成交量
ax2.bar(df['日期'], df['成交量']/1e6, color=colors, width=1)
ax2.set_ylabel('成交量 (百万)', fontsize=12)
ax2.set_xlabel('日期', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 2.5 技术指标可视化

```python
import matplotlib.pyplot as plt
import pandas as pd
import akshare as ak

# 获取数据
df = ak.stock_zh_a_hist(symbol="600519", period="daily", 
                         start_date="20230101", end_date="20231231")
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# 计算 MA
df['MA5'] = df['收盘'].rolling(window=5).mean()
df['MA20'] = df['收盘'].rolling(window=20).mean()
df['MA60'] = df['收盘'].rolling(window=60).mean()

# 计算 RSI
delta = df['收盘'].diff()
gain = delta.where(delta > 0, 0).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))

# 绘图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])

# 股价 + MA
ax1.plot(df['日期'], df['收盘'], linewidth=1, label='收盘价', alpha=0.7)
ax1.plot(df['日期'], df['MA5'], linewidth=1, label='MA5', alpha=0.7)
ax1.plot(df['日期'], df['MA20'], linewidth=1.5, label='MA20')
ax1.plot(df['日期'], df['MA60'], linewidth=1.5, label='MA60')
ax1.set_title('贵州茅台技术分析', fontsize=14)
ax1.set_ylabel('价格 (元)', fontsize=12)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# RSI
ax2.plot(df['日期'], df['RSI'], linewidth=1.5, color='purple')
ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5)
ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5)
ax2.fill_between(df['日期'], 70, df['RSI'], where=df['RSI'] > 70, alpha=0.3, color='red')
ax2.fill_between(df['日期'], 30, df['RSI'], where=df['RSI'] < 30, alpha=0.3, color='green')
ax2.set_ylabel('RSI', fontsize=12)
ax2.set_xlabel('日期', fontsize=12)
ax2.set_ylim(0, 100)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 三、plotly 实战

### 3.1 plotly 基础

```python
import plotly.graph_objects as go
import pandas as pd

# 简单折线图
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[2, 4, 3, 5, 4], 
                         mode='lines+markers', name='数据'))
fig.update_layout(title='简单折线图', xaxis_title='X 轴', yaxis_title='Y 轴')
fig.show()
```

### 3.2 K 线图

```python
import plotly.graph_objects as go
import akshare as ak

# 获取数据
df = ak.stock_zh_a_hist(symbol="600519", period="daily", 
                         start_date="20230101", end_date="20231231")
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# K 线图
fig = go.Figure(data=[go.Candlestick(
    x=df['日期'],
    open=df['开盘'],
    high=df['最高'],
    low=df['最低'],
    close=df['收盘'],
    increasing_line_color='red',
    decreasing_line_color='green'
)])

fig.update_layout(
    title='贵州茅台 K 线图',
    xaxis_title='日期',
    yaxis_title='价格 (元)',
    xaxis_rangeslider_visible=False
)

fig.show()
```

### 3.3 交互式股票分析

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import akshare as ak

# 获取数据
df = ak.stock_zh_a_hist(symbol="600519", period="daily", 
                         start_date="20230101", end_date="20231231")
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# 计算 MA
df['MA5'] = df['收盘'].rolling(window=5).mean()
df['MA20'] = df['收盘'].rolling(window=20).mean()

# 创建子图
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.05,
                    subplot_titles=('价格走势', '成交量'))

# 价格 + MA
fig.add_trace(go.Scatter(x=df['日期'], y=df['收盘'], 
                         name='收盘价', line=dict(color='blue', width=1)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df['日期'], y=df['MA5'], 
                         name='MA5', line=dict(color='orange', width=1)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df['日期'], y=df['MA20'], 
                         name='MA20', line=dict(color='red', width=1)),
              row=1, col=1)

# 成交量
colors = ['red' if df['涨跌幅'].iloc[i] >= 0 else 'green' for i in range(len(df))]
fig.add_trace(go.Bar(x=df['日期'], y=df['成交量']/1e6, 
                     name='成交量', marker_color=colors),
              row=2, col=1)

fig.update_layout(height=800, showlegend=True)
fig.show()
```

### 3.4 动态 K 线图

```python
import plotly.graph_objects as go
import akshare as ak
import pandas as pd

# 获取一年数据
df = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                         start_date="20230101", end_date="20231231")
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# 创建滑块
fig = go.Figure(data=[go.Candlestick(
    x=df['日期'],
    open=df['开盘'],
    high=df['最高'],
    low=df['最低'],
    close=df['收盘']
)])

# 添加滑块
fig.update_layout(
    title='平安银行 K 线图（带滑块）',
    xaxis_rangeslider_visible=True,
    xaxis_rangeslider_thickness=0.05
)

fig.show()
```

---

## 四、seaborn 实战

### 4.1 seaborn 基础

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置样式
sns.set_style("whitegrid")

# 简单图表
x = np.random.randn(100)
y = 2 * x + np.random.randn(100)
sns.regplot(x=x, y=y)
plt.show()
```

### 4.2 财务数据分布

```python
import seaborn as sns
import matplotlib.pyplot as plt
import akshare as ak
import pandas as pd

# 获取多只股票 ROE
stocks = ['000001', '600519', '000002', '600036', '601398']
data = []
for code in stocks:
    try:
        indicator = ak.stock_fina_indicator(symbol=code)
        if len(indicator) > 0:
            latest = indicator.iloc[-1]
            data.append({
                'code': code,
                'roe': latest['roe'],
                'netprofit_margin': latest['netprofit_margin'],
                'grossprofit_margin': latest['grossprofit_margin']
            })
    except:
        continue

df = pd.DataFrame(data)

# 箱线图
plt.figure(figsize=(12, 6))
df_melted = df.melt(id_vars=['code'], value_vars=['roe', 'netprofit_margin', 'grossprofit_margin'],
                    var_name='指标', value_name='数值')
sns.boxplot(data=df_melted, x='指标', y='数值')
plt.title('财务指标分布')
plt.show()
```

### 4.3 相关性热力图

```python
import seaborn as sns
import matplotlib.pyplot as plt
import akshare as ak
import pandas as pd

# 获取股票列表
stocks = ['000001', '600519', '000002', '600036', '601398', '601988', '600000']

# 获取财务数据
data = []
for code in stocks:
    try:
        indicator = ak.stock_fina_indicator(symbol=code)
        if len(indicator) > 0:
            latest = indicator.iloc[-1]
            info = ak.stock_zh_a_spot_em()
            info = info[info['代码'] == code]
            if len(info) > 0:
                data.append({
                    'code': code,
                    'roe': latest['roe'],
                    'netprofit_margin': latest['netprofit_margin'],
                    'grossprofit_margin': latest['grossprofit_margin'],
                    'pe': float(info['市盈率'].iloc[0]) if info['市盈率'].iloc[0] != '-' else None
                })
    except:
        continue

df = pd.DataFrame(data)

# 计算相关性
corr = df[['roe', 'netprofit_margin', 'grossprofit_margin', 'pe']].corr()

# 热力图
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='RdYlGn', center=0)
plt.title('财务指标相关性')
plt.show()
```

---

## 五、实战案例

### 5.1 投资组合分析仪表板

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import akshare as ak

# 股票列表
stocks = ['600519', '000001', '600036']
names = ['贵州茅台', '平安银行', '招商银行']

# 创建子图
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    vertical_spacing=0.05,
                    subplot_titles=names)

# 获取并绑制每只股票
for i, (code, name) in enumerate(zip(stocks, names)):
    df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                            start_date="20230101", end_date="20231231")
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values('日期')
    
    # 归一化价格
    normalized = df['收盘'] / df['收盘'].iloc[0] * 100
    
    fig.add_trace(go.Scatter(x=df['日期'], y=normalized, 
                             name=name, fill='tozeroy'),
                  row=i+1, col=1)

fig.update_layout(height=900, showlegend=True,
                  title='投资组合表现（归一化）')
fig.show()
```

### 5.2 行业对比分析

```python
import plotly.express as px
import akshare as ak
import pandas as pd

# 获取行业数据
industries = ['半导体及元件', '计算机应用', '通信设备', '光学光电子', '汽车整车']

data = []
for industry in industries:
    try:
        stocks = ak.stock_board_industry_cons_th(symbol=industry)
        if len(stocks) > 0:
            # 计算行业平均涨跌幅
            avg_change = stocks['涨跌幅'].mean()
            data.append({
                '行业': industry,
                '平均涨跌幅': avg_change,
                '股票数量': len(stocks)
            })
    except:
        continue

df = pd.DataFrame(data)

# 水平柱状图
fig = px.bar(df, x='平均涨跌幅', y='行业', orientation='h',
             color='平均涨跌幅',
             color_continuous_scale='RdYlGn',
             title='行业平均涨跌幅对比')
fig.show()
```

---

## 六、学习要点总结

### 6.1 常用图表选择

| 数据类型 | 推荐图表 | 库 |
|----------|----------|-----|
| **时间序列** | 折线图 | matplotlib |
| **金融行情** | K 线图 | plotly |
| **多股票对比** | 叠加折线图 | plotly |
| **分布分析** | 箱线图 | seaborn |
| **相关性** | 热力图 | seaborn |
| **占比分析** | 饼图 | matplotlib |

### 6.2 库对比

| 库 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **matplotlib** | 灵活、强大 | 代码复杂 | 静态图表 |
| **plotly** | 交互、漂亮 | 渲染慢 | 交互分析 |
| **seaborn** | 简洁、统计 | 定制性弱 | 统计分析 |
| **mplfinance** | 金融专用 | 功能单一 | 金融行情 |

### 6.3 最佳实践

1. **选择合适图表**：根据数据和分析目的选择
2. **保持简洁**：避免过多元素
3. **标注清晰**：标题、坐标轴、图例完整
4. **交互性**：使用 plotly 增强分析体验
5. **一致性**：同一分析中保持风格一致

---

## 七、延伸学习

### 7.1 推荐研究

1. matplotlib 高级用法
2. plotly 交互功能
3. 金融专用图表
4. Dashboard 开发

### 7.2 待实践

1. 建立股票分析 Dashboard
2. 行业对比分析图
3. 投资组合监控面板
4. 实时数据可视化

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*
