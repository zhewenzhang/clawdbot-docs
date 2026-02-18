# 芯片研究报告多Agent流水线任务计划

## 文档信息
- **创建日期**: 2026-02-15
- **作者**: OpenClaw Agent System
- **版本**: v1.0
- **输出文件**: reports/芯片行业日报_2026-02-15.md

---

## 一、流水线架构概览

### 1.1 三阶段执行流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                        阶段1：数据采集 (并行执行)                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                   │
│  │ Agent-1 │ │ Agent-2 │ │ Agent-3 │ │ Agent-4 │                   │
│  │ 上市清单 │ │ 财务数据 │ │ 产品技术 │ │ 市场情报 │                   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘                   │
│       └────────────┴────────────┴────────────┘                       │
│                         ↓ 全部完成                                   │
├─────────────────────────────────────────────────────────────────────┤
│                        阶段2：分析 (并行执行)                        │
│  ┌─────────┐ ┌─────────┐                                           │
│  │ Agent-5 │ │ Agent-6 │                                           │
│  │ 竞争分析 │ │ 趋势分析 │                                           │
│  └────┬────┘ └────┬────┘                                           │
│       └────────────┘                                               │
│                         ↓ 全部完成                                   │
├─────────────────────────────────────────────────────────────────────┤
│                        阶段3：汇总                                    │
│  ┌─────────┐                                                       │
│  │ Agent-7 │                                                       │
│  │ 生成报告 │                                                       │
│  └─────────┘                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 时间预算

| 阶段 | Agent数量 | 单Agent超时 | 预计总耗时 |
|------|-----------|-------------|------------|
| 阶段1：数据采集 | 4个并行 | 5分钟 | **5分钟** |
| 阶段2：分析 | 2个并行 | 3分钟 | **3分钟** |
| 阶段3：汇总 | 1个 | 2分钟 | **2分钟** |
| **合计** | - | - | **约10分钟** |

---

## 二、任务依赖关系

### 2.1 任务依赖图

```
Task 1 (Agent-1): 扫描上市公司清单
    ↓
Task 2 (Agent-2): 收集财务数据 ─┐
    ↓                          │
Task 3 (Agent-3): 产品技术信息 ─┼──→ [阶段1完成屏障] → Task 5 (Agent-5): 竞争格局分析
    ↓                          │                    ↓
Task 4 (Agent-4): 市场情报 ─────┘                    Task 6 (Agent-6): 趋势分析
                                                      ↓
                                            [阶段2完成屏障] → Task 7 (Agent-7): 生成报告
```

### 2.2 任务详细说明

| 任务ID | Agent | 任务名称 | 前置依赖 | 输出文件 | 超时 |
|--------|-------|---------|---------|---------|------|
| Task-1 | Agent-1 | 扫描上市公司清单 | 无 | data/01_companies_list.json | 5min |
| Task-2 | Agent-2 | 收集财务数据 | 无 | data/02_financial_data.json | 5min |
| Task-3 | Agent-3 | 产品与技术信息 | 无 | data/03_product_tech.json | 5min |
| Task-4 | Agent-4 | 市场情报 | 无 | data/04_market_intel.json | 5min |
| Task-5 | Agent-5 | 竞争格局分析 | Task-1,2,3,4 | data/05_competitive_analysis.json | 3min |
| Task-6 | Agent-6 | 趋势分析 | Task-1,2,3,4 | data/06_trend_analysis.json | 3min |
| Task-7 | Agent-7 | 生成最终报告 | Task-5,6 | reports/芯片行业日报_2026-02-15.md | 2min |

---

## 三、Agent详细定义

### 3.1 Agent-1: 上市公司清单扫描

#### 基本信息
- **Agent ID**: agent-chip-01
- **任务**: 扫描最新芯片设计上市公司清单（A股+台湾）
- **超时**: 5分钟
- **优先级**: P0

#### 工作内容
1. **扫描范围**：
   - A股芯片设计上市公司（按市值排序前20）
   - 台湾半导体上市公司（按市值排序前15）
   - 重点关注：芯片设计、IC制造、封装测试全产业链

2. **数据源**：
   - 东方财富网
   - 同花顺
   - 台湾证券交易所
   - 公开招股说明书

3. **输出数据**：
   - 公司名称（中/英文）
   - 股票代码
   - 上市地点
   - 市值（最新）
   - 主营业务
   - 重点覆盖：欣兴(3037.TW)、深南电路(002176.SZ)、兴森科技(002436.SZ)、南亚电路(8046.TW)、景硕(3189.TW)

