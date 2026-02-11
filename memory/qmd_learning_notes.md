# QMD 功能深度学习笔记

> 学习日期：2026-02-05
> 来源：OpenClaw官方文档 + GitHub PR #3160

---

## 什么是 QMD？

**QMD (Quantized Memory Database)** 是 OpenClaw 的一个**可选内存后端**，是一个本地优先的搜索 sidecar。

**核心特点**：
- 结合 **BM25**（关键词搜索）+ **向量搜索** + **重排序（Reranking）**
- Markdown 文件仍然是真理的来源
- OpenClaw 调用 QMD 进行检索
- 完全本地运行，无需云服务

---

## QMD vs 默认内存后端

| 特性 | 默认 (memory-core) | QMD |
|------|-------------------|-----|
| 搜索方式 | 向量搜索 | BM25 + 向量 + 重排序 |
| 关键词搜索 | 弱 | **强**（BM25） |
| 语义搜索 | 向量相似度 | 向量相似度 |
| 结果排序 | 向量得分 | 综合得分（重排序） |
| 首次搜索速度 | 快 | 慢（需下载模型） |
| 会话索引 | 不支持 | **支持**（可选） |
| 本地模型 | 需额外配置 | 自动下载 GGUF |

---

## 安装 QMD

### 前置条件

1. **Bun** - JavaScript 运行时
   ```bash
   # macOS
   brew install bun
   
   # Linux
   curl -fsSL https://bun.sh/install | bash
   ```

2. **SQLite with extensions** - 支持扩展的 SQLite
   ```bash
   # macOS
   brew install sqlite
   ```

### 安装 QMD CLI

```bash
# 方法1: 从 npm/yarn 安装
bun install -g github.com/tobi/qmd

# 方法2: 从源码编译
git clone https://github.com/tobi/qmd.git
cd qmd
bun install
bun run build
```

### 验证安装

```bash
qmd --version
qmd --help
```

---

## 配置 QMD

### 方法1: 修改配置文件

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "memory": {
    "backend": "qmd",
    "citations": "auto",
    "qmd": {
      "includeDefaultMemory": true,
      "paths": [
        {
          "name": "docs",
          "path": "~/notes",
          "pattern": "**/*.md"
        }
      ],
      "sessions": {
        "enabled": true,
        "retentionDays": 30,
        "exportDir": "~/.openclaw/agents/main/qmd/sessions"
      },
      "update": {
        "interval": "5m",
        "debounceMs": 15000,
        "onBoot": true,
        "embedInterval": "1h"
      },
      "limits": {
        "maxResults": 6,
        "maxSnippetChars": 2000,
        "maxInjectedChars": 10000,
        "timeoutMs": 4000
      },
      "scope": {
        "default": "deny",
        "rules": [
          {
            "action": "allow",
            "match": {
              "chatType": "direct"
            }
          }
        ]
      }
    }
  }
}
```

### 方法2: 环境变量

```bash
export XDG_CONFIG_HOME="$HOME/.openclaw/agents/main/qmd/xdg-config"
export XDG_CACHE_HOME="$HOME/.openclaw/agents/main/qmd/xdg-cache"

# 手动触发索引更新
qmd update
qmd embed

# 预热（触发首次模型下载）
qmd query "test" -c memory-root --json
```

---

## QMD 核心功能

### 1. 混合搜索

QMD 结合三种搜索方式：

- **BM25**：关键词匹配，适合精确查找
- **向量搜索**：语义相似度，适合模糊查询
- **重排序**：综合排序，提升结果质量

### 2. 会话索引（可选）

当 `memory.qmd.sessions.enabled = true` 时：
- OpenClaw 导出清洗后的会话转录（User/Assistant turns）
- 保存到 `~/.openclaw/agents/<agent-id>/qmd/sessions/`
- memory_search 可以回溯最近对话
- 不触碰内置 SQLite 索引

### 3. 自动索引更新

- 默认每5分钟刷新索引
- 支持增量更新（debounce 15秒）
- 启动时自动更新

### 4. 多路径索引

```json
{
  "paths": [
    {
      "name": "docs",
      "path": "~/notes",
      "pattern": "**/*.md"
    },
    {
      "name": "projects",
      "path": "/srv/projects",
      "pattern": "**/*.md"
    }
  ]
}
```

---

## QMD CLI 命令

### 常用命令

```bash
# 版本信息
qmd --version

