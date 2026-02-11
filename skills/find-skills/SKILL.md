---
name: find-skills
description: 发现和安装 Agent Skills - 搜索、安装、更新 Skills，帮助用户扩展 Agent 能力
homepage: https://skills.sh/vercel-labs/skills/find-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["npx"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@openagentskills/find-skills",
              "bins": ["skills"],
              "label": "Install find-skills (npm)",
            },
          ],
      },
  }
---

# 🔍 Find Skills

发现和安装 Agent Skills 扩展包，帮助用户扩展 Agent 能力。

## 何时使用

当用户有以下需求时使用此 Skill：

- 询问"如何做 X"（可能已有现成 Skill）
- 说"找一个 X 的 Skill"或"有 X 的 Skill 吗"
- 说"你能做 X 吗"（X 是专业能力）
- 想扩展 Agent 能力
- 想搜索工具、模板、工作流
- 提到希望有特定领域的帮助（设计、测试、部署等）

## Skills CLI 是什么

Skills CLI (`npx skills`) 是 Agent Skills 生态系统的包管理器。

**核心命令**：

| 命令 | 功能 |
|------|------|
| `npx skills find [query]` | 交互式搜索或关键词搜索 |
| `npx skills add` | 从 GitHub 等来源安装 Skill |
| `npx skills check` | 检查 Skill 更新 |
| `npx skills update` | 更新所有 Skills |

浏览 Skills：[https://skills.sh/](https://skills.sh/)

## 如何帮助用户找到 Skills

### 步骤 1：理解需求

当用户寻求帮助时，识别：
- **领域**：React、测试、设计、部署等
- **具体任务**：写测试、创建动画、Review PRs
- **是否常见任务**：是否可能有现成的 Skill

### 步骤 2：搜索 Skills

运行 find 命令：

```bash
npx skills find [查询词]
```

**示例**：
- 用户问"如何加速 React 应用" → `npx skills find react performance`
- 用户问"能帮我 Review PR 吗" → `npx skills find pr review`
- 用户说"我需要创建变更日志" → `npx skills find changelog`

### 步骤 3：向用户展示选项

找到相关 Skills 后，向用户展示：
- Skill 名称和功能
- 安装命令
- skills.sh 链接

**示例回复**：

我找到一个可能有帮助的 Skill！"vercel-react-best-practices" 提供 Vercel 工程团队的 React 和 Next.js 性能优化指南。

安装命令：
```bash
npx skills add vercel-labs/agent-skills@vercel-react-best-practices
```

了解更多：https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

### 步骤 4：提供安装

如果用户想继续安装：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 表示全局安装（用户级别），`-y` 跳过确认提示。

## 常见 Skill 分类

搜索时考虑这些常见类别：

| 类别 | 示例查询 |
|------|----------|
| **Web 开发** | react, nextjs, typescript, css, tailwind |
| **测试** | testing, jest, playwright, e2e |
| **DevOps** | deploy, docker, kubernetes, ci-cd |
| **文档** | docs, readme, changelog, api-docs |
| **代码质量** | review, lint, refactor, best-practices |
| **设计** | ui, ux, design-system, accessibility |
| **效率** | workflow, automation, git |

## 搜索技巧

- **使用具体关键词**：`"react testing"` 比 `"testing"` 更好
- **尝试替代词**：如果 `"deploy"` 不行，试试 `"deployment"` 或 `"ci-cd"`
- **检查热门来源**：许多 Skills 来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 未找到 Skills 时

如果找不到相关 Skills：
- 承认没有找到匹配的 Skills
- 直接使用通用能力帮助用户完成任务
- 建议用户可以创建自己的 Skill

**示例**：

我搜索了与 "xyz" 相关的 Skills，但没有找到匹配的。

我可以直接帮你完成这个任务！要继续吗？

如果这是你经常做的事情，可以创建自己的 Skill：
```bash
npx skills init my-xyz-skill
```

## 快速使用

```bash
# 搜索 Skills
npx skills find react

# 搜索并安装
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

# 检查更新
npx skills check

# 更新所有 Skills
npx skills update
```

## 资源链接

- **Skills 市场**：https://skills.sh/
- **GitHub**：https://github.com/vercel-labs/skills
- **文档**：https://skills.sh/docs