#### Prompt模板
```
你是一个专业的芯片行业研究员。请执行以下任务：

**任务目标**：
扫描并整理最新芯片设计上市公司清单（A股+台湾）。

**扫描范围**：
1. A股上市公司（市值前20）：
   - 芯片设计公司
   - IC制造公司
   - 封装测试公司

2. 台湾上市公司（市值前15）：
   - 半导体设计
   - 晶圆制造
   - 封装测试

**重点公司**（必须包含）：
- 欣兴电子 (3037.TW) - IC载板龙头
- 深南电路 (002176.SZ) - 国内载板龙头
- 兴森科技 (002436.SZ) - PCB+载板
- 南亚电路 (8046.TW) - 台系载板厂
- 景硕科技 (3189.TW) - IC载板

**输出要求**：
请以JSON格式输出到 data/01_companies_list.json：

{
  "report_date": "2026-02-15",
  "data_source": ["东方财富", "台湾证券交易所"],
  "mainland_a_list": [
    {
      "name": "公司名称",
      "code": "股票代码",
      "market": "深圳/上海",
      "market_cap": "市值（亿元）",
      "business": "主营业务",
      "chip_segment": "芯片环节"
    }
  ],
  "taiwan_list": [
    {
      "name": "公司名称",
      "code": "股票代码",
      "market": "台湾",
      "market_cap": "市值（新台币亿元）",
      "business": "主营业务",
      "chip_segment": "芯片环节"
    }
  ],
  "focus_companies_status": {
    "欣兴电子": {"status": "包含", "code": "3037.TW"},
    "深南电路": {"status": "包含", "code": "002176.SZ"},
    "兴森科技": {"status": "包含", "code": "002436.SZ"},
    "南亚电路": {"status": "包含", "code": "8046.TW"},
    "景硕科技": {"status": "包含", "code": "3189.TW"}
  }
}

**注意事项**：
- 使用最新公开数据（2025年年报/2024年Q4数据）
- 市值取最近交易日收盘数据
- 主营业务描述简洁准确
- 超时阈值：5分钟
```

#### 输出文件
- **路径**: `data/01_companies_list.json`
- **格式**: JSON
- **示例**:
```json
{
  "report_date": "2026-02-15",
  "data_source": ["东方财富", "台湾证券交易所"],
  "mainland_a_list": [
    {
      "name": "中芯国际",
      "code": "688981.SH",
      "market": "上海",
      "market_cap": "1800.5",
      "business": "晶圆代工",
      "chip_segment": "IC制造"
    }
  ],
  "taiwan_list": [],
  "focus_companies_status": {
    "欣兴电子": {"status": "包含", "code": "3037.TW"},
    "深南电路": {"status": "包含", "code": "002176.SZ"}
  }
}
```

---

### 3.2 Agent-2: 财务数据收集

#### 基本信息
- **Agent ID**: agent-chip-02
- **任务**: 收集重点公司财务数据（欣兴/深南/兴森/南亚/景硕）
- **超时**: 5分钟
- **优先级**: P0

#### 工作内容
1. **目标公司**：
   - 欣兴电子 (3037.TW)
   - 深南电路 (002176.SZ)
   - 兴森科技 (002436.SZ)
   - 南亚电路 (8046.TW)
   - 景硕科技 (3189.TW)

2. **数据维度**：
   - 营收（近4季度）
   - 毛利率
   - 净利润
   - ROE
   - 负债率
   - 现金流

3. **数据源**：
   - 公司年报/季报
   - 东方财富
   - Yahoo Finance (台湾)
   - 公司官网投资者关系

#### Prompt模板
```
你是一个专业的芯片行业财务分析师。请收集以下5家重点公司的最新财务数据：

**目标公司**：
1. 欣兴电子 (3037.TW) - IC载板龙头
2. 深南电路 (002176.SZ) - 国内载板龙头
3. 兴森科技 (002436.SZ) - PCB+载板
4. 南亚电路 (8046.TW) - 台系载板厂
5. 景硕科技 (3189.TW) - IC载板

**数据需求**：
请收集最新年报（2025年）及最近季度（2024年Q4）财务数据：

1. 营收数据：
   - 2024年全年营收
   - 2024年Q4营收
   - 同比增长率

2. 盈利能力：
   - 毛利率
   - 净利润率
   - ROE（净资产收益率）

3. 财务健康：
   - 资产负债率
   - 经营活动现金流

4. 估值指标（如果有）：
   - PE
   - PB

**输出格式**：
输出到 data/02_financial_data.json，格式如下：

{
  "report_date": "2026-02-15",
  "companies": [
    {
      "name": "欣兴电子",
      "code": "3037.TW",
      "currency": "新台币",
      "fiscal_year_2024": {
        "revenue": "营收金额",
        "revenue_yoy": "同比增速%",
        "gross_margin": "毛利率%",
        "net_profit": "净利润",
        "net_margin": "净利率%",
        "roe": "ROE%",
        "debt_ratio": "资产负债率%",
        "cash_flow": "经营活动现金流"
      },
      "quarter_2024q4": {
        "revenue": "Q4营收",
        "revenue_yoy": "Q4同比%",
        "gross_margin": "Q4毛利率%",
        "notes": "备注说明"
      },
      "data_source": ["来源1", "来源2"],
      "last_update": "2026-02-15"
    }
  ],
  "summary": {
    "top_revenue": "营收最高公司",
    "top_margin": "毛利率最高公司",
    "top_roe": "ROE最高公司",
    "analysis": "简要财务对比分析"
  }
}

**注意事项**：
- 台湾公司财报年度为历年制（1月1日-12月31日）
- 人民币/新台币汇率按 1:4.3 换算参考
- 数据不可得时标注"暂无数据"
- 超时阈值：5分钟
```

#### 输出文件
- **路径**: `data/02_financial_data.json`
- **格式**: JSON

