# DeepSeek 技术演进研究报告

## 研究背景

DeepSeek 是中国领先的 AI 研究实验室，以开源大模型闻名。其模型在架构创新和训练效率方面有重大突破。

---

## 一、技术演进时间线

### 2024 年

| 时间 | 模型 | 参数 | 核心创新 |
|-----|------|------|---------|
| 2024.05 | **DeepSeek-V2** | 236B 总, 21B 激活 | MLA + DeepSeekMoE, 128K 上下文 |
| 2024.12 | **DeepSeek-V3** | 671B 总, 37B 激活 | FP8 训练, 无辅助损失负载均衡, MTP |

### 2025 年

| 时间 | 模型 | 参数 | 核心创新 |
|-----|------|------|---------|
| 2025.01 | **DeepSeek-R1** | 基于 V3-Base | GRPO, 纯 RL 推理激发 |
| 2025.12 | **DeepSeek-V3.2** | 增强版 V3 | DSA, 可扩展 RL 框架 |

---

## 二、核心架构创新

### 1. Multi-head Latent Attention (MLA)

**提出时间**: DeepSeek-V2 (2024.05)

**核心思想**: 
- 压缩 KV 缓存为单一矩阵
- 相比标准 KV 缓存，大幅降低推理内存

**技术细节**:
```
n_h = 128 attention heads
d_h = 128 per-head dimension  
d_c = 512 (KV compression dim)
d_c_prime = 512 (Query compression dim)
```

**优势**:
- 降低推理内存占用
- 保持甚至提升模型性能
- 每个 Query head 有独特的 K/V

### 2. DeepSeekMoE

**架构**: 稀疏 Mixture-of-Experts

**特点**:
- 经济高效的训练
- 专家路由机制
- 只激活部分专家

### 3. Auxiliary-Loss-Free Load Balancing

**提出时间**: DeepSeek-V3 (2024.12)

**创新**: 无辅助损失实现负载均衡

**优势**:
- 简化训练流程
- 提升模型性能

### 4. Multi-Token Prediction (MTP)

**提出时间**: DeepSeek-V3 (2024.12)

**功能**: 训练时预测多个 token

**优势**:
- 提升生成效率
- 改善生成质量

---

## 三、训练技术创新

### 1. FP8 训练

**应用**: DeepSeek-V3

**优势**: 降低训练成本

### 2. DualPipe 流水线并行

**应用**: DeepSeek-V3

**功能**:
- 重叠注意力与 MoE 计算
- 重叠 MoE 通信
- 减少流水线气泡

### 3. GRPO (Group Relative Policy Optimization)

**提出时间**: DeepSeek-R1 (2025.01)

**框架**: 群体相对策略优化

**突破**: 纯 RL 激发推理能力，无需人工标注

### 4. 可扩展 RL 框架

**应用**: DeepSeek-V3.2

**特点**: 后训练计算规模化

---

## 四、关键论文

| 年份 | 论文 | ArXiv ID | 核心贡献 |
|-----|------|---------|---------|
| 2024.05 | DeepSeek-V2 | 2405.04434 | MLA + DeepSeekMoE |
| 2024.12 | DeepSeek-V3 | 2412.19437 | 671B MoE, FP8, MTP |
| 2025.01 | DeepSeek-R1 | 2501.12948 | 纯 RL 推理激发 |
| 2025.12 | DeepSeek-V3.2 | 2512.02556 | 推理增强 |

**论文链接**:
- https://arxiv.org/abs/2405.04434
- https://arxiv.org/abs/2412.19437
- https://arxiv.org/abs/2501.12948
- https://arxiv.org/abs/2512.02556

---

## 五、待深入研究课题

1. **MLA 详细实现**
   - KV 压缩矩阵设计
   - 与 MQA/MHA 对比

2. **GRPO vs PPO**
   - 策略优化对比
   - 推理能力涌现机制

3. **MoE 专家路由**
   - 路由策略分析
   - 负载均衡机制

4. **FP8 训练精度**
   - 数值稳定性分析
   - 精度 vs 效率 trade-off

5. **DualPipe 调度**
   - 流水线气泡分析
   - 计算-通信重叠

---

## 六、研究计划

### 短期 (1-2周)
- [ ] 下载并阅读 DeepSeek-V2 原论文
- [ ] 深入理解 MLA 实现

### 中期 (1个月)
- [ ] 阅读 DeepSeek-V3 论文
- [ ] 分析 FP8 训练细节

### 长期 (持续)
- [ ] 跟进 R1 系列论文
- [ ] 复现关键实验

---

**更新时间**: 2026-02-02
**版本**: v1.0
