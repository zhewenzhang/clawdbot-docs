#!/usr/bin/env python3
"""
Gmail + Calendar Heartbeat 自动检查配置
自动配置 Heartbeat 任务，实现每日自动检查
"""

import json
import os
from datetime import datetime

def create_gmail_check_script():
    """创建 Gmail 自动检查脚本"""
    script = '''#!/usr/bin/env python3
"""
Gmail 自动检查脚本
每日运行，检查重要邮件
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def check_gmail():
    """检查 Gmail"""
    creds = None
    
    # 加载凭据
    if os.path.exists('/Users/dave/clawd/token_gmail.json'):
        creds = Credentials.from_authorized_user_file(
            '/Users/dave/clawd/token_gmail.json', SCOPES)
    
    if not creds or not creds.valid:
        return "❌ Gmail 未授权"
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # 获取未读邮件数
        results = service.users().getProfile(userId='me').execute()
        email = results['emailAddress']
        
        # 获取最近5封邮件
        messages = service.users().messages().list(
            userId='me', maxResults=5, labelIds=['INBOX']).execute()
        
        unread_count = 0
        important_emails = []
        
        for msg in messages.get('messages', []):
            msg_detail = service.users().messages().get(
                userId='me', id=msg['id'], format='metadata').execute()
            
            labels = msg_detail.get('labelIds', [])
            if 'UNREAD' in labels:
                unread_count += 1
            
            # 检查是否有重要关键词
            subject = ''
            for header in msg_detail.get('payload', {}).get('headers', []):
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            
            keywords = ['紧急', '重要', '会议', '日程', '投资', '财报', 'AI', '半导体']
            if any(k in subject for k in keywords):
                important_emails.append(subject)
        
        # 生成报告
        report = f"""
📧 Gmail 检查报告

邮箱: {email}
未读邮件: {unread_count}

"""
        
        if important_emails:
            report += "📌 重要邮件：\n"
            for email in important_emails[:3]:
                report += f"  - {email}\n"
        else:
            report += "✅ 无重要邮件"
        
        return report
        
    except Exception as e:
        return f"❌ Gmail 检查失败: {e}"

if __name__ == '__main__':
    print(check_gmail())
'''
    
    with open('/Users/dave/clawd/scripts/gmail_heartbeat_check.py', 'w') as f:
        f.write(script)
    
    os.chmod('/Users/dave/clawd/scripts/gmail_heartbeat_check.py', 0o755)
    print("✅ 已创建 Gmail 检查脚本: scripts/gmail_heartbeat_check.py")

def create_calendar_check_script():
    """创建 Calendar 自动检查脚本"""
    script = '''#!/usr/bin/env python3
"""
Calendar 自动检查脚本
每日运行，检查今日和明日日程
"""

import os
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def check_calendar():
    """检查 Calendar"""
    creds = None
    
    # 加载凭据
    if os.path.exists('/Users/dave/clawd/token_calendar.json'):
        creds = Credentials.from_authorized_user_file(
            '/Users/dave/clawd/token_calendar.json', SCOPES)
    
    if not creds or not creds.valid:
        return "❌ Calendar 未授权"
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # 今日日程
        today = datetime.utcnow()
        start_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_today = today.replace(hour=23, minute=59, second=59, microsecond=0)
        
        events_today = service.events().list(
            calendarId='primary',
            timeMin=start_today.isoformat() + 'Z',
            timeMax=end_today.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime').execute()
        
        # 明日日程
        tomorrow = today + timedelta(days=1)
        start_tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        end_tomorrow = tomorrow.replace(hour=23, minute=59, second=59, microsecond=0)
        
        events_tomorrow = service.events().list(
            calendarId='primary',
            timeMin=start_tomorrow.isoformat() + 'Z',
            timeMax=end_tomorrow.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime').execute()
        
        # 生成报告
        report = f"""
📅 Calendar 检查报告

今日 ({today.strftime('%Y-%m-%d')}): {len(events_today.get('items', []))} 个事件
明日 ({tomorrow.strftime('%Y-%m-%d')}): {len(events_tomorrow.get('items', []))} 个事件

"""
        
        if events_today.get('items'):
            report += "📌 今日事件：\n"
            for event in events_today.get('items', [])[:5]:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', '无标题')
                time_str = start[11:16] if 'T' in start else '全天'
                report += f"  - {time_str} | {summary}\n"
        else:
            report += "✅ 今日无事件\n"
        
        if events_tomorrow.get('items'):
            report += "\n📌 明日事件：\n"
            for event in events_tomorrow.get('items', [])[:5]:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', '无标题')
                time_str = start[11:16] if 'T' in start else '全天'
                report += f"  - {time_str} | {summary}\n"
        else:
            report += "\n✅ 明日无事件\n"
        
        return report
        
    except Exception as e:
        return f"❌ Calendar 检查失败: {e}"

if __name__ == '__main__':
    print(check_calendar())
'''
    
    with open('/Users/dave/clawd/scripts/calendar_heartbeat_check.py', 'w') as f:
        f.write(script)
    
    os.chmod('/Users/dave/clawd/scripts/calendar_heartbeat_check.py', 0o755)
    print("✅ 已创建 Calendar 检查脚本: scripts/calendar_heartbeat_check.py")

