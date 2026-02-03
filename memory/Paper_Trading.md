# 模拟交易（Paper Trading）实战
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、模拟交易概述

### 1.1 什么是模拟交易

```
模拟交易 = 用虚拟资金模拟真实交易环境

┌─────────────────────────────────────────────────────────┐
│                   模拟交易系统                          │
├─────────────────┬─────────────────┬─────────────────────┤
│   虚拟账户      │   真实行情      │   模拟撮合          │
├─────────────────┼─────────────────┼─────────────────────┤
│ • 初始资金      │ • 实时价格      │ • 限价单成交        │
│ • 持仓记录      │ • 盘口数据      │ • 市价单成交        │
│ • 盈亏统计      │ • 成交记录      │ • 滑点模拟          │
└─────────────────┴─────────────────┴─────────────────────┘
```

### 1.2 模拟交易 vs 真实交易

| 维度 | 模拟交易 | 真实交易 |
|------|----------|----------|
| **资金** | 虚拟 | 真实 |
| **风险** | 无 | 有 |
| **心理** | 轻松 | 紧张 |
| **学习** | 适合 | 不适合 |
| **滑点** | 可忽略 | 实际存在 |
| **流动性** | 充足 | 可能不足 |

### 1.3 模拟交易目的

| 目的 | 说明 |
|------|------|
| **策略验证** | 测试交易策略有效性 |
| **积累经验** | 熟悉交易流程 |
| **心理训练** | 培养交易心态 |
| **参数优化** | 调整策略参数 |
| **回测验证** | 补充回测不足 |

---

## 二、模拟交易系统设计

### 2.1 系统架构

```
模拟交易系统架构

┌─────────────────────────────────────────────────────────┐
│                   用户界面层                            │
│              (Streamlit/命令行/API)                     │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   策略执行层                            │
│              （信号生成/仓位管理/风险管理）              │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   交易模拟层                            │
│              （订单管理/撮合/结算）                      │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   数据层                                │
│              （行情数据/账户数据）                       │
└─────────────────────────────────────────────────────────┘
```

### 2.2 核心类设计

```python
class PaperTrader:
    """模拟交易系统"""
    
    def __init__(self, initial_capital=1000000):
        self.cash = initial_capital          # 可用资金
        self.initial_capital = initial_capital  # 初始资金
        self.positions = {}                   # 持仓
        self.orders = []                      # 订单记录
        self.trades = []                      # 成交记录
        self.portfolio_value = []             # 组合价值历史
        self.daily_pnl = []                   # 每日盈亏
        
    def get_current_price(self, symbol):
        """获取当前价格"""
        # 这里接入真实行情数据
        pass
    
    def place_order(self, symbol, side, quantity, order_type='market', price=None):
        """下单"""
        pass
    
    def cancel_order(self, order_id):
        """取消订单"""
        pass
    
    def get_portfolio_value(self):
        """获取组合价值"""
        pass
    
    def get_daily_report(self):
        """获取日报"""
        pass
```

