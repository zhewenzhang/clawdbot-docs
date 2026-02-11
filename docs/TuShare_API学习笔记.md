# TuShare API 学习笔记

## 1. TuShare 概述

TuShare 是一个专业的中国金融市场数据接口平台，主要服务于量化投资研究和数据分析。提供包括股票、基金、期货、期权、数字货币等金融数据。

### 1.1 核心特点
- **数据丰富**：覆盖 A 股、港股、期货、期权等
- **接口标准化**：统一的 API 调用方式
- **积分制度**：不同积分级别可访问不同数据
- **Python 支持**：原生 Python 包，易于集成

### 1.2 积分制度
- **注册即得**：100 积分
- **完善信息**：+20 积分
- **数据权限**：根据积分级别开放不同 API
  - 基础数据：120 积分
  - 个股资金流向：2000 积分
  - 沪深股通资金流向：2000 积分
  - 行业资金流向：5000 积分

---

## 2. 安装与配置

### 2.1 安装 TuShare
```bash
pip install tushare
```

### 2.2 配置 Token
```python
import tushare as ts

# 设置 Token（建议使用环境变量）
ts.set_token('your_token_here')

# 初始化 API
pro = ts.pro_api()
```

### 2.3 最佳实践
```python
import os
import tushare as ts

# 从环境变量读取 Token
TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()

# 测试连接
df = pro.trade_cal(exchange='SSE', start_date='20240101', end_date='20240101')
print("TuShare 连接成功！" if len(df) > 0 else "连接失败")
```

---

## 3. API 分类

TuShare API 主要分为以下几类：

### 3.1 基础数据
| API | 描述 | 积分要求 |
|-----|------|---------|
| stock_basic | 股票基础信息 | 2000 |
| trade_cal | 交易日历 | 120 |
| trade_cal | 交易所日历 | 120 |
| name_change | 股票名称变更 | 120 |

### 3.2 行情数据
| API | 描述 | 积分要求 |
|-----|------|---------|
| daily | 每日行情 | 120 |
| daily_basic | 每日指标 | 2000 |
| adj_factor | 复权因子 | 120 |
| weekly | 周行情 | 120 |
| monthly | 月行情 | 120 |

### 3.3 资金流向数据（核心）
| API | 描述 | 积分要求 | 更新频率 |
|-----|------|---------|---------|
| moneyflow | 个股资金流向 | 2000 | 每日19:00 |
| moneyflow_hsgt | 沪深股通资金流向 | 2000 | 每日18:00-20:00 |
| moneyflow_ind_ths | 同花顺行业资金流向 | 5000 | 每日盘后 |
| moneyflow_ind_dc | 东财板块资金流向 | 5000 | 每日盘后 |

### 3.4 融资融券数据
| API | 描述 | 积分要求 |
|-----|------|---------|
| margin | 融资融券汇总 | 2000 |
| margin_detail | 融资融券明细 | 2000 |

### 3.5 基本面数据
| API | 描述 | 积分要求 |
|-----|------|---------|
| income | 利润表 | 2000 |
| balance_sheet | 资产负债表 | 2000 |
| cashflow_statement | 现金流量表 | 2000 |
| express | 业绩预告 | 120 |
| dividend | 分红送股 | 120 |

---

## 4. 资金流向相关 API 详解

### 4.1 moneyflow - 个股资金流向

**接口说明**：获取沪深 A 股资金流向数据，分析大单小单成交情况，用于判别资金动向。

**数据开始于**：2010年

**积分要求**：2000积分

**更新频率**：交易日 19:00

#### 输入参数
| 参数名 | 类型 | 必选 | 描述 |
|--------|------|------|------|
| ts_code | str | N | 股票代码（如：000001.SZ） |
| trade_date | str | N | 交易日期（YYYYMMDD） |
| start_date | str | N | 开始日期 |
| end_date | str | N | 结束日期 |

