# DeepSeek 技术研究 - 持续跟踪

## 研究目标
持续追踪 DeepSeek 大模型论文，分析每年技术突破和优化方向。

## 文件位置
- `/Users/dave/clawd/deepseek_research/DeepSeek_Technical_Evolution.xlsx`
- `/Users/dave/clawd/deepseek_research/DeepSeek_Technical_Report.md`

## 核心创新总结

### 架构创新
1. **MLA (Multi-head Latent Attention)** - KV压缩, 高效推理
2. **DeepSeekMoE** - 经济高效的稀疏MoE
3. **Auxiliary-Loss-Free Load Balancing** - 无辅助损失负载均衡
4. **MTP (Multi-Token Prediction)** - 多token预测训练

### 训练创新
1. **FP8 训练** - 降低训练成本
2. **DualPipe** - 计算-通信重叠
3. **GRPO** - 纯RL推理激发
4. **可扩展RL框架** - 后训练规模化

## 技术演进

| 时间 | 模型 | 参数 | 关键突破 |
|-----|------|------|---------|
| 2024.05 | DeepSeek-V2 | 236B总/21B激活 | MLA + DeepSeekMoE, 128K |
| 2024.12 | DeepSeek-V3 | 671B总/37B激活 | FP8, MTP, 无辅助损失 |
| 2025.01 | DeepSeek-R1 | 基于V3-Base | GRPO, 纯RL推理 |
| 2025.12 | DeepSeek-V3.2 | 增强版 | DSA, 可扩展RL |

## 关键论文

- DeepSeek-V2: arXiv:2405.04434
- DeepSeek-V3: arXiv:2412.19437
- DeepSeek-R1: arXiv:2501.12948
- DeepSeek-V3.2: arXiv:2512.02556

## 待深入研究

1. MLA KV压缩矩阵详细实现
2. GRPO vs PPO 对比分析
3. MoE 专家路由策略
4. FP8 训练精度分析
5. DualPipe 调度算法

## 定期检查

### 每月检查
- 时间: 每月1号 9:00
- 任务: 搜索 DeepSeek 新论文

### 每周扫描
- 时间: 每周一 10:00
- 任务: 检查 arXiv 是否有 DeepSeek 新发布

## 关注领域
- 推理能力提升 (R1系列)
- 训练效率优化
- MoE 架构演进
- 开源社区影响

## 更新记录
- 2026-02-02: 初始版本, 包含 V2/V3/R1/V3.2