# 帮助信息
qmd --help

# 更新索引
qmd update

# 生成向量嵌入
qmd embed

# 搜索
qmd query "关键词" --json

# 指定 collection 搜索
qmd query "关键词" -c memory-root --json

# 查看所有 collections
qmd list

# 删除 collection
qmd delete <name>

# 导出 collection
qmd export <name> -o output.json
```

### 搜索示例

```bash
# 基本搜索
qmd query "半导体市场"

# JSON 格式输出（供程序解析）
qmd query "AI芯片" --json

# 指定 collection
qmd query "投资策略" -c investment-notes --json

# 限制结果数量
qmd query "技术趋势" --json --limit 10
```

---

## 性能优化

### 首次使用优化

首次搜索可能很慢，因为需要：
1. 下载 GGUF 模型（reranker/query expansion）
2. 生成所有文档的向量嵌入

**预热方法**：
```bash
# 设置环境变量
export XDG_CONFIG_HOME="$HOME/.openclaw/agents/main/qmd/xdg-config"
export XDG_CACHE_HOME="$HOME/.openclaw/agents/main/qmd/xdg-cache"

# 触发首次下载和索引
qmd update
qmd embed

# 预热搜索
qmd query "test" -c memory-root --json >/dev/null 2>&1
```

### 索引优化

```json
{
  "qmd": {
    "update": {
      "interval": "10m",  // 增加间隔，减少CPU占用
      "debounceMs": 30000  // 增加防抖时间
    },
    "limits": {
      "maxResults": 10,    // 限制结果数量
      "timeoutMs": 5000,   // 增加超时时间
      "maxSnippetChars": 1500  // 减少单条snippet长度
    }
  }
}
```

---

## 故障排除

### QMD 未找到

```bash
# 检查是否安装
which qmd
qmd --version

# 重新安装
bun install -g github.com/tobi/qmd
```

### SQLite 扩展错误

```bash
# macOS: 重新安装 SQLite
brew install sqlite

# 检查 SQLite 版本
sqlite3 --version

# 确保支持扩展
sqlite3
SQLite version 3.x.x
sqlite> SELECT load_extension('');
# 应该成功，无报错
```

### 搜索超时

```json
{
  "qmd": {
    "limits": {
      "timeoutMs": 10000  // 增加超时时间
    }
  }
}
```

### 回退到默认后端

如果 QMD 失败，OpenClaw 会自动回退到内置 SQLite 管理器：

```bash
# 检查当前使用的后端
openclaw-cn status

# 查看日志
tail -f ~/.openclaw/logs/*.log
```

---

## QMD 适用场景

### 适合使用 QMD 的情况

1. **大量关键词搜索需求**
   - 技术文档检索
   - 代码库搜索
   - 知识库查询

2. **需要会话记忆**
   - 长期对话项目
   - 多轮分析任务

3. **本地化优先**
   - 敏感数据处理
   - 离线工作环境

4. **混合搜索需求**
   - 关键词 + 语义结合
   - 需要更精确的结果排序

### 不需要 QMD 的情况

1. **简单对话**
   - 日常问答
   - 短任务处理

2. **网络不稳定**
   - 首次加载可能慢
   - 需要下载模型

3. **资源受限环境**
   - 内存有限
   - 存储有限

---

## 下一步计划

- [ ] 安装 QMD CLI
- [ ] 配置 OpenClaw 使用 QMD
- [ ] 测试搜索功能
- [ ] 配置会话索引
- [ ] 优化性能参数
- [ ] 记录使用体验

---

## 参考资源

1. **官方文档**: https://docs.openclaw.ai/concepts/memory
2. **GitHub PR**: https://github.com/openclaw/openclaw/pull/3160
3. **QMD 项目**: https://github.com/tobi/qmd
4. **OpenClaw Skills**: https://github.com/openclaw/skills (搜索 qmd-skill-2)

---

*本笔记由 Clawdbot 自动生成*