---

### 3.3 Agent-3: 产品与技术信息收集

#### 基本信息
- **Agent ID**: agent-chip-03
- **任务**: 收集ABF/BT载板产能与技术参数
- **超时**: 5分钟
- **优先级**: P0

#### 工作内容
1. **产品类别**：
   - ABF载板（Ajinomoto Build-up Film）
   - BT载板（Bismaleimide Triazine）

2. **技术参数**：
   - 层数
   - 线宽线距
   - 最小孔径
   - 板厚
   - 尺寸规格

3. **产能信息**：
   - 现有产能（千平方米/月）
   - 在建产能
   - 产能利用率
   - 扩产计划

#### Prompt模板
```
你是一个专业的半导体封装技术专家。请收集ABF/BT载板的产品与技术信息：

**任务背景**：
ABF载板和BT载板是芯片封装的关键材料，广泛应用于CPU、GPU、ASIC等高端芯片。

**重点公司**：
1. 欣兴电子 - ABF载板龙头
2. 深南电路 - 国内ABF/BT载板龙头
3. 兴森科技 - IC载板新进入者
4. 南亚电路 - BT载板为主
5. 景硕科技 - ABF/BT载板

**数据需求**：

1. ABF载板技术参数（每家公司）：
   - 可生产层数（层）
   - 最小线宽/线距（μm）
   - 最小过孔直径（μm）
   - 板厚范围（mm）
   - 最大尺寸（mm）
   - 工艺节点支持

2. BT载板技术参数：
   - 同上参数
   - 主要应用领域

3. 产能情况（2025年）：
   - ABF载板产能（千平米/月）
   - BT载板产能（千平米/月）
   - 产能利用率（%）
   - 2026年扩产计划

**输出格式**：
输出到 data/03_product_tech.json：

{
  "report_date": "2026-02-15",
  "abf_substrate": {
    "description": "ABF载板概述",
    "key_players": ["欣兴", "深南", "景硕"],
    "technology_trend": "技术发展趋势",
    "companies": [
      {
        "name": "欣兴电子",
        "code": "3037.TW",
        "abf_capacity": "产能数据",
        "technology": {
          "max_layers": "最大层数",
          "min_line_space": "最小线宽线距",
          "min_via_size": "最小孔径",
          "max_board_size": "最大尺寸",
          "thickness_range": "板厚范围"
        },
        "key_customers": ["客户1", "客户2"],
        "expansion_plan": "扩产计划"
      }
    ]
  },
  "bt_substrate": {
    "description": "BT载板概述",
    "key_players": ["南亚电路", "景硕"],
    "companies": []
  },
  "market_share": {
    "abf_global": "ABF全球份额",
    "bt_global": "BT全球份额",
    "china_domestic": "国内厂商份额"
  },
  "data_sources": ["来源1", "来源2"]
}

**注意事项**：
- 数据以最新公开信息为准
- 产能数据标注统计口径
- 注明数据时间节点
- 超时阈值：5分钟
```

#### 输出文件
- **路径**: `data/03_product_tech.json`
- **格式**: JSON

---

### 3.4 Agent-4: 市场情报收集

#### 基本信息
- **Agent ID**: agent-chip-04
- **任务**: 收集Prismark最新数据、行业新闻
- **超时**: 5分钟
- **优先级**: P0

#### 工作内容
1. **Prismark数据**：
   - IC载板市场规模
   - 增长率
   - 细分市场（ABF/BT）
   - 区域市场
   - 市场份额

2. **行业新闻**：
   - 重大行业动态
   - 政策变化
   - 技术突破
   - 供需变化
   - 客户订单

3. **竞争对手动态**：
   - 扩产动态
   - 技术进展
   - 财务表现

#### Prompt模板
```
你是一个专业的半导体市场分析师。请收集芯片载板市场的最新情报：

**任务目标**：
收集Prismark最新数据、行业新闻、竞争对手动态。

**数据需求**：

1. Prismark市场数据（最新版本）：
   - 2024年全球IC载板市场规模
   - ABF载板市场规模
   - BT载板市场规模
   - 2025年市场增长率预测
   - 2026-2030年复合增长率预测
   - 区域市场分布
   - 主要厂商市场份额

2. 行业新闻（近30天）：
   - 芯片设计/制造重大新闻
   - IC载板供需变化
   - 扩产/建厂动态
   - 技术突破
   - 政策/贸易政策变化
   - 客户需求变化

3. 竞争对手动态：
   - 欣兴电子最新动态
   - 深南电路最新动态
   - 兴森科技最新动态
   - 南亚电路最新动态
   - 景硕科技最新动态

**输出格式**：
输出到 data/04_market_intel.json：

{
  "report_date": "2026-02-15",
  "prismark_data": {
    "report_version": "2024.Q4或2025.Q1",
    "global_market_size_2024": "市场规模（亿美元）",
    "abf_market_size_2024": "ABF市场规模",
    "bt_market_size_2024": "BT市场规模",
    "growth_rate_2025": "2025年增长率%",
    "cagr_2025_2030": "2025-2030年复合增长率%",
    "regional_distribution": {
      "china": "中国占比%",
      "taiwan": "台湾占比%",
      "korea": "韩国占比%",
      "japan": "日本占比%",
      "others": "其他占比%"
    },
    "market_share_ranking": [
      {"rank": 1, "company": "公司", "share": "份额%", "segment": "ABF/BT"}
    ]
  },
  "industry_news": [
    {
      "date": "日期",
      "title": "新闻标题",
      "summary": "简要内容",
      "impact": "高/中/低",
      "source": "来源"
    }
  ],
  "competitor_updates": {
    "欣兴电子": {"news": ["动态1"]},
    "深南电路": {"news": ["动态2"]}
  },
  "supply_demand": {
    "overall": "供需状况概述",
    "abf": "ABF载板供需",
    "bt": "BT载板供需",
    "price_trend": "价格趋势"
  },
  "data_sources": ["Prismark", "行业新闻"]
}

**注意事项**：
- Prismark数据标注版本号
- 新闻注明时间和来源
- 供需分析客观中立
- 超时阈值：5分钟
```

