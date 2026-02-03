# 🧠 模型进化史 (Model Evolution History)

记录 Clawdbot 核心模型的变更、升级与测试记录。

## 2026-02-01: Gemini 全家桶部署
*   **动作**: 新增配置
*   **原因**: 用户 (合伙人) 指示，构建 Google Gemini 全场景能力矩阵。
*   **变更详情**:
    *   ✅ 主力: `google/gemini-3-pro-preview` (Gemini 3)
    *   ✅ 新增: `google/gemini-2.0-flash-exp` (Alias: `flash`) - 用于极速/低成本任务
    *   ✅ 新增: `google/gemini-1.5-pro` (Alias: `pro-1.5`) - 用于长上下文兜底
*   **状态**: 已生效

---
