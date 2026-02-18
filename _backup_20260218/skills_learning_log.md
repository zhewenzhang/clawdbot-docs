# Skills自主学习计划

**创建日期**：2026-02-07
**最近更新**：2026-02-07
**状态**：进行中

---

## 一、Superpowers 整体架构

### 核心哲学
- **测试驱动开发**：先写测试
- **系统性胜过随意**：流程胜过猜测
- **复杂度降低**：简洁是首要目标
- **证据胜过声明**：验证后再宣布成功

### 完整工作流程
```
1. brainstorming → 设计细化
2. using-git-worktrees → 隔离工作区
3. writing-plans → 创建实施计划
4. subagent-driven-development / executing-plans → 执行任务
5. test-driven-development → TDD红绿重构
6. requesting-code-review → 任务间审查
7. finishing-a-development-branch → 完成分支
```

---

## 二、已完成学习的Skills（6/14）

### 1.1 planning-with-files ✅
**功能**：复杂任务规划，创建task_plan.md/findings.md/progress.md

**核心原则**：
- Context Window = RAM (有限), Filesystem = Disk (无限)
- 任何重要信息写入磁盘

**关键规则**：
- 2-Action Rule：每2次操作后写文件
- 强制创建计划
- 记录所有错误

---

### 1.2 systematic-debugging ✅
**功能**：Bug修复、问题诊断

**铁律**：没有根因分析，不准修复

**四阶段**：
1. Root Cause：理解WHAT和WHY
2. Pattern：找working例子对比
3. Hypothesis：形成理论最小测试
4. Implementation：创建测试、修复、验证

**关键洞察**：
- 3次修复失败 = 架构问题
- 系统性调试比猜快（15-30分钟 vs 2-3小时）

---

### 1.3 verification-before-completion ✅
**功能**：完成前验证

**铁律**：没有新鲜证据，不准宣布完成

**模式**：
```
IDENTIFY命令 → RUN执行 → READ输出 → VERIFY确认 → 做声明
```

**禁止**：
- "应该可以"
- "看起来对"
- "可能完成了"

---

### 1.4 receiving-code-review ✅
**功能**：接收代码审查反馈

**核心**：技术评估，不是情感表演

**响应模式**：
```
READ完整反馈 → UNDERSTAND重述 → VERIFY检查 → EVALUATE评估 → RESPOND回应 → IMPLEMENT实施
```

**禁止**：
- "You're absolutely right!"
- "Great point!"

---

### 1.5 requesting-code-review ✅
**功能**：请求代码审查

**核心原则**：早审查，勤审查

**何时**：
- 强制：每任务后、主要功能完成前、合并前
- 可选：卡住时、重构前、复杂bug修复后

---

### 1.6 subagent-driven-development ✅
### 1.9 using-git-worktrees ✅（2026-02-08新增）
**功能**：Git工作樹隔離

**核心原則**：
- 目錄選擇優先級：現有 > CLAUDE.md > 詢問用戶
- 安全驗證：項目目錄必須被.gitignore忽略
- 自動檢測並運行項目設置

**流程**：
```
檢查現有目錄 → 驗證.gitignore → 創建工作樹 → 運行設置 → 驗證測試
```

**關鍵洞察**：
- 避免污染主分支
- 隔離工作環境
- 快速切換上下文

---

### 1.10 finishing-a-development-branch ✅（2026-02-08新增）
**功能**：完成分支決策

**核心原則**：
- 驗證測試 → 呈現選項 → 執行選擇 → 清理

**流程**：
```
測試驗證 → 本地合併 / PR / 保留 / 放棄 → 工作樹清理
```

**選項**：
1. 本地合併
2. 推送並創建PR
3. 保留分支
4. 放棄工作

---

### 1.11 dispatching-parallel-agents ✅（2026-02-08新增）
**功能**：並行子代理分派

**核心原則**：
- 獨立問題並行處理
- 每個代理專注單一問題域

**何時使用**：
- 3+個測試文件失敗，根因獨立
- 多個子系統獨立損壞
- 每個問題可在不了解其他問題的情況下理解

**何時不使用**：
- 失敗相關（修復一個可能修復另一個）
- 需要完整系統上下文
- 探索性調試

---

### 1.12 executing-plans ✅（2026-02-08新增）
**功能**：批量執行計劃

**核心原則**：
- 分批執行，檢查點審查
- 默認前3個任務為一批

