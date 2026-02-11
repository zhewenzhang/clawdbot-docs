# 报告输出改进总结

**日期**: 2026-02-09

---

## 错误回顾

| 序号 | 错误 | 后果 |
|-----|------|------|
| 1 | 忘记使用 Playwright 脚本生成 PDF | 浪费时间尝试无效方案 |
| 2 | 页面四周留空白（15mm） | 不专业，浪费空间 |
| 3 | 字号太小（11pt） | 阅读困难 |
| 4 | 存在空白页 | 内容不紧凑 |
| 5 | 布局过于松散 | 每页信息量低 |

---

## 正确流程（以后必须遵守）

### PDF 生成流程

```bash
# 方法1：使用 gen.js 脚本（首选）
cd /Users/dave/clawd/reports
node gen.js

# 或直接用 Playwright
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///path/to/report.html');
  await page.waitForLoadState('networkidle');
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

### PDF 格式要求

| 项目 | 要求 |
|-----|------|
| 边距 | 0mm（无边距） |
| 页面方向 | 横排（A4 landscape） |
| 字号 | 11pt（正文），标题更大 |
| 布局 | 紧凑，双栏/多栏混排 |
| 背景 | 彩色打印（printBackground: true） |

---

## 设计优化要点

### ✅ 正确做法

1. **边距**：设置 `@page { margin: 0; }`
2. **字号**：正文 11pt，指标数字 22pt+，标题 14-20pt
3. **布局**：双栏或网格布局，充分利用空间
4. **视觉**：深色主题（#0f3460）+ 白色背景，专业感
5. **紧凑**：移除所有不必要的 padding 和 margin

### ❌ 错误做法

1. 边距 > 5mm
2. 字号 < 11pt
3. 单栏大段文字
4. 留白过多
5. 无视觉层次

---

## 输出流程

```
【任务完成后的输出】
1. 先生成 HTML 报告
2. 用 Playwright 生成 PDF（无边距、横排）
3. PDF 发送给老板
4. 主动询问反馈
```

---

## 教训

> **核心问题**: 忘记了已经验证过的最佳实践（gen.js 脚本）

**改进**:
- ✅ 记住 `gen.js` 脚本路径和用法
- ✅ 记住 PDF 格式要求（0边距、横排、11pt）
- ✅ 记住设计原则（紧凑、视觉层次、双栏布局）
- ✅ 输出前先自查格式

---

**创建时间**: 2026-02-09
**作者**: 可乐 (OpenClaw)