#### 输出字段
| 字段名 | 描述 |
|--------|------|
| ts_code | 股票代码 |
| trade_date | 交易日期 |
| buy_sm_vol | 小单买入量（手） |
| buy_sm_amt | 小单买入金额（万元） |
| sell_sm_vol | 小单卖出量（手） |
| sell_sm_amt | 小单卖出金额（万元） |
| buy_md_vol | 中单买入量（手） |
| buy_md_amt | 中单买入金额（万元） |
| sell_md_vol | 中单卖出量（手） |
| sell_md_amt | 中单卖出金额（万元） |
| buy_lg_vol | 大单买入量（手） |
| buy_lg_amt | 大单买入金额（万元） |
| sell_lg_vol | 大单卖出量（手） |
| sell_lg_amt | 大单卖出金额（万元） |
| buy_elg_vol | 超大单买入量（手） |
| buy_elg_amt | 超大单买入金额（万元） |
| sell_elg_vol | 超大单卖出量（手） |
| sell_elg_amt | 超大单卖出金额（万元） |
| net_mf_vol | 净流入量（手） |
| net_mf_amt | 净流入金额（万元） |
| net_amount | 净流入额（万元） |

#### 示例代码
```python
import tushare as ts
import os

# 设置 Token
TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()

# 获取单只股票的资金流向
def get_stock_moneyflow(ts_code, start_date, end_date):
    """
    获取指定股票的资金流向数据

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
    df = get_stock_moneyflow('000001.SZ', '20240101', '20240131')
    print(df.head())
```

---

### 4.2 moneyflow_hsgt - 沪深股通资金流向

**接口说明**：获取沪股通、深股通、港股通每日资金流向数据。

**积分要求**：2000积分

**更新频率**：每日 18:00-20:00

**限制**：单次最多返回 300 条记录

#### 输入参数
| 参数名 | 类型 | 必选 | 描述 |
|--------|------|------|------|
| trade_date | str | N | 交易日期（YYYYMMDD） |
| start_date | str | N | 开始日期 |
| end_date | str | N | 结束日期 |

#### 输出字段
| 字段名 | 描述 |
|--------|------|
| trade_date | 交易日期 |
| hsgt_type | 类型（沪股通/深股通/港股通） |
| buy_amount | 买入金额（亿元） |
| sell_amount | 卖出金额（亿元） |
| net_amount | 净流入金额（亿元） |

#### 示例代码
```python
import tushare as ts
import os

TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()

def get_hsgt_moneyflow(start_date, end_date):
    """
    获取沪深股通资金流向数据

    参数:
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame: 沪深股通资金流向数据
    """
    df = pro.moneyflow_hsgt(
        start_date=start_date,
        end_date=end_date
    )
    return df

# 示例
if __name__ == "__main__":
    df = get_hsgt_moneyflow('20240101', '20240131')
    print(df.head(10))
```

---

### 4.3 margin_detail - 融资融券明细

**接口说明**：获取沪深两市每日融资融券明细数据。

**积分要求**：2000积分

**更新频率**：每日收盘后

**限制**：单次最多返回 4000 行数据

#### 输入参数
| 参数名 | 类型 | 必选 | 描述 |
|--------|------|------|------|
| ts_code | str | N | 股票代码 |
| trade_date | str | N | 交易日期 |
| start_date | str | N | 开始日期 |
| end_date | str | N | 结束日期 |

#### 输出字段
| 字段名 | 描述 |
|--------|------|
| ts_code | 股票代码 |
| trade_date | 交易日期 |
| rzye | 融资余额（万元） |
| rzrqye | 融资买入额（万元） |
| rqyl | 融券余量（股） |
| rqrqyl | 融券卖出量（股） |

#### 示例代码
```python
import tushare as ts
import os

TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()

def get_margin_detail(ts_code, start_date, end_date):
    """
    获取融资融券明细数据

    参数:
        ts_code: 股票代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame: 融资融券明细
    """
    df = pro.margin_detail(
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date
    )
    return df

# 示例
if __name__ == "__main__":
    df = get_margin_detail('000001.SZ', '20240101', '20240131')
    print(df.head())
```

---

### 4.4 stock_basic - 股票基础信息

**接口说明**：获取基础信息数据，包括股票代码、名称、上市日期等。

**积分要求**：2000积分

**建议**：获取一次后保存本地，避免重复调用

#### 输入参数
| 参数名 | 类型 | 必选 | 描述 |
|--------|------|------|------|
| exchange | str | N | 交易所 SSE/SZSE |
| list_status | str | N | 上市状态 L/D/P |
| fields | str | N | 指定返回字段 |

