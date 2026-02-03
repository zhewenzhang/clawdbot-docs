# Python 数据抓取实战：akshare/财报数据/API 对接
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、Python 金融数据获取概述

### 1.1 数据来源分类

```
金融数据来源

├── 免费数据源
│   ├── akshare（A股数据）
│   ├── yfinance（Yahoo Finance）
│   ├── baostock（A股数据）
│   └── tushare（需 Token）
│
├── 付费数据源
│   ├── Bloomberg
│   ├── Refinitiv
│   ├── FactSet
│   └── Wind
│
└── API 接口
    ├── 交易所 API
    ├── 公司 IR API
    └── 第三方 API
```

### 1.2 数据类型

| 数据类型 | 频率 | 来源 |
|----------|------|------|
| **行情数据** | 实时/日频 | akshare、yfinance |
| **财务数据** | 季度 | akshare、Wind |
| **基本面数据** | 日频 | akshare、Eastmoney |
| **宏观数据** | 月/季频 | akshare、Wind |
| **行业数据** | 日/周频 | 行业协会、咨询公司 |

---

## 二、akshare 实战

### 2.1 akshare 介绍

**akshare** 是 Python 的开源金融数据接口库

```python
# 安装
pip install akshare

# 导入
import akshare as ak
```

### 2.2 股票行情数据

**获取股票列表**

```python
import akshare as ak

# A 股股票列表
stock_list = ak.stock_info_a_code_name()
print(stock_list.head())
```

**获取日线行情**

```python
# 股票日线行情（东方财富接口）
df = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                         start_date="20230101", end_date="20231231")
print(df.head())
```

**输出示例**

```
     日期    开盘    收盘    最高    最低     成交量      成交额
0  2023-01-03  15.20  15.45  15.50  15.10  45000000  690000000
1  2023-01-04  15.45  15.60  15.70  15.40  38000000  588000000
2  2023-01-05  15.60  15.55  15.65  15.50  35000000  542500000
```

**获取实时行情**

```python
# 实时行情
df = ak.stock_zh_a_spot_em()
print(df[['代码', '名称', '最新价', '涨跌幅']].head(10))
```

### 2.3 财务数据

**获取利润表**

```python
# 利润表
income = ak.stock_financial_analysis_indicator(symbol="000001")
print(income[['报告期', '营业收入', '净利润']].tail(5))
```

**获取资产负债表**

```python
# 资产负债表
balance = ak.stock_balancesheet_a(symbol="000001", report_type="4")
print(balance[['报告期', '资产总计', '负债合计', '所有者权益']].tail(5))
```

**获取现金流表**

```python
# 现金流表
cashflow = ak.stock_cashflow_a(symbol="000001", report_type="4")
print(cashflow[['报告期', '经营活动产生的现金流量净额']].tail(5))
```

### 2.4 财务指标

```python
# 财务指标
indicator = ak.stock_fina_indicator(symbol="000001")
print(indicator[['报告期', 'roe', 'netprofit_margin', 'grossprofit_margin']].tail(5))
```

**常用指标**

| 指标 | 字段 | 说明 |
|------|------|------|
| ROE | roe | 净资产收益率 |
| 净利率 | netprofit_margin | 净利润率 |
| 毛利率 | grossprofit_margin | 毛利率 |
| 营收增速 | revenue_year_on_year | 营收同比 |
| 净利增速 | profit_year_on_year | 净利润同比 |

### 2.5 行业数据

**行业列表**

```python
# 行业列表
industry = ak.stock_board_industry_name_em()
print(industry.head(20))
```

**行业成分股**

```python
# 行业成分股
industry_stocks = ak.stock_board_industry_cons_th(symbol="半导体及元件")
print(industry_stocks.head(20))
```

**行业行情**

```python
# 行业行情
industry_price = ak.stock_board_industry_change_em()
print(industry_price.head(20))
```

### 2.6 宏观数据

**GDP 数据**

```python
# GDP 数据
gdp = ak.macro_china_gdp()
print(gdp.head(10))
```

**CPI 数据**

```python
# CPI 数据
cpi = ak.macro_china_cpi()
print(cpi.head(10))
```

**货币供应量**

```python
# M2 数据
m2 = ak.macro_china_m2()
print(m2.head(10))
```

---

## 三、yfinance 实战

### 3.1 yfinance 介绍

**yfinance** 是 Yahoo Finance 的 Python 接口

```python
# 安装
pip install yfinance

# 导入
import yfinance as yf
```

### 3.2 获取美股数据

**获取股票数据**

```python
import yfinance as yf

# 获取 NVIDIA 数据
nvda = yf.Ticker("NVDA")

# 历史价格
hist = nvda.history(start="2023-01-01", end="2023-12-31")
print(hist.head())

# 信息
info = nvda.info
print(f"市值: {info.get('marketCap')}")
print(f"P/E: {info.get('trailingPE')}")
print(f"营收: {info.get('totalRevenue')}")
```

**批量获取数据**

```python
# 批量获取多只股票
tickers = yf.Tickers("NVDA AMD TSM QCOM")

# 获取所有信息
for ticker in ["NVDA", "AMD", "TSM", "QCOM"]:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    info = stock.info
    print(f"{ticker}: 当前价 ${hist['Close'].iloc[-1]:.2f}, P/E: {info.get('trailingPE', 'N/A')}")
```

### 3.3 获取基本面数据

```python
# 财务报表
nvda = yf.Ticker("NVDA")

# 利润表
income = nvda.financials
print(income.loc['totalRevenue'])

# 资产负债表
balance = nvda.balance_sheet
print(balance.loc['totalAssets'])

# 现金流
cashflow = nvda.cashflow
print(cashflow.loc['freeCashFlow'])
```

