# 实时监控面板开发：数据流/预警机制/Dashboard
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、监控面板概述

### 1.1 监控要素

```
监控面板要素

┌─────────────────────────────────────────────────────────┐
│                   实时监控面板                          │
├─────────────────┬─────────────────┬─────────────────────┤
│     行情监控    │     组合监控    │     预警监控        │
├─────────────────┼─────────────────┼─────────────────────┤
│ • 实时价格      │ • 组合价值      │ • 价格预警          │
│ • 涨跌幅        │ • 收益率        │ • 涨跌幅预警        │
│ • 成交量        │ • 持仓比例      │ • 消息推送          │
│ • K 线图        │ • 风险指标      │ • 邮件/短信        │
└─────────────────┴─────────────────┴─────────────────────┘
```

### 1.2 技术架构

```
监控面板架构

┌─────────────────────────────────────────────────────────┐
│                   前端展示层                            │
│              (Streamlit/Dash/Plotly)                    │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   数据处理层                            │
│                 (Pandas/NumPy)                          │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   数据获取层                            │
│              (akshare/行情 API)                         │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   预警触发层                            │
│               (条件判断/消息推送)                        │
└─────────────────────────────────────────────────────────┘
```

---

## 二、Streamlit Dashboard 实战

### 2.1 Streamlit 基础

**安装 Streamlit**

```bash
pip install streamlit
```

**运行 Dashboard**

```bash
streamlit run dashboard.py
```

**基础结构**

```python
import streamlit as st
import pandas as pd
import numpy as np

# 设置页面
st.set_page_config(page_title="投资监控面板", layout="wide")

# 标题
st.title("🎯 投资监控面板")
st.markdown("---")

# 侧边栏
st.sidebar.header("设置")
symbol = st.sidebar.selectbox("选择股票", ["600519", "000001", "600036"])
```

### 2.2 实时行情监控

```python
import streamlit as st
import pandas as pd
import akshare as ak
import time
from datetime import datetime

# 设置页面
st.set_page_config(page_title="行情监控", layout="wide")

st.title("📈 实时行情监控")

# 股票列表
stocks = {
    "贵州茅台": "600519",
    "平安银行": "000001",
    "招商银行": "600036",
    "台积电": "TSM"
}

# 选择股票
col1, col2 = st.columns([1, 3])
with col1:
    selected_stock = st.selectbox("选择股票", list(stocks.keys()))
    symbol = stocks[selected_stock]
    
    # 刷新间隔
    refresh_rate = st.slider("刷新间隔（秒）", 5, 60, 10)

with col2:
    # 获取实时数据
    if symbol == "TSM":
        import yfinance as yf
        data = yf.Ticker(symbol)
        df = data.history(period="5d")
        latest_price = df['Close'].iloc[-1]
        prev_close = df['Open'].iloc[0]
        change = (latest_price - prev_close) / prev_close * 100
        volume = df['Volume'].iloc[-1]
    else:
        df = ak.stock_zh_a_spot_em()
        stock_data = df[df['代码'] == symbol]
        if len(stock_data) > 0:
            latest_price = float(stock_data['最新价'].iloc[0])
            prev_close = float(stock_data['昨收'].iloc[0])
            change = float(stock_data['涨跌幅'].iloc[0])
            volume = float(stock_data['成交量'].iloc[0])

    # 显示关键指标
    m1, m2, m3 = st.columns(3)
    m1.metric("最新价", f"${latest_price:.2f}" if symbol == "TSM" else f"¥{latest_price:.2f}", 
              f"{change:.2f}%")
    m2.metric("涨跌额", f"{latest_price - prev_close:.2f}")
    m3.metric("成交量", f"{volume/1e6:.2f}M")

# 自动刷新
if st.button("刷新数据"):
    st.rerun()

# 自动刷新脚本
if refresh_rate > 0:
    time.sleep(refresh_rate)
    st.rerun()
```

### 2.3 K 线图监控

