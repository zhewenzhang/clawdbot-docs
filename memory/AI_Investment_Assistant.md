# AI 投资助手：LLM 财报解读/估值报告生成
> 学习笔记 | 版本：1.0 | 2026-02-03

---

## 一、AI 投资助手概述

### 1.1 应用场景

```
AI 投资助手应用场景

┌─────────────────────────────────────────────────────────┐
│                   AI 投资助手                           │
├─────────────────┬─────────────────┬─────────────────────┤
│   财报解读      │   估值分析      │   投资问答          │
├─────────────────┼─────────────────┼─────────────────────┤
│ • 自动提取关键  │ • DCF 估值      │ • 行业分析          │
│ • 识别异常指标  │ • 相对估值      │ • 公司对比          │
│ • 生成摘要      │ • 估值报告      │ • 投资建议          │
│ • 趋势分析      │ • 估值对比      │ • 风险提示          │
└─────────────────┴─────────────────┴─────────────────────┘
```

### 1.2 技术架构

```
AI 投资助手架构

┌─────────────────────────────────────────────────────────┐
│                   用户界面                              │
│              (Streamlit/命令行/API)                     │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   意图识别                              │
│              (判断用户需求类型)                          │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   数据处理                              │
│          (获取财务数据/行情数据)                         │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   LLM 分析                              │
│              (财报解读/估值分析)                         │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   输出生成                              │
│              (报告/建议/回答)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 二、LLM 财报解读

### 2.1 财报数据获取与结构化

```python
import akshare as ak
import pandas as pd
from datetime import datetime

def get_financial_data(stock_code):
    """获取财务数据"""
    data = {}
    
    # 财务指标
    try:
        indicator = ak.stock_fina_indicator(symbol=stock_code)
        if len(indicator) > 0:
            latest = indicator.iloc[-1]
            data['indicators'] = {
                'roe': latest.get('roe', 0),
                'netprofit_margin': latest.get('netprofit_margin', 0),
                'grossprofit_margin': latest.get('grossprofit_margin', 0),
                'revenue_yoy': latest.get('revenue_year_on_year', 0),
                'profit_yoy': latest.get('profit_year_on_year', 0),
                'eps': latest.get('eps', 0),
                'bvps': latest.get('bps', 0)
            }
    except Exception as e:
        print(f"获取财务指标失败: {e}")
    
    # 利润表
    try:
        income = ak.stock_income_statement(symbol=stock_code)
        if len(income) > 0:
            latest = income.iloc[-1]
            data['income'] = {
                'revenue': latest.get('operating_revenue', latest.get('total_operate_income', 0)),
                'net_profit': latest.get('net_profit', latest.get('net_profit_attributable', 0)),
                'operating_profit': latest.get('operating_profit', 0)
            }
    except Exception as e:
        print(f"获取利润表失败: {e}")
    
    # 资产负债表
    try:
        balance = ak.stock_balance_sheet(symbol=stock_code)
        if len(balance) > 0:
            latest = balance.iloc[-1]
            data['balance'] = {
                'total_assets': latest.get('total_assets', 0),
                'total_liabilities': latest.get('total_liabilities', 0),
                'total_equity': latest.get('total_hldr_eqy_excl_min_int', latest.get('total_owner_equity', 0))
            }
    except Exception as e:
        print(f"获取资产负债表失败: {e}")
    
    return data

# 示例
data = get_financial_data("600519")
print(data)
```

### 2.2 财报分析 Prompt

```python
FINANCIAL_ANALYSIS_PROMPT = """
你是一位专业的财务分析师。请分析以下财务数据并给出详细报告：

【公司信息】
公司代码：{stock_code}
分析日期：{analysis_date}

【财务指标】
- ROE（净资产收益率）：{roe:.2f}%
- 净利润率：{netprofit_margin:.2f}%
- 毛利率：{grossprofit_margin:.2f}%
- 营收增长率：{revenue_yoy:.2f}%
- 净利润增长率：{profit_yoy:.2f}%
- 每股收益（EPS）：{eps:.2f}元
- 每股净资产（BPS）：{bvps:.2f}元

【利润表摘要】
- 营业收入：{revenue:,.0f}百万元
- 净利润：{net_profit:,.0f}百万元

【资产负债表摘要】
- 总资产：{total_assets:,.0f}百万元
- 总负债：{total_liabilities:,.0f}百万元
- 股东权益：{total_equity:,.0f}百万元

请分析以下内容：
1. 盈利能力分析
2. 成长性分析
3. 偿债能力分析
4. 运营效率分析
5. 风险提示
6. 综合评价

请用简洁、专业的语言回答，避免过多使用 Markdown 格式。
"""