#### 输出文件
- **路径**: `data/04_market_intel.json`
- **格式**: JSON

---

### 3.5 Agent-5: 竞争格局分析

#### 基本信息
- **Agent ID**: agent-chip-05
- **任务**: 竞争格局分析（市场份额、财务排名、产能对比）
- **超时**: 3分钟
- **优先级**: P1

#### 前置依赖
- Task-1 (Agent-1) ✅
- Task-2 (Agent-2) ✅
- Task-3 (Agent-3) ✅
- Task-4 (Agent-4) ✅

#### 工作内容
1. **市场份额分析**：
   - 全球市场份额
   - 区域市场份额
   - 产品类别份额

2. **财务排名**：
   - 营收排名
   - 毛利率排名
   - 净利润排名

3. **产能对比**：
   - ABF产能排名
   - BT产能排名
   - 产能利用率对比

4. **竞争力评估**：
   - 技术能力
   - 成本优势
   - 客户结构

#### Prompt模板
```
你是一个资深的半导体行业分析师。请基于以下数据执行竞争格局分析：

**输入数据**：
请读取以下文件：
- data/01_companies_list.json - 上市公司清单
- data/02_financial_data.json - 财务数据
- data/03_product_tech.json - 产品技术信息
- data/04_market_intel.json - 市场情报

**分析任务**：

1. 市场份额分析：
   - 列出全球IC载板前10大厂商及份额
   - 分析ABF/BT载板细分市场格局
   - 评估5家重点公司的市场地位

2. 财务排名对比：
   - 营收规模排名
   - 盈利能力排名（毛利率/净利率）
   - 成长性排名（营收增速）
   - ROE/ROA对比

3. 产能对比：
   - ABF载板产能排名（千平米/月）
   - BT载板产能排名
   - 产能利用率对比
   - 扩产计划对比

4. 竞争力评估矩阵：
   | 公司 | 技术 | 成本 | 客户 | 规模 | 综合评分 |
   |------|------|------|------|------|----------|
   | 欣兴 | 5 | 4 | 5 | 5 | 4.8 |

**输出格式**：
输出到 data/05_competitive_analysis.json：

{
  "report_date": "2026-02-15",
  "market_share": {
    "global_ranking": [
      {"rank": 1, "company": "公司名", "share": "份额%", "segment": "ABF/BT/Both"}
    ],
    "abf_market": {"top_players": [], "notes": "ABF市场格局"},
    "bt_market": {"top_players": [], "notes": "BT市场格局"}
  },
  "financial_ranking": {
    "revenue_rank": [{"rank": 1, "company": "公司", "revenue": "金额", "currency": "币种"}],
    "margin_rank": [{"rank": 1, "company": "公司", "gross_margin": "毛利率%"}],
    "growth_rank": [{"rank": 1, "company": "公司", "growth_rate": "增速%"}]
  },
  "capacity_comparison": {
    "abf_capacity": [
      {"company": "公司", "capacity": "产能", "unit": "千平米/月", "utilization": "利用率%"}
    ],
    "bt_capacity": [],
    "expansion_plans": "扩产计划对比"
  },
  "competitive_matrix": {
    "dimensions": ["技术", "成本", "客户", "规模", "成长"],
    "companies": {
      "欣兴电子": {"技术": 5, "成本": 4, "客户": 5, "规模": 5, "成长": 4, "notes": "龙头地位稳固"},
      "深南电路": {"技术": 4, "成本": 5, "客户": 4, "规模": 4, "成长": 5, "notes": "国产替代受益者"}
    }
  },
  "key_findings": [
    "发现1",
    "发现2"
  ]
}

**注意事项**：
- 基于输入数据进行分析
- 保持客观中立
- 突出重点发现
- 超时阈值：3分钟
```

#### 输出文件
- **路径**: `data/05_competitive_analysis.json`
- **格式**: JSON

---

### 3.6 Agent-6: 趋势分析

#### 基本信息
- **Agent ID**: agent-chip-06
- **任务**: 趋势分析（技术趋势、需求预测、风险提示）
- **超时**: 3分钟
- **优先级**: P1

#### 前置依赖
- Task-1 (Agent-1) ✅
- Task-2 (Agent-2) ✅
- Task-3 (Agent-3) ✅
- Task-4 (Agent-4) ✅

