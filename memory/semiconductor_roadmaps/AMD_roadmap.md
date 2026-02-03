# AMD CPU/GPU Roadmap (2024-2026)

**更新时间**: 2026-02-03  
**数据来源**: AMD官方、Wikipedia、Tom's Hardware、行业分析报告

---

## 📊 CPU架构演进时间线

| 架构 | 代号 | 发布时间 | 制程节点 | 代表产品 | 定位 |
|------|------|----------|----------|----------|------|
| **Zen 4** | Raphael | 2022 Q3 | TSMC N5 (4nm) | Ryzen 7000, EPYC 9004 | 桌面/服务器 |
| **Zen 4C** | Genoa-X | 2023 Q3 | TSMC N5 | EPYC 9004X | 服务器(高缓存) |
| **Zen 5** | Nirvana | 2024 Q2 | TSMC N3 (3nm) | Ryzen 9000, EPYC 9005 | 桌面/服务器 |
| **Zen 5C** | Turin-X | 2025 Q1 | TSMC N3 | EPYC 9005X | 服务器(高缓存) |
| **Zen 6** | Morpheus | 2026 H2 | TSMC N3P/N2 | Ryzen 10000, EPYC 10000 | 桌面/服务器 |
| **Zen 6C** | Medusa | 2026 H2 | TSMC N3P/N2 | EPYC 10000X | 服务器(高缓存) |
| **Zen 7** | TBD | 2027 H2 | TSMC N2 | Ryzen 11000 | 桌面 |

---

## 🎯 服务器CPU规格对比 (EPYC 9000系列)

| 产品 | 发布时间 | 制程 | 核心/线程 | L3缓存 | TDP | 市场定位 |
|------|----------|------|-----------|--------|-----|----------|
| **EPYC 9004 (Genoa)** | 2022 Q4 | N5 | 96C/192T | 384MB | 360W | 通用服务器 |
| **EPYC 9004X (Genoa-X)** | 2023 Q3 | N5 | 96C/192T | 1152MB | 400W | 高缓存应用 |
| **EPYC 9005 (Turin)** | 2024 Q4 | N3 | 128C/256T | 512MB | 500W | 高性能计算 |
| **EPYC 9005X (Turin-X)** | 2025 Q1 | N3 | 128C/256T | 1536MB | 500W | 高缓存应用 |
| **EPYC 10000 (Zen 6)** | 2026 H2 | N3P | 192C/384T | TBD | TBD | 下一代旗舰 |
| **EPYC 10000X** | 2026 H2 | N3P | TBD | TBD | TBD | 高缓存版本 |

---

## 🎮 GPU架构演进 (消费级)

| 架构 | 发布时间 | 制程 | 代表产品 | 目标市场 |
|------|----------|------|----------|----------|
| **RDNA 3** | 2022 Q4 | TSMC N5/N6 | RX 7900 XTX | 高端游戏 |
| **RDNA 4** | 2025 Q1 | TSMC N4 | RX 8800/8700 | 主流游戏+AI |
| **RDNA 5** | 2027 H1 | TSMC N3 | TBD | 下一代 |

---

## 🤖 AI加速器 Roadmap (Instinct系列)

| 产品 | 发布时间 | 制程 | HBM规格 | FP8性能 | 定位 |
|------|----------|------|---------|---------|------|
| **MI300X** | 2024 Q1 | N5 | 192GB HBM3 | 1.3 PFLOPS | AI训练/推理 |
| **MI325X** | 2024 Q4 | N5 | 256GB HBM3e | 1.8 PFLOPS | 增强版 |
| **MI350X** | 2025 Q1 | N3 | 288GB HBM3e | 4.0 PFLOPS | 主力AI加速器 |
| **MI350D** | 2025 Q2 | N3 | 288GB HBM3e | 4.0 PFLOPS | 推理优化 |
| | 2026 **MI400** H1 | N3P | 432GB HBM4 | 20 PFLOPS | 下一代旗舰 |
| **MI400X** | 2026 H2 | N3P | 432GB HBM4 | 20 PFLOPS | 高端版本 |

### Instinct MI400关键规格
- **FP4性能**: 40 PFLOPS
- **FP8性能**: 20 PFLOPS
- **HBM4容量**: 432GB
- **HBM4带宽**: 19.6 TB/s
- **制程**: TSMC 3nm (N3P)

---

## 📈 CDNA架构演进 (数据中心GPU)

| 架构 | 发布时间 | 制程 | 代表产品 | 关键特性 |
|------|----------|------|----------|----------|
| **CDNA 3** | 2024 Q1 | N5 | MI300X | 统一内存架构 |
| **CDNA 4** | 2025 Q1 | N3 | MI350X | 增强AI性能 |
| **CDNA 5** | 2026 H1 | N3P | MI400 | 下一代架构 |

---

## 🔗 制程节点演进

| 架构 | 初始制程 | 后续迭代 | 性能提升 |
|------|----------|----------|----------|
| Zen 4 | N5 (4nm) | - | 相比Zen 3: +29% IPC |
| Zen 5 | N3 (3nm) | N3X | 相比Zen 4: +16% IPC |
| Zen 6 | N3P (3nm) | N2 (2nm) | 相比Zen 5: TBD |
| Zen 7 | N2 (2nm) | - | 相比Zen 6: TBD |

---

## 💡 关键洞察

1. **服务器CPU市场突破**: EPYC 9005 (Turin)采用128核192线程，在HPC和AI推理领域竞争力增强
2. **AI加速器追赶策略**: MI350X对标NVIDIA H200，MI400瞄准Blackwell/Rubin
3. **3nm制程全面切换**: 2024-2025年Zen 5和Instinct系列全面转向TSMC 3nm
4. **HBM4升级节点**: 2026年MI400将首发432GB HBM4，容量翻倍
5. **2027年展望**: Zen 7和RDNA 5将首批采用TSMC 2nm制程

---

## 🔗 参考来源

1. [AMD Zen 6 Wikipedia](https://en.wikipedia.org/wiki/Zen_6) - Wikipedia
2. [AMD Roadmap Zen 7](https://www.tomshardware.com/pc-components/cpus/amd-reveals-new-roadmap-for-its-ryzen-cpus-teasing-zen-7-as-the-true-next-generation-leap-with-2nm) - Tom's Hardware
3. [AMD Instinct MI350 Roadmap](https://tech.yahoo.com/computing/articles/amd-lays-instinct-mi350-roadmap-172800362.html) - Yahoo Tech
4. [AMD EPYC Market Share](https://markets.financialcontent.com/wral/article/predictstreet-2025-9-30-amd-powering-the-future-of-ai-and-high-performance-computing-as-of-9302025) - Financial Content
5. [AMD Roadmap Analysis](https://www.nextplatform.com/2025/11/14/amd-solid-roadmaps-beget-money-which-beget-better-roadmaps-and-even-more-money/) - The Next Platform

---

*文档维护: 半导体Roadmap深度整理项目*  
*最后更新: 2026-02-03*
