# 股票组合回测：Python 回测框架/绩效分析
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、回测概述

### 1.1 回测定义

**回测 = 用历史数据测试投资策略**

```
回测流程

┌─────────────────────────────────────────────────────────┐
│                    设定策略                              │
│              （买入/卖出规则）                           │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    历史数据                              │
│              （价格、财务、宏观数据）                     │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    信号生成                              │
│               （根据策略生成交易信号）                    │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    模拟交易                              │
│              （按信号模拟买入/卖出）                      │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    绩效分析                              │
│              （收益率、回撤、夏普等）                     │
└─────────────────────────────────────────────────────────┘
```

### 1.2 回测框架选择

| 框架 | 优点 | 缺点 | 适用 |
|------|------|------|------|
| **Backtrader** | 功能强大 | 学习曲线陡 | 复杂策略 |
| **zipline** | 专业、回测严谨 | 数据获取复杂 | 机构 |
| **vn.py** | 国产、实盘支持 | 文档少 | 量化交易 |
| **pandas** | 简单灵活 | 功能有限 | 简单策略 |
| **QuantConnect** | 云端、多数据 | 付费 | 在线回测 |

---

## 二、pandas 回测实战

### 2.1 基础回测框架

```python
import pandas as pd
import numpy as np
import akshare as ak
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取股票数据
def get_stock_data(symbol, start_date, end_date):
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                            start_date=start_date, end_date=end_date)
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values('日期')
    df.set_index('日期', inplace=True)
    return df

# 获取多只股票数据
symbols = ['600519', '000001', '600036']
names = ['贵州茅台', '平安银行', '招商银行']

data = {}
for symbol, name in zip(symbols, names):
    df = get_stock_data(symbol, '20230101', '20231231')
    data[name] = df['收盘']
    
# 合并为 DataFrame
prices = pd.DataFrame(data)
prices = prices.dropna()
print(prices.head())
```

### 2.2 简单策略回测

```python
class SimpleBacktest:
    def __init__(self, prices, initial_capital=1000000):
        self.prices = prices
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = {}  # 持仓
        self.portfolio_value = []  # 组合价值
        self.trades = []  # 交易记录
        
    def run(self, strategy_func):
        """运行回测"""
        dates = self.prices.index
        
        for date in dates:
            # 获取当日价格
            day_prices = self.prices.loc[date]
            
            # 获取交易信号
            signals = strategy_func(self.prices.loc[:date], self.positions)
            
            # 执行交易
            for symbol, action in signals.items():
                if symbol not in self.positions:
                    self.positions[symbol] = 0
                    
                if action == 'buy' and symbol in day_prices.index:
                    price = day_prices[symbol]
                    if self.cash >= price * 100:  # 至少买 100 股
                        shares = int(self.cash / price * 0.1)  # 每次买 10%
                        cost = shares * price
                        self.cash -= cost
                        self.positions[symbol] += shares
                        self.trades.append({
                            'date': date,
                            'symbol': symbol,
                            'action': 'buy',
                            'price': price,
                            'shares': shares
                        })
                        
                elif action == 'sell' and symbol in self.positions:
                    price = day_prices[symbol]
                    shares = self.positions[symbol]
                    revenue = shares * price
                    self.cash += revenue
                    self.trades.append({
                        'date': date,
                        'symbol': symbol,
                        'action': 'sell',
                        'price': price,
                        'shares': shares
                    })
                    del self.positions[symbol]
            
            # 计算当日组合价值
            portfolio_value = self.cash
            for symbol, shares in self.positions.items():
                if symbol in day_prices.index:
                    portfolio_value += shares * day_prices[symbol]
            self.portfolio_value.append({
                'date': date,
                'value': portfolio_value
            })
        
        return self.get_results()
    
    def get_results(self):
        """获取回测结果"""
        portfolio_df = pd.DataFrame(self.portfolio_value)
        portfolio_df.set_index('date', inplace=True)
        
        returns = portfolio_df['value'].pct_change()
        
        results = {
            'portfolio': portfolio_df,
            'returns': returns,
            'total_return': (portfolio_df['value'].iloc[-1] / self.initial_capital - 1) * 100,
            'trades': pd.DataFrame(self.trades),
            'positions': self.positions
        }
        return results

# 定义简单策略：MA 金叉买入，死叉卖出
def ma_strategy(prices, positions):
    signals = {}
    for symbol in prices.columns:
        if symbol in positions and positions[symbol] > 0:
            # 持有，检查是否死叉
            recent = prices[symbol].tail(20)
            if len(recent) >= 2:
                ma5 = recent.tail(5).mean()
                ma20 = recent.mean()
                if ma5 < ma20:
                    signals[symbol] = 'sell'
        else:
            # 空仓，检查是否金叉
            recent = prices[symbol].tail(20)
            if len(recent) >= 2:
                ma5 = recent.tail(5).mean()
                ma20 = recent.mean()
                if ma5 > ma20:
                    signals[symbol] = 'buy'
    return signals

# 运行回测
backtest = SimpleBacktest(prices, initial_capital=1000000)
results = backtest.run(ma_strategy)

print(f"总收益率: {results['total_return']:.2f}%")
print(f"最终价值: {results['portfolio']['value'].iloc[-1]:,.0f}")
print(f"交易次数: {len(results['trades'])}")
```

