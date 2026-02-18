# A股看板快速部署指南

## 方法一：手动部署（推荐）

### 1. 创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名：`a-share-dashboard`
3. 选择 **Public**（GitHub Pages需要）
4. 勾选 "Add a README file"
5. 点击 "Create repository"

### 2. 上传文件
在仓库页面点击 "upload an existing file"，拖放以下文件：
- `index.html` (主页面)
- `README.md` (说明文档)

或使用Git命令行：

```bash
# 克隆仓库
git clone https://github.com/你的用户名/a-share-dashboard.git
cd a-share-dashboard

# 复制文件
cp /Users/dave/clawd/index.html .
cp /Users/dave/clawd/README.md .

# 提交
git add index.html README.md
git commit -m "Add A股市场看板"
git push origin main
```

### 3. 配置GitHub Pages
1. 进入仓库 Settings
2. 左侧点击 **Pages**
3. Build and deployment / Source: 选择 `Deploy from a branch`
4. Branch: `main` → `/(root)`
5. 点击 Save
6. 等待1-2分钟

### 4. 访问你的看板
链接格式：`https://你的用户名.github.io/a-share-dashboard/`

示例：`https://davegithub.github.io/a-share-dashboard/` (请替换为你的用户名)

---

## 方法二：使用GitHub CLI（如有安装）

```bash
# 登录
gh auth login

# 创建仓库
gh repo create a-share-dashboard --public --source=. --push

# 配置Pages
gh api -X PUT repos/你的用户名/a-share-dashboard/pages \
  -f source='{"branch":"main","path":"/"}'
```

---

## 测试部署

1. 访问你的GitHub Pages URL
2. 应该看到"A股市场看板"页面
3. 默认显示模拟数据
4. 点击"刷新数据"按钮测试

---

## 配置TuShare真实数据（可选）

1. 访问 https://tushare.pro 注册并获取token
2. 打开你的看板页面
3. 按F12打开开发者工具
4. 在Console执行：
```javascript
localStorage.setItem('tushare_token', '你的token');
location.reload();
```
5. 页面将显示真实市场数据

---

## 需要帮助？

- GitHub Pages配置问题：https://docs.github.com/en/pages
- TuShare API文档：https://tushare.pro/document/2

---

**完成部署后，请访问你的链接并测试功能。**
