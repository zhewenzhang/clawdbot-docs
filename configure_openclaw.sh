#!/bin/bash

# OpenClaw 高级配置脚本
# 运行方式: bash configure_openclaw.sh

OPENCLAW_DIR="$HOME/.openclaw"
CONFIG_FILE="$OPENCLAW_DIR/openclaw.json"

echo "🔧 开始配置 OpenClaw 高级权限..."

# 1. 备份现有配置
echo "📋 备份现有配置..."
cp "$CONFIG_FILE" "$OPENCLAW_DIR/openclaw.json.backup_$(date +%Y%m%d_%H%M%S)"

# 2. 添加 exec 权限配置
echo "⚙️  添加 exec 权限配置..."

# 使用 Python 来更新 JSON 配置
python3 << PYTHON_SCRIPT
import json
import os

config_file = os.path.expanduser('~/.openclaw/openclaw.json')

# 读取现有配置
with open(config_file, 'r') as f:
    config = json.load(f)

# 添加/更新 exec 配置
config['exec'] = {
    'mode': 'allowlist',  # 使用白名单模式
    'allowlist': {
        '/usr/bin': True,       # 允许执行系统命令
        '/bin': True,
        '/opt/homebrew/bin': True,  # Homebrew 命令
        '/usr/local/bin': True,
        '/Users/dave/clawd': True,  # 工作目录
        '/Users/dave/clawd/semiconductor-platform': True,
        'cd': True,   # 允许切换目录
        'npm': True,  # 允许 npm 命令
        'git': True,  # 允许 git 命令
    },
    'security': 'medium',  # 安全级别
    'timeout': 300,  # 超时 5 分钟
}

# 添加 browser 配置
config['browser'] = {
    'mode': 'auto',  # 自动检测
    'profile': 'openclaw',  # 使用独立 profile
    'headless': False,  # 不使用 headless 模式
    'extensions': {
        'relay': True,  # 启用 Chrome Extension Relay
    },
    'screenshot': True,  # 允许截图
    'download': {
        'enabled': True,
        'path': '~/Downloads/openclaw',
    }
}

# 更新 agents 配置，使用 sub-agent 模式
config['agents'] = {
    'defaults': {
        'model': {
            'primary': 'minimax/MiniMax-M2.1',
            'fallbacks': ['minimax-portal/MiniMax-M2.1-lightning']
        },
        'workspace': '/Users/dave/clawd',
        'maxConcurrent': 4,
        'subagents': {
            'maxConcurrent': 8,
            'isolation': 'full',  # 完全隔离
            'timeout': 600,  # 10 分钟超时
        }
    }
}

# 保存配置
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 配置更新完成!")
print("")
print("📝 下一步:")
print("1. 重启 OpenClaw Gateway: openclaw gateway restart")
print("2. 或者运行: openclaw configure 重新配置向导")
print("")
print("⚠️  注意: 如果 exec 权限仍然受限，可能需要在系统偏好设置中允许 Terminal 访问辅助功能")

PYTHON_SCRIPT

echo ""
echo "🔄 请运行以下命令重启 Gateway："
echo "   openclaw gateway restart"
echo ""
echo "📖 详细文档：https://docs.openclaw.ai/"