### 2.3 策略示例

**策略 1：动量策略**

```python
def momentum_strategy(prices, lookback=20, holding=5):
    """动量策略：买入近期涨幅最大的股票"""
    signals = {}
    
    # 计算近期收益率
    returns = prices.pct_change(lookback)
    latest_returns = returns.iloc[-1]
    
    # 排序，选择涨幅最大的
    if not latest_returns.isna().all():
        sorted_returns = latest_returns.sort_values(ascending=False)
        top_stocks = sorted_returns.head(holding).index.tolist()
        
        # 生成信号
        for symbol in prices.columns:
            if symbol in top_stocks:
                signals[symbol] = 'buy'
            else:
                signals[symbol] = 'sell'
    
    return signals
```

**策略 2：低波动策略**

```python
def low_volatility_strategy(prices, lookback=60, holding=3):
    """低波动策略：买入波动率最低的股票"""
    signals = {}
    
    # 计算波动率
    returns = prices.pct_change()
    volatility = returns.rolling(lookback).std()
    latest_volatility = volatility.iloc[-1]
    
    # 排序，选择波动率最低的
    if not latest_volatility.isna().all():
        sorted_vol = latest_volatility.sort_values(ascending=True)
        low_vol_stocks = sorted_vol.head(holding).index.tolist()
        
        # 生成信号
        for symbol in prices.columns:
            if symbol in low_vol_stocks:
                signals[symbol] = 'buy'
            else:
                signals[symbol] = 'sell'
    
    return signals
```

**策略 3：双均线策略**

```python
def dual_ma_strategy(prices, short_window=10, long_window=30):
    """双均线策略"""
    signals = {}
    
    for symbol in prices.columns:
        series = prices[symbol]
        
        # 计算均线
        short_ma = series.rolling(short_window).mean()
        long_ma = series.rolling(long_window).mean()
        
        if len(short_ma) < 2:
            signals[symbol] = 'hold'
            continue
        
        # 金叉/死叉判断
        if short_ma.iloc[-2] < long_ma.iloc[-2] and short_ma.iloc[-1] > long_ma.iloc[-1]:
            signals[symbol] = 'buy'
        elif short_iloc[-2] > long_ma.iloc[-2] and short_ma.iloc[-1] < long_ma.iloc[-1]:
            signals[symbol] = 'sell'
        else:
            signals[symbol] = 'hold'
    
    return signals
```

---

## 三、绩效分析

### 3.1 收益率指标

