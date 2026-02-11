# 芯片公司分析報告 - 標準模板 v2.0

## 📋 報告結構

```
公司名稱（中文+英文）公司分析報告
├── 1. 公司概況（10項欄位）
├── 2. 產品Roadmap（簡易版）
├── 3. 產品Roadmap（詳細版）
├── 4. 市場分析
├── 5. 競爭格局
└── 6. 風險評估
```

---

## 一、公司概況模板

### 1.1 基本信息表

| 欄位 | 內容 |
|------|------|
| **1) 公司名稱** | 中文：英飛凌半導體 / 英文：Infineon Technologies |
| **2) 公司總部** | 德國，慕尼黑 |
| **3) 公司類型** | IC Design / Foundry / OSAT / IDM / EDA&IP / OEM-EMS / Distributors / Others |
| **4) 成立時間** | 1999年4月1日 |
| **5) 註冊資本** | 百萬/USD（如：€1,964百萬） |
| **6) 應用分類** | AI / HPC / Automotive / Networking / FPGA / ASIC / Others |
| **7) 芯片產品應用** | 如：IGBT、MOSFET、MCU、WiFi晶片、汽車雷達等 |
| **8) 是否上市** | 是，法蘭克福交易所_IFX；否（備註：是否有上市計畫） |
| **9) 上市時間** | 2000年11月17日 |
| **10) 前三大股東** | 1. The Vanguard Group (8.2%) 2. BlackRock (7.1%) 3. State Street (5.3%) |

---

## 二、產品Roadmap模板

### 2.1 簡易版本（One-Page Overview）

| 產品類別 | 2024 | 2025 | 2026 | 2027 | 2028+ | 備註 |
|----------|------|------|------|------|-------|------|
| 功率半導體 | 第5代IGBT | 第6代IGBT | SiC Gen2 | SiC Gen3 | GaN全面量產 | 技術節點 |
| 汽車微控制器 | TriCore AURIX TC4x | AURIX TC4x量產 | AURIX TC5x | 新一代MCU | - | 命名規則 |
| 傳感器 | 雷達晶片Gen3 | 雷達晶片Gen4 | 固態LiDAR | - | - | 感知技術 |

### 2.2 詳細版本（Detailed Roadmap）

#### 功率半導體產品線

| 產品系列 | 類型 | 製程節點 | 2024產品 | 2025產品 | 2026產品 | 應用領域 | 關鍵特性 |
|----------|------|----------|----------|----------|----------|----------|----------|
| IGBT 5 | IGBT | 12吋晶圓 | IGBT5 Standard | IGBT5 Enhanced | IGBT6 | 工業變頻 | 低損耗 |
| CoolSiC | SiC MOSFET | 8吋SiC | CoolSiC Gen1 | CoolSiC Gen2 | CoolSiC Gen3 | 電動車 | 高壓1200V |
| CoolGaN | GaN HEMT | 8吋GaN | - | GaN 400V | GaN 650V | 快充/數據中心 | 高頻高效 |

#### 汽車微控制器產品線

| 產品系列 | 製程節點 | 2024 | 2025 | 2026 | 2027 | 安全等級 | 生態系統 |
|----------|----------|------|------|------|------|----------|----------|
| AURIX TC4x | 28nm | TC4x Sample | TC4x量產 | - | - | ASIL D | Eclipse/CPP |
| AURIX TC5x | 16nm | - | TC4x+樣品 | TC5x量產 | - | ASIL D | 新生態系統 |
| TRAVEO T2G | 40nm | T2G Gen2 | T2G Gen3 | - | - | ASIL B | 低功耗 |

#### 先進封裝技術Roadmap

| 封裝類型 | 2024 | 2025 | 2026 | 2027 | 合作夥伴 |
|----------|------|------|------|------|----------|
| 2.5D | 成熟 | 擴大量產 | 先進2.5D | - | TSMC |
| 3D | 研發 | 小量產 | 擴大量產 | 3D量產 | ASE |
| Chiplet | 評估 | 原型 | 驗證 | 量產 | AMD-Xilinx |

---

## 三、PDF報告標準格式

### 3.1 頁面設置
- 頁面方向：橫向（A4 Landscape）
- 字體：中文 Microsoft JhengHei，英文 Arial
- 標題字號：18-24pt
- 正文字號：10-12pt
- 邊距：0mm（無邊距）
- 主題色：深藍色 #0f3460

