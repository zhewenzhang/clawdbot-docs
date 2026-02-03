# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## TTS 语音配置

### 语音偏好
- **语言**: 中文 (zh-CN)
- **声音**: 温柔女声
  - 建议使用: `zh-CN-XiaoxiaoNeural` (微软 TTS 温柔女声)
- **播放设备**: Mac mini 喇叭
- **使用场景**: 重要报告朗读，平常用文字

## 工作环境

### 设备信息
- **主设备**: Mac mini (工作平台)
- **工作地点**: 书房
- **操作系统**: macOS

### 文件管理
- **工作目录**: `/Users/dave/clawd`
- **权限**: 全盘访问（除系统文件和 openclaw 敏感文件外）
- **原则**: 信任自主管理，重要操作先确认

## 安全与隐私

### 原则
- 敏感文件需授权
- 不触碰系统关键文件
- 尊重隐私

### 当前限制
- 摄像头: 无
- SSH 设备: 暂无
- 智能家居: 暂无

## 待办清单

### 网站监控列表
- [ ] 半导体相关网站 (待补充)

### 后续可扩展
- [ ] SSH 远程连接 (树莓派/NAS/服务器)
- [ ] 摄像头监控 (未来)
- [ ] 智能家居控制 (未来)
- [ ] 更多 TTS 声音测试优化

## 常用命令速查

```bash
# 文件管理
ls -la ~/Downloads/    # 查看下载文件
open ~/Downloads/      # 打开下载文件夹

# 系统状态
uptime                 # 运行时间
openclaw-cn status     # Clawdbot 状态

# 模型管理
openclaw-cn models     # 查看可用模型
```

## 备注

- 老板信任我的文件管理能力，我会珍惜这份信任
- 数据品质是核心要求，每项工作都要严谨
- "走过必留痕迹" - 记录和可追溯