def generate_financial_report(stock_code, stock_name):
    """生成财务分析报告"""
    data = get_financial_data(stock_code)
    
    if not data or 'indicators' not in data:
        return "无法获取财务数据"
    
    indicators = data['indicators']
    income = data.get('income', {})
    balance = data.get('balance', {})
    
    # 填充 Prompt
    prompt = FINANCIAL_ANALYSIS_PROMPT.format(
        stock_code=f"{stock_name} ({stock_code})",
        analysis_date=datetime.now().strftime("%Y-%m-%d"),
        roe=indicators.get('roe', 0),
        netprofit_margin=indicators.get('netprofit_margin', 0),
        grossprofit_margin=indicators.get('grossprofit_margin', 0),
        revenue_yoy=indicators.get('revenue_yoy', 0),
        profit_yoy=indicators.get('profit_yoy', 0),
        eps=indicators.get('eps', 0),
        bvps=indicators.get('bvps', 0),
        revenue=income.get('revenue', 0),
        net_profit=income.get('net_profit', 0),
        total_assets=balance.get('total_assets', 0),
        total_liabilities=balance.get('total_liabilities', 0),
        total_equity=balance.get('total_equity', 0)
    )
    
    return prompt
```

### 2.3 LLM 集成

```python
import os

# 使用 OpenAI API
def call_llm(prompt, model="gpt-4"):
    """调用 LLM"""
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位专业的投资顾问和财务分析师。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content

# 使用 Claude API
def call_claude(prompt, model="claude-3-5-sonnet-20241022"):
    """调用 Claude"""
    import anthropic
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text

