# TuShare API 速查表

## 1. 快速入门

### 1.1 安装
```bash
pip install tushare
```

### 1.2 初始化
```python
import tushare as ts

# 设置 Token（推荐使用环境变量）
ts.set_token('your_token_here')

# 创建 API 实例
pro = ts.pro_api()
```

### 1.3 快速测试
```python
# 测试连接
df = pro.trade_cal(exchange='SSE', start_date='20240101', end_date='20240101')
print("连接成功" if len(df) > 0 else "连接失败")
```

---

## 2. 资金流向 API 速查

### 2.1 moneyflow - 个股资金流向

**描述**：获取沪深 A 股资金流向数据

**积分要求**：2000

**更新频率**：交易日 19:00

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| ts_code | str | 否 | 股票代码 | '000001.SZ' |
| trade_date | str | 否 | 交易日期 | '20240115' |
| start_date | str | 否 | 开始日期 | '20240101' |
| end_date | str | 否 | 结束日期 | '20240131' |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| ts_code | str | 股票代码 |
| trade_date | str | 交易日期 |
| buy_sm_vol | float | 小单买入量（手） |
| buy_sm_amt | float | 小单买入金额（万元） |
| sell_sm_vol | float | 小单卖出量（手） |
| sell_sm_amt | float | 小单卖出金额（万元） |
| buy_md_vol | float | 中单买入量（手） |
| buy_md_amt | float | 中单买入金额（万元） |
| sell_md_vol | float | 中单卖出量（手） |
| sell_md_amt | float | 中单卖出金额（万元） |
| buy_lg_vol | float | 大单买入量（手） |
| buy_lg_amt | float | 大单买入金额（万元） |
| sell_lg_vol | float | 大单卖出量（手） |
| sell_lg_amt | float | 大单卖出金额（万元） |
| buy_elg_vol | float | 超大单买入量（手） |
| buy_elg_amt | float | 超大单买入金额（万元） |
| sell_elg_vol | float | 超大单卖出量（手） |
| sell_elg_amt | float | 超大单卖出金额（万元） |
| net_mf_vol | float | 净流入量（手） |
| net_mf_amt | float | 净流入金额（万元） |

**示例**：
```python
# 获取单只股票
df = pro.moneyflow(ts_code='000001.SZ', start_date='20240101', end_date='20240131')

# 获取全部股票
df = pro.moneyflow(start_date='20240101', end_date='20240131')
```

---

### 2.2 moneyflow_hsgt - 沪深股通资金流向

**描述**：获取沪股通、深股通、港股通每日资金流向数据

**积分要求**：2000

**更新频率**：每日 18:00-20:00

**限制**：单次最多返回 300 条

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| trade_date | str | 否 | 交易日期 | '20240115' |
| start_date | str | 否 | 开始日期 | '20240101' |
| end_date | str | 否 | 结束日期 | '20240131' |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | str | 交易日期 |
| hsgt_type | str | 类型（沪股通/深股通/港股通） |
| buy_amount | float | 买入金额（亿元） |
| sell_amount | float | 卖出金额（亿元） |
| net_amount | float | 净流入金额（亿元） |

**示例**：
```python
# 按日期范围获取
df = pro.moneyflow_hsgt(start_date='20240101', end_date='20240131')

# 按单日获取
df = pro.moneyflow_hsgt(trade_date='20240115')
```

---

### 2.3 margin_detail - 融资融券明细

**描述**：获取沪深两市每日融资融券明细

**积分要求**：2000

**更新频率**：每日收盘后

**限制**：单次最多返回 4000 行

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| ts_code | str | 否 | 股票代码 | '000001.SZ' |
| trade_date | str | 否 | 交易日期 | '20240115' |
| start_date | str | 否 | 开始日期 | '20240101' |
| end_date | str | 否 | 结束日期 | '20240131' |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| ts_code | str | 股票代码 |
| trade_date | str | 交易日期 |
| rzye | float | 融资余额（万元） |
| rzrqye | float | 融资买入额（万元） |
| rqyl | float | 融券余量（股） |
| rqrqyl | float | 融券卖出量（股） |

**示例**：
```python
# 获取单只股票
df = pro.margin_detail(ts_code='000001.SZ', start_date='20240101', end_date='20240131')

# 获取全部股票
df = pro.margin_detail(trade_date='20240115')
```

---

## 3. 辅助 API 速查

