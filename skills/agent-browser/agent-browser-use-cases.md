# agent-browser 应用场景设计

**创建时间**: 2026-02-04  
**Skill**: agent-browser  
**目的**: 设计适合半导体行业的工作场景

---

## 📊 目录

1. [场景概述](#1-场景概述)
2. [行业研究场景](#2-行业研究场景)
3. [竞品监控场景](#3-竞品监控场景)
4. [数据采集场景](#4-数据采集场景)
5. [自动化测试场景](#5-自动化测试场景)
6. [知识管理场景](#6-知识管理场景)
7. [实战项目](#7-实战项目)
8. [效率提升总结](#8-效率提升总结)

---

## 1. 场景概述

### agent-browser 优势

```
对比其他工具：

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  工具           复杂度    交互性    适用场景               │
│                                                             │
│  agent-browser   中        高       复杂网站、交互操作     │
│  blogwatcher     低        无       博客RSS监控           │
│  web_fetch       低        无       静态页面内容          │
│  web_search      低        无       搜索引擎查询          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 适合场景

| 场景类型 | 复杂度 | 交互需求 | 推荐程度 |
|---------|-------|---------|---------|
| 复杂网站采集 | 高 | 需要点击/填写 | ⭐⭐⭐⭐⭐ |
| 表单自动化 | 中 | 需要表单填写 | ⭐⭐⭐⭐⭐ |
| 动态内容抓取 | 中 | 需要等待加载 | ⭐⭐⭐⭐ |
| 多页面对比 | 中 | 需要导航跳转 | ⭐⭐⭐⭐ |
| 简单内容提取 | 低 | 无需交互 | ⭐⭐⭐ |

---

## 2. 行业研究场景

### 场景2.1：Prismark 报告数据提取

```
场景：从 Prismark 网站提取 IC 载板市场数据

目标URL：https://www.prismark.com

操作步骤：
1. 打开 Prismark 首页
2. 导航到 Reports 页面
3. 找到 IC Substrate 相关报告
4. 提取报告摘要和关键数据
5. 截图留档
6. 保存链接到知识库

数据提取：
- 市场规模数据
- 增长率预测
- 市场份额排名
- 技术趋势分析

技术实现：
agent-browser open https://www.prismark.com
agent-browser snapshot -i
agent-browser click @e1  # 点击 Reports
agent-browser wait --load networkidle
agent-browser get text @e2  # 报告标题
agent-browser get html @e3  # 报告摘要
agent-browser screenshot report.png
agent-browser pdf report_detail.pdf
```

### 场景2.2：TrendForce 产能数据监控

```
场景：监控全球 IC 载板厂商产能数据

目标URL：https://www.trendforce.cn

监控指标：
- SK海力士产能
- 三星电机产能
- 欣兴电子产能
- 扩产计划

工作流程：
1. 打开 TrendForce 页面
2. 导航到 DRAM/IC Substrate 栏目
3. 提取最新产能数据
4. 与历史数据对比
5. 识别变化趋势
6. 更新知识库

频率：每周执行一次

脚本示例：
#!/bin/bash
DATE=$(date +%Y%m%d)
agent-browser open https://www.trendforce.cn
agent-browser snapshot -i
agent-browser get text @capacity_table
agent-browser screenshot capacity_$DATE.png
# 保存数据到 CSV
```

### 场景2.3：公司财报信息提取

```
场景：从公司官网提取财报信息

目标公司：
- 欣兴电子 (Unimicron)
- 南亚电路 (Nan Ya)
- 三星电机 (SEMCO)

提取内容：
- 营收数据
- 毛利率
- 资本支出
- 扩产计划

操作流程：
1. 打开公司投资者关系页面
2. 导航到 Financial Reports
3. 下载最新财报 PDF
4. 提取关键财务指标
5. 更新数据库

工具组合：
agent-browser + nano-pdf + memory
```

---

## 3. 竞品监控场景

### 场景3.1：欣兴电子产品发布监控

```
场景：监控欣兴官网的产品发布动态

目标URL：https://www.unimicron.com

监控内容：
- 新产品发布
- 技术突破新闻
- 客户合作公告
- 产能扩张消息

关键词筛选：
- "New Product"
- "Technology"
- "Capacity Expansion"
- "Customer"

工作流程：
1. agent-browser open https://www.unimicron.com
2. agent-browser click @news  # 新闻页面
3. agent-browser snapshot -i
4. 遍历所有新闻条目
5. 提取标题、日期、内容
6. 筛选关键词相关条目
7. 保存到 memory/
```

### 场景3.2：三星电机技术动态跟踪

```
场景：跟踪三星电机在 IC 载板领域的技术动态

目标URL：https://www.semiconductor.samsung.com

关注点：
- HBM 相关技术
- 先进封装
- 新材料研发

自动化脚本：
#!/bin/bash
agent-browser open https://www.samsung.com/semiconductor/
agent-browser snapshot -i
agent-browser find text "HBM" click
agent-browser wait --load networkidle
agent-browser get text @article_title
agent-browser screenshot article.png
```

### 场景3.3：行业展会信息收集

```
场景：收集半导体行业展会信息

目标网站：
- ECTC 官网
- IMAPS 官网
- 中国国际半导体展

收集内容：
- 展会时间
- 演讲嘉宾
- 技术议题
- 展位信息

应用场景：
1. 规划参会行程
2. 了解行业趋势
3. 收集技术资料
4. 建立行业联系
```

---

## 4. 数据采集场景

### 场景4.1：价格数据采集

```
场景：采集 IC 载板相关原材料价格

采集对象：
- ABF 薄膜价格
- BT 树脂价格
- 铜箔价格
- 金盐价格

数据来源：
- 行业网站
- 期货市场
- 供应商报价

技术实现：
1. 打开价格网站
2. snapshot -i 获取表格
3. 提取价格数据
4. 格式化输出
5. 存储到 CSV

输出格式：
日期, 材料, 价格, 单位, 来源
2026-02-04, ABF薄膜, $120, /panel, 行业网站
```

### 场景4.2：产能数据汇总

```
场景：汇总全球主要厂商产能数据

厂商列表：
- SK海力士
- 三星电机
- 欣兴电子
- 南亚电路
- Ibiden

采集内容：
- 月产能（K/m²）
- 产能利用率
- 扩产计划
- 新厂进度

工作流程：
1. 打开各厂商官网
2. 提取产能数据
3. 对比分析
4. 生成汇总报告
5. 更新数据库

工具组合：
agent-browser + summarize + memory
```

### 场景4.3：技术参数对比

```
场景：采集不同代际产品的技术参数

产品代际：
- HBM2e vs HBM3 vs HBM3e
- ABF Gen 5 vs Gen 6 vs Gen 7
- 载板层数 16L vs 24L vs 32L

对比维度：
- 带宽
- 功耗
- 价格
- 良率

应用：
1. 技术选型参考
2. 成本效益分析
3. 供应商评估
```

---

## 5. 自动化测试场景

### 场景5.1：网页交互测试

```
场景：测试行业网站的表单交互

测试用例：
1. 搜索功能测试
2. 筛选功能测试
3. 分页功能测试
4. 下载功能测试

测试脚本：
agent-browser open https://example.com/search
agent-browser fill @search_box "HBM"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser get count ".result_item"
agent-browser screenshot search_results.png
```

### 场景5.2：页面加载测试

```
场景：测试页面加载性能

监控指标：
- 首屏加载时间
- 交互响应时间
- 资源加载完成时间

测试方法：
1. 打开目标页面
2. 记录开始时间
3. 等待加载完成
4. 截图记录
5. 对比历史数据
```

### 场景5.3：内容更新测试

```
场景：验证网站内容是否更新

监控策略：
1. 定期访问目标页面
2. 截图对比
3. 检测内容变化
4. 发送变化通知

触发条件：
- 页面内容变化
- 新增新闻报道
- 价格数据更新
```

---

## 6. 知识管理场景

### 场景6.1：行业知识库更新

```
场景：定期更新半导体行业知识库

更新内容：
- 新技术术语
- 新公司信息
- 新应用案例
- 新市场数据

工作流程：
1. 定义监控关键词列表
2. 定期搜索行业网站
3. 采集相关内容
4. 提取关键信息
5. 整理成文档
6. 更新知识库

关键词示例：
- "IC Substrate"
- "Advanced Packaging"
- "HBM"
- "Chiplet"
- "2.5D/3D Packaging"
```

### 场景6.2：专家观点收集

```
场景：收集行业专家的观点和分析

目标来源：
- LinkedIn 专家文章
- Twitter/X 技术博主
- 知乎专业回答
- 行业论坛讨论

收集方法：
1. 打开目标页面
2. 搜索专家账号
3. 采集最新观点
4. 整理核心论点
5. 添加个人评论
6. 保存到知识库
```

### 场景6.3：竞品分析报告生成

```
场景：生成竞品对比分析报告

分析维度：
- 技术能力对比
- 产能规模对比
- 成本结构对比
- 客户结构对比
- 财务表现对比

报告结构：
1. 公司概况
2. 技术对比
3. 产能对比
4. 成本分析
5. 客户分析
6. 财务对比
7. 综合评估

工具组合：
agent-browser + nano-pdf + summarize + write
```

---

## 7. 实战项目

### 项目7.1：IC 载板市场周报自动生成

```
目标：每周自动生成 IC 载板市场简报

自动化流程：
1. 周一 9:00 cron 触发
2. agent-browser 采集本周数据
3. summarize 总结关键信息
4. 生成 Markdown 报告
5. 发送到 Telegram

报告内容：
- 市场规模变化
- 主要厂商动态
- 技术趋势更新
- 价格走势分析
- 重要新闻摘要

预计节省时间：2-3小时/周
```

### 项目7.2：HBM 技术路线图持续跟踪

```
目标：持续跟踪 HBM 技术发展

跟踪内容：
- SK海力士技术进展
- 三星技术路线
- 美光技术布局
- NVIDIA/AMD 需求变化

采集频率：每周
更新方式：增量更新
存储格式：知识库 + 时间线

工具组合：
agent-browser + memory + cron
```

### 项目7.3：半导体行业会议信息库

```
目标：建立行业会议信息库

会议类型：
- ECTC (Electronics Components and Technology Conference)
- IMAPS (International Microelectronics Assembly and Packaging)
- 中国国际半导体展
- 台积电技术论坛

信息收集：
- 会议时间地点
- 演讲嘉宾
- 技术议题
- 参会公司
- 展示产品

应用：
- 参会规划
- 技术趋势了解
- 行业人脉建立
```

---

## 8. 效率提升总结

### 8.1 时间节省

| 场景 | 手动时间 | 自动时间 | 节省 |
|-----|---------|---------|------|
| 行业数据采集 | 2小时/次 | 15分钟/次 | 87% |
| 竞品监控 | 1小时/天 | 10分钟/天 | 83% |
| 报告生成 | 4小时/周 | 1小时/周 | 75% |
| 数据对比 | 3小时/周 | 30分钟/周 | 83% |

### 8.2 数据质量提升

```
质量对比：

┌──────────────────────────────────────────────┐
│                                              │
│  手动采集              agent-browser          │
│                                              │
│  ✓ 数据准确          ✓✓✓ 数据更准确          │
│  ✓ 格式统一          ✓✓✓ 格式标准化          │
│  ✓ 时效性差          ✓✓✓ 实时更新            │
│  ✓ 可追溯性弱        ✓✓✓ 完整审计轨迹        │
│                                              │
└──────────────────────────────────────────────┘
```

### 8.3 工作流程优化

```
优化前：
1. 手动打开浏览器
2. 手动导航页面
3. 手动复制数据
4. 手动整理格式
5. 手动保存文件

优化后：
1. cron 定时触发
2. agent-browser 自动采集
3. 格式化输出
4. 自动保存到知识库
5. Telegram 发送通知

效率提升：5倍+
```

---

## 📚 相关资源

### 工具文档
- agent-browser: `/Users/dave/clawd/skills/agent-browser/agent-browser-guide.md`
- cron: 定时任务
- memory: 知识管理

### 推荐组合
- 数据采集: agent-browser + cron + memory
- 报告生成: agent-browser + summarize + write
- 竞品监控: agent-browser + blogwatcher + telegram

---

## 🎯 行动建议

### 立即可做
1. 安装 agent-browser
2. 测试基本命令（open, snapshot, get）
3. 尝试采集一个网页

### 本周计划
1. 配置定时采集任务
2. 建立第一个监控场景
3. 生成第一份自动报告

### 长期规划
1. 建立完整的竞品监控体系
2. 实现行业知识库自动更新
3. 开发自定义分析工具

---

**创建时间**: 2026-02-04  
**版本**: v1.0
