# Skills 使用情况诊断报告

生成时间：2026-02-04 08:18

---

## 📊 Skills 使用率统计

| 类型 | 数量 | 实际使用 | 使用率 |
|------|------|---------|--------|
| 应该用的核心 Skills | 15+ | 0 | **0%** |
| 简单查询 Skills | 3 | 1 | **33%** |

---

## ❌ 问题诊断

### 1. Skills 位置错误

**planning-with-files** 的正确位置：
```
应该：/Users/dave/clawd/skills/planning-with-files/skills/planning-with-files/SKILL.md
实际：/Users/dave/clawd/skills/planning-with-files/SKILL.md (不存在)
```

### 2. 核心 Skills 使用率为 0

**这些 Skills 从未被使用**：

| Skill | 场景 | 使用次数 |
|-------|------|---------|
| planning-with-files | 深度分析任务 | 0 |
| systematic-debugging | Bug 修复 | 0 |
| receiving-code-review | 代码 Review | 0 |
| requesting-code-review | 提交前检查 | 0 |
| writing-plans | 任务规划 | 0 |
| using-git-worktrees | Git 操作 | 0 |
| verification-before-completion | 完成前验证 | 0 |
| test-driven-development | TDD 开发 | 0 |
| finishing-a-development-branch | 分支完成 | 0 |
| brainstorming | 创意头脑风暴 | 0 |
| dispatching-parallel-agents | 并行代理 | 0 |
| executing-plans | 执行计划 | 0 |
| subagent-driven-development | 子代理开发 | 0 |
| writing-skills | 编写 Skills | 0 |
| using-superpowers | 使用 Superpowers | 0 |

### 3. 唯一使用的 Skill

**weather** - ✅ 100% 使用率
- 场景：天气查询
- 使用次数：多次

---

## 🎯 场景 → Skill 映射表

| 任务类型 | 应该调用的 Skill |
|---------|-----------------|
| 深度分析任务 | `planning-with-files` |
| Bug 修复 | `systematic-debugging` |
| 代码 Review | `receiving-code-review` |
| 提交代码前 | `requesting-code-review` |
| 多步骤任务规划 | `writing-plans` |
| Git 操作隔离 | `using-git-worktrees` |
| 完成前验证 | `verification-before-completion` |
| TDD 开发 | `test-driven-development` |
| 分支完成整合 | `finishing-a-development-branch` |
| 创意头脑风暴 | `brainstorming` |
| 并行任务 | `dispatching-parallel-agents` |
| 执行计划 | `executing-plans` |
| 子代理开发 | `subagent-driven-development` |
| 创建 Skill | `skill-creator` + `writing-skills` |
| 天气查询 | `weather` |
| 文档总结 | `summarize` |
| GitHub 操作 | `github` |
| Gmail/日历 | `gog` |

---

## 🔧 修复方案

### 立即修复

1. **添加使用规则到 AGENTS.md**
2. **创建"Skill 调用检查器"**
3. **定期自我检查**

### 长期改进

1. **养成"先读 Skill"的习惯**
2. **每次执行任务前问自己"应该用哪个 Skill"**
3. **记录 Skills 使用情况**

---

## 📝 AGENTS.md 需添加的规则

```markdown
## 🎯 Skills 使用规则

### 调用前必须
1. 识别任务类型
2. 调用对应 Skill（不是直接读取）
3. 读取其 SKILL.md
4. 按照指导执行

### 常见任务 → Skill 映射
| 任务 | 调用 |
|------|------|
| 深度分析 | planning-with-files |
| Bug 修复 | systematic-debugging |
| 代码 Review | receiving-code-review |
| 任务规划 | writing-plans |
| Git 操作 | using-git-worktrees |
| 创建 Skill | skill-creator |
```

---

## 💡 自我检查清单

每次执行任务前问：

- [ ] 这个任务有对应的 Skill 吗？
- [ ] 我调用了那个 Skill 吗？
- [ ] 我按照它的指导执行了吗？

---

## 结论

**问题严重程度**：中高
**改进优先级**：高
**预计改进时间**：立即开始，持续改进

**关键行动**：
1. 添加规则到 AGENTS.md
2. 每次任务前先识别 Skill
3. 养成"先读 Skill 后执行"的习惯