---

## 四、API 数据对接

### 4.1 东方财富 API

```python
import requests

# 东方财富股票列表
def get_stock_list():
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1,
        "pz": 5000,
        "fields": "f12,f14",
        "fs": "m:1 s:2"
    }
    response = requests.get(url, params=params)
    data = response.json()
    stocks = data['data']['list']
    return [{'code': s['f12'], 'name': s['f14']} for s in stocks]

stocks = get_stock_list()
print(f"共 {len(stocks)} 只股票")
```

### 4.2 新浪财经 API

```python
import requests

# 新浪财经股票行情
def get_stock_price(symbol):
    url = f"https://hq.sinajs.cn/list={symbol}"
    headers = {'Referer': 'http://finance.sina.com.cn'}
    response = requests.get(url, headers=headers)
    data = response.text
    values = data.split(',')
    return {
        'open': float(values[1]),
        'close': float(values[2]),
        'high': float(values[3]),
        'low': float(values[4]),
        'volume': int(values[5])
    }

price = get_stock_price("sh600519")
print(price)
```

### 4.3 腾讯财经 API

```python
import requests

# 腾讯财经股票行情
def get_tencent_price(symbol):
    code = symbol.replace('sh', '').replace('sz', '')
    market = '1' if symbol.startswith('sh') else '0'
    url = f"http://qt.gtimg.cn/q={market}{code}"
    response = requests.get(url)
    data = response.text
    values = data.split('~')
    return {
        'code': values[0],
        'name': values[1],
        'price': float(values[3]),
        'change': float(values[32]),
        'volume': int(values[6])
    }

price = get_tencent_price("sh600519")
print(price)
```

---

## 五、数据存储

### 5.1 CSV 存储

```python
import pandas as pd

# 保存到 CSV
df = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                         start_date="20230101", end_date="20231231")
df.to_csv("stock_data.csv", index=False)

# 读取 CSV
df = pd.read_csv("stock_data.csv")
print(df.head())
```

### 5.2 Excel 存储

```python
# 保存到 Excel
df.to_excel("stock_data.xlsx", index=False)

# 读取 Excel
df = pd.read_excel("stock_data.xlsx")
print(df.head())
```

### 5.3 SQLite 存储

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect('stock_data.db')

# 保存数据
df.to_sql('stock_daily', conn, if_exists='replace', index=False)

# 查询数据
df = pd.read_sql('SELECT * FROM stock_daily WHERE 收盘 > 15', conn)
print(df.head())

# 关闭连接
conn.close()
```

### 5.4 MySQL 存储

```python
import pymysql
import pandas as pd

# 连接 MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='stock_data'
)

# 保存数据
df.to_sql('stock_daily', conn, if_exists='replace', index=False)

# 查询数据
df = pd.read_sql('SELECT * FROM stock_daily', conn)
print(df.head())

# 关闭连接
conn.close()
```

---

## 六、数据处理示例

### 6.1 批量获取股票数据

```python
import akshare as ak
import pandas as pd

# 获取股票列表
stock_list = ak.stock_info_a_code_name()

# 批量获取数据
data_list = []
for idx, row in stock_list.head(100).iterrows():
    code = row['代码']
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                start_date="20240101", end_date="20240131")
        if len(df) > 0:
            df['code'] = code
            df['name'] = row['名称']
            data_list.append(df)
    except:
        continue

# 合并数据
all_data = pd.concat(data_list, ignore_index=True)
print(f"获取 {len(all_data)} 条记录")
```

### 6.2 财务数据整合

```python
import akshare as ak
import pandas as pd

# 股票列表
stocks = ['000001', '000002', '600519']

# 批量获取财务数据
financial_data = []
for code in stocks:
    try:
        # 财务指标
        indicator = ak.stock_fina_indicator(symbol=code)
        if len(indicator) > 0:
            latest = indicator.iloc[-1]
            financial_data.append({
                'code': code,
                'roe': latest['roe'],
                'netprofit_margin': latest['netprofit_margin'],
                'grossprofit_margin': latest['grossprofit_margin'],
                'revenue_yoy': latest['revenue_year_on_year']
            })
    except:
        continue

# 转换为 DataFrame
df = pd.DataFrame(financial_data)
print(df)
```

---

## 七、学习要点总结

### 7.1 常用数据源

| 数据源 | 用途 | 费用 |
|--------|------|------|
| **akshare** | A 股数据 | 免费 |
| **yfinance** | 美股数据 | 免费 |
| **baostock** | A 股数据 | 免费 |
| **Wind** | 全方位 | 付费 |
| **Bloomberg** | 全方位 | 付费 |

### 7.2 关键函数

| 功能 | akshare | yfinance |
|------|---------|----------|
| **日线行情** | stock_zh_a_hist() | history() |
| **实时行情** | stock_zh_a_spot_em() | info |
| **财务报表** | stock_financial_*() | financials |
| **财务指标** | stock_fina_indicator() | - |
| **行业数据** | stock_board_*() | - |

### 7.3 数据存储格式

| 格式 | 适用场景 | 优点 |
|------|----------|------|
| **CSV** | 小数据量 | 简单、通用 |
| **Excel** | 中等数据量 | 可视化友好 |
| **SQLite** | 本地数据库 | 查询方便 |
| **MySQL** | 服务器数据库 | 多用户、远程 |

---

## 八、延伸学习

### 8.1 推荐研究

1. akshare 官方文档
2. yfinance 高级用法
3. 实时数据获取
4. 数据质量控制

### 8.2 待实践

1. 建立股票数据获取脚本
2. 自动化财务数据更新
3. 建立本地数据库
4. 数据可视化分析

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*