# 使用 MiniMax API
def call_minimax(prompt):
    """调用 MiniMax"""
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv("MINIMAX_API_KEY"),
        base_url="https://api.minimax.io/anthropic"
    )
    
    response = client.chat.completions.create(
        model="MiniMax-M2.1",
        messages=[
            {"role": "system", "content": "你是一位专业的投资顾问和财务分析师。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content
```

---

## 三、估值报告生成

### 3.1 估值分析 Prompt

```python
VALUATION_REPORT_PROMPT = """
你是一位专业的投资分析师。请对以下公司进行估值分析并生成详细报告：

【公司信息】
公司代码：{stock_code}
当前股价：{current_price:.2f}
行业：{industry}

【财务数据】
- 最新市盈率（P/E）：{pe:.2f}
- 市净率（P/B）：{pb:.2f}
- 股息率：{dividend_yield:.2f}%
- ROE：{roe:.2f}%
- 营收增长率：{revenue_growth:.2f}%

【行业数据】
- 行业平均 P/E：{industry_pe:.2f}
- 行业平均 P/B：{industry_pb:.2f}

【历史估值区间】
- 5 年最低 P/E：{pe_5y_low:.2f}
- 5 年最高 P/E：{pe_5y_high:.2f}
- 5 年平均 P/E：{pe_5y_avg:.2f}

请分析以下内容：
1. 估值水平判断（当前估值在历史区间的位置）
2. 与行业对比分析
3. 估值合理性评估
4. 估值风险提示
5. 估值区间预测
6. 投资建议

请给出：
- 合理估值区间
- 当前估值评级（低估/合理/高估）
- 风险评级（低/中/高）
- 投资评级（买入/持有/卖出）

请用简洁、专业的语言回答，避免过多使用 Markdown 格式。
"""

def generate_valuation_report(stock_code, stock_name, current_price, pe, pb, 
                               industry, industry_pe, industry_pb):
    """生成估值报告"""
    prompt = VALUATION_REPORT_PROMPT.format(
        stock_code=f"{stock_name} ({stock_code})",
        current_price=current_price,
        industry=industry,
        pe=pe,
        pb=pb,
        dividend_yield=1.5,  # 假设
        roe=15.0,  # 假设
        revenue_growth=10.0,  # 假设
        industry_pe=industry_pe,
        industry_pb=industry_pb,
        pe_5y_low=15.0,  # 假设
        pe_5y_high=35.0,  # 假设
        pe_5y_avg=25.0  # 假设
    )
    
    return prompt
```

---

## 四、AI 投资助手实现

### 4.1 完整助手类

```python
import streamlit as st
import pandas as pd
import akshare as ak
from datetime import datetime

class InvestmentAssistant:
    def __init__(self):
        self.capabilities = {
            "财报分析": self.analyze_financials,
            "估值分析": self.analyze_valuation,
            "投资建议": self.get_investment_advice,
            "行业分析": self.analyze_industry,
            "公司对比": self.compare_companies,
            "风险评估": self.assess_risk
        }
    
    def analyze_financials(self, stock_code, stock_name):
        """财报分析"""
        # 获取数据
        data = get_financial_data(stock_code)
        
        # 生成报告
        prompt = generate_financial_report(stock_code, stock_name)
        
        # 调用 LLM
        report = call_minimax(prompt)
        
        return report
    
    def analyze_valuation(self, stock_code, stock_name, current_price, pe, pb):
        """估值分析"""
        # 获取行业数据
        industry = "半导体"  # 假设
        industry_pe = 30.0
        industry_pb = 4.0
        
        # 生成报告
        prompt = generate_valuation_report(
            stock_code, stock_name, current_price, pe, pb,
            industry, industry_pe, industry_pb
        )
        
        # 调用 LLM
        report = call_minimax(prompt)
        
        return report
    
    def get_investment_advice(self, stock_code, stock_name):
        """投资建议"""
        prompt = f"""
        请对 {stock_name} ({stock_code}) 给出投资建议。
        
        分析维度：
        1. 当前市场环境
        2. 公司基本面
        3. 技术面分析
        4. 风险因素
        5. 投资建议
        
        请给出：
        - 投资评级（买入/持有/卖出）
        - 目标价
        - 止损价
        - 持有期限
        - 仓位建议
        """
        
        return call_minimax(prompt)
    
    def analyze_industry(self, industry_name):
        """行业分析"""
        prompt = f"""
        请对 {industry_name} 行业进行深度分析：
        
        分析维度：
        1. 行业规模和增长趋势
        2. 竞争格局
        3. 政策环境
        4. 技术发展趋势
        5. 风险因素
        6. 投资机会
        
        请给出行业投资评级。
        """
        
        return call_minimax(prompt)
    
    def compare_companies(self, companies):
        """公司对比"""
        prompt = f"""
        请对以下公司进行对比分析：
        
        公司列表：
        {chr(10).join([f'- {c}' for c in companies])}
        
        分析维度：
        1. 盈利能力对比
        2. 成长性对比
        3. 估值对比
        4. 风险对比
        5. 综合评价
        6. 投资建议
        
        请给出：
        - 最佳投资标的
        - 各公司优劣势
        """
        
        return call_minimax(prompt)
    
    def assess_risk(self, stock_code, stock_name):
        """风险评估"""
        prompt = f"""
        请对 {stock_name} ({stock_code}) 进行风险评估：
        
        风险维度：
        1. 市场风险
        2. 行业风险
        3. 公司经营风险
        4. 财务风险
        5. 流动性风险
        6. 地缘政治风险
        
        请给出：
        - 风险等级（低/中/高）
        - 主要风险因素
        - 风险应对建议
        """
        
        return call_minimax(prompt)
```

### 4.2 Streamlit 界面

```python
import streamlit as st
import pandas as pd
import akshare as ak

# 初始化助手
assistant = InvestmentAssistant()

st.title("🤖 AI 投资助手")

# 侧边栏
st.sidebar.header("功能选择")
function = st.sidebar.selectbox(
    "选择功能",
    ["财报分析", "估值分析", "投资建议", "行业分析", "公司对比", "风险评估"]
)

# 股票选择
st.sidebar.subheader("股票选择")
stock_name = st.sidebar.text_input("公司名称", "贵州茅台")
stock_code = st.sidebar.text_input("股票代码", "600519")

# 主内容区
if function == "财报分析":
    st.header("📊 财报分析")
    if st.button("生成财报分析"):
        with st.spinner("正在分析财报..."):
            report = assistant.analyze_financials(stock_code, stock_name)
            st.write(report)

elif function == "估值分析":
    st.header("💰 估值分析")
    col1, col2 = st.columns(2)
    with col1:
        current_price = st.number_input("当前股价", value=1800.0)
    with col2:
        pe = st.number_input("市盈率 P/E", value=30.0)
    
    if st.button("生成估值分析"):
        with st.spinner("正在分析估值..."):
            report = assistant.analyze_valuation(stock_code, stock_name, current_price, pe, 5.0)
            st.write(report)

elif function == "投资建议":
    st.header("💡 投资建议")
    if st.button("获取投资建议"):
        with st.spinner("正在生成建议..."):
            advice = assistant.get_investment_advice(stock_code, stock_name)
            st.write(advice)

elif function == "行业分析":
    st.header("📈 行业分析")
    industry = st.text_input("行业名称", "半导体")
    if st.button("分析行业"):
        with st.spinner("正在分析行业..."):
            analysis = assistant.analyze_industry(industry)
            st.write(analysis)

elif function == "公司对比":
    st.header("⚖️ 公司对比")
    companies = st.text_area("输入公司列表（每行一个）", "贵州茅台\n五粮液\n洋河股份")
    if st.button("对比公司"):
        company_list = [c.strip() for c in companies.split('\n') if c.strip()]
        with st.spinner("正在对比..."):
            comparison = assistant.compare_companies(company_list)
            st.write(comparison)

elif function == "风险评估":
    st.header("⚠️ 风险评估")
    if st.button("评估风险"):
        with st.spinner("正在评估风险..."):
            risk = assistant.assess_risk(stock_code, stock_name)
            st.write(risk)
```

---

## 五、Prompt 工程最佳实践

### 5.1 Prompt 结构

```
标准 Prompt 结构

1. 角色定义：你是一位专业的投资分析师
2. 任务描述：请分析以下公司的财务数据
3. 数据提供：具体的财务数据
4. 分析要求：明确的分析维度
5. 输出格式：期望的回答格式
6. 约束条件：避免的事项
```

### 5.2 高效 Prompt 示例

```python
# 好的 Prompt
GOOD_PROMPT = """
你是一位资深的投资分析师。请分析 {stock} 的投资价值。

要求：
1. 分析要简洁明了
2. 给出明确的投资建议
3. 列出关键风险因素

请在 500 字内完成分析。
"""

# 不好的 Prompt
BAD_PROMPT = """
分析一下这个股票怎么样？
"""

# 优化后的 Prompt
OPTIMIZED_PROMPT = """
作为专业投资分析师，请对 {stock} 进行快速评估：

【关键数据】
- 当前股价：{price}
- P/E：{pe}
- P/B：{pb}
- ROE：{roe}
- 营收增长：{revenue_growth}%

【分析要求】
1. 估值水平（1-2句话）
2. 核心投资逻辑（1-2句话）
3. 主要风险（1-2句话）
4. 投资评级：买入/持有/卖出

请直接给出结论，避免冗长分析。
"""
```

### 5.3 常见问题处理

```python
# 处理数据缺失
def safe_get_value(data, key, default="数据暂无"):
    """安全获取数据"""
    try:
        value = data.get(key, default)
        if value is None:
            return default
        return value
    except:
        return default

# 处理 LLM 超时
import timeout_decorator

@timeout_decorator.timeout(30)
def call_llm_with_timeout(prompt):
    """带超时的 LLM 调用"""
    return call_llm(prompt)

# 处理错误
def handle_llm_error(func):
    """LLM 调用错误处理"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"分析失败：{str(e)}。请稍后重试。"
    return wrapper
```

---

## 六、学习要点总结

### 6.1 AI 投资助手核心能力

| 能力 | 说明 | 技术 |
|------|------|------|
| **财报解读** | 自动提取关键指标、异常识别 | 数据抓取 + LLM |
| **估值分析** | DCF/相对估值、估值区间 | 估值模型 + LLM |
| **投资问答** | 行业分析、公司对比 | LLM |
| **风险评估** | 多维度风险识别 | LLM |
| **报告生成** | 自动生成分析报告 | LLM |

### 6.2 LLM 选择

| LLM | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **GPT-4** | 能力强 | 昂贵 | 复杂分析 |
| **Claude** | 长文本 | 较慢 | 长报告 |
| **MiniMax** | 便宜、快速 | 能力一般 | 日常分析 |
| **本地模型** | 隐私 | 需要资源 | 敏感数据 |

### 6.3 最佳实践

1. **明确任务**：清晰定义分析目标
2. **提供数据**：给出关键财务数据
3. **约束输出**：限制回答长度和格式
4. **错误处理**：处理 API 异常
5. **持续优化**：根据反馈改进 Prompt

---

## 七、延伸学习

### 7.1 推荐研究

1. Prompt Engineering
2. RAG（检索增强生成）
3. 微调 LLM
4. 多模态分析

### 7.2 待实践

1. 建立行业分析知识库
2. 实现实时数据集成
3. 开发语音助手
4. 构建投资决策系统

---

*本学习笔记由 Clawdbot 自主学习整理*
*版本：1.0 | 2026-02-03*