### 3.1 stock_basic - 股票基础信息

**描述**：获取基础信息数据

**积分要求**：2000

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| exchange | str | 否 | 交易所 SSE/SZSE | 'SSE' |
| list_status | str | 否 | 上市状态 L/D/P | 'L' |
| fields | str | 否 | 指定返回字段 | 'ts_code,name' |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| ts_code | str | 股票代码 |
| symbol | str | 股票简称 |
| name | str | 股票名称 |
| area | str | 所在地域 |
| industry | str | 所属行业 |
| list_date | str | 上市日期 |

**示例**：
```python
# 获取所有上市股票
df = pro.stock_basic(exchange='', list_status='L')

# 获取指定字段
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')
```

---

### 3.2 trade_cal - 交易日历

**描述**：获取交易日历

**积分要求**：120

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| exchange | str | 否 | 交易所 SSE/SZSE | 'SSE' |
| start_date | str | 否 | 开始日期 | '20240101' |
| end_date | str | 否 | 结束日期 | '20240131' |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| exchange | str | 交易所 |
| cal_date | str | 日期 |
| is_open | int | 是否开盘 0/1 |
| pretrade_date | str | 前一交易日 |

**示例**：
```python
# 获取交易日历
df = pro.trade_cal(exchange='SSE', start_date='20240101', end_date='20240131')

# 获取所有交易日
trading_days = df[df['is_open'] == 1]['cal_date'].tolist()
```

---

## 4. 常用查询模板

### 4.1 获取某日所有股票资金流向
```python
def get_all_stocks_moneyflow(date):
    """
    获取某日所有股票资金流向
    注意：数据量可能很大，建议分批处理
    """
    # 获取所有股票
    stocks = pro.stock_basic(
        exchange='',
        list_status='L',
        fields='ts_code'
    )

    all_data = []
    for idx, row in stocks.iterrows():
        try:
            df = pro.moneyflow(ts_code=row['ts_code'], trade_date=date)
            if df is not None:
                all_data.append(df)
        except Exception as e:
            print(f"Error: {e}")

    return pd.concat(all_data, ignore_index=True) if all_data else None
```

### 4.2 计算主力净流入
```python
def calculate_main_net_flow(df):
    """
    计算主力净流入
    主力 = 大单 + 超大单
    """
    df = df.copy()
    df['main_buy'] = df['buy_lg_amt'] + df['buy_elg_amt']
    df['main_sell'] = df['sell_lg_amt'] + df['sell_elg_amt']
    df['main_net_flow'] = df['main_buy'] - df['main_sell']
    return df
```

### 4.3 计算散户净流入
```python
def calculate_retail_net_flow(df):
    """
    计算散户净流入
    散户 = 小单 + 中单
    """
    df = df.copy()
    df['retail_buy'] = df['buy_sm_amt'] + df['buy_md_amt']
    df['retail_sell'] = df['sell_sm_amt'] + df['sell_md_amt']
    df['retail_net_flow'] = df['retail_buy'] - df['retail_sell']
    return df
```

### 4.4 计算资金集中度
```python
def calculate_concentration(df):
    """
    计算资金集中度
    集中度 = 主力净流入 / 总净流入 * 100%
    """
    df = df.copy()
    total = df['main_net_flow'] + df['retail_net_flow']
    df['concentration'] = np.where(
        total != 0,
        df['main_net_flow'] / total * 100,
        0
    )
    return df
```

### 4.5 筛选资金流入股票
```python
def screen_inflow_stocks(date, min_flow=1000):
    """
    筛选资金净流入股票
    """
    df = get_all_stocks_moneyflow(date)
    if df is None:
        return None

    df = calculate_main_net_flow(df)
    df = df[df['main_net_flow'] > min_flow]
    return df.sort_values('main_net_flow', ascending=False)
```

---

## 5. 错误处理

### 5.1 常见错误代码

| 错误代码 | 说明 | 解决方案 |
|---------|------|---------|
| 40001 | Token 无效 | 检查 Token 是否正确 |
| 40002 | Token 过期 | 重新获取 Token |
| 40003 | 积分不足 | 提升积分等级 |
| 40004 | 参数错误 | 检查参数格式 |
| 40005 | 无数据 | 检查日期是否为交易日 |
| 40006 | 请求过于频繁 | 添加延迟后重试 |