### 2.3 完整模拟交易系统

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class PaperTrader:
    def __init__(self, initial_capital=1000000):
        self.cash = initial_capital
        self.initial_capital = initial_capital
        self.positions = {}  # {symbol: {'shares':, 'avg_cost':}}
        self.orders = []     # 订单列表
        self.trades = []     # 成交列表
        self.portfolio_history = []
        self.daily_pnl = []
        
    def get_price(self, symbol, date):
        """获取指定日期的价格（模拟数据）"""
        # 模拟价格数据
        np.random.seed(42)
        base_price = 100
        returns = np.random.randn(100) * 0.02
        prices = base_price * np.cumprod(1 + returns)
        return prices[date % 100]
    
    def place_order(self, symbol, side, quantity, price, order_type='limit'):
        """下单"""
        order = {
            'id': len(self.orders) + 1,
            'symbol': symbol,
            'side': side,  # 'buy' or 'sell'
            'quantity': quantity,
            'price': price,
            'status': 'pending',
            'created_at': datetime.now()
        }
        self.orders.append(order)
        return order
    
    def execute_order(self, order, current_price):
        """执行订单"""
        if order['status'] != 'pending':
            return None
            
        # 检查资金/持仓
        if order['side'] == 'buy':
            cost = order['quantity'] * order['price']
            if cost > self.cash:
                return None
            self.cash -= cost
            
            # 更新持仓
            if order['symbol'] not in self.positions:
                self.positions[order['symbol']] = {'shares': 0, 'avg_cost': 0}
            
            pos = self.positions[order['symbol']]
            total_shares = pos['shares'] + order['quantity']
            total_cost = pos['shares'] * pos['avg_cost'] + order['quantity'] * order['price']
            pos['shares'] = total_shares
            pos['avg_cost'] = total_cost / total_shares
            
        else:  # sell
            if order['symbol'] not in self.positions:
                return None
            if self.positions[order['symbol']]['shares'] < order['quantity']:
                return None
            
            self.cash += order['quantity'] * order['price']
            pos = self.positions[order['symbol']]
            pos['shares'] -= order['quantity']
            if pos['shares'] == 0:
                del self.positions[order['symbol']]
        
        # 记录成交
        trade = {
            'id': len(self.trades) + 1,
            'order_id': order['id'],
            'symbol': order['symbol'],
            'side': order['side'],
            'quantity': order['quantity'],
            'price': order['price'],
            'executed_at': datetime.now()
        }
        self.trades.append(trade)
        order['status'] = 'executed'
        
        return trade
    
    def get_portfolio_value(self, current_prices):
        """计算组合价值"""
        value = self.cash
        for symbol, pos in self.positions.items():
            price = current_prices.get(symbol, pos['avg_cost'])
            value += pos['shares'] * price
        return value
    
    def run_backtest(self, strategy, symbols, start_date, end_date):
        """运行回测"""
        # 模拟每日交易
        current_prices = {}
        for date in range(100):  # 简化：100 天
            for symbol in symbols:
                current_prices[symbol] = self.get_price(symbol, date)
            
            # 生成交易信号
            signals = strategy(current_prices, self.positions)
            
            # 执行信号
            for signal in signals:
                price = current_prices[signal['symbol']]
                self.place_order(
                    symbol=signal['symbol'],
                    side=signal['side'],
                    quantity=signal.get('quantity', 100),
                    price=price
                )
            
            # 执行所有挂单
            for order in self.orders:
                if order['status'] == 'pending':
                    self.execute_order(order, current_prices.get(order['symbol'], order['price']))
            
            # 记录组合价值
            portfolio_value = self.get_portfolio_value(current_prices)
            self.portfolio_history.append({
                'date': date,
                'value': portfolio_value
            })
            
            # 清空挂单
            self.orders = [o for o in self.orders if o['status'] == 'pending']
        
        return self.get_results()
    
    def get_results(self):
        """获取回测结果"""
        portfolio_df = pd.DataFrame(self.portfolio_history)
        portfolio_df['daily_return'] = portfolio_df['value'].pct_change()
        
        total_return = (portfolio_df['value'].iloc[-1] / self.initial_capital - 1) * 100
        annualized_return = ((1 + total_return/100) ** (252/len(portfolio_df)) - 1) * 100
        
        # 最大回撤
        cummax = portfolio_df['value'].cummax()
        drawdown = (portfolio_df['value'] - cummax) / cummax
        max_drawdown = drawdown.min() * 100
        
        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'max_drawdown': max_drawdown,
            'portfolio_df': portfolio_df,
            'trades': self.trades,
            'positions': self.positions
        }


# 使用示例
if __name__ == "__main__":
    # 创建交易系统
    trader = PaperTrader(initial_capital=1000000)
    
    # 定义简单策略
    def simple_strategy(prices, positions):
        signals = []
        for symbol, price in prices.items():
            if symbol not in positions or positions[symbol]['shares'] == 0:
                signals.append({
                    'symbol': symbol,
                    'side': 'buy',
                    'quantity': 100
                })
        return signals
    
    # 运行回测
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    results = trader.run_backtest(simple_strategy, symbols, 0, 100)
    
    # 打印结果
    print(f"总收益率: {results['total_return']:.2f}%")
    print(f"年化收益率: {results['annualized_return']:.2f}%")
    print(f"最大回撤: {results['max_drawdown']:.2f}%")
    print(f"交易次数: {len(results['trades'])}")
```

---

## 三、交易策略实现

### 3.1 均线交叉策略

```python
def ma_crossover_strategy(prices, positions, short_window=5, long_window=20):
    """
    均线交叉策略
    金叉买入，死叉卖出
    """
    signals = []
    
    for symbol in prices.keys():
        # 这里简化处理，实际需要使用历史数据
        current_price = prices[symbol]
        
        # 假设使用简单的价格序列
        ma_short = current_price * 0.99  # 简化：短期均线略低于当前价
        ma_long = current_price * 0.95   # 简化：长期均线低于当前价
        
        if symbol not in positions or positions.get(symbol, {'shares': 0})['shares'] == 0:
            # 空仓，金叉买入
            if ma_short > ma_long:
                signals.append({
                    'symbol': symbol,
                    'side': 'buy',
                    'quantity': 100
                })
        else:
            # 持仓，死叉卖出
            if ma_short < ma_long:
                shares = positions[symbol]['shares']
                signals.append({
                    'symbol': symbol,
                    'side': 'sell',
                    'quantity': shares
                })
    
    return signals
