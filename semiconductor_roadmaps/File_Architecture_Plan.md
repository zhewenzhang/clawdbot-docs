# 📁 半导体公司 Roadmap 文件架构规划

## 目标
以**每家公司为一个Excel档案**，便于独立管理和更新。

---

## 📂 文件架构

```
/Users/dave/clawd/semiconductor_roadmaps/
│
├── nvidia/
│   └── NVIDIA_Roadmap.xlsx          # ✅ 已完成
│
├── amd/
│   └── AMD_Roadmap.xlsx              # ✅ 已完成
│
├── intel/
│   └── Intel_Roadmap.xlsx            # ✅ 已完成
│
├── google/
│   └── Google_TPU_Roadmap.xlsx       # ⏳ 待执行 (Phase 2)
│
├── taiwan/
│   ├── MediaTek_Roadmap.xlsx         # ⏳ 待执行
│   ├── Novatek_Roadmap.xlsx          # ⏳ 待执行
│   └── ...
│
├── china/
│   ├── Huawei_Roadmap.xlsx           # ⏳ 待执行
│   ├── Cambricon_Roadmap.xlsx        # ⏳ 待执行
│   └── ...
│
└── competitors/
    └── Competitor_Comparison.xlsx    # ✅ 已完成 (综合对比)

```

---

## 📋 Excel 档案结构标准

每家公司档案包含以下 Sheet：

| Sheet 名称 | 内容 | 必填 |
|-----------|------|-----|
| **Overview** | 公司简介、产品线总览 | ✅ |
| **GPU_Roadmap** | GPU 产品路线图 | ✅ (如有) |
| **CPU_Roadmap** | CPU 产品路线图 | ✅ (如有) |
| **Interconnect** | 互联技术 | ✅ |
| **Tech_Specs** | 技术规格对比 | ✅ |
| **History** | 历史版本 | ✅ |
| **Sources** | 数据来源 | ✅ |

---

## 📊 各档案内容概览

### 1. NVIDIA_Roadmap.xlsx (已创建)
**Sheet: 15个**
- Overview
- GPU_Roadmap (30+产品)
- CPU_Roadmap (Grace/Vera)
- Interconnect
- DPU_Networking
- System_Platform
- Code_Naming
- Tech_Specs_Compare
- Jetson_Embedded
- Metropolis
- Enterprise_Solutions
- Price_History
- AMD_Instinct (临时)
- Intel_Gaudi (临时)
- Competition (临时)

**待分离**: AMD/Intel/Competition 移至独立档案

### 2. AMD_Roadmap.xlsx (待创建)
**Sheet: 6个**
- Overview
- GPU_Roadmap (Instinct MI300/350/400)
- CPU_Roadmap (如有)
- Interconnect (Infinity Fabric)
- Tech_Specs_Compare
- Sources

### 3. Intel_Roadmap.xlsx (待创建)
**Sheet: 6个**
- Overview
- GPU_Roadmap (Gaudi/Falcon Shores)
- CPU_Roadmap (Xeon)
- Interconnect (CXL)
- Tech_Specs_Compare
- Sources

### 4. Google_TPU_Roadmap.xlsx (待创建)
**Sheet: 6个**
- Overview
- TPU_Roadmap (v5/v6/v7/v8)
- Interconnect (TPU Pods)
- Tech_Specs_Compare
- Sources

---

## 🔄 文件命名规则

```
{公司名}_Roadmap_{YYYY-MM-DD}.xlsx
```

示例:
- `NVIDIA_Roadmap_2026-02-02.xlsx`
- `AMD_Roadmap_2026-02-02.xlsx`
- `Intel_Roadmap_2026-02-02.xlsx`

**当前版本** (无日期) = 主文件
**历史版本** (带日期) = 归档

---

## 📅 更新计划

### Phase 1 (已完成)
- [x] NVIDIA_Roadmap.xlsx
- [x] Competitor_Comparison.xlsx
- [x] 文件管理架构规划

### Phase 2 (当前)
- [ ] 分离 AMD 数据 → AMD_Roadmap.xlsx
- [ ] 分离 Intel 数据 → Intel_Roadmap.xlsx
- [ ] 创建 Google_TPU_Roadmap.xlsx
- [ ] 清理 NVIDIA_Roadmap.xlsx (保留纯NVIDIA)

### Phase 3 (待执行)
- [ ] MediaTek_Roadmap.xlsx
- [ ] Novatek_Roadmap.xlsx
- [ ] 其他台湾 IC 设计公司
- [ ] Huawei_Roadmap.xlsx
- [ ] Cambricon_Roadmap.xlsx
- [ ] 其他中国 AI 芯片公司

---

## ⚙️ 自动化任务

| 任务 | 触发 | 动作 |
|-----|------|-----|
| 季度更新 | 1/4/7/10 月 | 更新所有 Roadmap |
| 月度汇总 | 每月1日 | 行业新闻汇总 |
| 财报监控 | 财报季 | 自动检查更新 |

---

**创建时间**: 2026-02-02
**版本**: v1.0