### 5.2 异常处理模板
```python
import tushare as ts
import time

def safe_api_call(func, max_retries=3, delay=1):
    """
    安全调用 API，带重试机制
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            error_msg = str(e)
            if '积分不足' in error_msg:
                raise Exception("积分不足，请提升积分等级")
            elif '过于频繁' in error_msg:
                time.sleep(delay * (attempt + 1))
                continue
            else:
                raise e
    raise Exception(f"重试{max_retries}次后失败")
```

### 5.3 数据验证
```python
def validate_moneyflow_data(df):
    """
    验证资金流向数据
    """
    if df is None:
        return False, "数据为空"

    if len(df) == 0:
        return False, "无数据记录"

    required_fields = ['ts_code', 'trade_date', 'buy_lg_amt', 'sell_lg_amt']
    for field in required_fields:
        if field not in df.columns:
            return False, f"缺少必要字段: {field}"

    return True, "数据验证通过"
```

---

## 6. 性能优化

### 6.1 批量处理
```python
def batch_get_moneyflow(stocks, start_date, end_date, batch_size=100):
    """
    分批获取资金流向
    """
    all_data = []
    for i in range(0, len(stocks), batch_size):
        batch = stocks[i:i + batch_size]
        for code in batch:
            try:
                df = pro.moneyflow(ts_code=code, start_date=start_date, end_date=end_date)
                if df is not None:
                    all_data.append(df)
            except:
                continue
    return pd.concat(all_data, ignore_index=True) if all_data else None
```

### 6.2 添加延迟
```python
import time

def get_moneyflow_with_delay(ts_code, start_date, end_date, delay=0.1):
    """
    带延迟获取数据
    """
    time.sleep(delay)
    return pro.moneyflow(ts_code=ts_code, start_date=start_date, end_date=end_date)
```

### 6.3 数据缓存
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_moneyflow(ts_code, start_date, end_date):
    """
    缓存常用数据
    """
    return pro.moneyflow(ts_code=ts_code, start_date=start_date, end_date=end_date)
```

---

## 7. 数据字典

### 7.1 资金规模定义

| 规模 | 单笔成交额 | 字段 |
|------|----------|------|
| 超大单 | ≥50万元 | buy_elg_amt / sell_elg_amt |
| 大单 | 10-50万元 | buy_lg_amt / sell_lg_amt |
| 中单 | 4-10万元 | buy_md_amt / sell_md_amt |
| 小单 | <4万元 | buy_sm_amt / sell_sm_amt |

### 7.2 交易所代码

| 代码 | 交易所 |
|------|--------|
| SSE | 上海证券交易所 |
| SZSE | 深圳证券交易所 |

### 7.3 上市状态

| 代码 | 状态 |
|------|------|
| L | 上市 |
| D | 退市 |
| P | 暂停上市 |

---

## 8. 快捷参考

### 8.1 常用查询速查

| 需求 | API | 示例 |
|------|-----|------|
| 获取股票列表 | stock_basic | pro.stock_basic(list_status='L') |
| 获取单日资金流向 | moneyflow | pro.moneyflow(trade_date='20240115') |
| 获取单只股票资金流向 | moneyflow | pro.moneyflow(ts_code='000001.SZ') |
| 获取沪深股通资金流向 | moneyflow_hsgt | pro.moneyflow_hsgt(start_date='20240101') |
| 获取融资融券数据 | margin_detail | pro.margin_detail(ts_code='000001.SZ') |
| 获取交易日历 | trade_cal | pro.trade_cal(exchange='SSE') |

### 8.2 积分要求速查

| API | 积分要求 |
|-----|---------|
| trade_cal | 120 |
| stock_basic | 2000 |
| moneyflow | 2000 |
| moneyflow_hsgt | 2000 |
| margin_detail | 2000 |
| daily | 120 |

---

## 9. 注意事项

1. **Token 安全**：使用环境变量存储，不要硬编码
2. **积分管理**：了解各 API 积分要求，合理使用
3. **频率控制**：添加延迟，避免频繁调用
4. **数据验证**：使用前检查数据完整性
5. **错误处理**：添加完善的异常处理机制
6. **数据缓存**：高频数据建议缓存到本地

---

## 10. 参考链接

- TuShare 官网：https://tushare.pro
- API 文档：https://tushare.pro/document
- GitHub：https://github.com/waditu/tushare
- 积分说明：https://tushare.pro/credit
