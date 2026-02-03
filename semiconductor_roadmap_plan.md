# 🚀 半导体公司产品路线图管理计划

## 📋 项目概述

**目标**: 持续追踪主要半导体公司的产品路线图，保持数据最新，为决策提供支持。

**覆盖公司**:
- NVIDIA (已完成)
- AMD (已完成)
- Intel (已完成)
- Google TPU (待补充)
- 台湾 ic 设计公司 (待补充)
- 中国 AI 芯片公司 (待补充)

---

## 📁 文件管理架构

### 1. 文件存储位置

```
/Users/dave/clawd/
├── semiconductor_roadmaps/
│   ├── nvidia/
│   │   ├── NVIDIA_Roadmap.xlsx (主文件)
│   │   ├── NVIDIA_Roadmap_Visual.md (可视化)
│   │   ├── history/
│   │   │   ├── NVIDIA_Roadmap_2026-02-02.xlsx
│   │   │   └── ...
│   │   └── source_references/
│   │       ├── GTC2025_NVIDIA.pdf
│   │       └── ...
│   ├── amd/
│   │   └── AMD_Instinct_Roadmap.xlsx
│   ├── intel/
│   │   └── Intel_Gaudi_Roadmap.xlsx
│   └── competitors/
│       └── Competitor_Roadmaps.xlsx (综合对比)
```

### 2. 文件命名规则

```
{公司名}_{产品线}_{类型}_{日期}.{扩展名}

示例:
- NVIDIA_Roadmap_2026-02-02.xlsx
- AMD_Instinct_Roadmap_2026-02-02.xlsx
- Competitor_Roadmaps_2026-02-02.xlsx
- NVIDIA_Roadmap_Visual_2026-02-02.md
```

### 3. 版本控制

- **主文件**: 不带日期，始终是最新的
- **历史版本**: 带日期，保存每次更新
- **命名格式**: `公司_类型_YYYY-MM-DD.xlsx`

---

## 🔄 定期更新机制

### 更新频率

| 公司/产品 | 更新频率 | 触发条件 |
|----------|---------|---------|
| NVIDIA | 每季度 | 财报后、GTC大会后 |
| AMD | 每季度 | 财报后、发布会后 |
| Intel | 每季度 | 财报后、IDF大会后 |
| 竞争对手对比 | 每季度 | 重大产品发布时 |
| 市场分析 | 每月 | 行业新闻汇总 |

### 更新触发器

1. **财报季** (每季度)
   - 1月/4月/7月/10月
   - 自动触发更新任务

2. **行业大会**
   - GTC (NVIDIA, 3月)
   - Computex (6月)
   - IDF (Intel, 下半年)
   - CES (1月)

3. **重大新闻**
   - 产品发布
   - 架构更新
   - 供应链消息

---

## 📊 数据结构标准

### 必填字段

| 字段 | 说明 | 格式 |
|-----|------|-----|
| 发布时间 | 产品发布/上市时间 | YYYY-Qn |
| 产品系列 | 数据中心/消费级/嵌入式 | 文本 |
| 架构代号 | Ampere/Hopper/Blackwell等 | 文本 |
| 产品型号 | A100/H100/B200等 | 文本 |
| 制程 | 7nm/4nm/3nm等 | 文本 |
| HBM | HBM版本和容量 | 文本 |
| 主要特性 | 关键规格 | 文本 |
| 备注 | 状态/价格 | 文本 |

### 数据来源标注

| 来源类型 | 标识 |
|---------|-----|
| 官方发布 | [官方] |
| 行业分析 | [分析] |
| 供应链消息 | [供应链] |
| 媒体预测 | [预测] |

---

## ⚙️ 自动化任务配置

### Cron 任务

```json
{
  "tasks": [
    {
      "name": "季度半导体路线图更新",
      "schedule": "0 10 1 1,4,7,10 *",
      "action": "更新 NVIDIA/AMD/Intel Roadmap"
    },
    {
      "name": "行业大会监控",
      "schedule": "在 GTC/Computex/IDF 前一周触发",
      "action": "提前收集信息"
    },
    {
      "name": "月度行业新闻汇总",
      "schedule": "0 9 1 * *",
      "action": "汇总本月半导体新闻"
    }
  ]
}
```

---

## 📈 数据质量控制

### 数据验证清单

- [ ] 发布时间是否准确
- [ ] 规格参数是否有据可查
- [ ] 是否标注数据来源
- [ ] 是否有竞品对比
- [ ] 是否标注置信度

### 置信度评级

| 级别 | 含义 | 标记 |
|-----|------|-----|
| 高 | 官方确认 | ✅ |
| 中 | 行业分析 | ⚠️ |
| 低 | 媒体预测 | ❓ |
| 未知 | 待确认 | 🔲 |

---

## 🎯 后续扩展计划

### Phase 1 (已完成)
- [x] NVIDIA Roadmap
- [x] AMD Roadmap
- [x] Intel Roadmap
- [x] 竞争对手对比
- [x] Feynman 详细信息

### Phase 2 (待执行)
- [ ] Google TPU Roadmap
- [ ] Amazon Trainium/Inferentia
- [ ] 台湾 ic 设计公司 (联发科、联咏等)
- [ ] 中国 AI 芯片 (华为、寒武纪)

### Phase 3 (长期)
- [ ] 自动化数据抓取
- [ ] AI 预测模型
- [ ] 可视化大屏
- [ ] API 接口

---

## 📞 关键时间节点提醒

| 时间 | 事件 | 行动 |
|-----|------|-----|
| 2026-01 | CES 2026 | 检查 NVIDIA/AMD 新品 |
| 2026-03 | GTC 2026 | NVIDIA 新架构发布 |
| 2026-04 | Q2 财报季 | 更新所有 Roadmap |
| 2026-06 | Computex | AMD/Intel 新品 |
| 2026-07 | Q3 财报季 | 更新所有 Roadmap |
| 2026-10 | Q4 财报季 | 更新所有 Roadmap |

---

**创建时间**: 2026-02-02
**最后更新**: 2026-02-02
**负责人**: Clawdbot (可乐)
