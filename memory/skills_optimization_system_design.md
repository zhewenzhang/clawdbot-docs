# Skills深度优化方案：分类体系与任务识别系统

**设计时间**: 2026-02-04  
**目标**: 从根本上改善Skills使用率，实现"每个任务自动匹配最佳Skill"  
**核心理念**: 不是让人适应57个Skills，而是让Skills适应人的工作流

---

## 第一部分：重新定义问题

### 1.1 当前问题的本质

**表面现象**：
- 57个Skills安装后使用率为0%
- 知道有Skill但不使用
- 认为"不用Skill也能完成"

**深层原因**：
```
不是"不知道用什么Skill"
而是"懒得想用什么Skill"

不是"Skill不好用"
而是"没有形成使用习惯"

不是"任务太简单"
而是"没有意识到复杂任务需要系统性方法"
```

**关键洞察**：
```
人的工作流是"任务驱动"的：
任务 → 直接执行 → 完成

理想的工作流应该是：
任务 → 识别类型 → 选择Skill → 执行 → 验证 → 完成

问题在于"识别类型"和"选择Skill"这两个步骤
在当前工作流中是不存在的
```

### 1.2 重新定义目标

**旧目标**：让人记住57个Skills，并在合适场景使用
**新目标**：让系统自动识别任务类型，并推荐最佳Skill

**区别**：
- 旧目标：依赖人的记忆和判断（高认知负荷）
- 新目标：依赖系统的分类和推荐（低认知负荷）

**核心转变**：
```
从"人找Skill" → "Skill找人"
从"主动使用" → "被动触发"
从"记忆负担" → "系统辅助"
```

---

## 第二部分：Skills分类体系设计

### 2.1 分类原则

**不是按功能分类**，而是按**使用场景**和**优先级**分类：

```
一级分类：使用频率
  - 日常型（每天用）
  - 项目型（每周用）
  - 工具型（按需用）

二级分类：任务复杂度
  - 简单任务（直接执行）
  - 中等任务（Skill辅助）
  - 复杂任务（系统性方法）

三级分类：风险等级
  - 低风险（可快速执行）
  - 中风险（需验证）
  - 高风险（需系统性方法）
```

### 2.2 推荐分类方案：使用场景分类

#### **A类：日常高频（Daily）**
| Skill | 使用频率 | 触发条件 | 预期收益 |
|-------|---------|---------|---------|
| weather | 每日1次 | 用户询问天气 | 快速响应 |
| summarize | 每日1-3次 | 用户要求总结 | 节省阅读时间 |
| github | 每日多次 | 代码操作 | 提高效率 |

**特点**：高频使用，需要快速响应

#### **B类：项目级（Project）**
| Skill | 使用频率 | 触发条件 | 预期收益 |
|-------|---------|---------|---------|
| planning-with-files | 每周1-2次 | 开始深度分析 | 系统性分析 |
| systematic-debugging | 按需 | 遇到Bug | 快速定位 |
| skill-creator | 按需 | 需要新功能 | 规范化开发 |

**特点**：中等频率，需要系统性方法

#### **C类：工具级（Utility）**
| Skill | 使用频率 | 触发条件 | 预期收益 |
|-------|---------|---------|---------|
| nano-pdf | 按需 | 处理PDF | 提取信息 |
| openai-whisper | 按需 | 处理音频 | 转文字 |
| agent-browser | 按需 | 网页操作 | 自动化 |

**特点**：低频率，按需调用

### 2.3 推荐分类方案：优先级分类

#### **P0：必须使用**
| Skill | 场景 | 原因 |
|-------|------|------|
| planning-with-files | 深度分析 | 保证系统性 |
| systematic-debugging | Bug修复 | 避免遗漏 |
| skill-creator | 创建新Skill | 规范化 |

#### **P1：强烈推荐**
| Skill | 场景 | 原因 |
|-------|------|------|
| verification-before-completion | 提交前 | 避免错误 |
| writing-plans | 多步骤任务 | 避免遗漏 |
| receiving-code-review | 代码审查 | 提高质量 |

#### **P2：按需使用**
| Skill | 场景 | 原因 |
|-------|------|------|
| using-git-worktrees | Git操作 | 隔离环境 |
| nano-pdf | PDF处理 | 提取信息 |
| agent-browser | 网页操作 | 自动化 |