def update_cron_jobs():
    """更新 cron 任务配置"""
    
    # 读取现有配置
    with open('/Users/dave/.openclaw/cron/jobs.json', 'r') as f:
        jobs_config = json.load(f)
    
    # 添加新的 heartbeat 检查任务
    new_jobs = [
        {
            "id": "gmail-heartbeat-check",
            "agentId": "main",
            "name": "Gmail Heartbeat Check",
            "enabled": True,
            "schedule": {
                "kind": "cron",
                "expr": "0 8 * * *",
                "tz": "Asia/Shanghai"
            },
            "sessionTarget": "isolated",
            "wakeMode": "next-heartbeat",
            "payload": {
                "kind": "agentTurn",
                "message": "📧 Gmail Heartbeat 检查\n\n执行 Gmail 自动检查脚本：\n\n1. 运行 scripts/gmail_heartbeat_check.py\n2. 获取未读邮件数和重要邮件\n3. 生成简报\n4. 发送到 Telegram\n\n【格式要求】\n- 禁止使用 Markdown 表格\n- 使用纯文字格式\n\n回复：'Gmail 检查完成'",
                "model": "minimax/MiniMax-M2.1"
            }
        },
        {
            "id": "calendar-heartbeat-check",
            "agentId": "main",
            "name": "Calendar Heartbeat Check",
            "enabled": True,
            "schedule": {
                "kind": "cron",
                "expr": "0 8 * * *",
                "tz": "Asia/Shanghai"
            },
            "sessionTarget": "isolated",
            "wakeMode": "next-heartbeat",
            "payload": {
                "kind": "agentTurn",
                "message": "📅 Calendar Heartbeat 检查\n\n执行 Calendar 自动检查脚本：\n\n1. 运行 scripts/calendar_heartbeat_check.py\n2. 获取今日和明日日程\n3. 生成简报\n4. 发送到 Telegram\n\n【格式要求】\n- 禁止使用 Markdown 表格\n- 使用纯文字格式\n\n回复：'Calendar 检查完成'",
                "model": "minimax/MiniMax-M2.1"
            }
        }
    ]
    
    # 检查是否已存在
    existing_ids = [job['id'] for job in jobs_config['jobs']]
    
    for new_job in new_jobs:
        if new_job['id'] not in existing_ids:
            jobs_config['jobs'].append(new_job)
            print(f"✅ 已添加任务: {new_job['name']}")
        else:
            print(f"⚠️ 任务已存在: {new_job['name']}")
    
    # 保存配置
    with open('/Users/dave/.openclaw/cron/jobs.json', 'w') as f:
        json.dump(jobs_config, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Cron 任务配置已更新")

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 Gmail + Calendar Heartbeat 自动检查配置")
    print("=" * 60)
    print()
    
    # 检查凭据文件
    gmail_path = '/Users/dave/clawd/gmail_credentials.json'
    calendar_path = '/Users/dave/clawd/calendar_credentials.json'
    
    if not os.path.exists(gmail_path):
        print("❌ Gmail 凭据文件不存在")
        return
    
    if not os.path.exists(calendar_path):
        print("❌ Calendar 凭据文件不存在")
        return
    
    print("✅ 凭据文件检查通过")
    print()
    
    # 创建检查脚本
    create_gmail_check_script()
    create_calendar_check_script()
    
    # 更新 cron 任务
    update_cron_jobs()
    
    print()
    print("=" * 60)
    print("📋 配置完成！")
    print("=" * 60)
    print()
    print("下一步：")
    print("1. 授权 Gmail API: python3 /Users/dave/clawd/scripts/test_gmail_api.py")
    print("2. 授权 Calendar API: python3 /Users/dave/clawd/scripts/test_calendar_api.py")
    print("3. 重启 Gateway: openclaw gateway restart")
    print()
    print("📧 Gmail 检查脚本: /Users/dave/clawd/scripts/gmail_heartbeat_check.py")
    print("📅 Calendar 检查脚本: /Users/dave/clawd/scripts/calendar_heartbeat_check.py")

if __name__ == '__main__':
    main()
