# agent-browser Skill 使用指南

**创建时间**: 2026-02-04  
**Skill**: agent-browser  
**功能**: 基于 Rust 的无头浏览器自动化工具

---

## 📖 目录

1. [功能概述](#1-功能概述)
2. [安装配置](#2-安装配置)
3. [核心命令](#3-核心命令)
4. [应用场景](#4-应用场景)
5. [实战示例](#5-实战示例)
6. [最佳实践](#6-最佳实践)

---

## 1. 功能概述

### 核心能力

```
agent-browser 是一个强大的浏览器自动化工具，支持：

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ✓ 页面导航     - 打开网页、前进、后退、刷新           │
│  ✓ 元素交互     - 点击、输入、悬停、拖拽              │
│  ✓ 数据提取     - 截图、PDF、文本、表格              │
│  ✓ 表单处理     - 填写表单、提交数据                 │
│  ✓ 状态检查     - 可见性、启用状态、选中状态         │
│  ✓ 网络控制     - 请求拦截、Mock响应                 │
│  ✓ 视频录制     - 操作录制、回放演示                 │
│  ✓ 设备模拟     - 视口大小、设备型号、地理位置      │
│  ✓ 存储管理     - Cookie、LocalStorage              │
│  ✓ 多标签页     - 标签页管理、窗口管理              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 与现有 Skills 对比

| Skill | 功能 | 复杂度 | 推荐场景 |
|-------|------|-------|---------|
| **agent-browser** | 完整浏览器自动化 | 中 | 复杂交互网站 |
| **blogwatcher** | 博客监控抓取 | 低 | 简单内容监控 |
| **web_fetch** | 网页内容提取 | 低 | 静态页面 |
| **web_search** | 搜索引擎 | 低 | 信息搜索 |

---

## 2. 安装配置

### 安装方式

```bash
# 方式一：npm 全局安装（推荐）
npm install -g agent-browser
agent-browser install

# 方式二：带依赖安装
agent-browser install --with-deps

# 方式三：从源码安装
git clone https://github.com/vercel-labs/agent-browser
cd agent-browser
pnpm install
pnpm build
agent-browser install
```

### 验证安装

```bash
agent-browser --version
agent-browser --help
```

### 依赖要求

| 依赖 | 要求 | 说明 |
|-----|------|-----|
| Node.js | >= 14 | JavaScript 运行时 |
| npm | >= 6 | 包管理器 |
| Chrome/Chromium | 最新版 | 浏览器引擎 |

---

## 3. 核心命令

### 3.1 页面导航

```bash
# 打开网页
agent-browser open <url>

# 前进/后退/刷新
agent-browser back
agent-browser forward
agent-browser reload

# 关闭浏览器
agent-browser close
```

**示例**：
```bash
agent-browser open https://www.google.com
agent-browser back
agent-browser reload
```

### 3.2 页面快照（重要！）

```bash
# 完整可访问性树
agent-browser snapshot

# 仅交互元素（推荐！）
agent-browser snapshot -i

# 紧凑输出
agent-browser snapshot -c

# 限制深度
agent-browser snapshot -d 3

# 限定选择器
agent-browser snapshot -s "#main"
```

**交互元素引用**：
```
snapshot -i 输出示例：

[
  {
    "ref": "@e1",
    "type": "button",
    "name": "Submit",
    "role": "button"
  },
  {
    "ref": "@e2",
    "type": "textbox",
    "name": "Email",
    "role": "textbox"
  }
]
```

### 3.3 元素交互

```bash
# 点击（使用 @ref）
agent-browser click @e1
agent-browser dblclick @e1

# 聚焦
agent-browser focus @e1

# 输入（清空后输入）
agent-browser fill @e2 "text"

# 输入（不清空）
agent-browser type @e2 "more text"

# 键盘操作
agent-browser press Enter
agent-browser press Control+a
agent-browser keydown Shift
agent-browser keyup Shift

# 悬停
agent-browser hover @e1

# 勾选框
agent-browser check @e1
agent-browser uncheck @e1

# 下拉选择
agent-browser select @e1 "value"

# 滚动
agent-browser scroll down 500
agent-browser scrollintoview @e1

# 拖拽
agent-browser drag @e1 @e2

# 上传文件
agent-browser upload @e1 file.pdf
```

### 3.4 信息获取

```bash
# 获取文本
agent-browser get text @e1

# 获取HTML
agent-browser get html @e1

# 获取输入值
agent-browser get value @e1

# 获取属性
agent-browser get attr @e1 href

# 获取页面信息
agent-browser get title
agent-browser get url

# 计数
agent-browser get count ".item"

# 元素位置
agent-browser get box @e1
```

### 3.5 状态检查

```bash
# 检查可见性
agent-browser is visible @e1

# 检查启用状态
agent-browser is enabled @e1

# 检查选中状态
agent-browser is checked @e1
```

### 3.6 截图与PDF

```bash
# 截图（输出到stdout）
agent-browser screenshot

# 保存截图
agent-browser screenshot path.png

# 全页面截图
agent-browser screenshot --full

# 保存为PDF
agent-browser pdf output.pdf
```

### 3.7 等待机制

```bash
# 等待元素
agent-browser wait @e1

# 等待毫秒
agent-browser wait 2000

# 等待文本
agent-browser wait --text "Success"

# 等待URL
agent-browser wait --url "/dashboard"

# 等待网络空闲
agent-browser wait --load networkidle

# 等待JS条件
agent-browser wait --fn "window.ready"
```

### 3.8 鼠标控制

```bash
# 移动鼠标
agent-browser mouse move 100 200

# 按下/释放
agent-browser mouse down left
agent-browser mouse up left

# 滚轮
agent-browser mouse wheel 100
```

### 3.9 语义定位（备选方案）

```bash
# 按角色查找
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"

# 索引查找
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

---

## 4. 应用场景

### 4.1 行业研究场景

```
场景：自动抓取半导体行业网站数据

目标网站：
- Prismark (prismark.com)
- TrendForce (trendforce.cn)
- 公司官网

工作流程：
1. agent-browser open <行业网站>
2. agent-browser snapshot -i
3. 提取数据表格
4. 保存为CSV
5. 定期执行

效果：
- 节省人工收集时间
- 数据更准确
- 可定期自动化
```

### 4.2 竞品监控场景

```
场景：监控竞争对手官网动态

目标：
- 产品发布
- 新闻动态
- 投资者关系

操作步骤：
1. 打开竞争对手官网
2. 导航到新闻/产品页面
3. 截图留档
4. 提取关键信息
5. 对比历史数据

工具组合：
agent-browser + cron + memory
```

### 4.3 数据采集场景

```
场景：从网页采集结构化数据

类型：
- 财报数据
- 产品价格
- 库存信息
- 薪资调查

技术要点：
1. 先 snapshot -i 获取元素ref
2. 使用 get text @eN 获取数据
3. 使用 get count 统计数量
4. 循环采集所有项目
5. 输出JSON/CSV格式
```

### 4.4 表单自动化场景

```
场景：自动填写并提交表单

示例：简历投递

步骤：
1. agent-browser open 招聘网站
2. agent-browser snapshot -i
3. agent-browser fill @e1 "姓名"
4. agent-browser fill @e2 "邮箱"
5. agent-browser upload @e3 resume.pdf
6. agent-browser click @e4 "提交"
7. agent-browser wait --text "成功"
```

### 4.5 UI测试场景

```
场景：测试网页交互是否正常

测试用例：
1. 点击按钮 -> 验证页面变化
2. 填写表单 -> 验证数据提交
3. 滚动页面 -> 验证懒加载
4. 切换标签 -> 验证内容切换

工作流程：
1. 打开测试页面
2. 执行交互操作
3. 截图或获取数据
4. 对比预期结果
5. 输出测试报告

工具组合：
agent-browser + screenshot + wait
```

### 4.6 内容聚合场景

```
场景：从多页面聚合内容

目标：
- 教程文章
- 产品对比
- 评论汇总

技术方案：
1. 打开列表页面
2. snapshot -i 获取所有链接
3. 遍历每个链接
4. 采集内容
5. 汇总输出

效果：
- 减少手动复制粘贴
- 保证数据一致性
- 便于后续分析
```

---

## 5. 实战示例

### 5.1 示例一：采集新闻标题

```bash
# 打开新闻网站
agent-browser open https://news.example.com

# 获取交互元素
agent-browser snapshot -i

# 假设输出：
# @e1 = "Technology" 分类链接
# @e2 = "AI芯片" 分类链接

# 点击科技分类
agent-browser click @e1

# 等待加载
agent-browser wait --load networkidle

# 获取文章标题
agent-browser get count "h2.title"
# 假设有20个标题

# 循环获取（实际使用脚本）
agent-browser get text @e3  # 第一个标题
```

### 5.2 示例二：监控价格变化

```bash
# 打开电商页面
agent-browser open https://item.example.com/12345

# 获取当前价格
agent-browser get text @e1
# 输出：$999

# 截图留档
agent-browser screenshot price_$(date +%Y%m%d).png

# 等待一段时间
agent-browser wait 3600000  # 1小时

# 刷新页面
agent-browser reload

# 再次获取价格
agent-browser get text @e1
```

### 5.3 示例三：自动登录系统

```bash
# 打开登录页
agent-browser open https://app.example.com/login

# 获取表单元素
agent-browser snapshot -i

# 假设：
# @e1 = 用户名输入框
# @e2 = 密码输入框
# @e3 = 登录按钮

# 填写凭证
agent-browser fill @e1 "your@email.com"
agent-browser fill @e2 "password123"

# 点击登录
agent-browser click @e3

# 等待仪表盘加载
agent-browser wait --url "/dashboard"

# 截图
agent-browser screenshot dashboard.png

# 保存登录状态
agent-browser state save auth.json
```

### 5.4 示例四：多页面对比

```bash
# 打开第一个页面
agent-browser open https://site-a.com/product

# 获取数据
agent-browser get text @e1
agent-browser screenshot product_a.png

# 打开第二个页面
agent-browser open https://site-b.com/product

# 获取数据
agent-browser get text @e1
agent-browser screenshot product_b.png

# 对比结果
# ... 数据对比分析
```

---

## 6. 最佳实践

### 6.1 稳定性优化

```
问题：页面加载慢，元素找不到

解决方案：

1. 等待策略
├── 等待网络空闲
├── 等待特定元素
└── 等待文本出现

2. 重试机制
├── 最多重试3次
├── 每次间隔2秒
└── 记录失败日志

3. 页面刷新
├── 先尝试等待
├── 超时后刷新
└── 重新获取元素
```

### 6.2 数据提取最佳实践

```
步骤：
1. 先 snapshot -i
2. 记录元素 ref
3. 使用 ref 获取数据
4. 验证数据完整性
5. 格式化输出

注意：
- Ref 在页面导航后会变化
- 每次操作后重新 snapshot
- 保存中间结果
```

### 6.3 错误处理

```bash
# 常见错误及处理

错误1：元素找不到
agent-browser wait @e1       # 先等待
agent-browser snapshot -i     # 重新获取

错误2：页面超时
agent-browser reload        # 刷新页面
agent-browser wait 5000    # 等待加载

错误3：网络错误
agent-browser wait --load networkidle  # 等待网络
agent-browser reload                # 刷新
```

### 6.4 性能优化

```
优化建议：

1. 减少截图频率
└── 仅必要时截图

2. 优化等待时间
├── 使用精确等待
└── 避免过长等待

3. 批量处理
├── 减少页面跳转
└── 集中采集数据

4. 使用Session
├── 并行处理
├── 状态隔离
└── 提高效率
```

### 6.5 安全注意事项

```
⚠️ 敏感信息处理

✓ 最佳实践：
├── 使用环境变量存储密码
├── 使用 --headed 模式调试
└── 定期清理 Cookie

✗ 避免：
├── 命令行明文密码
├── 截图包含敏感信息
└── 保存未加密状态
```

---

## 📚 参考资源

### 官方资源
- GitHub: https://github.com/vercel-labs/agent-browser
- 文档: agent-browser --help

### 常见问题

| 问题 | 解决方案 |
|-----|---------|
| 命令找不到 | 检查安装路径 |
| 元素找不到 | 重新 snapshot |
| 页面未加载 | 添加 wait |
| 截图失败 | 检查文件路径 |

---

## 🎯 使用建议

### 初学者
1. 先掌握基础命令（open, snapshot, click, get）
2. 练习简单场景（打开页面、获取标题）
3. 再学习复杂操作（表单、等待）

### 进阶使用
1. 组合多个命令
2. 使用脚本自动化
3. 集成到工作流

### 专业应用
1. 建立标准化操作流程
2. 开发自定义工具脚本
3. 分享最佳实践

---

**创建时间**: 2026-02-04  
**版本**: v1.0
