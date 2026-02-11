#!/usr/bin/env python3
"""
Calendar 自动检查脚本
每日运行，检查今日和明日日程
"""

import os
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
        return "Calendar 未授权"
    
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
        report = "📅 Calendar 检查报告\n"
        report += "-" * 30 + "\n"
        report += f"今日 ({today.strftime('%Y-%m-%d')}): {len(events_today.get('items', []))} 个事件\n"
        report += f"明日 ({tomorrow.strftime('%Y-%m-%d')}): {len(events_tomorrow.get('items', []))} 个事件\n\n"
        
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
        return f"Calendar 检查失败: {str(e)}"

if __name__ == '__main__':
    print(check_calendar())