```python
def calculate_returns_metrics(portfolio_values, benchmark=None):
    """计算收益率指标"""
    
    # 日收益率
    daily_returns = portfolio_values.pct_change().dropna()
    
    # 总收益率
    total_return = (portfolio_values.iloc[-1] / portfolio_values.iloc[0] - 1) * 100
    
    # 年化收益率
    n_days = len(portfolio_values)
    n_years = n_days / 252
    annualized_return = ((1 + total_return/100) ** (1/n_years) - 1) * 100
    
    # 月度收益率
    monthly_returns = portfolio_values.resample('M').last().pct_change().dropna()
    monthly_win_rate = (monthly_returns > 0).sum() / len(monthly_returns) * 100
    
    metrics = {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'daily_mean': daily_returns.mean() * 100,
        'daily_std': daily_returns.std() * 100,
        'monthly_win_rate': monthly_win_rate,
        'best_month': monthly_returns.max() * 100,
        'worst_month': monthly_returns.min() * 100
    }
    
    return metrics
```

### 3.2 风险指标

```python
def calculate_risk_metrics(portfolio_values, benchmark=None):
    """计算风险指标"""
    
    daily_returns = portfolio_values.pct_change().dropna()
    
    # 最大回撤
    cumulative = (1 + daily_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100
    
    # 最大回撤持续时间
    dd_duration = (drawdown == drawdown.min()).sum()
    
    # 夏普比率
    risk_free_rate = 0.03 / 252  # 年化 3%
    excess_return = daily_returns.mean() - risk_free_rate
    sharpe_ratio = (excess_return / daily_returns.std()) * np.sqrt(252)
    
    # 索提诺比率
    downside_returns = daily_returns[daily_returns < 0]
    downside_std = downside_returns.std()
    sortino_ratio = (excess_return / downside_std) * np.sqrt(252)
    
    # 卡尔马比率
    calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    metrics = {
        'max_drawdown': max_drawdown,
        'max_drawdown_duration': dd_duration,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'calmar_ratio': calmar_ratio,
        'volatility': daily_returns.std() * np.sqrt(252) * 100
    }
    
    return metrics
```

### 3.3 回测结果可视化

```python
def plot_backtest_results(portfolio_values, prices, results):
    """绑制回测结果"""
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    # 1. 组合价值曲线
    ax1 = axes[0]
    ax1.plot(portfolio_values.index, portfolio_values['value'], linewidth=2, label='组合价值')
    ax1.set_title('组合价值曲线', fontsize=14)
    ax1.set_ylabel('价值 (元)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 归一化价格对比
    ax2 = axes[1]
    normalized_prices = prices / prices.iloc[0] * 100
    for col in normalized_prices.columns:
        ax2.plot(normalized_prices.index, normalized_prices[col], alpha=0.5, label=col)
    ax2.set_title('归一化股价对比', fontsize=14)
    ax2.set_ylabel('归一化价格')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. 回撤曲线
    ax3 = axes[2]
    daily_returns = portfolio_values['value'].pct_change()
    cumulative = (1 + daily_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max * 100
    ax3.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
    ax3.set_title('回撤曲线', fontsize=14)
    ax3.set_ylabel('回撤 (%)')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('backtest_results.png', dpi=150)
    plt.show()
    
    # 打印指标
    print("\n" + "="*60)
    print("回测结果")
    print("="*60)
    print(f"总收益率: {results['total_return']:.2f}%")
    print(f"年化收益率: {results['annualized_return']:.2f}%")
    print(f"最大回撤: {results['max_drawdown']:.2f}%")
    print(f"夏普比率: {results['sharpe_ratio']:.2f}")
    print(f"交易次数: {len(results['trades'])}")
```

---

## 四、进阶回测功能

### 4.1 滑点与手续费