#### 工作内容
1. **技术趋势**：
   - 先进封装发展（HBM/CoWoS）
   - 载板技术演进
   - 工艺节点突破

2. **需求预测**：
   - AI芯片需求
   - 汽车电子需求
   - 消费电子需求
   - 2025-2026年需求预测

3. **风险提示**：
   - 产能过剩风险
   - 价格下行风险
   - 技术替代风险
   - 政策风险
   - 供应链风险

#### Prompt模板
```
你是一个资深的半导体行业战略分析师。请基于以下数据执行趋势分析：

**输入数据**：
请读取以下文件：
- data/01_companies_list.json
- data/02_financial_data.json
- data/03_product_tech.json
- data/04_market_intel.json

**分析任务**：

1. 技术趋势分析：
   - IC载板技术演进路线（层数↑、线宽↓、孔径↓）
   - 先进封装对载板的需求变化（HBM、CoWoS、SoIC）
   - 材料创新（ABF vs BT vs 其他）
   - 国产替代进程

2. 需求预测：
   - AI芯片需求（GPU/TPU/ASIC）
   - 汽车芯片需求（自动驾驶、智能座舱）
   - 消费电子需求（手机、PC、IoT）
   - 2025-2026年细分市场增长预测

3. 风险提示：
   | 风险类型 | 风险描述 | 影响程度 | 发生概率 | 应对建议 |
   |---------|---------|---------|---------|---------|
   | 产能过剩 | 各大厂扩产导致供过于求 | 高 | 中 | 关注产能利用率 |
   | 价格下行 | 竞争加剧导致毛利率下降 | 中 | 高 | 关注毛利率变化 |
   | 技术替代 | 新封装技术减少载板需求 | 中 | 低 | 跟踪技术演进 |

4. 投资观点：
   - 行业景气度判断
   - 推荐关注标的
   - 催化剂与时间窗口

**输出格式**：
输出到 data/06_trend_analysis.json：

{
  "report_date": "2026-02-15",
  "technology_trends": {
    "miniaturization": "向更小线宽、更多层数演进",
    "advanced_packaging": "HBM/CoWoS推动高端载板需求",
    "materials": "ABF需求持续增长",
    "timeline": {
      "2025": "2-3mil线宽成为主流",
      "2026": "1.8mil线宽开始量产",
      "2027": "更高层数载板需求增加"
    }
  },
  "demand_forecast": {
    "overall": "2025年预计增长8-12%",
    "by_segment": {
      "ai_chip": "AI芯片需求预计增长30-40%",
      "automotive": "汽车电子预计增长15-20%",
      "consumer": "消费电子预计增长3-5%"
    },
    "key_drivers": [
      "AI服务器需求爆发",
      "智能驾驶渗透率提升",
      "高性能计算需求增长"
    ]
  },
  "risk_analysis": [
    {
      "type": "产能过剩",
      "description": "欣兴/南亚等大厂持续扩产，2026年产能释放可能供过于求",
      "impact": "高",
      "probability": "中",
      "mitigation": "关注产能利用率和稼动率"
    },
    {
      "type": "价格下行",
      "description": "竞争加剧导致ASP下降",
      "impact": "中",
      "probability": "高",
      "mitigation": "关注毛利率变化"
    }
  ],
  "investment_view": {
    "sentiment": "审慎乐观",
    "preferred_stocks": ["深南电路", "欣兴电子"],
    "catalysts": ["AI芯片需求爆发", "国产替代加速"],
    "risks_to_watch": ["产能过剩", "宏观经济下行"]
  },
  "key_insights": [
    "AI是最大增长引擎",
    "国产替代是长期主题",
    "关注产能扩张节奏"
  ]
}

**注意事项**：
- 客观分析，避免过度乐观
- 明确标注预测依据
- 风险提示要具体
- 超时阈值：3分钟
```

#### 输出文件
- **路径**: `data/06_trend_analysis.json`
- **格式**: JSON

---

### 3.7 Agent-7: 汇总生成报告

#### 基本信息
- **Agent ID**: agent-chip-07
- **任务**: 整合所有数据，生成最终报告
- **超时**: 2分钟
- **优先级**: P1

#### 前置依赖
- Task-5 (Agent-5) ✅
- Task-6 (Agent-6) ✅

#### 工作内容
1. **数据整合**：
   - 汇总7个任务的所有数据
   - 数据验证和质量检查
   - 格式统一化

2. **报告生成**：
   - 执行摘要
   - 重点公司分析
   - 竞争格局
   - 趋势展望
   - 投资建议

3. **输出**：
   - Markdown格式报告
   - 数据快照
   - 更新索引

#### Prompt模板
```
你是一个专业的投资研究报告撰写人。请整合所有分析数据，生成最终的芯片行业研究报告。

**输入数据**：
请读取以下文件并整合：
- data/01_companies_list.json
- data/02_financial_data.json
- data/03_product_tech.json
- data/04_market_intel.json
- data/05_competitive_analysis.json
- data/06_trend_analysis.json

**报告结构**：

```
# 芯片行业日报

**报告日期**: 2026-02-15
**分析师**: OpenClaw Multi-Agent System

---

