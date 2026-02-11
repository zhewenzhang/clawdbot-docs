# Cron任务格式分析报告

**生成时间**: 2026-02-04  
**问题**: Markdown格式在Telegram显示混乱

---

## 问题根源

**违反规则**：
- AGENTS.md: "不用 Markdown，需要表格时生成 PDF/Excel"
- 但 cron 任务 prompt 包含 Markdown 表格格式
- 输出直接发送到 Telegram，显示错误

**证据**（从运行记录中发现）：

### Daily Token Report
```
| 项目 | 状态 |
|-----|------|
| ✅ 数据获取 | session_status, uptime, token_stats.json |
```

### Daily Token Report 运行记录
```json
{
  "summary": "📊 **2026-02-04 每日综合报告**\n\n🤖 **Token 消耗**\n📉 昨日 (02-03): **3,734** tokens (In: 3,579 / Out: 155)\n📊 本月累计: **160,047** tokens\n📈 日均消耗: ~53,349 tokens\n\n🖥️ **系统状态**\n⏱️ **连续运行:** 2天 10小时 35分钟\n⚙️ **平均负载:** 1.25 / 1.20 / 1.17\n⚡ **瞬时功耗:** AC Power (N/A)\n\n🧠 **当前模型:** MiniMax-M2.1"
}
```

### 金价报告
```markdown
📊 **2月3日黄金价格日报**

**【国际金价】**
$4,913/盎司（较前一日+4.5%）
```

---

## 问题任务清单

| 任务ID | 任务名称 | 问题类型 | 严重程度 |
|--------|---------|---------|---------|
| 64632e2e-e480-4f29-a95a-77b2f87f46f9 | Daily Token Report | Markdown表格、格式复杂 | 🔴 高 |
| f9220fb6-6a00-4511-8ed7-9140a9bee14b | 每日金价查询汇报 | Markdown标题、列表 | 🟡 中 |
| ad1f0879-5fba-4d65-930a-21225cbf8387 | 每日Token额度检查 | 无表格，但格式可简化 | 🟢 低 |
| 38db15b2-06e6-4d94-b3c1-c25bdaeded47 | ABF Daily Analysis | 无表格，格式良好 | ✅ 正常 |
| 794f17f0-84b3-4912-8205-b3cf5decb8a8 | 每日行业报告摘要 | 无表格，格式良好 | ✅ 正常 |

---

## 根因分析

### 1. Cron任务配置存储位置
- 存储在 Gateway 数据库中（不可直接读取）
- 需要通过 `openclaw cron edit` 命令修改
- 无法查看完整 prompt 配置（只能查看运行摘要）

### 2. 输出格式问题
- Agent 执行 cron 任务时，直接发送 Markdown 到 Telegram
- Telegram 不支持 Markdown 表格显示
- 需要改为：
  - 纯文字格式（简单报告）
  - HTML/PDF 文件附件（复杂报告）

### 3. Prompt设计缺陷
- 原始 prompt 没有指定输出格式
- Agent 自由发挥，导致格式不一致
- 需要在 prompt 中明确规定输出格式

---

## 优化方案

### 方案1：简化Prompt（立即执行）

修改 cron 任务 prompt，明确要求：
1. **禁止使用 Markdown 表格**
2. **使用纯文字列表或段落**
3. **表格数据保存为临时文件并发送附件**

### 方案2：统一输出模板

为常用任务创建标准化模板：

#### Token报告模板（简化版）
```
📊 Token使用情况

✅ 已用/剩余：XX/XX tokens
✅ 上下文：XX%（健康）
✅ 建议：继续任务/建议清理
```

#### 金价报告模板（简化版）
```
📈 金价日报（2月3日）

国际金价：$4,913/盎司（+4.5%）
中国金价：约 1,027元/克

分析：维持高位震荡，短期动能偏多
```

### 方案3：高级方案（需要开发）

1. 创建统一报告生成器
2. 所有 cron 任务调用统一接口
3. 自动生成 HTML/PDF 格式
4. 发送文件附件而非直接输出

---

## 立即行动

### 步骤1：识别问题任务
- ✅ 已完成：Daily Token Report（金价报告需要简化）

### 步骤2：简化 Daily Token Report
```bash
# 查看当前配置
openclaw cron list | grep "Token Report"

# 修改 prompt（需要完整配置）
openclaw cron edit 64632e2e-e480-4f29-a95a-77b2f87f46f9 \
  --message "📊 Token使用情况报告
  
1. 检查 session_status 获取当前 Token 数
2. 读取 memory/token_stats.json
3. 生成简报格式（禁止Markdown表格）：
   - 已用/剩余
   - 上下文使用率
   - 建议（继续/清理）
4. 发送纯文字到Telegram，禁止Markdown格式
5. 回复：'Token检查完成'"
```

### 步骤3：简化金价报告
```bash
# 修改金价任务
openclaw cron edit f9220fb6-6a00-4511-8ed7-9140a9bee14b \
  --message "📈 今日金价
  
查询并报告：
1. 国际金价（美元/盎司）
2. 中国金价（元/克）
3. 简要分析（1-2句话）

格式要求：
- 禁止Markdown表格
- 使用纯文字段落
- 发送简洁报告"
```

### 步骤4：验证修改
- 等待下次执行或手动运行
- 检查 Telegram 输出格式

---

## 需要老板操作

⚠️ **重要**：需要通过命令行修改 cron 任务配置

**命令示例**：
```bash
# 修改 Daily Token Report
openclaw cron edit 64632e2e-e480-4f29-a95a-77b2f87f46f9 \
  --message "【新prompt内容】"
```

**或者**：我可以帮你生成修改脚本，你只需复制粘贴执行。

---

## 长期优化建议

1. **创建 cron 任务模板库**
   - 标准化所有 cron 任务 prompt
   - 统一输出格式
   - 便于维护和修改

2. **添加格式验证**
   - Agent 执行前检查输出格式
   - 禁止 Markdown 表格发送到 Telegram
   - 自动转换为纯文字或文件附件

3. **开发报告生成器**
   - 统一所有定期报告格式
   - 自动生成 HTML/PDF
   - 发送文件附件

---

## 附录

### A. 问题 cron 任务ID
- Daily Token Report: `64632e2e-e480-4f29-a95a-77b2f87f46f9`
- 金价查询: `f9220fb6-6a00-4511-8ed7-9140a9bee14b`
- Token额度检查: `ad1f0879-5fba-4d65-930a-21225cbf8387`
- ABF每日分析: `38db15b2-06e6-4d94-b3c1-c25bdaeded47`
- 行业摘要: `794f17f0-84b3-4912-8205-b3cf5decb8a8`

### B. 参考规则
- AGENTS.md: "不用 Markdown，需要表格时生成 PDF/Excel"
- HEARTBEAT.md: 每日检查项目配置

### C. 相关文件
- /Users/dave/clawd/AGENTS.md
- /Users/dave/clawd/HEARTBEAT.md
- /Users/dave/clawd/memory/token_stats.json
- /Users/dave/clawd/memory/heartbeat-state.json

---

**报告生成**: AI Assistant  
**版本**: v1.0  
**状态**: 待执行修改