#### 输出字段
| 字段名 | 描述 |
|--------|------|
| ts_code | 股票代码 |
| symbol | 股票简称 |
| name | 股票名称 |
| area | 所在地域 |
| industry | 所属行业 |
| list_date | 上市日期 |

#### 示例代码
```python
import tushare as ts
import os

TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()

def get_stock_list():
    """
    获取所有上市股票列表
    """
    df = pro.stock_basic(
        exchange='',
        list_status='L',
        fields='ts_code,symbol,name,area,industry,list_date'
    )
    return df

# 示例
if __name__ == "__main__":
    df = get_stock_list()
    print(f"共获取 {len(df)} 只股票")
    print(df.head())
```

---

## 5. 数据获取最佳实践

### 5.1 批量获取数据
```python
import tushare as ts
import pandas as pd
from tqdm import tqdm

TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()

def get_all_stocks_moneyflow(start_date, end_date):
    """
    获取所有股票的资金流向数据
    注意：需要处理积分限制
    """
    # 先获取股票列表
    stocks = pro.stock_basic(
        exchange='',
        list_status='L',
        fields='ts_code,name'
    )

    all_data = []

    for idx, row in tqdm(stocks.iterrows(), total=len(stocks)):
        try:
            df = pro.moneyflow(
                ts_code=row['ts_code'],
                start_date=start_date,
                end_date=end_date
            )
            if df is not None and len(df) > 0:
                all_data.append(df)
        except Exception as e:
            print(f"Error fetching {row['ts_code']}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return None
```

### 5.2 处理数据量限制
```python
import tushare as ts

TOKEN = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(TOKEN)
pro = ts.pro_api()

def get_moneyflow_with_limit(start_date, end_date):
    """
    处理 moneyflow_hsgt 的 300 条限制
    """
    all_data = []
    current_date = start_date

    while current_date <= end_date:
        df = pro.moneyflow_hsgt(
            trade_date=current_date
        )
        if df is not None and len(df) > 0:
            all_data.append(df)
        current_date = add_days(current_date, 1)  # 假设有日期加减函数

    return pd.concat(all_data, ignore_index=True) if all_data else None
```

### 5.3 数据质量检查
```python
def validate_moneyflow_data(df):
    """
    验证资金流向数据质量
    """
    checks = {
        'null_count': df.isnull().sum(),
        'negative_values': (df.select_dtypes(include=['number']) < 0).sum(),
        'data_types': df.dtypes,
        'shape': df.shape
    }

    for check_name, result in checks.items():
        print(f"{check_name}: {result}")

    return checks
```

---

## 6. 常见问题与注意事项

### 6.1 积分不足
**问题**：调用 API 返回积分不足错误
**解决方案**：
1. 提升 TuShare 积分等级
2. 申请学生/教育优惠
3. 购买企业版服务

### 6.2 调用频率限制
**问题**：API 调用被限流
**解决方案**：
1. 添加请求间隔（推荐 0.1 秒以上）
2. 使用批量接口减少调用次数
3. 缓存常用数据到本地

### 6.3 数据缺失
**问题**：部分日期数据缺失
**解决方案**：
1. 检查是否为非交易日
2. 联系 TuShare 官方反馈
3. 使用替代数据源

### 6.4 字段变更
**问题**：API 返回字段与文档不符
**解决方案**：
1. 使用 fields 参数指定需要的字段
2. 检查 TuShare 官方更新公告
3. 更新代码适配新字段

---

## 7. 注意事项总结

1. **Token 安全**：使用环境变量存储 Token，不要硬编码
2. **积分管理**：了解各 API 的积分要求，合理规划使用
3. **数据缓存**：高频使用的本地数据建议缓存
4. **错误处理**：添加完善的异常处理机制
5. **频率控制**：控制 API 调用频率，避免被限流
6. **数据验证**：使用前进行数据质量检查

---

## 8. 参考资源

- TuShare 官网：https://tushare.pro
- TuShare 文档：https://tushare.pro/document
- GitHub：https://github.com/waditu/tushare
- 积分说明：https://tushare.pro/credit
