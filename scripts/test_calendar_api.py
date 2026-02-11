#!/usr/bin/env python3
"""
Calendar API 测试脚本
用于验证 Calendar API 连接是否正常
"""

import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Calendar API 权限范围
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def test_calendar():
    """测试 Calendar API 连接"""
    print("=" * 60)
    print("📅 Calendar API 连接测试")
    print("=" * 60)
    
    creds = None
    
    # 检查是否有已保存的 token
    if os.path.exists('/Users/dave/clawd/token_calendar.json'):
        creds = Credentials.from_authorized_user_file(
            '/Users/dave/clawd/token_calendar.json', SCOPES)
    
    # 如果没有有效的凭据，需要登录
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 刷新 Calendar token...")
            creds.refresh(Request())
        else:
            print("⚠️ 需要用户授权 Calendar")
            print("\n步骤：")
            print("1. 运行此脚本后，会自动打开浏览器")
            print("2. 登录 Google 账号")
            print("3. 点击'允许'授权")
            print("4. token 会自动保存到 /Users/dave/clawd/token_calendar.json")
            print("\n运行命令：")
            print("python3 /Users/dave/clawd/scripts/test_calendar_api.py")
            
            # 启动授权流程
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/dave/clawd/calendar_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 保存凭据
        with open('/Users/dave/clawd/token_calendar.json', 'w') as token:
            token.write(creds.to_json())
    
    # 测试 API
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # 获取今日日程
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_of_day.isoformat() + 'Z',
            timeMax=end_of_day.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime').execute()
        
        events = events_result.get('items', [])
        
        print(f"\n✅ Calendar API 连接成功！")
        print(f"   今日事件数: {len(events)}")
        
        if events:
            print("\n今日日程：")
            for event in events[:5]:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', '无标题')
                print(f"   - {start[:16]} | {summary}")
        
        # 获取明日日程
        tomorrow = now + timedelta(days=1)
        start_tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        end_tomorrow = tomorrow.replace(hour=23, minute=59, second=59, microsecond=0)
        
        events_tomorrow = service.events().list(
            calendarId='primary',
            timeMin=start_tomorrow.isoformat() + 'Z',
            timeMax=end_tomorrow.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime').execute()
        
        print(f"\n明日事件数: {len(events_tomorrow.get('items', []))}")
        
        return True
    except Exception as e:
        print(f"❌ Calendar API 连接失败: {e}")
        return False

if __name__ == '__main__':
    test_calendar()