```

### 3.2 动量策略

```python
def momentum_strategy(prices, positions, lookback=20, holding=5):
    """
    动量策略
    买入近期涨幅最大的股票
    """
    signals = []
    
    # 计算收益率
    returns = {}
    for symbol, price in prices.items():
        # 简化：使用随机收益率
        returns[symbol] = np.random.randn() * 0.02
    
    # 排序
    sorted_returns = sorted(returns.items(), key=lambda x: x[1], reverse=True)
    top_stocks = [s[0] for s in sorted_returns[:holding]]
    
    # 当前持仓
    current_holdings = list(positions.keys())
    
    # 买入信号
    for symbol in top_stocks:
        if symbol not in current_holdings:
            signals.append({
                'symbol': symbol,
                'side': 'buy',
                'quantity': 100
            })
    
    # 卖出信号
    for symbol in current_holdings:
        if symbol not in top_stocks:
            shares = positions[symbol]['shares']
            signals.append({
                'symbol': symbol,
                'side': 'sell',
                'quantity': shares
            })
    
    return signals
```

### 3.3 网格交易策略

```python
class GridTrader:
    def __init__(self, symbol, entry_price, grid_size=10, grid_pct=0.02):
        self.symbol = symbol
        self.entry_price = entry_price
        self.grid_size = grid_size
        self.grid_pct = grid_pct
        self.orders = []
        self.trades = []
        
    def generate_grid_orders(self):
        """生成网格订单"""
        price_range = self.entry_price * self.grid_pct
        grid_step = price_range / self.grid_size
        
        # 卖出网格（上方）
        for i in range(1, self.grid_size + 1):
            sell_price = self.entry_price + i * grid_step
            self.orders.append({
                'symbol': self.symbol,
                'side': 'sell',
                'price': sell_price,
                'quantity': 100,
                'status': 'pending'
            })
        
        # 买入网格（下方）
        for i in range(1, self.grid_size + 1):
            buy_price = self.entry_price - i * grid_step
            self.orders.append({
                'symbol': self.symbol,
                'side': 'buy',
                'price': buy_price,
                'quantity': 100,
                'status': 'pending'
            })
    
    def check_orders(self, current_price):
        """检查订单是否成交"""
        for order in self.orders:
            if order['status'] == 'pending':
                if order['side'] == 'buy' and current_price <= order['price']:
                    order['status'] = 'executed'
                    self.trades.append(order)
                elif order['side'] == 'sell' and current_price >= order['price']:
                    order['status'] = 'executed'
                    self.trades.append(order)
```

---

## 四、绩效评估

### 4.1 收益率指标

```python
def calculate_returns_metrics(portfolio_values, initial_capital):
    """计算收益率指标"""
    
    # 总收益率
    total_return = (portfolio_values[-1] / initial_capital - 1) * 100
    
    # 年化收益率
    n_days = len(portfolio_values)
    n_years = n_days / 252
    annualized_return = ((1 + total_return/100) ** (1/n_years) - 1) * 100
    
    # 日收益率
    daily_returns = pd.Series(portfolio_values).pct_change().dropna()
    
    # 月度收益率
    monthly_returns = pd.Series(portfolio_values).resample('M').last().pct_change().dropna()
    monthly_win_rate = (monthly_returns > 0).sum() / len(monthly_returns) * 100
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'daily_mean': daily_returns.mean() * 100,
        'daily_std': daily_returns.std() * 100,
        'monthly_win_rate': monthly_win_rate,
        'best_month': monthly_returns.max() * 100,
        'worst_month': monthly_returns.min() * 100
    }
