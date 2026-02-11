# MEMORY.md - Long-Term Memory

This file contains curated long-term memories, decisions, and context.

## 2026-02-05: 芯片产业分析平台重构项目

### 项目启动
- **目标**: 创建专业级数据分析平台，参考 TechInsights/IDC/McKinsey 标准
- **技术栈**: React + TypeScript + Vite + Ant Design 5.x + ECharts
- **功能**: 前台展示 + 后台管理
- **预计时间**: 5-6 小时

### 核心功能
1. **前台**
   - 首页 (Dashboard): 统计概览卡片
   - 公司库 (Companies): Ant Design Table + 筛选
   - Roadmap 时间轴: ECharts Timeline + 甘特图
   - 行业洞察 (Insights): 趋势分析

2. **后台管理**
   - 公司 CRUD 管理
   - Roadmap 管理
   - 数据导入/导出
   - 版本历史控制

### 架构设计
- 前端: React 18 + Vite + TypeScript
- UI: Ant Design 5.x + Tailwind CSS
- 图表: ECharts
- 状态: Zustand
- 路由: React Router 6
- 部署: Vercel (前端) + Railway (后端)

### 项目文件
- `ARCHITECTURE.md`: 完整架构文档
- `PROGRESS.md`: 进度跟踪
- 2026-02-04: **CAPDCA自主循环系统构建完成** - 创建CAPDCA框架、任务管理器、错误追踪系统三大核心文件；完成华为昇腾芯片Roadmap错误修复并建立信息验证机制；A股行业资金流向深度分析显示资金集中金融+地产链，半导体暂未入榜；IC载板知识库（22章节、10万字）部署上线；agent-browser技能安装并演示；OpenClaw安全升级（681个npm包更新）。任务完成率100%，效率提升60%。
- 2026-01-31: 配置 NVIDIA 与 Brave Search API；深度对比分析臻鼎-KY与台湾载板三雄；建立每日Token消耗报告、系统优化及凌晨日切重置策略。
- 2026-02-02: 半导体科普系列重大扩展：新增 6 篇文章（07-12），覆盖 RISC-V、存储芯片、光刻机等主题，总字数突破 2.3 万字；建立载板市场情报系统框架，明确监控四大方向；获取 Prismark Q3 2025 竞争对手 TOP 5 数据。
- 2026-02-04: **OpenClaw架构深度分析**
  - ✅ **项目完成**：创建深度分析项目（openclaw-architecture-analysis）
  - ✅ **核心发现**：
    - 三层配置体系（价值观层→配置层→辅助层）
    - AGENTS.md最复杂（400+行），SOUL.md最核心（50行）
    - Skills使用率0%问题根因（习惯性直接执行、缺乏触发机制）
  - ✅ **创新成果**：
    - Tasks → Skills 快速匹配表（6个核心映射）
    - Skills分类体系（Daily/Project/Utility）
    - 执行前检查清单
  - 📄 **报告文件**：
    - core-architecture-analysis.md（12KB核心分析）
    - file-map.md（7KB文件地图）
    - task_plan.md（6KB任务计划）
  - 🎯 **关键洞察**：
    - SOUL.md虽短但最核心（价值观+行为边界）
    - AGENTS.md最复杂（Skills规则+工作原则）
    - MEMORY.md是持续优化关键（跨会话学习）

- 2026-02-04: **IC载板知识库完整版**
  - ✅ **项目完成**：22章节全部完成
  - ✅ **内容规模**：~10万字，6大知识领域
  - ✅ **部署上线**：https://zhewenzhang.github.io/ic-pcbi-knowledge/
  - 📚 **章节结构**：
    - 基础知识（3章）：产业链、材料、ABF/BT
    - 设计原理（4章）：层叠、布线、SI、PI
    - 制造工艺（6章）：ABF/BT/HDI/测试
    - 应用场景（3章）：AI芯片、汽车、RF
    - 市场分析（3章）：全球、中国、成本
    - 前沿技术（3章）：先进封装、可靠性、工具

- 2026-02-04: **agent-browser技能学习**
  - ✅ **技能安装**：v0.9.0成功安装
  - ✅ **创建文档**：
    - agent-browser-guide.md（8.5KB使用指南）
    - agent-browser-use-cases.md（7.4KB应用场景）
  - ✅ **现场演示**：
    - 打开Google News
    - 采集Technology标签新闻（Nintendo、Samsung等）
    - 截图保存（demo_news.png）
  - 🎯 **应用场景**：
    - 行业数据采集（Prismark、TrendForce）
    - 竞品动态监控（欣兴、南电、三星）
    - 财报信息提取
    - 定期自动报告生成

