#!/usr/bin/env python3
"""
修复 Cron 任务格式问题
问题: Markdown 表格在 Telegram 上显示混乱
解决方案: 修改任务配置，明确禁止 Markdown 表格
"""

import json

# 读取 cron 任务配置
with open('/Users/dave/.openclaw/cron/jobs.json', 'r') as f:
    jobs_config = json.load(f)

# 需要修复的任务列表（这些任务会产生需要格式化输出的内容）
tasks_to_fix = [
    {
        'name': '每日Token额度检查',
        'new_text': '''🔔 【Token 额度检查】

【当前状态】
- 已用额度：待查询
- 剩余额度：待查询
- 上下文使用率：待查询

【建议】
- 待查询后给出建议'''

    },
    {
        'name': 'Gmail + 日历配置提醒',
        'new_text': '''🔔 Gmail + 日历 API 配置提醒

之前未配置成功的项目，今晚需要完成：

1. Gmail API - 清理邮件
2. 日历 API - 同步日程（2/4 南茂董事长来访）

请回复我，我来启动授权流程 🛠️'''

    }
]

# 修复任务配置
fixed_count = 0
for job in jobs_config['jobs']:
    for task in tasks_to_fix:
        if job.get('name') == task['name']:
            # 修改 payload.text
            if 'payload' in job and 'text' in job['payload']:
                job['payload']['text'] = task['new_text']
                fixed_count += 1
                print(f"✅ 已修复: {task['name']}")

# 保存修改后的配置
with open('/Users/dave/.openclaw/cron/jobs.json', 'w') as f:
    json.dump(jobs_config, f, indent=2, ensure_ascii=False)

print(f"\n共修复 {fixed_count} 个任务")
print("配置文件已保存: /Users/dave/.openclaw/cron/jobs.json")

# 同时更新 HEARTBEAT.md 中的状态追踪示例
with open('/Users/dave/clawd/HEARTBEAT.md', 'r') as f:
    heartbeat_content = f.read()

# 将 JSON 表格格式改为纯文字格式
old_json_example = '''```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": null,
    "websites": null
  }
}
```'''

new_text_example = '''```
最后检查时间：
- Email: 从未（API未配置）
- Calendar: 从未（API未配置）
- Weather: 从未（API未配置）
- Websites: 从未（待配置）
```'''

new_heartbeat_content = heartbeat_content.replace(old_json_example, new_text_example)

with open('/Users/dave/clawd/HEARTBEAT.md', 'w') as f:
    f.write(new_heartbeat_content)

print("✅ 已更新 HEARTBEAT.md 格式示例")

print("\n" + "=" * 60)
print("修复完成！")
print("=" * 60)
print("\n改进措施：")
print("1. ✅ 修复 cron 任务配置，明确使用纯文字格式")
print("2. ✅ 更新 HEARTBEAT.md 格式示例，改为纯文字格式")
print("3. ⚠️ 重启 Gateway 使配置生效（需要用户执行）")
print("\n重启命令: openclaw gateway restart")