## 一、核心摘要

[用3-5句话概括今日核心观点]

## 二、市场概览

### 2.1 全球IC载板市场规模（Prismark数据）
- 2024年市场规模：XXX亿美元
- 同比增长：X%
- 2025年预测：增长X%

### 2.2 细分市场
- ABF载板：市场规模XX亿美元，增长X%
- BT载板：市场规模XX亿美元，增长X%

## 三、重点公司财务数据

### 3.1 欣兴电子 (3037.TW)
- 2024年营收：新台币XXX亿元（同比X%）
- 毛利率：XX%
- ABF产能：XX千平米/月

### 3.2 深南电路 (002176.SZ)
- 2024年营收：人民币XXX亿元（同比X%）
- 毛利率：XX%
- 载板产能：XX千平米/月

### 3.3 兴森科技 (002436.SZ)
- ...

### 3.4 南亚电路 (8046.TW)
- ...

### 3.5 景硕科技 (3189.TW)
- ...

## 四、竞争格局

### 4.1 市场份额
[全球Top 10厂商及份额]

### 4.2 产能对比
[5家重点公司产能对比表]

### 4.3 竞争力评估
[技术/成本/客户/规模矩阵]

## 五、技术与趋势

### 5.1 技术趋势
- 先进封装推动高端载板需求
- HBM/CoWoS带动ABF载板量价齐升

### 5.2 需求预测
- AI芯片：预计增长30-40%
- 汽车电子：预计增长15-20%

### 5.3 风险提示
- ⚠️ 产能过剩风险
- ⚠️ 价格下行风险
- ⚠️ 技术替代风险

## 六、投资建议

### 6.1 行业评级
**审慎乐观**

### 6.2 推荐标的
1. 深南电路 - 国产替代核心标的
2. 欣兴电子 - ABF龙头

### 6.3 关注要点
- 产能扩张节奏
- 毛利率变化
- AI芯片需求

---

**免责声明**：本报告仅供参考，不构成投资建议。

**数据来源**：Prismark、公司年报、公开市场信息
**生成时间**：2026-02-15
```

**输出文件**：
1. 主报告：`reports/芯片行业日报_2026-02-15.md`
2. 数据快照：`data/daily_summary_2026-02-15.json`

**注意事项**：
- 报告格式清晰易读
- 数据标注来源
- 图表使用Markdown表格
- 保持客观专业
- 超时阈值：2分钟
```

#### 输出文件
- **主报告**: `reports/芯片行业日报_2026-02-15.md`
- **数据快照**: `data/daily_summary_2026-02-15.json`
- **格式**: Markdown + JSON

---

## 四、数据格式规范

### 4.1 通用JSON格式

所有Agent输出的JSON文件必须遵循以下规范：

```json
{
  "report_date": "YYYY-MM-DD",
  "agent_id": "agent-chip-XX",
  "version": "v1.0",
  "last_updated": "YYYY-MM-DD HH:mm:ss",
  "data_source": ["来源1", "来源2"],
  "data": {
    // 具体数据
  },
  "metadata": {
    "confidence": "高/中/低",
    "completeness": "完整/部分/缺失"
  }
}
```

### 4.2 文件命名规范

| 任务 | 文件名 | 路径 |
|------|--------|------|
| Agent-1 | `01_companies_list.json` | data/ |
| Agent-2 | `02_financial_data.json` | data/ |
| Agent-3 | `03_product_tech.json` | data/ |
| Agent-4 | `04_market_intel.json` | data/ |
| Agent-5 | `05_competitive_analysis.json` | data/ |
| Agent-6 | `06_trend_analysis.json` | data/ |
| Agent-7 | `芯片行业日报_2026-02-15.md` | reports/ |

### 4.3 数据验证规则

```python
# 数据验证伪代码
def validate_data(file_path):
    checks = [
        check_file_exists(file_path),
        check_json_format(file_path),
        check_required_fields(file_path, ["report_date", "data"]),
        check_date_format("report_date"),
        check_data_completeness(file_path)
    ]
    return all(checks)
```

---

## 五、监控机制

### 5.1 阶段完成屏障

#### Stage 1 Completion Barrier
```python
def wait_for_stage1_completion():
    """
    等待阶段1所有Agent完成
    条件：Task-1, Task-2, Task-3, Task-4 全部完成
    超时：5分钟 + buffer
    """
    required_tasks = ["Task-1", "Task-2", "Task-3", "Task-4"]
    completed = []
    
    while len(completed) < len(required_tasks):
        for task in required_tasks:
            if task.status == "COMPLETED" and task not in completed:
                completed.append(task)
        
        if elapsed_time > 6 * 60:  # 6分钟
            logger.warning("Stage 1 timeout, proceeding with available data")
            break
        
        sleep(10)  # 每10秒检查一次
```

#### Stage 2 Completion Barrier
```python
def wait_for_stage2_completion():
    """
    等待阶段2所有Agent完成
    条件：Task-5, Task-6 全部完成
    超时：3分钟 + buffer
    """
    required_tasks = ["Task-5", "Task-6"]
    completed = []
    
    while len(completed) < len(required_tasks):
        for task in required_tasks:
            if task.status == "COMPLETED" and task not in completed:
                completed.append(task)
        
        if elapsed_time > 4 * 60:  # 4分钟
            logger.warning("Stage 2 timeout, proceeding with available data")
            break
        
        sleep(10)
```

