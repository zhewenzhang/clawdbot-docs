# Q-Time 任务管理系统 v1.0

## 系统目标
防止大模型超时、上下文溢出、工具调用失败

## 核心参数
```python
Q_TIME_CONFIG = {
    "max_operations_per_batch": 5,      # 每批最大操作数
    "rest_duration_seconds": 30,        # 间歇时间（秒）
    "context_threshold": 0.8,           # 上下文使用率阈值（80%）
    "auto_cleanup_threshold": 0.9,      # 自动清理阈值（90%）
    "timeout_max_seconds": 300,         # 最大超时时间（5分钟）
    "model_switch_threshold": 0.85,     # 模型切换阈值
}
```

## 三阶段防护机制

### 阶段1：预防（任务开始前）
```
任务接收
  ↓
【CAPTCHA检查】
- 当前上下文使用率？
- 如果 >80% → 强制清理
- 如果 >90% → 切换模型
  ↓
【任务分片】
- 任务复杂度评分（1-10）
- 如果 >7分 → 拆分为子任务
- 每批最多5个操作
  ↓
开始执行
```

### 阶段2：监控（任务执行中）
```
每3个操作后
  ↓
【Q-Time间歇】
- 暂停30秒
- 检查上下文使用率
- 记录操作日志
- 如果 >85% → 切换备用模型
  ↓
继续执行或切换模型
```

### 阶段3：恢复（任务完成后）
```
任务完成
  ↓
【系统检查】
- 上下文使用率？
- 工具调用成功率？
- 响应时间？
  ↓
如果异常 → 自动清理 + 记录日志
如果正常 → 更新任务状态
  ↓
准备下一任务
```

## 模型切换策略

| 场景 | 主模型 | 备用模型 | 触发条件 |
|-----|-------|---------|---------|
| 正常 | Kimi K2.5 | MiniMax M2.1 | 默认 |
| 上下文>85% | MiniMax | StepFun | 自动切换 |
| 超时>5分钟 | OpenRouter Auto | - | 强制切换 |
| 工具失败>3次 | MiniMax | Kimi | 降级切换 |

## 强制间歇规则

### 必须间歇的情况
- [ ] 完成5个连续操作后 → 强制休息30秒
- [ ] 上下文使用>70% → 休息60秒 + 检查
- [ ] 工具调用失败 → 休息10秒 + 重试
- [ ] 生成>1000 tokens → 休息15秒

### 间歇期间操作
1. 记录任务进度
2. 检查系统状态
3. 更新内存文件
4. 压缩会话（如需要）

## 自动清理触发器

```bash
# 上下文使用率检查
if [ $context_usage -gt 90 ]; then
    # 强制清理
    echo "上下文满载，强制清理..."
    /clear
elif [ $context_usage -gt 80 ]; then
    # 警告并建议清理
    echo "警告：上下文使用率 $context_usage%，建议清理"
fi
```

## 任务批处理模板

```python
def batch_process(tasks, batch_size=5, rest_time=30):
    """分批处理任务，带Q-Time间歇"""
    results = []
    
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i+batch_size]
        
        # 执行批次
        for task in batch:
            result = execute_task(task)
            results.append(result)
            
            # 检查状态
            if check_context_usage() > 0.8:
                print("⚠️ 上下文使用率高，强制间歇")
                time.sleep(rest_time * 2)
                if check_context_usage() > 0.9:
                    switch_model("minimax")
        
        # 批次间间歇
        if i + batch_size < len(tasks):
            print(f"⏸️ Q-Time: 休息{rest_time}秒...")
            time.sleep(rest_time)
    
    return results
```

## 错误恢复流程

### 超时恢复（>300秒）
```
1. 记录超时任务
2. 自动切换到备用模型
3. 重试任务（最多3次）
4. 如果仍失败 → 拆分为更小子任务
```

### 工具调用失败
```
1. 记录失败工具 + 参数
2. 等待10秒
3. 重新初始化工具
4. 重试（最多3次）
5. 如果仍失败 → 跳过该工具，记录错误
```

### 上下文溢出
```
1. 立即停止当前任务
2. 保存关键信息到内存文件
3. 执行 /clear 清理会话
4. 重新加载必要上下文
5. 从断点继续任务
```

## 监控指标

| 指标 | 正常范围 | 警告阈值 | 危险阈值 |
|-----|---------|---------|---------|
| 上下文使用率 | <70% | 70-85% | >85% |
| 响应时间 | <30s | 30-120s | >300s |
| 工具成功率 | >95% | 85-95% | <85% |
| 模型切换次数 | <3/小时 | 3-5/小时 | >5/小时 |

## 每日健康检查

```bash
#!/bin/bash
# daily_health_check.sh

echo "=== 模型健康检查 ==="
echo "1. 检查上下文使用率..."
openclaw status | grep "Context"

echo "2. 检查模型响应时间..."
# 发送测试请求
time echo "test" | openclaw chat

echo "3. 检查工具可用性..."
openclaw tools list

echo "4. 检查内存文件更新..."
ls -lt ~/clawd/memory/ | head -5

echo "5. 清理旧日志..."
find ~/clawd/logs -name "*.log" -mtime +7 -delete
```

## 紧急处理预案

### 场景A：Kimi完全超时
```bash
# 立即执行
openclaw config patch raw='{"agents":{"defaults":{"model":{"primary":"minimax/MiniMax-M2.1"}}}}'
openclaw restart
# 通知用户
```

### 场景B：上下文100%满载
```bash
# 保存关键信息
echo "上下文满载，执行紧急清理..." >> ~/clawd/logs/emergency.log
# 强制清理
openclaw session clear
# 重启服务
openclaw restart
```

### 场景C：工具链完全失效
```bash
# 重置工具状态
openclaw tools reset
# 降级到基础模式
openclaw mode minimal
# 逐步恢复工具
```

## 实施检查清单

- [ ] 安装Q-Time监控脚本
- [ ] 配置自动清理cron任务
- [ ] 设置上下文使用率告警
- [ ] 测试模型切换流程
- [ ] 验证工具恢复机制
- [ ] 创建每日健康检查任务

---
创建时间：2026-02-12
版本：v1.0
状态：已实施
