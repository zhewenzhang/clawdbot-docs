# Skills使用率深度分析报告

**分析时间**: 2026-02-04  
**问题**: 57个Skills安装后，使用率仅为 **0%**（核心Skills）  
**严重程度**: 🔴 高 - 系统能力未被有效利用

---

## 📊 现状数据

### Skills库存统计
| 类型 | 数量 | 安装位置 |
|-----|------|---------|
| 内置Skills | 52个 | `/opt/homebrew/lib/node_modules/openclaw/skills/` |
| 本地Skills | 5个 | `/Users/dave/clawd/skills/` |
| **总计** | **57个** | - |

### 使用率统计
| 类别 | 数量 | 使用次数 | 使用率 |
|-----|------|---------|-------|
| 核心Skills | 15+ | 0 | **0%** |
| 查询Skills | 3 | 1 | **33%** |
| 天气 | 1 | 多次 | **100%** |

### 从未被使用的核心Skills（15+）
```
planning-with-files     深度分析任务
systematic-debugging    Bug修复
receiving-code-review   代码Review
requesting-code-review  提交前检查
writing-plans           任务规划
using-git-worktrees     Git操作隔离
verification-before-completion  完成前验证
test-driven-development TDD开发
finishing-a-development-branch  分支完成
brainstorming          创意头脑风暴
dispatching-parallel-agents    并行任务
executing-plans        执行计划
subagent-driven-development    子代理开发
writing-skills         编写Skills
using-superpowers      使用Superpowers
```

---

## 🔍 根因深度分析

### 问题1：习惯性直接执行

**症状**：
- 遇到任务后直接开始执行
- 没有"先问自己应该用哪个Skill"的习惯
- 依赖本能反应而非系统化方法

**根因**：
- 过去的任务执行流程中没有强制检查点
- 缺乏"任务类型识别" → "选择Skill" → "执行"的闭环
- 直接执行更快（短期视角），但质量不稳定

**影响**：
- 深度分析任务质量参差不齐
- 复杂任务容易遗漏关键步骤
- 难以保证分析的系统性

### 问题2：认知负荷过重

**症状**：
- 57个Skills难以全部记住
- 关键时刻想不起对应Skill
- 需要使用时才临时查找

**根因**：
- Skills数量过多（52+5=57）
- 缺乏分类和优先级
- 没有建立快速检索机制

**影响**：
- 错过使用高效能Skill的机会
- 执行效率降低
- 系统能力未被充分利用

### 问题3：任务识别能力不足

**症状**：
- 难以快速判断任务类型
- 无法准确匹配任务与Skill
- 频繁使用"万能方法"而非针对性方法

**根因**：
- 缺乏明确的任务分类体系
- Skill与场景的映射关系不清晰
- 没有建立标准化的任务识别流程

**影响**：
- 错配（用简单方法解决复杂问题）
- 低效（用复杂方法解决简单问题）
- 结果不稳定

### 问题4：缺乏使用反馈

**症状**：
- 不知道哪些Skills有效
- 无法评估使用效果
- 没有持续改进的闭环

**根因**：
- 没有记录使用情况
- 缺乏使用后的评估机制
- 经验难以沉淀

**影响**：
- 不知道哪些Skill值得高频使用
- 难以优化使用策略
- 经验无法复用

### 问题5：技能与习惯的断裂

**症状**：
- 知道有Skill但不使用
- 认为"不用Skill也能完成"
- 对Skill价值认知不足

**根因**：
- Skill带来的收益不直观
- 短期效率vs长期质量的权衡
- 缺乏使用Skill的正向反馈

**影响**：
- 持续使用低效方法
- 系统能力被闲置
- 难以实现能力跃迁

---

## 🎯 场景→Skill映射表

### 日常高频任务