```python
import streamlit as st
import pandas as pd
import akshare as ak
import plotly.graph_objects as go
from datetime import datetime, timedelta

def get_kline_data(symbol, period="daily", days=90):
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    if symbol == "TSM":
        import yfinance as yf
        data = yf.Ticker(symbol)
        df = data.history(start=start_date, end=end_date)
    else:
        df = ak.stock_zh_a_hist(symbol=symbol, period=period, 
                                start_date=start_date, end_date=end_date)
    
    return df

# K 线图
st.title("📊 K 线图监控")

# 选择股票和时间周期
col1, col2, col3 = st.columns(3)
with col1:
    symbol = st.selectbox("股票", ["600519", "000001", "600036"])
with col2:
    period = st.selectbox("周期", ["日线", "周线", "月线"])
with col3:
    days = st.slider("显示天数", 30, 365, 90)

# 获取数据
period_map = {"日线": "daily", "周线": "weekly", "月线": "monthly"}
df = get_kline_data(symbol, period_map[period], days)

if len(df) > 0:
    # 处理日期
    if symbol == "TSM":
        df['日期'] = df.index
    else:
        df['日期'] = pd.to_datetime(df['日期'])
    
    # K 线图
    fig = go.Figure(data=[go.Candlestick(
        x=df['日期'],
        open=df['开盘'],
        high=df['最高'],
        low=df['最低'],
        close=df['收盘'],
        increasing_line_color='red',
        decreasing_line_color='green',
        name='K 线'
    )])
    
    # 添加均线
    df['MA5'] = df['收盘'].rolling(5).mean()
    df['MA20'] = df['收盘'].rolling(20).mean()
    df['MA60'] = df['收盘'].rolling(60).mean()
    
    fig.add_trace(go.Scatter(x=df['日期'], y=df['MA5'], name='MA5', line=dict(color='orange', width=1)))
    fig.add_trace(go.Scatter(x=df['日期'], y=df['MA20'], name='MA20', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=df['日期'], y=df['MA60'], name='MA60', line=dict(color='purple', width=1)))
    
    fig.update_layout(
        title=f"{symbol} K 线图",
        xaxis_title="日期",
        yaxis_title="价格",
        xaxis_rangeslider_visible=False,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

### 2.4 组合监控

```python
import streamlit as st
import pandas as pd
import akshare as ak
import numpy as np

# 设置页面
st.set_page_config(page_title="组合监控", layout="wide")

st.title("💼 组合监控")

# 定义组合
portfolio = {
    "贵州茅台": {"shares": 100, "cost": 1500},
    "平安银行": {"shares": 1000, "cost": 10},
    "招商银行": {"shares": 500, "cost": 35},
    "台积电": {"shares": 50, "cost": 80}
}

# 获取实时价格
current_prices = {}
for name, info in portfolio.items():
    if name == "台积电":
        import yfinance as yf
        data = yf.Ticker("TSM")
        df = data.history(period="1d")
        current_prices[name] = df['Close'].iloc[-1]
    else:
        symbol_map = {"贵州茅台": "600519", "平安银行": "000001", "招商银行": "600036"}
        df = ak.stock_zh_a_spot_em()
        stock_data = df[df['代码'] == symbol_map[name]]
        if len(stock_data) > 0:
            current_prices[name] = float(stock_data['最新价'].iloc[0])

# 计算组合价值
total_value = 0
total_cost = 0
portfolio_data = []

for name, info in portfolio.items():
    if name in current_prices:
        current_price = current_prices[name]
        cost = info['shares'] * info['cost']
        value = info['shares'] * current_price
        pnl = value - cost
        pnl_pct = (current_price - info['cost']) / info['cost'] * 100
        weight = value / sum(info['shares'] * current_prices.get(name, 0) for name in portfolio.keys() if name in current_prices)
        
        total_value += value
        total_cost += cost
        
        portfolio_data.append({
            "股票": name,
            "持股数": info['shares'],
            "成本价": info['cost'],
            "当前价": current_price,
            "市值": value,
            "盈亏": pnl,
            "盈亏%": pnl_pct,
            "占比": weight * 100
        })

# 显示组合概览
m1, m2, m3, m4 = st.columns(4)
m1.metric("总市值", f"¥{total_value:,.0f}")
m2.metric("总成本", f"¥{total_cost:,.0f}")
m3.metric("总盈亏", f"¥{total_value - total_cost:,.0f}")
m4.metric("收益率", f"{(total_value - total_cost) / total_cost * 100:.2f}%")

# 显示持仓详情
portfolio_df = pd.DataFrame(portfolio_data)
st.dataframe(
    portfolio_df.style.format({
        "成本价": "¥{:.2f}",
        "当前价": "¥{:.2f}",
        "市值": "¥{:.0f}",
        "盈亏": "¥{:.0f}",
        "盈亏%": "{:.2f}%",
        "占比": "{:.1f}%"
    }).background_gradient(subset=['盈亏%'], cmap='RdYlGn'),
    use_container_width=True
)