### 5.2 实时监控面板

```
┌─────────────────────────────────────────────────────────────────┐
│                    芯片研究流水线监控面板                         │
├─────────────────────────────────────────────────────────────────┤
│ 当前时间: 2026-02-15 09:35:00                                   │
│ 运行时间: 00:05:23                                               │
├─────────────────────────────────────────────────────────────────┤
│ 阶段1：数据采集 [███████░░░░░░░] 4/4 完成 ✅                    │
│ ├─ Task-1: 上市公司清单     ✅ 09:30:15 完成                     │
│ ├─ Task-2: 财务数据         ✅ 09:30:42 完成                     │
│ ├─ Task-3: 产品技术信息     ✅ 09:31:08 完成                     │
│ └─ Task-4: 市场情报         ✅ 09:31:55 完成                     │
├─────────────────────────────────────────────────────────────────┤
│ 阶段2：分析 [██████████░░░░] 2/2 进行中                          │
│ ├─ Task-5: 竞争格局分析     🔄 运行中 (预计剩余 1:30)            │
│ └─ Task-6: 趋势分析         🔄 运行中 (预计剩余 1:45)            │
├─────────────────────────────────────────────────────────────────┤
│ 阶段3：汇总 [░░░░░░░░░░░░░░░] 等待                              │
│ └─ Task-7: 生成报告        ⏳ 等待阶段2完成                      │
├─────────────────────────────────────────────────────────────────┤
│ 预计完成: 09:40:00                                               │
│ 状态: 正常运行                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 告警规则

| 告警级别 | 条件 | 通知方式 | 响应 |
|---------|------|---------|------|
| ⚠️ Warning | 单Agent超时 > 4分钟 | 记录日志 | 继续执行 |
| 🔴 Error | 单Agent超时 > 5分钟 | 告警+跳过 | 使用缓存数据 |
| 🔴 Critical | 阶段超时 > 70% | 即时通知 | 中止流水线 |

### 5.4 状态检查点

```python
# 关键检查点
checkpoints = {
    "checkpoint_1": {
        "name": "阶段1启动",
        "tasks_required": ["Task-1", "Task-2", "Task-3", "Task-4"],
        "timeout": 5 * 60,
        "on_timeout": "proceed_with_available_data"
    },
    "checkpoint_2": {
        "name": "阶段2启动",
        "tasks_required": ["Task-5", "Task-6"],
        "dependencies": ["checkpoint_1"],
        "timeout": 3 * 60,
        "on_timeout": "proceed_with_available_data"
    },
    "checkpoint_3": {
        "name": "阶段3启动",
        "tasks_required": ["Task-7"],
        "dependencies": ["checkpoint_2"],
        "timeout": 2 * 60,
        "on_timeout": "generate_partial_report"
    }
}
```

---

## 六、执行流程

### 6.1 完整执行脚本

```bash
#!/bin/bash
# chip_pipeline_execution.sh

# 初始化
TIMESTAMP=$(date +%Y-%m-%d)
LOG_FILE="logs/pipeline_${TIMESTAMP}.log"
DATA_DIR="data"
REPORT_DIR="reports"

echo "========================================" | tee -a $LOG_FILE
echo "芯片研究报告流水线启动" | tee -a $LOG_FILE
echo "时间: $(date)" | tee -a $LOG_FILE
echo "========================================" | tee -a $LOG_FILE

# 阶段1：并行执行
echo "[$(date '+%H:%M:%S')] 阶段1：数据采集（并行）" | tee -a $LOG_FILE

# 启动Agent-1
python run_agent.py --agent agent-chip-01 --timeout 300 \
    --output $DATA_DIR/01_companies_list.json &
PID1=$!

# 启动Agent-2
python run_agent.py --agent agent-chip-02 --timeout 300 \
    --output $DATA_DIR/02_financial_data.json &
PID2=$!

# 启动Agent-3
python run_agent.py --agent agent-chip-03 --timeout 300 \
    --output $DATA_DIR/03_product_tech.json &
PID3=$!

# 启动Agent-4
python run_agent.py --agent agent-chip-04 --timeout 300 \
    --output $DATA_DIR/04_market_intel.json &
PID4=$!

# 等待所有阶段1任务完成
wait $PID1 $PID2 $PID3 $PID4
STAGE1_STATUS=$?

if [ $STAGE1_STATUS -ne 0 ]; then
    echo "[WARN] 阶段1部分任务超时，继续执行" | tee -a $LOG_FILE
fi

echo "[$(date '+%H:%M:%S')] 阶段1完成" | tee -a $LOG_FILE

# 阶段2：并行执行
echo "[$(date '+%H:%M:%S')] 阶段2：分析（并行）" | tee -a $LOG_FILE

# 启动Agent-5
python run_agent.py --agent agent-chip-05 --timeout 180 \
    --input $DATA_DIR/01_companies_list.json \
    --input $DATA_DIR/02_financial_data.json \
    --input $DATA_DIR/03_product_tech.json \
    --input $DATA_DIR/04_market_intel.json \
    --output $DATA_DIR/05_competitive_analysis.json &