```

### 4.2 风险指标

```python
def calculate_risk_metrics(portfolio_values):
    """计算风险指标"""
    
    daily_returns = pd.Series(portfolio_values).pct_change().dropna()
    
    # 最大回撤
    cumulative = (1 + daily_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100
    
    # 夏普比率
    risk_free_rate = 0.03 / 252
    excess_return = daily_returns.mean() - risk_free_rate
    sharpe_ratio = (excess_return / daily_returns.std()) * np.sqrt(252)
    
    # 索提诺比率
    downside_returns = daily_returns[daily_returns < 0]
    downside_std = downside_returns.std()
    sortino_ratio = (excess_return / downside_std) * np.sqrt(252)
    
    # 卡尔马比率
    annualized_return = daily_returns.mean() * 252
    calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # 波动率
    volatility = daily_returns.std() * np.sqrt(252) * 100
    
    return {
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'calmar_ratio': calmar_ratio,
        'volatility': volatility
    }
```

### 4.3 交易统计

```python
def calculate_trading_stats(trades):
    """计算交易统计"""
    
    if len(trades) == 0:
        return {
            'total_trades': 0,
            'win_rate': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'profit_factor': 0
        }
    
    # 计算盈亏
    buy_prices = []
    sell_prices = []
    
    for trade in trades:
        if trade['side'] == 'buy':
            buy_prices.append(trade['price'])
        else:
            sell_prices.append(trade['price'])
    
    # 简化计算
    wins = []
    losses = []
    
    for i, trade in enumerate(trades):
        if trade['side'] == 'sell':
            # 找对应的买入
            for j in range(i-1, -1, -1):
                if trades[j]['side'] == 'buy' and trades[j]['symbol'] == trade['symbol']:
                    pnl = trade['price'] - trades[j]['price']
                    if pnl > 0:
                        wins.append(pnl)
                    else:
                        losses.append(abs(pnl))
                    break
    
    win_rate = len(wins) / (len(wins) + len(losses)) * 100 if (len(wins) + len(losses)) > 0 else 0
    avg_win = np.mean(wins) if wins else 0
    avg_loss = np.mean(losses) if losses else 0
    profit_factor = sum(wins) / sum(losses) if losses and sum(losses) > 0 else 0
    
    return {
        'total_trades': len(trades),
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor
    }
```

---

## 五、可视化分析

### 5.1 组合曲线

```python
def plot_portfolio(portfolio_df, initial_capital):
    """绑制组合曲线"""
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    # 1. 组合价值曲线
    ax1 = axes[0]
    ax1.plot(portfolio_df.index, portfolio_df['value'], linewidth=2, label='组合价值')
    ax1.axhline(y=initial_capital, color='gray', linestyle='--', label='初始资金')
    ax1.set_title('组合价值曲线', fontsize=14)
    ax1.set_ylabel('价值 (元)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 回撤曲线
    ax2 = axes[1]
    cumulative = (1 + portfolio_df['daily_return']).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max * 100
    ax2.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
    ax2.set_title('回撤曲线', fontsize=14)
    ax2.set_ylabel('回撤 (%)')
    ax2.grid(True, alpha=0.3)
    
    # 3. 收益率分布
    ax3 = axes[2]
    ax3.hist(portfolio_df['daily_return'].dropna(), bins=50, edgecolor='black', alpha=0.7)
    ax3.axvline(x=0, color='red', linestyle='--')
    ax3.set_title('日收益率分布', fontsize=14)
    ax3.set_ylabel('频次')
    ax3.set_xlabel('日收益率')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('portfolio_analysis.png', dpi=150)
    plt.show()
```

### 5.2 交易记录可视化

```python
def plot_trades(prices_df, trades):
    """绑制交易记录"""
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # 绑制价格
    ax.plot(prices_df.index, prices_df['close'], linewidth=1.5, label='价格')
    
    # 标记买入
    for trade in trades:
        if trade['side'] == 'buy':
            ax.scatter(trade['date'], trade['price'], marker='^', 
                      color='green', s=100, label='买入', zorder=5)
    
    # 标记卖出
    for trade in trades:
        if trade['side'] == 'sell':
            ax.scatter(trade['date'], trade['price'], marker='v', 
                      color='red', s=100, label='卖出', zorder=5)
    
    ax.set_title('交易记录', fontsize=14)
    ax.set_ylabel('价格')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('trades.png', dpi=150)
    plt.show()
```

---

## 六、学习要点总结

### 6.1 模拟交易核心

| 组件 | 说明 |
|------|------|
| **虚拟账户** | 记录资金、持仓、订单 |
| **行情数据** | 实时或历史价格 |
| **交易引擎** | 订单管理、撮合、结算 |
| **绩效评估** | 收益率、风险、交易统计 |

### 6.2 策略开发流程

```
1. 策略设计 → 2. 回测验证 → 3. 模拟交易 → 4. 实盘部署
     ↓              ↓              ↓              ↓
  逻辑编写      参数优化        心理训练       小资金试错
```

### 6.3 注意事项

| 注意事项 | 说明 |
|----------|------|
| **滑点** | 模拟时考虑滑点 |
| **流动性** | 大单可能无法成交 |
| **手续费** | 考虑交易成本 |
| **数据质量** | 使用高质量数据 |
| **过拟合** | 避免过度拟合历史 |

---

## 七、延伸学习

### 7.1 推荐研究

1. 实盘交易接口（券商 API）
2. 高频交易策略
3. 机器学习在交易中的应用
4. 风险管理系统

### 7.2 待实践

1. 连接真实行情数据
2. 实现更多交易策略
3. 进行长时间模拟交易
4. 与实盘结果对比分析

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*
