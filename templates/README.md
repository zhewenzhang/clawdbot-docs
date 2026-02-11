# 咨询公司报告模板系统

**版本**: v1.0  
**创建日期**: 2026-02-08  
**基于**: McKinsey 金字塔原理方法论

---

## 目录

1. [简介](#简介)
2. [模板类型](#模板类型)
3. [快速开始](#快速开始)
4. [数据配置](#数据配置)
5. [自定义指南](#自定义指南)
6. [最佳实践](#最佳实践)
7. [常见问题](#常见问题)

---

## 简介

本模板系统整合了全球顶尖咨询公司的报告方法论，包括：

- **McKinsey (麦肯锡)**: 金字塔原理、MECE框架
- **BCG (波士顿咨询)**: 矩阵分析、战略框架
- **Bain (贝恩)**: 数据驱动分析
- **Roland Berger (罗兰贝格)**: 欧洲风格排版

### 核心特性

✅ **金字塔结构**: 结论先行，逻辑清晰  
✅ **专业配色**: 深蓝+金色，商务风格  
✅ **响应式设计**: A4打印优化  
✅ **组件化**: 可复用的卡片、表格、时间线  
✅ **易定制**: CSS变量轻松修改

---

## 模板类型

### 1. 对外报告模板

**文件**: `templates/external_report_template.html`

适用于：
- 客户交付报告
- 投资分析报告
- 战略规划报告
- 项目结案报告

**结构**:
```
封面 → 执行摘要 → 核心发现 → 详细分析 → 附录
```

### 2. 内部报告模板

**文件**: `templates/internal_report_template.html` (待创建)

适用于：
- 周报/月报
- 项目进度报告
- 内部评审材料
- 快速数据汇总

**结构**:
```
标题 → 关键发现 → 分析过程 → 建议 → 讨论要点
```

---

## 快速开始

### 方法1: 直接编辑HTML

1. 复制模板文件
2. 用文本编辑器打开
3. 修改内容占位符
4. 保存并用浏览器打开

```html
<!-- 修改标题 -->
<h1 class="cover-title">您的报告标题</h1>

<!-- 修改表格数据 -->
<tr><td>新数据</td><td>新数据</td></tr>
```

### 方法2: 使用Python脚本生成

```bash
# 安装依赖
pip install jinja2

# 运行生成脚本
python scripts/generate_report.py \
    --data examples/report_data.json \
    --output reports/my_report.html
```

### 方法3: 使用命令行工具

```bash
# 使用 make 命令
make report title="新报告" data="data.json"

# 查看帮助
make help
```

---

## 数据配置

### JSON数据格式

```json
{
    "title": "深度分析报告",
    "subtitle": "公司名称 · 项目名称",
    "date": "2026年2月8日",
    "version": "v1.0",
    "confidentiality": "内部使用",
    
    "executive_summary": [
        "核心发现1",
        "核心发现2",
        "核心发现3"
    ],
    
    "key_findings": [
        {
            "stars": "★★★★★",
            "title": "发现标题",
            "description": "详细描述..."
        }
    ],
    
    "metrics": [
        {"value": "A", "label": "综合评级"},
        {"value": "4.0", "label": "投资建议"}
    ],
    
    "sections": [
        {
            "title": "章节标题",
            "summary": "核心要点描述",
            "grid": [
                {
                    "title": "左侧标题",
                    "table": {
                        "header": [
                            {"text": "列1"},
                            {"text": "列2", "align": "text-right"}
                        ],
                        "rows": [
                            {
                                "highlight": false,
                                "cells": [
                                    {"text": "数据1"},
                                    {"text": "100", "align": "text-right"}
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    ],
    
    "appendix": {
        "sources": [
            {"name": "来源名称", "year": "2024", "status": "已验证"}
        ],
        "recommendations": [
            {"priority": "★★★☆☆", "title": "建议项目"}
        ]
    }
}
```

### 数据字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 报告标题 |
| `subtitle` | string | 否 | 副标题 |
| `date` | string | 否 | 日期 |
| `version` | string | 否 | 版本号 |
| `confidentiality` | string | 否 | 机密等级 |
| `executive_summary` | array | 否 | 执行摘要列表 |
| `key_findings` | array | 否 | 核心发现列表 |
| `metrics` | array | 否 | 指标卡片 |
| `sections` | array | 否 | 内容章节 |
| `appendix` | object | 否 | 附录内容 |

---

## 自定义指南

### 1. 修改配色

打开模板文件，修改 `:root` 中的CSS变量：

```css
:root {
    /* 主色 - 改为您的品牌色 */
    --primary: #003366;
    
    /* 强调色 */
    --accent: #C4A962;
    
    /* 成功/警告/危险色 */
    --success: #2E7D32;
    --warning: #F9A825;
    --danger: #C62828;
}
```

### 2. 修改字体

```css
body {
    font-family: "您的字体", 
                 "PingFang TC", 
                 "Microsoft JhengHei", 
                 sans-serif;
}
```

### 3. 添加自定义组件

#### 添加新卡片类型

```css
/* 在 <style> 中添加 */
.my-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
}
```

#### 添加新图表类型

```html
<!-- 在页面中添加 -->
<div class="chart-container">
    <!-- 您的图表代码 -->
</div>
```

### 4. 修改布局

```css
/* 改为A4竖排 */
.page {
    width: 210mm;
    height: 297mm;
}
```

---

## 最佳实践

### 1. 内容结构 (金字塔原理)

```
✅ 推荐结构:
1. 核心结论 (开头)
2. 支撑论据 (3-5点)
3. 详细证据 (数据/图表)
4. 行动建议 (具体步骤)

❌ 避免结构:
- 长篇铺垫
- 信息过载
- 逻辑跳跃
```

### 2. 表格设计

```css
/* 推荐做法 */
- 表格行数 < 20 行
- 表头固定背景色
- 重要数据高亮
- 数字右对齐

/* 避免做法 */
- 过多列 (>8列)
- 单元格合并
- 缺少边框
```

### 3. 配色使用

```
配色比例:
- 主色 (蓝色): 60-70% 面积
- 强调色 (金色): 10-15% 面积
- 功能色 (红/绿): 5-10% 面积
- 背景色: 保持白色/浅灰
```

### 4. 页面平衡

```
✅ 推荐做法:
- 留白充足
- 视觉平衡
- 关键信息突出

❌ 避免做法:
- 文字过密
- 图表过大
- 重点不突出
```

---

## 常见问题

### Q1: 如何添加新页面？

```html
<!-- 复制以下代码到模板末尾 -->
<div class="page content-page">
    <div class="title-main">新页面标题</div>
    
    <!-- 您的内容 -->
    
    <div class="footer">
        <span class="footer-left">{{ title }} v1.0</span>
        <span class="footer-right">第 X 页 · 机密文件</span>
    </div>
</div>
```

### Q2: 如何修改页边距？

```css
.page {
    padding: 12mm 15mm;  /* 上下12mm, 左右15mm */
}
```

### Q3: 如何添加公司Logo？

```html
<!-- 在封面页添加 -->
<div class="page cover">
    <img src="logo.png" alt="Logo" class="cover-logo">
    <!-- ... -->
</div>
```

```css
.cover-logo {
    width: 120px;
    margin-bottom: 20px;
}
```

### Q4: 如何导出为PDF？

1. 用浏览器打开HTML文件
2. Ctrl+P (Cmd+P) 打开打印
3. 选择"保存为PDF"
4. 设置边距为"无"
5. 启用"背景图形"

### Q5: 中文显示有问题？

确保HTML文件编码为UTF-8：

```html
<meta charset="UTF-8">
```

---

## 文件清单

```
templates/
├── external_report_template.html  # 对外报告模板
├── internal_report_template.html  # 内部报告模板 (待创建)
└── README.md                      # 本使用说明

scripts/
├── generate_report.py            # 报告生成脚本
└── examples/
    └── report_data.json          # 数据示例

memory/
└── consulting_reports_best_practices_2026-02-08.md  # 方法论指南
```

---

## 参考资源

**书籍**:
- 《金字塔原理》- Barbara Minto
- 《麦肯锡方法》- Ethan M. Rasiel
- 《麦肯锡意识》- Ethan M. Rasiel

**网站**:
- SlideModel.com
- Flevy.com
- McKinsey官网

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-02-08 | 初始版本，集成McKinsey方法论 |

---

**技术支持**: 使用中有任何问题，请查看 [最佳实践指南](../memory/consulting_reports_best_practices_2026-02-08.md)