### 2.4 分类后的Skills聚焦表

**日常高频（Daily）- 每天看到**
```
weather          天气查询
summarize        文档总结
github           GitHub操作
```

**项目级（Project）- 周常看到**
```
planning-with-files   深度分析（P0）
systematic-debugging  Bug修复（P0）
skill-creator         创建新功能（P0）
verification-before-completion  完成验证（P1）
writing-plans         任务规划（P1）
receiving-code-review 代码审查（P1）
```

**工具级（Utility）- 按需查看**
```
nano-pdf           PDF处理
openai-whisper     音频转文字
agent-browser      浏览器自动化
web-design-guidelines  UI审查
frontend-design     前端设计
```

---

## 第三部分：任务识别系统设计

### 3.1 任务识别的核心挑战

**当前问题**：
```
用户说："帮我分析一下ABF市场"
→ AI直接开始分析
→ 没有识别这是"深度分析"任务
→ 没有调用planning-with-files
→ 跳过系统性方法
→ 结果质量不稳定
```

**理想流程**：
```
用户说："帮我分析一下ABF市场"
→ 系统识别："这是深度分析任务"
→ 系统推荐："建议使用planning-with-files"
→ AI确认："好的，使用planning-with-files进行分析"
→ 按照系统性方法执行
→ 保证分析质量
```

### 3.2 任务类型识别矩阵

**基于输入特征识别**：

#### **输入信号1：关键词**
| 任务类型 | 触发关键词 |
|---------|----------|
| 深度分析 | 分析、研究、调研、报告、评估 |
| Bug修复 | 修复、错误、Bug、问题、报错 |
| 代码审查 | 审查、Review、检查、优化 |
| 任务规划 | 规划、计划、安排、设计 |
| 创建新功能 | 创建、开发、实现、新增、功能 |

#### **输入信号2：任务复杂度**
| 信号 | 简单任务 | 中等任务 | 复杂任务 |
|-----|---------|---------|---------|
| 时间预期 | 几分钟 | 几十分钟 | 几小时 |
| 步骤数量 | 1-3步 | 4-10步 | 10+步 |
| 涉及文件 | 1个 | 2-5个 | 5+个 |
| 人员数量 | 1人 | 1-3人 | 3+人 |
| 风险等级 | 低 | 中 | 高 |

#### **输入信号3：上下文**
| 信号 | 识别为 |
|-----|-------|
| 用户说"快速" | 简单任务 |
| 用户说"深度" | 复杂任务 |
| 用户说"详细" | 复杂任务 |
| 用户说"随便" | 简单任务 |

### 3.3 自动化识别规则

**规则1：关键词优先**
```
IF 任务包含 "分析/研究/调研/报告/评估"
THEN 识别为 "深度分析"
     推荐 Skill: planning-with-files

IF 任务包含 "修复/错误/Bug/问题/报错"
THEN 识别为 "Bug修复"
     推荐 Skill: systematic-debugging

IF 任务包含 "审查/Review/检查/优化代码"
THEN 识别为 "代码审查"
     推荐 Skill: receiving-code-review

IF 任务包含 "规划/计划/安排/设计/步骤"
THEN 识别为 "任务规划"
     推荐 Skill: writing-plans

IF 任务包含 "创建/开发/实现/新增/新功能"
THEN 识别为 "创建新功能"
     推荐 Skill: skill-creator
```

**规则2：复杂度评估**
```
IF 任务预估时间 > 30分钟
   OR 涉及文件 > 2个
   OR 用户说"深度/详细/全面"
THEN 识别为 "复杂任务"
     推荐: 使用系统性方法（planning-with-files）

ELSE IF 任务预估时间 < 5分钟
   AND 涉及文件 = 1个
   AND 用户说"快速/简单"
THEN 识别为 "简单任务"
     推荐: 直接执行（可不用Skill）
```

**规则3：上下文推断**
```
IF 前置任务类型是 X
   AND 当前任务是 X 的延续
THEN 识别为: 同类型任务
     推荐: 同类型Skill
```

### 3.4 任务识别与Skill匹配的完整流程