**流程**：
```
加載計劃 → 審查計劃 → 執行批次 → 彙報 → 反饋 → 繼續下一批 → 完成
```

**關鍵洞察**：
- 批量執行提高效率
- 檢查點確保質量
- 及時停止尋求幫助

---

### 1.13 writing-skills ✅（2026-02-08新增）
**功能**：創建新Skills

**核心原則**：
- TDD應用於過程文檔
- 鐵律：無失敗測試，不準創建技能

**流程**：
```
RED：編寫失敗測試（基線）→ GREEN：編寫最小技能 → REFACTOR：堵塞漏洞
```

**類型**：
- Technique：具體方法，有步驟
- Pattern：思維方式
- Reference：API文檔，語法指南

---

## 二、待學習Skills（0/14）

| Skill | 功能 | 狀態 |
|-------|------|------|
| - | 全部完成 | ✅ 14/14 |

---

## 三、學習日誌

### 2026-02-08
- [x] **夜間深度工作**
  - Prismark知識深度整理
  - Roadmap優化完善
  - 完成14/14 Skills學習
  - 生成夜間工作彙報

### 2026-02-07
- [x] 深度自我反思（deep_self_reflection.md）
- [x] 識別5大核心問題
- [x] 建立CAPDCA改進框架
- [x] 創建Supervisor Agent配置文件
- [x] 配置cron每日彙報任務（2026-02-07新增）
**功能**：创意构思转化为设计

**核心原则**：
- 每次只问一个问题
- 多选优于开放
- YAGNI原则
- 渐进式验证

**流程**：
```
理解想法 → 探索方案（2-3种）→ 分段呈现设计 → 验证每部分 → 记录到docs/
```

**关键洞察**：
- 200-300字为一段
- 不一次性展示全部
- 先问"是否正确"再继续（2026-02-07新增）
**功能**：编写实施计划，多步骤任务规划

**核心原则**：
- 2-5分钟颗粒度任务
- 完整代码，不是"添加验证"
- TDD + DRY + YAGNI

**流程**：
```
规格 → 编写计划 → 保存到docs/plans → 执行选项（子代理/并行）
```

**关键洞察**：
- 假设工程师零上下文，但技术熟练
- 必须提供精确文件路径（2026-02-07新增）
**功能**：子代理驅動開發，單任務分派+兩階段審查

**核心原則**：
- 每個任務派發Fresh subagent
- 兩階段審查：規格符合 → 代碼質量
- 同一會話，無需上下文切換

**流程**：
```
任務 → 派發implementer → 實現/測試/自審 → 派發spec reviewer → 規格審查
→ 派發code quality reviewer → 質量審查 → 完成
```

**優勢**：
- 子代理遵循TDD自然
- 新鮮上下文每任務（無干擾）
- 問題在修復前浮現（比事後好）
- 質量門檻自動化

**铁律**：
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**循环**：
1. **RED**：写失败的测试
2. **Verify RED**：确认测试失败
3. **GREEN**：写最小代码通过测试
4. **Verify GREEN**：确认测试通过
5. **REFACTOR**：重构代码

**关键洞察**：
- 测试先于代码才能证明它真的在测试某样东西
- YAGNI（You Aren't Gonna Need It）：不要添加不需要的功能

**常见借口**：
| 借口 | 现实 |
|-----|------|
| "太简单不用测试" | 简单代码也会崩，测试只需30秒 |
| "之后测试" | 立即通过的测试证明不了任何事 |
| "手动测试过了" | 手动测试是随机的，没有记录 |

---

## 三、待学习Skills（8/14）

| Skill | 功能 | 优先级 |
|-------|------|-------|
| subagent-driven-development | 子代理驱动开发 | P1 |
| writing-plans | 创建实施计划 | P1 |
| brainstorming | Socratic设计细化 | P2 |
| using-git-worktrees | Git工作树隔离 | P2 |
| finishing-a-development-branch | 完成分支决策 | P2 |
| dispatching-parallel-agents | 并行子代理 | P2 |
| executing-plans | 批量执行计划 | P2 |
| writing-skills | 创建新Skills | P3 |

---

## 四、已学配套技术

### 4.1 root-cause-tracing
**功能**：通过调用链回溯找根因

**流程**：
```
观察症状 → 直接原因 → 谁调用 → 继续向上 → 源头修复 → 多层防御
```

### 4.2 defense-in-depth
多层防御机制

### 4.3 condition-based-waiting
基于条件的轮询替代任意超时

---