# 饼图
import plotly.express as px
fig = px.pie(portfolio_df, values='市值', names='股票', title='持仓占比')
st.plotly_chart(fig, use_container_width=True)
```

---

## 三、预警机制

### 3.1 预警类实现

```python
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class PriceAlert:
    def __init__(self):
        self.alerts = []
        
    def add_alert(self, symbol, alert_type, price, message=""):
        """添加预警"""
        alert = {
            "symbol": symbol,
            "type": alert_type,  # 'above' 或 'below'
            "target_price": price,
            "message": message,
            "created_at": datetime.now(),
            "triggered": False
        }
        self.alerts.append(alert)
        
    def check(self, symbol, current_price):
        """检查是否触发预警"""
        triggered = []
        for alert in self.alerts:
            if alert["symbol"] == symbol and not alert["triggered"]:
                if alert["type"] == "above" and current_price >= alert["target_price"]:
                    alert["triggered"] = True
                    triggered.append(alert)
                elif alert["type"] == "below" and current_price <= alert["target_price"]:
                    alert["triggered"] = True
                    triggered.append(alert)
        return triggered
    
    def get_active_alerts(self):
        """获取活跃预警"""
        return [a for a in self.alerts if not a["triggered"]]
    
    def get_triggered_alerts(self):
        """获取已触发预警"""
        return [a for a in self.alerts if a["triggered"]]

# 使用示例
alert_system = PriceAlert()
alert_system.add_alert("600519", "above", 2000, "茅台涨破 2000 元")
alert_system.add_alert("600519", "below", 1500, "茅台跌破 1500 元")
```

### 3.2 预警面板

```python
import streamlit as st
import pandas as pd
from datetime import datetime

# 预警管理系统
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

def add_alert(symbol, alert_type, price, message):
    st.session_state.alerts.append({
        "symbol": symbol,
        "type": alert_type,
        "price": price,
        "message": message,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "活跃"
    })

def delete_alert(index):
    st.session_state.alerts.pop(index)

st.title("🔔 预警管理")

# 添加预警
with st.expander("添加新预警"):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_symbol = st.text_input("股票代码", "600519")
    with col2:
        new_type = st.selectbox("预警类型", ["涨破", "跌破"])
    with col3:
        new_price = st.number_input("目标价格", value=100.0)
    
    new_message = st.text_input("备注", "")
    
    if st.button("添加预警"):
        add_alert(new_symbol, new_type, new_price, new_message)
        st.success("预警添加成功！")

# 显示预警列表
if len(st.session_state.alerts) > 0:
    alerts_df = pd.DataFrame(st.session_state.alerts)
    
    # 状态筛选
    status_filter = st.selectbox("状态筛选", ["全部", "活跃", "已触发"])
    if status_filter != "全部":
        alerts_df = alerts_df[alerts_df["status"] == status_filter]
    
    # 显示预警
    for i, row in alerts_df.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
        with col1:
            st.write(f"**{row['symbol']}**")
        with col2:
            color = "green" if row['type'] == '涨破' else 'red'
            st.markdown(f"<span style='color:{color}'>{row['type']} ¥{row['price']}</span>", unsafe_allow_html=True)
        with col3:
            st.caption(row['message'])
        with col4:
            if st.button("删除", key=f"del_{i}"):
                delete_alert(i)
                st.rerun()
else:
    st.info("暂无预警，点击上方添加")
```

---

## 四、综合 Dashboard

### 4.1 完整 Dashboard

```python
import streamlit as st
import pandas as pd
import numpy as np
import akshare as ak
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# 设置页面
st.set_page_config(
    page_title="投资监控中心",
    layout="wide",
    page_icon="📈"
)

# 标题
st.title("🎯 投资监控中心")
st.markdown("---")

# 侧边栏设置
st.sidebar.header("设置")

# 股票选择
stocks = {
    "贵州茅台": {"code": "600519", "type": "A"},
    "平安银行": {"code": "000001", "type": "A"},
    "招商银行": {"code": "600036", "type": "A"},
    "台积电": {"code": "TSM", "type": "US"}
}

selected_stock = st.sidebar.selectbox("选择股票", list(stocks.keys()))
stock_info = stocks[selected_stock]

# 刷新间隔
refresh_rate = st.sidebar.slider("刷新间隔（秒）", 5, 300, 30)

# 监控选项
st.sidebar.subheader("监控选项")
show_kline = st.sidebar.checkbox("K 线图", value=True)
show_indicator = st.sidebar.checkbox("技术指标", value=True)
show_volume = st.sidebar.checkbox("成交量", value=True)

# 主内容区
col_main, col_side = st.columns([3, 1])