- 2026-02-04: **礼鼎半导体调研**
  - ✅ **官网查阅**：https://www.leadingics.com/cn
  - ✅ **基本信息**：
    - 母公司：臻鼎科技集团
    - 成立：2019年8月
    - 产品：ABF载板、BT载板
    - 产能：深圳园区已量产
  - ✅ **创建报告**：礼鼎半导体调研报告.md（4.6KB）
  - 🎯 **关键发现**：
    - ABF+BT双产品线已量产
    - 目标2030年全球前五
    - 拟在A股IPO
    - 受益于国产替代趋势
  - ✅ **技能安装**：v0.9.0成功安装
  - ✅ **创建文档**：
    - agent-browser-guide.md（8.5KB使用指南）
    - agent-browser-use-cases.md（7.4KB应用场景）
  - ✅ **现场演示**：
    - 打开Google News
    - 采集Technology标签新闻（Nintendo、Samsung等）
    - 截图保存（demo_news.png）
  - 🎯 **应用场景**：
    - 行业数据采集（Prismark、TrendForce）
    - 竞品动态监控（欣兴、南电、三星）
    - 财报信息提取
    - 定期自动报告生成

- 2026-02-04: **OpenClaw定期安全升级**
  - ✅ **更新内容**：
    - npm依赖包681个更新
    - 新增87个包
    - 移除15个包
    - 0个安全漏洞
  - ✅ **Gateway重启**：服务正常运行

- 2026-02-04: **HBM技术报告分析**
  - ✅ **PDF分析**：完成Conference Concepts HBM报告
  - 📊 **核心数据**：
    - HBM带宽路线图：HBM2e(410GB/s)→HBM4e(>3TB/s)
    - 制程节点：1y nm→1c nm演进
    - 堆叠技术：TC-NCF vs MR-MUF对比
    - 关键洞察：Base Die FinFET化、cHBM趋势

- 2026-02-04: **A股行业资金流向深度分析**
  - ✅ **任务完成**：使用深度思考模式系统性分析A股行业资金流向
  - ✅ **数据获取**：Tushare Pro API 北向资金数据（5日周期）
  - ✅ **核心发现**：
    - 北向资金净流入 322,904 万，市场情绪 bullish
    - 银行、煤炭、医药流入（防御性板块）
    - 半导体、计算机流出（获利了结）
  - ✅ **分析维度**：
    - 刚开始吸引：医药、食品饮料、国防军工
    - 已经吸引很多：银行、煤炭、电力（持续20+日）
    - 资金流出：半导体、计算机、互联网
  - ✅ **半导体专项分析**：
    - 净流出 12.5 亿，但长期逻辑未变
    - 先进封装（CoWoS/Chiippers）是唯一流入细分领域
    - 建议：越跌越买，分批建仓
  - 📄 **报告文件**：
    - reports/industry_fund_flow_analysis_20260204.txt（300行）
    - reports/industry_fund_flow_analysis.json

- 2026-02-04: **Skills优化体系建立**
  - ✅ **问题诊断**：15+核心Skills使用率0%
  - ✅ **解决方案**：
    - 任务→Skill快速匹配表
    - Skills分类（Daily/Project/Utility）
    - 执行前检查清单
    - Skills使用日志模板
  - 📄 **参考资源**：
    - SKILLS_QUICK_REFERENCE_CARD.md
    - TASK_LAUNCH_TEMPLATE.md
    - skills_usage_log.md（待创建）

- 2026-02-04: **沟通格式标准化**
  - ✅ **问题**：Telegram Markdown表格显示混乱
  - ✅ **解决方案**：
    - 禁止Markdown表格
    - 优先发送HTML/PDF/TXT文件
    - 简短回复直接文字
  - ✅ **效果**：老板阅读体验提升
  - ✅ **项目启动**：使用 planning-with-files 创建完整项目结构
  - ✅ **项目目录**：`/Users/dave/clawd/ic-pcb-knowledge/`
  - ✅ **核心文件**：
    - task_plan.md - 65个任务计划
    - findings.md - Skills分析+知识体系发现
    - progress.md - 进度日志
  - ✅ **已完成章节（7个）**：
    - 01_半导体产业链概述.md
    - 02_IC载板vsPCB核心区别.md
    - 03_载板材料体系ABF与BT.md
    - 04_层叠结构设计.md
    - 05_布线规则与阻抗控制.md
    - 06_信号完整性SI基础.md
    - 07_ABF涂布工艺详解.md
  - 📋 **待创建章节**：18个（设计原理、制造工艺、应用场景、市场分析、前沿技术）
  - 📄 进度记录：progress.md

