# 📁 半导体芯片 Roadmap 数据库

## 🎯 统一主数据库 (核心)

| 档案 | Sheet数 | 内容 |
|-----|---------|-----|
| `CHIP_Master_Database.xlsx` | 4 | **67 款芯片统一标准化数据** |

**标准化字段**:
- ID / 公司 / 总部 / 产品线 / 发布时间 / 架构 / 制程
- 核心数 / 线程数 / 性能指标 / 内存 / 功耗 / 应用

**可视化**:
- Timeline_Gantt - 时间轴甘特图
- Statistics - 统计分析
- Process_Timeline - 制程节点演进

---

## 📂 完整文件架构

```
semiconductor_roadmaps/
├── CHIP_Master_Database.xlsx 🎯  (67款芯片, 4 sheets)
├── INDEX.md
├── usa/
│   ├── NVIDIA_Roadmap.xlsx     (7款)
│   ├── AMD_Roadmap.xlsx        (3款)
│   ├── Intel_Roadmap.xlsx      (2款)
│   └── Broadcom_Roadmap.xlsx   (5款)
├── taiwan/
│   ├── MediaTek_Roadmap.xlsx   (3款)
│   ├── Novatek_Roadmap.xlsx    (3款)
│   ├── Realtek_Roadmap.xlsx    (2款)
│   ├── SiliconPower_Roadmap.xlsx (2款)
│   └── GlobalUnichip_Roadmap.xlsx (2款)
├── china/
│   ├── Huawei_Roadmap.xlsx     (4款)
│   ├── Hygon_Roadmap.xlsx      (2款)
│   ├── Cambricon_Roadmap.xlsx  (2款)
│   ├── Loongson_Roadmap.xlsx   (2款)
│   ├── Phytium_Roadmap.xlsx    (2款)
│   ├── Zhaoxin_Roadmap.xlsx    (1款)
│   └── THead_Roadmap.xlsx      (2款)
├── korea/
│   ├── SamsungExynos_Roadmap.xlsx (2款)
│   └── SKHynix_Roadmap.xlsx    (4款)
├── japan/
│   ├── Renesas_Roadmap.xlsx    (2款)
│   ├── SonyCIS_Roadmap.xlsx    (1款)
│   ├── Fujitsu_Roadmap.xlsx    (2款)
│   └── Toshiba_Roadmap.xlsx    (1款)
├── europe/
│   ├── STMicro_Roadmap.xlsx    (3款)
│   ├── Infineon_Roadmap.xlsx   (2款)
│   └── NXP_Roadmap.xlsx        (2款)
└── foundry/
    └── TSMC_Roadmap.xlsx       (4款)
```

---

## 📊 总完成统计

| 地区 | 公司数 | 芯片数 | 产品线数 |
|-----|-------|--------|----------|
| 🇺🇸 美国 | 4 | 17 | 6 |
| 🇨🇳 中国 | 7 | 15 | 7 |
| 🇹🇼 台湾 | 5 | 12 | 5 |
| 🇰🇷 韩国 | 2 | 6 | 2 |
| 🇯🇵 日本 | 4 | 6 | 4 |
| 🇪🇺 欧洲 | 3 | 7 | 4 |
| 🏭 代工 | 1 | 4 | 2 |
| 📦 封装载板 | 1 | - | 1 |
| **总计** | **27** | **67** | **32** |

---

## 📦 封装载板

```
semiconductor_roadmaps/
└── packaging/
    └── Liding_Roadmap.md        (礼鼎半导体 ABF 载板)
```

| 公司 | 类型 | 产品 | 状态 |
|-----|------|------|------|
| **礼鼎半导体** | ABF 载板 | 20-26 层量产，28-30 层研发 | ✅ 已收录 |

---

**更新日期**: 2026-02-02
**版本**: v8.0