with col_main:
    # 获取实时数据
    if stock_info["type"] == "A":
        df = ak.stock_zh_a_hist(
            symbol=stock_info["code"], 
            period="daily", 
            start_date=(datetime.now() - timedelta(days=180)).strftime('%Y%m%d'),
            end_date=datetime.now().strftime('%Y%m%d')
        )
        df['日期'] = pd.to_datetime(df['日期'])
    else:
        data = yf.Ticker(stock_info["code"])
        df = data.history(period="1y")
        df.index.name = '日期'
        df = df.reset_index()
        df['日期'] = pd.to_datetime(df['Date']).dt.date
        df.columns = ['日期', '开盘', '收盘', '最高', '最低', '成交量', 'Dividends', 'Stock Splits']
    
    # 最新数据
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # 价格信息
    price = latest['收盘']
    change = ((price - prev['收盘']) / prev['收盘']) * 100
    
    # 显示关键指标
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        selected_stock, 
        f"¥{price:.2f}" if stock_info["type"] == "A" else f"${price:.2f}",
        f"{change:.2f}%"
    )
    m2.metric("最高", f"¥{latest['最高']:.2f}" if stock_info["type"] == "A" else f"${latest['最高']:.2f}")
    m3.metric("最低", f"¥{latest['最低']:.2f}" if stock_info["type"] == "A" else f"${latest['最低']:.2f}")
    m4.metric("成交量", f"{latest['成交量']/1e6:.2f}M")
    
    # K 线图
    if show_kline:
        st.subheader("K 线图")
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                           vertical_spacing=0.05,
                           subplot_titles=('K 线', '成交量'),
                           height=600)
        
        # K 线
        fig.add_trace(go.Candlestick(
            x=df['日期'],
            open=df['开盘'],
            high=df['最高'],
            low=df['最低'],
            close=df['收盘'],
            name='K 线',
            increasing_line_color='red',
            decreasing_line_color='green'
        ), row=1, col=1)
        
        # 均线
        df['MA5'] = df['收盘'].rolling(5).mean()
        df['MA20'] = df['收盘'].rolling(20).mean()
        df['MA60'] = df['收盘'].rolling(60).mean()
        
        fig.add_trace(go.Scatter(x=df['日期'], y=df['MA5'], name='MA5', line=dict(color='orange', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['日期'], y=df['MA20'], name='MA20', line=dict(color='blue', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['日期'], y=df['MA60'], name='MA60', line=dict(color='purple', width=1)), row=1, col=1)
        
        # 成交量
        if show_volume:
            colors = ['red' if df['收盘'].iloc[i] >= df['开盘'].iloc[i] else 'green' for i in range(len(df))]
            fig.add_trace(go.Bar(x=df['日期'], y=df['成交量'], name='成交量', marker_color=colors), row=2, col=1)
        
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=650,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 技术指标
    if show_indicator:
        st.subheader("技术指标")
        
        # RSI
        delta = df['收盘'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema12 = df['收盘'].ewm(span=12, adjust=False).mean()
        ema26 = df['收盘'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['Signal']
        
        # 绑制 RSI
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df['日期'], y=df['RSI'], name='RSI', line=dict(color='purple', width=1)))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="超买")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="超卖")
        fig_rsi.update_layout(title="RSI (14)", height=250, yaxis_range=[0, 100])
        
        st.plotly_chart(fig_rsi, use_container_width=True)

with col_side:
    # 快捷操作
    st.subheader("快捷操作")
    
    if st.button("刷新数据"):
        st.rerun()
    
    if st.button("添加自选"):
        st.success(f"{selected_stock} 已添加")
    
    # 预警设置
    st.subheader("价格预警")
    alert_price = st.number_input("预警价格", value=float(price))
    alert_type = st.selectbox("预警类型", ["涨破", "跌破"])
    
    if st.button("设置预警"):
        st.success(f"已设置 {selected_stock} {alert_type} ¥{alert_price}")
    
    # 相关信息
    st.subheader("相关信息")
    st.info(f"代码: {stock_info['code']}")
    st.info(f"类型: {'A 股' if stock_info['type'] == 'A' else '美股'}")

# 自动刷新
if refresh_rate > 0:
    time.sleep(refresh_rate)
    st.rerun()
```

---

## 五、学习要点总结

### 5.1 监控面板要素

| 要素 | 说明 | 实现方式 |
|------|------|----------|
| **实时数据** | 股票价格、涨跌幅 | akshare、yfinance |
| **K 线图** | 技术分析图 | plotly |
| **组合监控** | 持仓价值、盈亏 | pandas |
| **预警机制** | 价格预警、消息推送 | 自定义类 |
| **自动刷新** | 定时更新 | streamlit rerun |

### 5.2 技术栈选择

| 组件 | 推荐工具 | 优点 |
|------|----------|------|
| **前端展示** | Streamlit | 简单、快速 |
| **交互图表** | Plotly | 交互、漂亮 |
| **数据获取** | akshare | 免费、丰富 |
| **实时性** | 定时刷新 | 简单有效 |

### 5.3 最佳实践

1. **合理刷新频率**：平衡实时性和服务器压力
2. **数据缓存**：避免重复请求
3. **错误处理**：处理网络异常
4. **用户友好**：清晰的界面设计

---

## 六、延伸学习

### 6.1 推荐研究

1. Streamlit 高级组件
2. Dash 框架
3. WebSocket 实时数据
4. 数据库存储

### 6.2 待实践

1. 部署到云端
2. 添加用户认证
3. 实现多用户
4. 添加回测功能

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*