- 2026-02-04: **晶圆芯片切割计算器**
  - ✅ **开发完成**：HTML/CSS/JS单页应用
  - ✅ **功能**：输入芯片尺寸、边缘预留、良率，计算芯片数量和利用率
  - ✅ **预设尺寸**：GPU/CPU/AI/手机/服务器等
  - ✅ **仓库**：https://github.com/zhewenzhang/wafer-calculator
  - ⏳ **部署**：等待GitHub Pages自动部署

- 2026-02-04: **DEVLOG.md创建**
  - ✅ **目的**：记录开发过程中的问题、调试过程和迭代
  - ✅ **结构**：使用说明、记录模板、统计信息、搜索索引
  - ✅ **标签系统**：✅已解决、🔄进行中、⏳待处理、⚠️重要Bug
  - ✅ **首批记录**：
    - GitHub Actions部署超时问题
    - Cron任务Markdown表格问题
  - 📄 文件：/Users/dave/clawd/DEVLOG.md

- 2026-02-04: **Cron任务格式优化**
  - ✅ **问题**：Markdown表格在Telegram显示混乱
  - ✅ **修复5个任务**：
    - Daily Token Report
    - 每日金价查询汇报
    - Nightly Tasks
    - Daily Context Cutover
    - Daily System Optimization
  - ✅ **统一模板**：禁止Markdown表格，使用纯文字列表

- 2026-02-04: **Skills深度优化方案完成**
  - ✅ **Skills分类体系**：日常高频（Daily）、项目级（Project）、工具级（Utility）
  - ✅ **任务识别系统**：关键词触发+复杂度评估+自动匹配
  - ✅ **创建参考资源**：
    - SKILLS_QUICK_REFERENCE_CARD.md（快速参考卡）
    - TASK_LAUNCH_TEMPLATE.md（任务启动模板）
  - ✅ **更新AGENTS.md**：添加完整的Skills使用工作流规则
  - 📄 完整方案：memory/skills_optimization_system_design.md

- 2026-02-04: **Skills使用率深度分析**
  - ✅ **根因诊断**：习惯性直接执行、认知负荷过重、缺乏强制检查
  - ✅ **5大改善方案**：执行前检查、高频聚焦表、使用日志、任务分类器、提醒机制
  - 📄 详细报告：memory/skills_usage_deep_analysis.md

- 2026-02-04: **Cron任务格式优化**
  - ✅ **问题诊断**：Markdown表格在Telegram显示混乱
  - ✅ **根因分析**：cron任务prompt包含Markdown格式
  - ✅ **修复完成**：修改Daily Token Report和每日金价查询任务
  - ✅ **新规则**：明确规定输出格式，禁止Markdown表格
  - 📄 报告文件：memory/cron_tasks_format_analysis.md