## 五、OpenClaw GitHub项目研究（2026-02-07）

### 5.1 OpenClaw 核心架构

**官方定位**：
- 个人AI助手，支持任何OS、任何平台
- 多渠道接入：WhatsApp、Telegram、Slack、Discord等

**核心组件**：
| 组件 | 功能 |
|-----|------|
| Gateway | 控制平面，单一WS控制 |
| Workspace | 工作区，~/.openclaw/workspace |
| Skills | 技能系统，~/.openclaw/skills/ |
| CLI | 命令行工具 |

**关键配置文件**：
- AGENTS.md：Agent配置
- SOUL.md：人格设定
- TOOLS.md：工具配置
- USER.md：用户信息

### 5.2 ClawHub（Skill注册表）

**功能**：
- 发布、版本管理、技能搜索
- 基于向量的语义搜索
- 支持Bun + Convex构建

**技术栈**：
- 前端：TanStack Start (React, Vite/Nitro)
- 后端：Convex (DB + 文件存储)
- 搜索：OpenAI embeddings

### 5.3 项目亮点

**多渠道接入**：
- WhatsApp, Telegram, Slack, Discord
- Google Chat, Signal, iMessage
- BlueBubbles, Microsoft Teams

**工具系统**：
- Browser控制
- Canvas可视化
- Nodes设备控制
- Cron定时任务

**安全模型**：
- 沙箱隔离
- DM配对机制
- OAuth认证

### 5.4 学习要点

1. **架构设计**：Gateway + Agent的分离模式
2. **技能系统**：SKILL.md + 配套文件的标准化
3. **多平台支持**：Tailscale远程访问
4. **安全优先**：默认不信任任何输入

---

## 六、学习日志

### 2026-02-07
- [x] 学习 test-driven-development
- [x] 研究 OpenClaw GitHub项目
- [x] 研究 ClawHub Skill注册表
- [x] 更新学习日志

### 累计进度（6/14）
- [x] planning-with-files
- [x] systematic-debugging
- [x] verification-before-completion
- [x] receiving-code-review
- [x] requesting-code-review
- [x] test-driven-development

### 待继续
- [ ] subagent-driven-development
- [ ] writing-plans
- [ ] brainstorming

---

## 七、执行检查清单

### 复杂任务
```
[] 这是复杂任务吗？（>3步骤）
[] 需要planning-with-files吗？
[] 调用对应Skill了吗？
[] 遵循2-Action Rule吗？
```

### Bug修复
```
[] 完成Root Cause分析了吗？
[] 3次修复失败后质疑架构了吗？
[] 修复后运行验证命令了吗？
```

### 代码提交
```
[] 完成所有任务了吗？
[] 运行验证命令了吗？
[] 请求代码审查了吗？
```

---

## 八、学习资源

### 官方文档
- Superpowers README: /Users/dave/clawd/skills/superpowers/README.md
- Skills目录: /Users/dave/clawd/skills/superpowers/skills/
- OpenClaw GitHub: https://github.com/openclaw/openclaw
- ClawHub: https://github.com/openclaw/clawhub

### 模板文件
- task_plan.md模板
- findings.md模板
- progress.md模板

---

## 九、实践改进案例

### 9.1 跨地区公司比较改进

**问题**：比较跨地区公司（日本、台湾）时，货币不同无法直接比较

**改进措施**：
1. 统一货币基准（使用美元USD）
2. 添加相对比较（以某公司为基准=100%）
3. 标注汇率换算

**改进后数据**：
| 公司 | 原币别 | 换算美元 | 相对GUC |
|-----|-------|---------|---------|
| Socionext | 1,854亿日币 | 12.0億USD | **545%** |
| GUC | 341亿台币 | 2.2億USD | 100%基准 |
| Alchip | 309亿台币 | 2.0億USD | 91% |

**心得**：
- 跨地区比较必须统一货币
- 相对比较能更直观看出差距
- 标注汇率让数据可追溯

---

## 十、OpenClaw架构学习要点

### 10.1 Gateway架构
- 单WS控制平面
- 支持多渠道路由
- 内置安全机制

### 10.2 Skills系统
- SKILL.md标准化格式
- 技能安装/卸载机制
- 技能版本管理

### 10.3 多渠道接入
- 支持10+主流通讯平台
- 统一的API接口
- 灵活的路由配置

### 10.4 安全模型
- 默认不信任任何输入
- DM配对机制
- OAuth认证

---

**下次更新**：继续学习subagent-driven-development