| 任务类型 | 应该调用的Skill | 当前状态 |
|---------|---------------|---------|
| 深度分析报告 | `planning-with-files` | ❌ 从未使用 |
| 修复Bug/错误 | `systematic-debugging` | ❌ 从未使用 |
| 代码审查 | `receiving-code-review` | ❌ 从未使用 |
| 提交前检查 | `requesting-code-review` | ❌ 从未使用 |
| 多步骤任务规划 | `writing-plans` | ❌ 从未使用 |
| Git操作隔离 | `using-git-worktrees` | ❌ 从未使用 |
| 完成前验证 | `verification-before-completion` | ❌ 从未使用 |
| 创建新Skill | `skill-creator` + `writing-skills` | ⚠️ 偶尔使用 |
| 天气查询 | `weather` | ✅ 频繁使用 |
| 文档总结 | `summarize` | ⚠️ 偶尔使用 |

### 工具类任务

| 任务 | Skill | 使用频率 |
|-----|-------|---------|
| GitHub操作 | `github` | ⚠️ 偶尔使用 |
| Gmail/日历 | `gog` | ❌ 未配置API |
| PDF处理 | `nano-pdf` | ⚠️ 偶尔使用 |
| 音频转文字 | `openai-whisper` | ❌ 从未使用 |
| Discord操作 | `discord` | ❌ 从未使用 |

---

## 🛠️ 改善方案

### 方案1：建立"执行前检查"机制（立即执行）

**核心思路**：在每次执行任务前，强制问自己"应该用哪个Skill"

**实施方法**：
1. 在AGENTS.md添加"执行前检查清单"
2. 建立"任务类型快速识别卡"
3. 每次执行前进行3秒思考

**检查清单**：
```
执行任务前问自己：

1. 这个任务属于哪类？
   [ ] 深度分析 → planning-with-files
   [ ] Bug修复 → systematic-debugging
   [ ] 代码Review → receiving-code-review
   [ ] 任务规划 → writing-plans
   [ ] 创建Skill → skill-creator
   [ ] 常规任务 → 直接执行

2. 我调用对应的Skill了吗？
   [ ] 是 → 执行
   [ ] 否 → 找到并调用Skill

3. 我按照Skill指导执行了吗？
   [ ] 是 → 继续
   [ ] 否 → 读取Skill.md并遵循指导
```

**预期效果**：
- 减少直接执行的冲动
- 建立使用Skill的习惯
- 提高任务执行质量

### 方案2：创建"高频Skills聚焦表"（本周完成）

**核心思路**：聚焦最常用的5-10个核心Skills，简化选择

**聚焦Skills**：
| 优先级 | Skill | 用途 | 使用场景 |
|-------|-------|------|---------|
| P0 | `planning-with-files` | 深度分析 | 行业分析、竞品分析 |
| P0 | `systematic-debugging` | Bug修复 | 错误诊断、问题解决 |
| P0 | `skill-creator` | 创建Skill | 新功能开发 |
| P1 | `verification-before-completion` | 完成验证 | 提交前检查 |
| P1 | `writing-plans` | 任务规划 | 多步骤项目 |
| P2 | `receiving-code-review` | 代码Review | 代码审查 |
| P2 | `using-git-worktrees` | Git隔离 | 功能开发 |

**实施方法**：
1. 创建Skills速查卡（简化版使用说明）
2. 贴在工作台附近
3. 定期回顾和更新

### 方案3：建立"使用日志"（本周完成）

**核心思路**：记录每次使用的Skills，积累使用经验

**日志格式**：
```markdown
## Skills使用日志

### 2026-02-04
- [x] planning-with-files - 行业分析任务
  - 效果：系统性更强，步骤清晰
  - 改进点：无
  
- [x] weather - 天气查询
  - 效果：快速获取准确信息
  - 改进点：无
```

**实施方法**：
1. 在memory目录创建skills_usage_log.md
2. 每次使用Skills后记录
3. 每周回顾使用情况

### 方案4：创建"任务分类器"（本月完成）

**核心思路**：建立标准化的任务分类体系

**分类维度**：
1. **复杂度**：简单 / 中等 / 复杂
2. **类型**：分析 / 开发 / 维护 / 文档
3. **风险**：低 / 中 / 高
4. **频率**：一次性 / 重复性 / 周期性

