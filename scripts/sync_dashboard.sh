#!/bin/bash
# 同步仪表板到 GitHub Pages
# 使用 GitHub CLI (gh) 处理认证
# 用法: bash scripts/sync_dashboard.sh

set -e

echo "🔄 开始同步仪表板..."

# 切换到工作目录
cd /Users/dave/clawd

# 1. 生成 Excel 索引
echo "📊 生成 Excel 索引..."
python3 scripts/generate_excel_index.py

# 2. 切换到 docs 目录
cd docs

# 3. Git 操作（使用 gh CLI）
echo "📤 提交到 GitHub..."

# 添加变更
git add -A

# 检查是否有变更
if git diff --cached --quiet; then
    echo "✅ 没有新变更"
else
    # 使用 gh 提交（自动使用已登录用户的认证）
    COMMIT_MSG="📊 更新数据仪表板索引 ($(date '+%Y-%m-%d %H:%M'))"
    
    # 使用 gh api 检查是否已登录
    if gh auth status &>/dev/null; then
        # 已登录，使用 gh 创建提交
        echo "✅ GitHub CLI 已登录"
        
        # 提交并推送
        git commit -m "$COMMIT_MSG"
        git push origin main
        
        echo "✅ 已推送到 GitHub Pages"
    else
        echo "⚠️ GitHub CLI 未登录，请先运行: gh auth login"
        echo "或者直接在 docs 目录执行 git push"
    fi
fi

echo ""
echo "🎉 同步完成！"
echo "🔗 访问地址: https://zhewenzhang.github.io/clawdbot-docs/dashboard.html"