PID5=$!

# 启动Agent-6
python run_agent.py --agent agent-chip-06 --timeout 180 \
    --input $DATA_DIR/01_companies_list.json \
    --input $DATA_DIR/02_financial_data.json \
    --input $DATA_DIR/03_product_tech.json \
    --input $DATA_DIR/04_market_intel.json \
    --output $DATA_DIR/06_trend_analysis.json &
PID6=$!

wait $PID5 $PID6
STAGE2_STATUS=$?

echo "[$(date '+%H:%M:%S')] 阶段2完成" | tee -a $LOG_FILE

# 阶段3：汇总执行
echo "[$(date '+%H:%M:%S')] 阶段3：汇总" | tee -a $LOG_FILE

python run_agent.py --agent agent-chip-07 --timeout 120 \
    --input $DATA_DIR/01_companies_list.json \
    --input $DATA_DIR/02_financial_data.json \
    --input $DATA_DIR/03_product_tech.json \
    --input $DATA_DIR/04_market_intel.json \
    --input $DATA_DIR/05_competitive_analysis.json \
    --input $DATA_DIR/06_trend_analysis.json \
    --output $REPORT_DIR/芯片行业日报_${TIMESTAMP}.md

echo "[$(date '+%H:%M:%S')] 流水线完成" | tee -a $LOG_FILE
echo "========================================" | tee -a $LOG_FILE
```

### 6.2 Agent执行器

```python
# run_agent.py
import json
import sys
import time
from pathlib import Path

class AgentRunner:
    def __init__(self, agent_id, timeout=300):
        self.agent_id = agent_id
        self.timeout = timeout
        self.data_dir = Path("data")
        self.report_dir = Path("reports")
        
    def run(self, output_file):
        """执行Agent任务"""
        start_time = time.time()
        
        try:
            # 加载prompt
            prompt = self._load_prompt()
            
            # 调用LLM执行
            response = self._call_llm(prompt)
            
            # 解析结果
            result = self._parse_response(response)
            
            # 验证数据
            if self._validate(result):
                # 保存输出
                self._save_output(result, output_file)
                status = "SUCCESS"
            else:
                status = "VALIDATION_FAILED"
                
        except TimeoutError:
            status = "TIMEOUT"
            self._handle_timeout()
        except Exception as e:
            status = f"ERROR: {str(e)}"
            
        elapsed = time.time() - start_time
        
        return {
            "agent": self.agent_id,
            "status": status,
            "elapsed_seconds": elapsed,
            "output_file": output_file
        }
```

---

## 七、附录

### 7.1 重点公司信息速查

| 公司 | 代码 | 主营业务 | 核心优势 | 市值（估算） |
|------|------|---------|---------|-------------|
| 欣兴电子 | 3037.TW | ABF/BT载板 | 全球ABF龙头 | 1500亿新台币 |
| 深南电路 | 002176.SZ | IC载板、PCB | 国内载板龙头 | 600亿人民币 |
| 兴森科技 | 002436.SZ | PCB、IC载板 | PCB转型载板 | 200亿人民币 |
| 南亚电路 | 8046.TW | BT载板 | 台系BT龙头 | 800亿新台币 |
| 景硕科技 | 3189.TW | ABF/BT载板 | IC载板专业厂 | 500亿新台币 |

### 7.2 数据源清单

| 数据类型 | 数据源 | 更新频率 | 可靠性 |
|---------|--------|---------|--------|
| 财务数据 | 公司年报/季报 | 季度 | 高 |
| 市值数据 | 东方财富/Yahoo Finance | 日 | 高 |
| 市场规模 | Prismark | 季度 | 高 |
| 行业新闻 | 行业媒体 | 日 | 中 |
| 技术参数 | 公司官网/招股书 | 不定期 | 高 |

### 7.3 常见问题处理

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| Agent超时 | 数据源访问慢/数据量大 | 减少扫描范围，跳过非核心数据 |
| 数据缺失 | 公司未披露 | 标注"暂无数据"，使用替代数据源 |
| 格式错误 | LLM输出格式不稳定 | 添加格式验证和重试机制 |
| 依赖失败 | 前置任务未完成 | 设置合理的超时和buffer时间 |

### 7.4 版本历史

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-02-15 | 初始版本 | OpenClaw |

---

## 八、快速开始

### 执行完整流水线

```bash
# 方法1：使用执行脚本
chmod +x chip_pipeline_execution.sh
./chip_pipeline_execution.sh

# 方法2：分阶段执行
# 阶段1
python run_agent.py --agent agent-chip-01
python run_agent.py --agent agent-chip-02
python run_agent.py --agent agent-chip-03
python run_agent.py --agent agent-chip-04

# 阶段2
python run_agent.py --agent agent-chip-05
python run_agent.py --agent agent-chip-06

# 阶段3
python run_agent.py --agent agent-chip-07
```

### 查看结果

```bash
# 查看报告
cat reports/芯片行业日报_2026-02-15.md

# 查看日志
tail -f logs/pipeline_2026-02-15.log

# 查看数据文件
ls -la data/*.json
```

---

**文档结束**