```
用户输入
    ↓
【任务识别引擎】
    ↓
识别结果：
- 任务类型：深度分析
- 复杂度：高
- 风险等级：中
- 推荐Skill：planning-with-files
    ↓
【确认环节】
    ↓
输出：
"检测到这是深度分析任务，建议使用 planning-with-files
 是否使用？（确认/跳过/换其他）"
    ↓
【执行环节】
    ↓
IF 用户确认
   THEN 调用 planning-with-files
   ELSE 直接执行（记录原因）
```

---

## 第四部分：触发机制设计

### 4.1 触发点设计

**触发点1：任务开始前**
```
时机：用户提出任务后，实际执行前
触发条件：所有任务
触发动作：显示"任务识别结果"和"推荐Skill"
```

**触发点2：任务进行中**
```
时机：执行过程中发现需要系统性方法
触发条件：复杂度升级、步骤遗漏、用户要求变更
触发动作：动态推荐相关Skill
```

**触发点3：任务完成前**
```
时机：用户说"完成"或"可以了"之前
触发条件：复杂任务
触发动作：推荐 verification-before-completion
```

### 4.2 触发机制实现

**实现方案A：AGENTS.md添加规则（立即可用）**

在AGENTS.md的"工作流程"部分添加：

```
## 🎯 Skills使用工作流

### Step 1：任务识别
收到任务后，先问自己：
1. 这个任务是什么类型？
2. 复杂度如何？
3. 需要系统性方法吗？

### Step 2：Skill匹配
根据任务类型，选择对应Skill：
- 深度分析 → planning-with-files
- Bug修复 → systematic-debugging
- 任务规划 → writing-plans
- 创建新功能 → skill-creator
- 完成验证 → verification-before-completion

### Step 3：确认执行
向用户确认：
"检测到这是[任务类型]，建议使用[Skill名称]
是否使用？（确认/跳过）"

### Step 4：执行与验证
- 使用Skill的系统性方法执行
- 完成后使用verification验证
```

**实现方案B：创建"任务启动模板"（本周完成）**

创建 `TASK_LAUNCH_TEMPLATE.md`：

```markdown
# 任务启动模板

## 1. 任务识别
任务描述：________
识别类型：________
复杂度：□低 □中 □高

## 2. Skill匹配
推荐Skill：________
备选Skill：________

## 3. 用户确认
是否使用推荐Skill？
□ 使用（推荐）
□ 跳过（有原因）

## 4. 执行方法
按照Skill的指导执行...

## 5. 完成验证
使用verification-before-completion验证
```

**实现方案C：集成到对话流程（需要开发）**

```
IF 用户提出任务
THEN
  显示任务识别卡片
  卡片内容：
    - 任务类型
    - 推荐Skill
    - 使用原因
    - 预期收益
  等待用户确认
  IF 确认
     THEN 调用Skill
     ELSE 直接执行
```

### 4.3 "任务→Skill"快速参考卡

**简化版（打印出来贴在电脑旁）**

```
┌─────────────────────────────────────┐
│     任务 → Skill 快速参考卡          │
├─────────────────────────────────────┤
│                                     │
│  深度分析 → planning-with-files    │
│  Bug修复 → systematic-debugging    │
│  任务规划 → writing-plans          │
│  创建新功能 → skill-creator        │
│  完成验证 → verification           │
│  代码审查 → receiving-code-review  │
│  Git操作 → using-git-worktrees     │
│                                     │
│  简单任务 → 直接执行（不用Skill）   │
│                                     │
└─────────────────────────────────────┘
```

**详细版（任务识别指南）**

```
任务类型识别指南

Q: 用户说"帮我分析一下X市场"
A: → 深度分析 → planning-with-files

Q: 用户说"帮我修复这个Bug"
A: → Bug修复 → systematic-debugging

Q: 用户说"帮我规划一下这个项目"
A: → 任务规划 → writing-plans

Q: 用户说"帮我创建个新功能"
A: → 创建新功能 → skill-creator

Q: 用户说"检查一下这段代码"
A: → 代码审查 → receiving-code-review

Q: 用户说"确认一下这个任务完成了"
A: → 完成验证 → verification-before-completion

Q: 用户说"帮我查一下天气"
A: → 简单任务 → weather（可不用Skill流程）

Q: 用户说"总结一下这个文档"
A: → 简单任务 → summarize（可不用Skill流程）
```