### 3.2 報告模板（HTML）
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>公司名稱公司分析報告</title>
    <style>
        /* 標準樣式見下方完整模板 */
    </style>
</head>
<body>
    <!-- 封面 -->
    <div class="page cover-page">...</div>
    
    <!-- 公司概況 -->
    <div class="page">...</div>
    
    <!-- Roadmap簡易版 -->
    <div class="page">...</div>
    
    <!-- Roadmap詳細版 -->
    <div class="page">...</div>
    
    <!-- 市場分析 -->
    <div class="page">...</div>
</body>
</html>
```

### 3.3 PDF生成命令
```bash
# 使用Playwright生成PDF
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///path/to/report.html');
  await page.pdf({
    path: '/path/to/report.pdf',
    format: 'A4',
    landscape: true,
    printBackground: true,
    margin: { top: '0mm', right: '0mm', bottom: '0mm', left: '0mm' }
  });
  await browser.close();
})();
"
```

---

## 四、檔案命名規範

| 公司類型 | 檔案名範例 |
|----------|-----------|
| IC Design | 英飛凌半導體_Infineon_公司分析報告.html/pdf |
| Foundry | 台積電_TSMC_公司分析報告.html/pdf |
| OSAT | 日月光_ASE_公司分析報告.html/pdf |
| IDM | 英特爾_Intel_公司分析報告.html/pdf |
| EDA | 新思科技_Synopsys_公司分析報告.html/pdf |

---

## 五、數據收集步驟

### 步驟一：官網收集
1. 訪問公司官網 Investor Relations
2. 下載年報（Annual Report）
3. 獲取產品發布新聞稿
4. 下載產品規格書（Datasheet）

### 步驟二：財報分析
1. FY2024營收按業務線拆分
2. 資本支出計劃
3. 產能擴張時間表
4. 技術節點路線圖

### 步�步三：第三方驗證
1. Gartner/IDC 市場報告
2. TrendForce 產能分析
3. 行業新聞媒體報導
4. 專利申請分析

---

## 六、範例：瑞薩電子（Renesas）

### 6.1 公司概況

| 欄位 | 內容 |
|------|------|
| **1) 公司名稱** | 中文：瑞薩電子 / 英文：Renesas Electronics Corporation |
| **2) 公司總部** | 日本，東京 |
| **3) 公司類型** | IC Design / **Foundry** / OSAT / **IDM** / EDA&IP / OEM-EMS / Distributors / Others |
| **4) 成立時間** | 2003年11月1日（2010年4月1日瑞薩科技與NEC電子合併） |
| **5) 註冊資本** | JPY 630,000百萬（約USD 4,200百萬） |
| **6) 應用分類** | AI / **HPC** / **Automotive** / **Networking** / FPGA / ASIC / Others |
| **7) 芯片產品應用** | MCU（RX、RA、RZ系列）、SoC、功率半導體、類比晶片、感測器 |
| **8) 是否上市** | 是，東京證券交易所_6723；否 |
| **9) 上市時間** | 2003年11月1日 |
| **10) 前三大股東** | 1. Toyota Motor Corporation (11.7%) 2. NTT Docomo (6.3%) 3. Mizuho Bank (4.5%) |

### 6.2 Roadmap簡易版（示例）

| 產品類別 | 2024 | 2025 | 2026 | 2027 | 2028+ |
|----------|------|------|------|------|-------|
| MCU（通用） | RA8 M系列 | RA8量產 | RA下一代 | - | - |
| MCU（汽車） | RH850/CFx | 新一代A-Preliminary | A系列量產 | A系列全面取代 | - |
| SoC（汽車） | R-Car V4M | R-Car V4H | R-Car V5N | R-Car V5M | R-Car V6 |
| SoC（工業） | RZ/T2 | RZ/N2 | RZ/G3h | RZ/G4 | - |
| 類比/電源 | ISL8xx | ISL9xx | 新一代類比 | - | - |

---

## 七、後續工作

### 待完成清單
- [ ] 確認瑞薩官網Roadmap格式
- [ ] 創建瑞薩詳細Roadmap模板
- [ ] 設計Infineon報告模板
- [ ] 設計NVIDIA報告模板
- [ ] 設計台積電報告模板
- [ ] 制定數據收集SOP

---

*模板版本：v2.0*
*創建日期：2026-02-09*