```python
class AdvancedBacktest:
    def __init__(self, prices, initial_capital=1000000, 
                 slippage=0.001, commission=0.001):
        self.prices = prices
        self.initial_capital = initial_capital
        self.slippage = slippage  # 滑点 0.1%
        self.commission = commission  # 手续费 0.1%
        self.cash = initial_capital
        self.positions = {}
        self.portfolio_value = []
        self.trades = []
        
    def run(self, strategy_func):
        dates = self.prices.index
        
        for date in dates:
            day_prices = self.prices.loc[date]
            signals = strategy_func(self.prices.loc[:date], self.positions)
            
            for symbol, action in signals.items():
                if symbol not in self.positions:
                    self.positions[symbol] = 0
                    
                if action == 'buy' and symbol in day_prices.index:
                    price = day_prices[symbol] * (1 + self.slippage)  # 滑点
                    if self.cash >= price * 100:
                        shares = int(self.cash / price * 0.1)
                        cost = shares * price * (1 + self.commission)  # 手续费
                        if self.cash >= cost:
                            self.cash -= cost
                            self.positions[symbol] += shares
                            self.trades.append({
                                'date': date, 'symbol': symbol,
                                'action': 'buy', 'price': price, 'shares': shares
                            })
                            
                elif action == 'sell' and symbol in self.positions:
                    price = day_prices[symbol] * (1 - self.slippage)  # 滑点
                    shares = self.positions[symbol]
                    revenue = shares * price * (1 - self.commission)  # 手续费
                    self.cash += revenue
                    self.trades.append({
                        'date': date, 'symbol': symbol,
                        'action': 'sell', 'price': price, 'shares': shares
                    })
                    del self.positions[symbol]
            
            # 计算组合价值
            portfolio_value = self.cash
            for symbol, shares in self.positions.items():
                if symbol in day_prices.index:
                    portfolio_value += shares * day_prices[symbol]
            self.portfolio_value.append({'date': date, 'value': portfolio_value})
        
        return self.get_results()
```

### 4.2 仓位管理

```python
def position_sizing(portfolio_value, atr, risk_per_trade=0.02):
    """
    仓位管理：根据 ATR 计算仓位
    portfolio_value: 组合价值
    atr: 平均真实波幅
    risk_per_trade: 每笔交易风险比例
    """
    risk_amount = portfolio_value * risk_per_trade
    position_size = risk_amount / atr
    return position_size
```

### 4.3 多周期回测

```python
def multi_timeframe_backtest(daily_prices, monthly_prices, strategy_func):
    """
    多周期回测
    每日生成信号，每月再平衡
    """
    signals = []
    
    for date in monthly_prices.index:
        # 获取当月数据
        month_data = daily_prices.loc[:date]
        
        # 生成信号
        daily_signals = strategy_func(month_data)
        
        # 转换为月度信号
        for symbol, action in daily_signals.items():
            if action == 'buy':
                signals.append({'date': date, 'symbol': symbol, 'action': 'buy'})
            elif action == 'sell':
                signals.append({'date': date, 'symbol': symbol, 'action': 'sell'})
    
    return signals
```

---

## 五、学习要点总结

### 5.1 回测框架组成

| 组件 | 说明 |
|------|------|
| **数据获取** | akshare、yfinance |
| **策略定义** | 买入/卖出规则 |
| **信号生成** | 根据价格计算信号 |
| **模拟交易** | 模拟买入/卖出 |
| **绩效分析** | 收益率、回撤、夏普 |

### 5.2 关键指标

| 指标 | 计算 | 含义 |
|------|------|------|
| **总收益率** | (期末-期初)/期初 | 总体表现 |
| **年化收益率** | (1+总收益)^(1/年)-1 | 年度化收益 |
| **最大回撤** | max(峰值-谷值)/峰值 | 最大损失 |
| **夏普比率** | (收益-无风险)/波动率 | 风险调整收益 |
| **胜率** | 盈利次数/总次数 | 交易成功率 |

### 5.3 回测注意事项

| 注意事项 | 说明 |
|----------|------|
| **前视偏差** | 避免使用未来数据 |
| **过拟合** | 避免过度优化参数 |
| **滑点** | 考虑交易成本 |
| **流动性** | 考虑大额交易影响 |
| **样本外测试** | 用未见数据验证 |

---

## 六、延伸学习

### 6.1 推荐研究

1. Backtrader 框架
2. vn.py 实盘交易
3. 机器学习策略
4. 高频回测

### 6.2 待实践

1. 实现更多策略
2. 添加滑点和手续费
3. 多周期回测
4. 策略参数优化

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*