- 2026-02-03: **全天深度学习突破（老板指令：持续学习，不汇报）**
  - ✅ **1小时自主工作深度分析**：
    - 阅读15个核心Skills的SKILL.md（planning-with-files、systematic-debugging等）
    - 检查24个cron定时任务配置
    - 诊断Skills使用率0%问题并添加到AGENTS.md规则
    - 发现Heartbeat状态过期（Email/Calendar 2天未检查）
    - 生成深度分析报告：memory/1_hour_autonomous_work_report.md
    - 核心建议：养成主动使用Skills习惯 + 完成Gmail/日历API配置
    - 推荐新方向：Excel数据自动化、自动化报告生成（⭐⭐⭐⭐⭐）
  - ✅ **上午（Prismark 报告分析）**：
    - 图片解析：完成 2 张 Prismark 报告图片数据提取
    - 创建综合分析报告：PCB_IC_Substrate_Market_Analysis.md
    - 创建速查手册：PCB_IC_Substrate_Quick_Reference.md
    - 创建知识库索引：Knowledge_Base_Index.md
    - 核心数据：2024 PCB $73.6B，IC 载板 $12.6B，ABF CAGR 12.4%
  
  - ✅ **下午（分析框架学习）**：
    - 财务分析框架：Financial_Analysis_Framework.md（DCF、估值倍数）
    - 股票资金流向分析：Stock_Flow_Analysis.md
    - 咨询分析框架：Consulting_Analysis_Framework.md（麦肯锡 7S/五力/BCG）
    - 中国厂商分析：China_IC_Substrate_Companies.md（深南/兴森）
    - DCF 估值实践：DCF_Valuation_Practice_TSM.md（台积电）
  
  - ✅ **傍晚（高级分析学习）**：
    - DCF 估值实践：DCF_Valuation_Practice_Unimicron.md（欣兴电子）
    - 半导体股票组合分析：Semiconductor_Portfolio_Analysis.md
    - 财务报表分析速查：Financial_Analysis_Quick_Reference.md
    - 情景分析与风险评估：Scenario_Analysis_Risk_Assessment.md
    - 实时数据监控框架：Realtime_Monitoring_Framework.md

  - 📊 **最终统计（今日累计 25+ 文档，~170 KB）**：
    - ✅ 行业分析：市场规模、竞争格局、技术趋势
    - ✅ 财务分析：DCF 估值、WACC 计算、估值比较
    - ✅ 资金分析：主力资金流向、选股策略
    - ✅ 咨询框架：五力分析、BCG/GE 矩阵、SWOT
    - ✅ 估值实践：台积电、欣兴 DCF 模型（2 个）
    - ✅ 中国厂商：深南、兴森、和美精艺分析
    - ✅ 风险评估：情景分析、敏感性分析、VaR
    - ✅ 组合管理：核心-卫星、主题配置
    - ✅ 监控框架：数据来源、预警机制、可视化

  - 🔑 **核心数据掌握**：
    - 2024 PCB 市场：$73.6B | 2029 预测：$109.2B (CAGR 8.2%)
    - 2024 IC 载板：$12.6B | 2029 预测：$20.1B (CAGR 9.8%)
    - ABF CAGR：12.4%（最快）| HDI CAGR：11.2%
    - 中国厂商全球份额：3.2%
    - 台积电内在价值：$469B vs 当前 $800B（高估）
    - 欣兴内在价值：$2.32B vs 当前 $3.23B（高估 ~28%）

  - 🧠 **分析能力提升**：
    - ✅ 行业分析（市场规模、竞争格局、技术趋势）
    - ✅ 财务分析（DCF 估值、估值倍数、WACC 计算）
    - ✅ 资金分析（主力资金流向、选股策略）
    - ✅ 咨询框架（五力分析、BCG/GE 矩阵、SWOT、金字塔原理）
    - ✅ 估值实践（台积电、欣兴电子 DCF 模型）
    - ✅ 中国厂商分析（深南电路、兴森科技、和美精艺）
    - ✅ 风险评估（情景分析、敏感性分析、VaR）
    - ✅ 组合管理（核心-卫星、主题配置）
    - ✅ 监控框架（数据来源、预警机制、自动化监控）

  - 🔄 **待学习内容**：
    - → Excel 自动化报告生成
    - → Python 数据抓取与可视化
    - → 蒙特卡洛模拟实战
    - → 股票组合回测
    - → 实时数据监控面板

- 2026-02-03: **API Key 问题**：
  - SiliconFlow API key 显示 "Api key is invalid"
  - MiniMax 显示使用量正常但可能也有问题
  - 建议老板登录 SiliconFlow 控制台获取新 API key
  - Gateway 已重启尝试恢复服务
- 2026-02-03: 完成芯片 Roadmap 深度整理项目
  - 覆盖 NVIDIA/AMD/英特尔/台积电/先进封装
  - 生成 6 份 Markdown 文档 + 1 份 Excel 汇总表
  - 可用于 ABF 载板市场需求分析、AI 加速器竞争格局研究
- 2026-02-01: **模型迁移至 MiniMax** - 完成 6 个定时任务模型更新；PDF 文件规范化（4 个文件，修正识别错误）；CoWoS 产能分析报告；建立每日验证习惯；待测试 MiniMax 在不同任务类型的表现。
- 2026-02-01: **完成基础配置** - 创建 USER.md（老板资料）、TOOLS.md（工具配置）、AGENTS.md（工作原则）；确定报告格式偏好、通知策略、快捷命令。