---

## 第五部分：实施方案

### 5.1 立即行动（今天）

#### **Action 1：更新AGENTS.md**
```markdown
## 🎯 Skills使用工作流（新增）

### 任务启动流程

#### Step 1：任务识别
收到任务后，立即识别：
- 任务类型（分析/修复/规划/创建/审查/其他）
- 复杂度（低/中/高）

#### Step 2：Skill匹配
根据任务类型选择：
| 任务类型 | 推荐Skill |
|---------|----------|
| 深度分析 | planning-with-files |
| Bug修复 | systematic-debugging |
| 任务规划 | writing-plans |
| 创建新功能 | skill-creator |
| 代码审查 | receiving-code-review |
| 完成验证 | verification-before-completion |
| 简单任务 | 直接执行 |

#### Step 3：确认使用
向用户确认：
"检测到这是[任务类型]，建议使用[Skill]
是否使用？（确认/跳过）"

#### Step 4：执行与验证
- 使用Skill的系统性方法
- 完成后验证
```

#### **Action 2：创建快速参考卡**
- 打印"任务→Skill快速参考卡"
- 贴在工作台显眼位置

#### **Action 3：创建任务启动模板**
- 创建 `TASK_LAUNCH_TEMPLATE.md`
- 复杂任务开始前先填模板

### 5.2 本周行动

#### **Action 4：建立使用日志**
- 创建 `skills_usage_log.md`
- 每次使用/不使用都记录

#### **Action 5：实践验证**
- 在5个实际任务中使用新流程
- 记录效果和反馈

#### **Action 6：优化调整**
- 根据实践反馈调整规则
- 更新参考卡和模板

### 5.3 本月行动

#### **Action 7：建立自动化识别**
- 创建简单的任务识别脚本
- 辅助快速判断任务类型

#### **Action 8：集成到cron任务**
- 定期发送使用提醒
- 统计使用率

#### **Action 9：持续优化**
- 每月回顾使用日志
- 优化任务识别规则
- 更新聚焦表和参考卡

---

## 第六部分：成功指标

### 短期（1周）
- [ ] 100%的深度分析任务使用planning-with-files
- [ ] 100%的Bug修复使用systematic-debugging
- [ ] 100%的新功能创建使用skill-creator
- [ ] 简单任务直接执行（不使用Skill流程）

### 中期（1个月）
- [ ] 任务识别准确率 > 80%
- [ ] 用户确认率 > 70%
- [ ] 核心Skills使用率 > 50%
- [ ] 任务执行质量稳定

### 长期（3个月）
- [ ] 形成"任务→Skill"自动化流程
- [ ] 核心Skills使用率 > 70%
- [ ] 任务执行质量显著提升
- [ ] 经验积累和知识沉淀

---

## 第七部分：持续改进机制

### 7.1 每周回顾
```
1. 阅读skills_usage_log.md
2. 识别使用模式
3. 发现改进机会
4. 更新规则和参考卡
```

### 7.2 每月评估
```
1. 统计使用率
2. 评估识别准确率
3. 优化匹配规则
4. 更新聚焦表
```

### 7.3 每季度重构
```
1. 回顾整体效果
2. 重构分类体系
3. 更新触发机制
4. 重新设计流程
```

---

## 附录

### A. 核心参考文件
- AGENTS.md
- TASK_LAUNCH_TEMPLATE.md（待创建）
- skills_usage_log.md（待创建）
- skills_usage_deep_analysis.md

### B. Skills聚焦表
- P0: planning-with-files, systematic-debugging, skill-creator
- P1: verification-before-completion, writing-plans, receiving-code-review
- P2: using-git-worktrees, nano-pdf, agent-browser

### C. 任务识别关键词
- 深度分析：分析、研究、调研、报告、评估
- Bug修复：修复、错误、Bug、问题、报错
- 任务规划：规划、计划、安排、设计
- 创建新功能：创建、开发、实现、新增

---

**设计完成时间**: 2026-02-04  
**版本**: v1.0  
**状态**: 待实施