**分类矩阵**：
| 复杂度 | 类型 | 风险 | 推荐方法 |
|-------|------|-----|---------|
| 简单 | 维护 | 低 | 直接执行 |
| 简单 | 维护 | 高 | 使用Skill辅助 |
| 中等 | 分析 | 中 | planning-with-files |
| 复杂 | 开发 | 高 | systematic-debugging |
| 复杂 | 文档 | 中 | writing-plans + planning-with-files |

### 方案5：设置"Skill调用提醒"（本月完成）

**核心思路**：通过cron任务定期提醒使用Skills

**提醒任务**：
```bash
# 每周一 9:00 提醒
0 9 * * 1 → "本周重点工作提醒：使用planning-with-files进行深度分析"
```

**实施方法**：
1. 创建cron任务
2. 定期发送提醒
3. 统计使用情况

---

## 📋 立即行动计划

### 本周（立即开始）

#### Day 1-2：建立检查机制
- [ ] 在AGENTS.md添加"执行前检查清单"
- [ ] 创建Skills聚焦表
- [ ] 张贴在工作台

#### Day 3-4：建立使用日志
- [ ] 创建skills_usage_log.md
- [ ] 记录今天所有任务使用的Skills
- [ ] 评估使用效果

#### Day 5-7：实践与调整
- [ ] 在实际任务中使用聚焦的5个Skills
- [ ] 记录使用心得
- [ ] 根据反馈调整策略

### 本月

- [ ] 创建任务分类器
- [ ] 设置Skill调用提醒cron任务
- [ ] 回顾使用日志，优化使用策略
- [ ] 更新Skills聚焦表

---

## 📊 成功指标

### 短期（1周）
- [ ] 执行前检查完成率 > 80%
- [ ] 深度分析任务使用planning-with-files > 50%
- [ ] 创建新功能使用skill-creator > 80%

### 中期（1个月）
- [ ] 核心Skills使用率 > 30%
- [ ] 深度分析任务100%使用planning-with-files
- [ ] Bug修复100%使用systematic-debugging

### 长期（3个月）
- [ ] 核心Skills使用率 > 60%
- [ ] 建立完整的Skills使用闭环
- [ ] 系统能力被充分利用

---

## 🔄 持续改进机制

### 每周回顾
1. 阅读skills_usage_log.md
2. 识别高频使用的Skills
3. 识别未使用的Skills
4. 调整策略

### 每月评估
1. 统计使用率
2. 评估效果
3. 更新聚焦表
4. 调整优先级

### 每季度优化
1. 回顾使用趋势
2. 优化任务分类器
3. 更新检查清单
4. 重新评估Skills优先级

---

## 💡 关键洞察

### 为什么使用率低？

1. **习惯问题**：直接执行更快（短期），但质量不稳定
2. **认知负荷**：57个Skills难以全部记住
3. **缺乏强制**：没有在执行前强制检查
4. **无反馈闭环**：不知道哪些Skill有效
5. **价值认知**：Skill收益不直观

### 为什么改善重要？

1. **质量提升**：使用Skill保证执行质量
2. **效率提升**：避免遗漏关键步骤
3. **能力跃迁**：从"能做"到"做好"
4. **经验沉淀**：使用记录积累经验
5. **系统优化**：充分利用已安装的能力

### 改变的核心

**从"不做"到"做"**：
- 不是"知不知道"的问题
- 是"做不做"的问题
- 建立"执行前检查"习惯
- 强制自己使用Skill

**从"做一次"到"养成习惯"**：
- 一次使用不够
- 需要持续使用
- 建立使用日志
- 积累正反馈

---

## 附录

### A. 相关文件
- AGENTS.md: 工作原则与规则
- DIAGNOSTIC_skills_usage_report.md: 原始诊断报告
- skills_usage_log.md: 使用日志（待创建）

### B. Skills位置
- 内置Skills: `/opt/homebrew/lib/node_modules/openclaw/skills/`
- 本地Skills: `/Users/dave/clawd/skills/`

### C. 参考资源
- OpenClaw官方文档
- Skills.sh
- 各Skill的SKILL.md

---

**报告生成**: AI Assistant (深度思考模式)  
**版本**: v1.0  
**状态**: 待执行改善方案