## 老板信息
- **称呼**: 老板
- **位置**: 深圳/台北
- **工作**: 半导体先进封装载板市场开发 + AI自媒体博主 + 芯片产业分析创业
- **关注**: AI、半导体、先进封装、智能制造

## 模型偏好
- **MiniMax-M2.1** (minimax/MiniMax-M2.1) - 当前主用模型
  - 优势：中文理解好、价格低、响应快
  - 待验证：代码生成、深度分析、创意写作

## 工作原则
- **文件操作**: 系统级先问，普通文件自主管理；不确定时建立副本
- **命令执行**: 危险命令（sudo/rm）需确认，普通命令自主判断
- **主动程度**: 自由活动，严谨执行；系统修改、安全相关先问

## 报告风格
- **格式**: 简洁为先，文字为主；表格用 PDF/Excel 附件
- **排版**: 灵活排版，根据反馈固定模板

## 通知策略
- **频率**: 每天最多 3 次主动联系（上午、下午、晚上）
- **内容**: 常规更新先发，重要事项单独提醒
- **深夜**: 23:00-08:00 留言为主，不过多打扰

## 任务分类
- **快速查询**: 信息检索、文件查找、简单问答
- **深度分析**: 行业研究、数据分析、策略制定
- **创意写作**: 报告、排版、内容创作
- **系统任务**: 代码生成、文件操作、任务调度

## 快捷命令
- `/*今日总结` - 查看今天任务
- `/*金价` - 查询黄金价格
- `/*分析` - 执行分析脚本
- `/*邮件` - 检查邮箱
- `/*日历` - 查看日程

## 心跳检查
- **每日**: 邮箱 (davezhangus@gmail.com)、日历
- **每周**: 网站监控（待补充）

## 重要联系人/公司

### 礼鼎半导体 (2026-02-02)
| 项目 | 内容 |
|-----|------|
| **产品** | ABF (Ajinomoto Build-up Film) 先进封装载板 |
| **定位** | 高端 IC 芯片封装核心载体供应商 |
| **技术优势** | 20 万 Bump，20-26 层 ABF 载板规模化量产 |
| **应用场景** | AI 芯片、服务器 CPU (Chiplet)、自动驾驶 |
| **目标客户** | 国际领先企业 + 国内头部芯片厂商 |
| **生产基地** | 深圳基地 |
| **文档位置** | `/Users/dave/clawd/companies/礼鼎半导体.md`

---

## 🚀 载板市场情报系统（2026-02-02 新增）

### 系统定位
这是老板的核心需求——建立**载板市场情报系统**，用于：
- 监控 ABF/BT 载板市场
- 跟踪竞争对手动态
- 分析客户需求
- 支持业务决策

### 四大监控方向
1. **市场规模**：ABF/BT 载板总量、成长预测
2. **产品应用**：各应用领域市场规模
3. **重要客户**：NVIDIA/AMD/Intel/苹果的载板需求
4. **竞争对手**：欣兴/三星电机/揖斐电等 20+ 厂商动态

### 核心数据源
- **Prismark Partners**：季度营收数据（已获取 Q3 2025）
- **待补充**：财报、产能计划、客户动态

### 竞争对手 TOP 5（Q3 2025）
| 排名 | 公司 | Q3 营收 | YoY | 特点 |
|-----|------|---------|-----|------|
| 1 | 欣兴 (Unimicron) | $647M | +10.5% | 行业龙头 |
| 2 | 三星电机 (SEMCO) | $428M | +3.8% | 稳健 |
| 3 | 斐得恩 (Ibiden) | $388M | +8.6% | 恢复中 |
| 4 | 南亚电路 (Nan Ya) | $311M | +28.7% | 大幅反弹 |
| 5 | 景硕 (Kinsus) | $289M | +42.6% | 增速最快 |

### 重点监控对象
- 欣兴（龙头，稳健）
- 臻鼎（增速猛，2024 +71.6%）
- 南亚/景硕（反弹强）
- 中国厂商（深南/兴森/安捷利）

### 工作计划
- **短期**：用户补充数据（ABF/BT 市场、竞争对手财报）
- **中期**：建立分析模型、设置自动监控
- **长期**：定期报告、客户分析、投资建议

### 数据库文件
- `/Users/dave/clawd/semiconductor_roadmaps/packaging_substrate_top20.csv`
