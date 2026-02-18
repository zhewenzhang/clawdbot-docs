# A股市场看板 (A-Share Market Dashboard)

一个简洁的A股市场看板Demo版本，每天早上为用户提供投资检讨所需的市场数据。

![Demo Screenshot](screenshot.png)

## 功能特点

✅ **整体市场状况** - 涨跌统计、平均涨跌幅、总成交额、市场情绪
✅ **板块涨幅榜** - 各大板块实时涨跌幅排行
✅ **资金流向** - 主力资金净流入/出板块统计
✅ **关注股票** - 自定义股票列表基本信息和表现
✅ **响应式设计** - 手机、平板、桌面完美适配
✅ **模拟数据降级** - TuShare API不可用时自动使用模拟数据
✅ **自动刷新** - 每5分钟自动更新数据

## 快速开始

### 方式1：直接打开（模拟数据模式）
```bash
# 下载 index.html 到本地，双击打开即可使用
# 默认使用模拟数据演示所有功能
```

### 方式2：配置TuShare API（真实数据）
1. 注册 TuShare：https://tushare.pro
2. 获取 token
3. 在浏览器中打开页面后，按 F12 打开开发者工具
4. 执行：`localStorage.setItem('tushare_token', '你的token')`
5. 刷新页面即可看到真实数据

## 部署到 GitHub Pages

### 步骤1：创建 GitHub 仓库

```bash
# 在 GitHub 上创建一个新仓库
# 仓库名建议：stock-dashboard 或 a-share-dashboard
# 设置为 Public（GitHub Pages 需要）
```

### 步骤2：上传代码

```bash
# 克隆仓库
git clone https://github.com/你的用户名/stock-dashboard.git
cd stock-dashboard

# 复制 index.html 到仓库
cp /path/to/index.html .

# 添加 README.md 和 .gitignore
echo "index.html" > .gitignore
echo "screenshot.png" >> .gitignore

# 提交并推送
git add .
git commit -m "Initial commit: A股市场看板"
git push origin main
```

### 步骤3：配置 GitHub Pages

1. 访问仓库 Settings
2. 左侧选择 **Pages**
3. **Source**: 选择 `Deploy from a branch`
4. **Branch**: 选择 `main` → `/(root)`
5. 点击 **Save**
6. 等待 1-2 分钟生效

### 步骤4：访问你的看板

GitHub Pages 链接格式：
```
https://你的用户名.github.io/stock-dashboard/
```

将此链接保存为书签，每天早上打开即可查看。

## 项目结构

```
stock-dashboard/
├── index.html          # 主页面（包含HTML/CSS/JS）
├── README.md           # 项目说明
├── .gitignore          # Git忽略文件
└── screenshot.png      # 页面截图（可选）
```

## 技术栈

- **前端**：纯 HTML5 + CSS3 + JavaScript (ES6+)
- **UI设计**：Material Design 风格，Mobile First
- **数据源**：[TuShare](https://tushare.pro) API（可选）
- **托管**：GitHub Pages (免费)
- **无需构建**：单文件部署，零依赖

## 数据说明

### TuShare API
- 免费版：每天 2000 次调用，每分钟 200 次
- 足够个人每日使用
- API 文档：https://tushare.pro/document/2

### 模拟数据
当未配置 token 或 API 不可用时，系统自动生成模拟数据，确保功能完整演示。

## 自定义配置

### 修改关注股票列表

在 `index.html` 中修改 `CONFIG.watchlist`：

```javascript
const CONFIG = {
  watchlist: [
    { code: '600519.SH', name: '贵州茅台' },
    { code: '000858.SZ', name: '五粮液' },
    // 添加更多...
  ]
};
```

### 修改刷新频率

```javascript
const CONFIG = {
  refreshInterval: 5 * 60 * 1000  // 5分钟，改为你想要的毫秒数
};
```

### 修改配色

在 `:root` CSS 变量中修改：

```css
:root {
  --up-color: #E53935;      /* 涨 - 红色 */
  --down-color: #43A047;    /* 跌 - 绿色 */
  --accent: #1976D2;        /* 主题色 */
}
```

## 常见问题

### Q: 为什么显示模拟数据？
A: 可能原因：
1. 未配置 TuShare token（默认模式）
2. token 无效或过期
3. API 调用失败（网络问题）
4. 超出调用限制

### Q: 如何配置真实的 TuShare token？
A: 参考上方的"方式2：配置TuShare API（真实数据）"

### Q: GitHub Pages 域名无法访问？
A: 检查：
1. 仓库是否为 Public
2. Pages 配置是否正确（branch: main, root）
3. 等待 1-2 分钟生效
4. 清除浏览器缓存

### Q: 数据更新时间？
A:
- 交易日白天：每5分钟自动刷新
- 非交易日/夜间：显示最近交易日数据
- 手动刷新：点击"刷新数据"按钮

## 未来改进（待开发）

- [ ] 用户自定义关注列表（localStorage持久化）
- [ ] 历史数据图表展示
- [ ] K线图查看
- [ ] 股票详情页
- [ ] 价格提醒功能
- [ ] 多页面支持

## 开源协议

MIT License - 自由使用、修改和分发。

## 致谢

数据来源：[TuShare](https://tushare.pro) - 免费、开源的A股数据接口

---

**版本**：v1.0 (Demo)
**最后更新**：2026-02-16
**作者**：Dave's Assistant
