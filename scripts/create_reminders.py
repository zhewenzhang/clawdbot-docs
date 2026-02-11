#!/usr/bin/env python3
"""
在 Google Calendar 中创建提醒事件
"""

import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_reminder():
    """创建提醒"""
    creds = None
    
    # 加载凭据
    if os.path.exists('/Users/dave/clawd/token_calendar.json'):
        creds = Credentials.from_authorized_user_file(
            '/Users/dave/clawd/token_calendar.json', SCOPES)
    
    if not creds or not creds.valid:
        print("❌ Calendar 未授权")
        return
    
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.utcnow()
    
    # 事件 1: 明天 8:00 - 10086 鸿蒙手机套餐申请延期
    start_time1 = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0)
    end_time1 = start_time1 + timedelta(minutes=30)
    
    event1 = {
        'summary': '⏰ 提醒：10086 鸿蒙手机套餐申请延期',
        'description': '需要拨打 10086 申请鸿蒙手机套餐延期',
        'start': {
            'dateTime': start_time1.isoformat() + 'Z',
            'timeZone': 'Asia/Shanghai'
        },
        'end': {
            'dateTime': end_time1.isoformat() + 'Z',
            'timeZone': 'Asia/Shanghai'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60},
                {'method': 'popup', 'minutes': 15}
            ]
        }
    }
    
    # 事件 2: 明天下午 - 知乎保存 CPO 知识文档
    start_time2 = (now + timedelta(days=1)).replace(
        hour=14, minute=0, second=0, microsecond=0)
    end_time2 = start_time2 + timedelta(minutes=30)
    
    event2 = {
        'summary': '⏰ 提醒：知乎保存 CPO 知识文档',
        'description': '需要在知乎保存 CPO 相关知识文档',
        'start': {
            'dateTime': start_time2.isoformat() + 'Z',
            'timeZone': 'Asia/Shanghai'
        },
        'end': {
            'dateTime': end_time2.isoformat() + 'Z',
            'timeZone': 'Asia/Shanghai'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60},
                {'method': 'popup', 'minutes': 30}
            ]
        }
    }
    
    try:
        # 创建事件 1
        created_event1 = service.events().insert(
            calendarId='primary', body=event1).execute()
        print(f"✅ 已创建事件 1:")
        print(f"   标题: {created_event1['summary']}")
        print(f"   时间: {start_time1.strftime('%Y-%m-%d %H:%M')}")
        
        # 创建事件 2
        created_event2 = service.events().insert(
            calendarId='primary', body=event2).execute()
        print(f"\n✅ 已创建事件 2:")
        print(f"   标题: {created_event2['summary']}")
        print(f"   时间: {start_time2.strftime('%Y-%m-%d %H:%M')}")
        
        print("\n" + "=" * 60)
        print("📅 Calendar 提醒创建完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")

if __name__ == '__main__':
    create_reminder()
