# QMD 使用指南

## 安装过程

### 1. 环境检查
```bash
# 检查Bun
which bun
bun --version

# 检查SQLite
sqlite3 --version
```

### 2. 安装QMD
```bash
# 克隆源码（需要网络）
cd /tmp && git clone https://github.com/tobi/qmd.git
cd qmd && bun install

# 添加到PATH（临时方式）
export PATH="/tmp/qmd:$PATH"

# 永久添加到PATH
echo 'export PATH="/tmp/qmd:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 配置与使用

### 1. 创建集合
```bash
# 为markdown文件创建索引集合
qmd collection add /Users/dave/clawd/memory --name memory --mask "*.md"

# 查看集合列表
qmd collection list
```

### 2. 生成向量嵌入
```bash
# 为文档生成向量索引（需要下载约330MB模型）
qmd embed

# 查看索引状态
qmd status
```

### 3. 搜索命令

#### BM25全文搜索（快速，无需额外模型）
```bash
# 基础搜索
qmd search "关键词" -n 5

# 指定集合搜索
qmd search "关键词" -c memory -n 5

# 输出格式
qmd search "关键词" --json          # JSON格式
qmd search "关键词" --md            # Markdown格式
qmd search "关键词" --files         # 仅文件名
```

#### 向量语义搜索（需要下载rerank模型约1.28GB）
```bash
# 混合搜索（BM25 + 向量 + 重排序）
qmd query "自然语言描述" -n 5

# 仅向量搜索
qmd vsearch "语义查询"
```

### 4. 其他有用命令
```bash
# 列出集合中的文件
qmd ls memory

# 获取文档内容
qmd get qmd://memory/2026-02-04.md

# 更新索引
qmd update

# 添加上下文描述
qmd context add /path "这个目录包含投资分析笔记"

# 查看上下文
qmd context list

# 清理缓存
qmd cleanup
```

## 高级配置

### 索引路径
- 默认索引位置：`~/.cache/qmd/index.sqlite`
- 模型缓存：`~/.cache/qmd/models/`

### 可用模型
| 用途 | 模型名 | 大小 |
|-----|-------|------|
| 嵌入 | embeddinggemma-300M-Q8_0 | 328MB |
| 重排序 | qwen3-reranker-0.6b-q8_0 | 1.28GB |

## 使用场景

### 1. 知识库检索
```bash
# 搜索投资相关笔记
qmd search "估值" -c memory

# 搜索半导体行业分析
qmd search "半导体" -c memory
```

### 2. 自然语言查询
```bash
# 语义搜索（需要rerank模型）
qmd query "宏观经济对科技行业的影响"
```

### 3. 项目跟踪
```bash
# 定期更新索引
qmd update && qmd embed

# 检查索引状态
qmd status
```

## 故障排除

### 问题1: 命令未找到
```bash
# 检查PATH
echo $PATH | grep qmd

# 手动添加
export PATH="/tmp/qmd:$PATH"
```

### 问题2: 模型下载慢
- 模型从HuggingFace下载
- 首次使用会下载约330MB嵌入模型
- 重排序模型约1.28GB（可选）

### 问题3: 索引不更新
```bash
# 强制重新索引
qmd update --force
```

## QMD vs OpenClaw默认后端对比

| 特性 | QMD | OpenClaw默认 |
|-----|-----|-------------|
| 部署方式 | 本地CLI | 服务集成 |
| 依赖 | SQLite + 向量扩展 | 外部API |
| 嵌入模型 | 本地Gemma 300M | OpenAI/Google API |
| 搜索速度 | 快（BM25）| 依赖网络 |
| 离线使用 | ✅ 支持 | ❌ 需要网络 |
| 成本 | 免费 | API调用费用 |

## 最佳实践

1. **定期更新索引**：添加新笔记后运行`qmd update`
2. **选择性嵌入**：大型知识库建议使用BM25搜索
3. **上下文标注**：为重要目录添加context描述
4. **监控磁盘空间**：模型和索引会占用数GB空间

## 注意事项

- QMD是独立CLI工具，与OpenClaw的memory功能是分开的
- 如需集成到OpenClaw，需要额外配置MCP服务器
- 目前使用临时PATH方式，需要每次会话手动激活或重启终端
